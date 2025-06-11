---
title: Kubernetes 实战：从零到一创建监控 Token
date: 2025-06-10 19:45:55
tags: ["Kubernetes", "监控", "RBAC", "安全", "DevOps"]
thumbnail: "https://tse4-mm.cn.bing.net/th/id/OIP-C.Rz0CSQWjZOMEqmynFJOTMQAAAA?rs=1&pid=ImgDetMain"
---

在 Kubernetes 的世界里，为外部应用（如 Prometheus、Grafana Agent 或 CI/CD 流水线）创建一个安全的访问凭证是每个运维和 DevOps 工程师的必备技能。这个凭证，通常是一个 Bearer Token，就像一把钥匙，允许应用与 Kubernetes API Server 对话。

但这把钥匙能打开哪些门，取决于我们授予它的权限。直接给出 `cluster-admin` 的"万能钥匙"虽然简单，却极不安全。遵循**最小权限原则 (Principle of Least Privilege, PoLP)** 才是专业的做法。

这篇博客将带你走过完整的流程：
1.  **创建一个专用的服务账户 (ServiceAccount)。**
2.  **定义精确的只读监控权限 (ClusterRole)。**
3.  **授权并生成一个安全的 Bearer Token。**
4.  **深入排查并解决最常见的 `403 Forbidden` 错误。**
5.  **提供一个一键部署的自动化脚本。**

准备好了吗？让我们开始吧！

## 核心理念：最小权限原则

我们的目标是创建一个用于监控的 Token，它只需要读取集群资源状态，而绝不需要修改或删除任何东西。因此，我们将创建一个专用的 `ServiceAccount`，并只授予它必要的 `get`, `list`, `watch` 权限。

### 步骤一：奠定基础 (Namespace 和 ServiceAccount)

将监控相关的组件放在一个独立的命名空间中是一种良好的实践，便于管理和隔离。

```bash
# 1. 创建一个名为 "monitoring" 的命名空间
kubectl create namespace monitoring

# 2. 在新命名空间中创建一个服务账户
kubectl create serviceaccount monitoring-sa -n monitoring
```

### 步骤二：定义权限 (ClusterRole)

监控系统需要查看集群范围的资源（如 Nodes）和所有命名空间中的 Pods，所以我们使用 `ClusterRole` 来定义权限。

一个常见的**错误起点**是只包含基础资源的只读权限。但别担心，我们将从这里开始，并逐步完善它。

### 步骤三：授权与生成 Token

现在，我们通过 `ClusterRoleBinding` 将 `ClusterRole` 的权限授予我们的 `monitoring-sa`。然后，使用现代 Kubernetes (v1.24+) 推荐的方式生成一个有时效性的 Token。

---

### 遭遇战：直面 `403 Forbidden` 错误

假设我们已经创建了包含基础只读权限的 `ClusterRole` 和 `ClusterRoleBinding`，并生成了 Token。当我们将这个 Token 配置到监控工具（例如 `kube-state-metrics` 或我们手动测试）中去获取节点资源利用率时，很可能会遇到第一个拦路虎：

```bash
# 使用 curl 测试访问 Kubelet 的 Summary API
$ curl -k -H "Authorization: Bearer $TOKEN" $APISERVER/stats/summary

# 返回的错误
{ "error": "https://127.0.0.1:6443/stats/summary returned HTTP status 403 Forbidden" }
```

这是一个经典的权限问题。API Server 告诉我们："我知道你是谁，但你没权限访问这个资源。"

#### 破案线索一：`/stats/summary` 是什么？

这个端点并非普通的 API 资源，它由每个节点上的 **Kubelet** 提供，用于返回节点和 Pod 的详细资源使用统计（CPU、内存等）。`kubectl top` 命令就依赖它。要访问它，`ClusterRole` 中必须包含对 `nodes/stats` 资源的权限。

#### 破案线索二：为什么又是 `403`？

修复了第一个问题后，我们再次尝试，却遇到了一个新的 `403` 错误，但这次的信息更具体了：

```json
{
  "status": "Failure",
  "message": "nodes \"vbox\" is forbidden: User \"system:serviceaccount:monitoring:monitoring-sa\" cannot get resource \"nodes/proxy\" ...",
  "code": 403
}
```

错误信息直指 `nodes/proxy`。这是为什么？

因为我们是通过 API Server 访问 Kubelet 的，这个过程其实是 **API Server 在为我们充当代理**。Kubernetes 对这个代理功能本身也设置了权限。
-   `nodes/stats` 是访问数据的权限。
-   `nodes/proxy` 则是**使用 API Server 代理功能的"门票"**。

两者缺一不可！

## 最终解决方案：完整的 ClusterRole

现在，我们知道了所有必需的权限。下面是最终正确的 `ClusterRole` YAML 定义：

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: monitoring-clusterrole
rules:
- apiGroups: [""]
  resources:
  - nodes
  - nodes/metrics
  - nodes/stats      # 允许访问 Kubelet 统计数据
  - nodes/proxy      # 允许使用 API Server 作为代理访问节点
  - services
  - endpoints
  - pods
  - replicationcontrollers
  - persistentvolumes
  - persistentvolumeclaims
  verbs: ["get", "list", "watch"]
- apiGroups: ["apps"]
  resources:
  - daemonsets
  - deployments
  - replicasets
  - statefulsets
  verbs: ["get", "list", "watch"]
- apiGroups: ["extensions", "networking.k8s.io"]
  resources:
  - ingresses
  verbs: ["get", "list", "watch"]
- nonResourceURLs: ["/metrics", "/metrics/cadvisor"]
  verbs: ["get"]
```

### 一键部署：自动化脚本

为了让整个过程变得简单可重复，这里提供一个完整的 Bash 脚本。它会创建所有必要的资源，并生成最终的 Token。这个脚本是**幂等**的，可以安全地重复运行。

将以下内容保存为 `create-monitoring-token.sh`：

```bash
#!/bin/bash

# =============================================================================
#
#  脚本名称: create-monitoring-token.sh
#  功能描述: 为 Kubernetes 监控创建一个拥有正确只读权限的 ServiceAccount 和 Bearer Token。
#
# =============================================================================

set -e

# --- 配置变量 ---
NAMESPACE="monitoring"
SERVICE_ACCOUNT_NAME="monitoring-sa"
CLUSTER_ROLE_NAME="monitoring-clusterrole"
CLUSTER_ROLE_BINDING_NAME="monitoring-clusterrole-binding"

# --- 美化输出 ---
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}Starting script to create monitoring token...${NC}"

# --- 步骤 1: 创建 Namespace (如果不存在) ---
echo "--> Checking/Creating Namespace: ${NAMESPACE}"
kubectl get namespace ${NAMESPACE} &> /dev/null || kubectl create namespace ${NAMESPACE}

# --- 步骤 2: 创建 ServiceAccount (如果不存在) ---
echo "--> Checking/Creating ServiceAccount: ${SERVICE_ACCOUNT_NAME}"
kubectl get serviceaccount ${SERVICE_ACCOUNT_NAME} -n ${NAMESPACE} &> /dev/null || kubectl create serviceaccount ${SERVICE_ACCOUNT_NAME} -n ${NAMESPACE}

# --- 步骤 3: 创建/更新 ClusterRole 和 ClusterRoleBinding ---
echo "--> Applying ClusterRole and ClusterRoleBinding..."
cat <<EOF | kubectl apply -f -
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: ${CLUSTER_ROLE_NAME}
rules:
- apiGroups: [""]
  resources:
  - nodes
  - nodes/metrics
  - nodes/stats
  - nodes/proxy
  - services
  - endpoints
  - pods
  verbs: ["get", "list", "watch"]
- apiGroups: ["apps"]
  resources:
  - deployments
  - replicasets
  - statefulsets
  - daemonsets
  verbs: ["get", "list", "watch"]
- apiGroups: ["extensions", "networking.k8s.io"]
  resources:
  - ingresses
  verbs: ["get", "list", "watch"]
- nonResourceURLs: ["/metrics"]
  verbs: ["get"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: ${CLUSTER_ROLE_BINDING_NAME}
subjects:
- kind: ServiceAccount
  name: ${SERVICE_ACCOUNT_NAME}
  namespace: ${NAMESPACE}
roleRef:
  kind: ClusterRole
  name: ${CLUSTER_ROLE_NAME}
  apiGroup: rbac.authorization.k8s.io
EOF

# --- 步骤 4: 生成 Bearer Token ---
echo "--> Generating Bearer Token for ServiceAccount: ${SERVICE_ACCOUNT_NAME}"
TOKEN=$(kubectl create token ${SERVICE_ACCOUNT_NAME} -n ${NAMESPACE})

# --- 步骤 5: 打印 Token ---
echo -e "\n${YELLOW}======================[ MONITORING BEARER TOKEN ]======================${NC}"
echo -e "${GREEN}${TOKEN}${NC}"
echo -e "${YELLOW}=======================================================================${NC}"
echo -e "\n${YELLOW}Script finished successfully. Store this token securely!${NC}\n"
```

**如何使用脚本：**
1.  保存为 `create-monitoring-token.sh`。
2.  赋予执行权限: `chmod +x create-monitoring-token.sh`。
3.  运行: `./create-monitoring-token.sh`。

脚本执行完毕后，您将得到一个可以直接用于监控配置的安全 Token。

### 深入理解 `ClusterRole` 中的资源权限

我们上面定义的 `ClusterRole` 看起来很长，但每一行都有其明确的目的。理解每个资源条目控制的内容，是掌握 Kubernetes RBAC 的关键。让我们逐一解析。

#### 核心 API 组 (`apiGroups: [""]`)

这是 Kubernetes 最基础、最核心的资源所在的分组。

-   **`nodes`**: 控制对集群节点的访问。
    -   `get`/`list`/`watch`: 允许监控系统发现集群中有哪些节点、它们的状态（如 `Ready`, `NotReady`）和基本信息（IP 地址、操作系统、Kubelet 版本等）。这是服务发现的基础。

-   **`nodes/proxy`**: 这是**关键权限**，控制是否允许通过 API Server **代理**到节点上的 Kubelet。
    -   `get`: 授予使用代理的"门票"。没有它，即便有后续权限，也无法通过 API Server 访问 Kubelet 的任何端点。

-   **`nodes/stats`**: 控制访问 Kubelet 提供的**资源统计**端点 (`/stats/`)。
    -   `get`: 允许获取节点及其上所有 Pod 的详细资源使用情况（CPU、内存、文件系统、网络）。这是 `kubectl top node/pod` 和 Metrics Server 获取数据的核心。

-   **`nodes/metrics`**: 控制访问 Kubelet 提供的**度量指标**端点 (`/metrics/`)。
    -   `get`: 允许获取 Kubelet 自身以及 cAdvisor、Prober 等组件以 Prometheus 格式暴露的详细指标。这对于深度监控节点健康至关重要。

-   **`services`**: 控制对 Service 资源的访问。
    -   `get`/`list`/`watch`: 允许发现应用是如何通过 Service 对外暴露的，获取其 ClusterIP、端口等信息。Prometheus 可以用它来发现需要抓取指标的目标。

-   **`endpoints`**: 控制对 Endpoints 资源的访问。Endpoints 对象存储了 Service 背后真实 Pod 的 IP 地址和端口。
    -   `get`/`list`/`watch`: 这是服务发现的**核心**。监控系统通过它找到具体提供服务的 Pod，然后去抓取这些 Pod 上的 `/metrics` 端点。

-   **`pods`**: 控制对 Pod 资源的访问。
    -   `get`/`list`/`watch`: 允许发现集群中运行的所有 Pod，获取它们的元数据（标签、注解）、状态（`Running`, `Pending`）、IP 地址等。这是自动发现监控目标（例如带有特定注解的 Pod）的基础。

#### **Apps API 组 (`apiGroups: ["apps"]`)**

这个分组包含了管理应用部署的核心工作负载资源。

-   **`deployments`**, **`replicasets`**, **`statefulsets`**, **`daemonsets`**:
    -   `get`/`list`/`watch`: 允许监控系统了解应用的部署结构。例如，一个 Deployment 有多少个预期的副本（`replicas`），当前有多少个可用，一个 StatefulSet 的所有实例是否都正常运行。这对于告警"应用副本数不足"或"部署失败"至关重要。

#### Networking API 组 (`apiGroups: ["extensions", "networking.k8s.io"]`)

这个分组控制集群的网络入口资源。*(注：`extensions` 是早期版本的 API 组，为了向后兼容而保留)*

-   **`ingresses`**:
    -   `get`/`list`/`watch`: 允许监控系统发现应用是如何通过 Ingress 暴露到集群外部的，可以监控 Ingress 的配置、后端服务和 TLS 设置等。

#### 非资源 URL (`nonResourceURLs`)

这类权限不针对某个具体的 Kubernetes 对象，而是直接针对 API Server 上的某个 URL 路径。

-   **`/metrics`**:
    -   `get`: 允许直接访问 API Server 自身的 `/metrics` 端点，以监控 API Server 的健康状况、请求延迟、错误率等核心指标。

---

通过这样精细化的权限配置，我们确保了监控 Token 只能做它该做的事：**观察**。它能看到集群的全貌，但无法进行任何修改，就像一个尽职尽责的哨兵，忠实地报告情况，但绝不干涉战场的运作。这种安全边界的建立，是生产级 Kubernetes 环境的基石。

### 验证 Token 是否生效

创建完 Token 后，我们需要验证它是否真的能正常工作。这里提供几个实用的测试命令：

```bash
# 1. 测试基本访问权限
curl -k -H "Authorization: Bearer $TOKEN" $APISERVER/api/v1/nodes

# 2. 测试 Pod 列表访问
curl -k -H "Authorization: Bearer $TOKEN" $APISERVER/api/v1/pods

# 3. 测试节点指标访问
curl -k -H "Authorization: Bearer $TOKEN" $APISERVER/api/v1/nodes/$(hostname)/proxy/metrics
```

如果这些命令都返回了正确的 JSON 响应，说明我们的 Token 配置成功了。


### 如何清理（删除创建的资源）

如果您想删除此脚本创建的所有资源，可以运行以下命令：

```bash
# !! 警告: 这将删除所有相关资源，请谨慎操作 !!

# 定义变量 (与脚本中保持一致)
NAMESPACE="monitoring"
SERVICE_ACCOUNT_NAME="monitoring-sa"
CLUSTER_ROLE_NAME="monitoring-clusterrole"
CLUSTER_ROLE_BINDING_NAME="monitoring-clusterrole-binding"

echo "Deleting monitoring RBAC resources and Namespace..."

# 删除 ClusterRoleBinding
kubectl delete clusterrolebinding ${CLUSTER_ROLE_BINDING_NAME} --ignore-not-found=true

# 删除 ClusterRole
kubectl delete clusterrole ${CLUSTER_ROLE_NAME} --ignore-not-found=true

# 删除整个 Namespace (这将同时删除其中的 ServiceAccount)
kubectl delete namespace ${NAMESPACE} --ignore-not-found=true

echo "Cleanup complete."
```

## 实际应用场景

### 场景一：Prometheus 监控

在 Prometheus 的配置中，我们需要使用这个 Token 来访问 Kubernetes API：

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: prometheus-k8s-token
  namespace: monitoring
type: Opaque
stringData:
  token: ${TOKEN}
---
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: k8s
  namespace: monitoring
spec:
  endpoints:
  - port: https
    scheme: https
    tlsConfig:
      insecureSkipVerify: true
    bearerTokenFile: /var/run/secrets/kubernetes.io/serviceaccount/token
```

### 场景二：Grafana Agent

Grafana Agent 也需要类似的配置：

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: grafana-agent-token
  namespace: monitoring
type: Opaque
stringData:
  token: ${TOKEN}
---
apiVersion: monitoring.grafana.com/v1alpha1
kind: GrafanaAgent
metadata:
  name: k8s-agent
  namespace: monitoring
spec:
  metrics:
    instances:
    - name: k8s
      scrapeConfigs:
      - jobName: kubernetes-apiservers
        kubernetes_sd_configs:
        - role: endpoints
        bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
```

## 常见问题排查

### 1. Token 过期问题

如果遇到 Token 过期，错误信息通常如下：

```json
{
  "kind": "Status",
  "apiVersion": "v1",
  "metadata": {},
  "status": "Failure",
  "message": "Unauthorized",
  "reason": "Expired",
  "code": 401
}
```

解决方案：
- 重新生成 Token
- 考虑使用 TokenRequest API 创建长期有效的 Token

### 2. 权限不足问题

如果遇到权限不足，错误信息会明确指出缺少什么权限：

```json
{
  "kind": "Status",
  "apiVersion": "v1",
  "metadata": {},
  "status": "Failure",
  "message": "nodes \"node-1\" is forbidden: User \"system:serviceaccount:monitoring:monitoring-sa\" cannot get resource \"nodes/proxy\" in API group \"\" at the cluster scope",
  "reason": "Forbidden",
  "code": 403
}
```

解决方案：
- 检查 ClusterRole 中是否包含了所需的资源权限
- 确认 ClusterRoleBinding 是否正确绑定
- 使用 `kubectl auth can-i` 命令检查权限

## 最佳实践建议

1. **定期轮换 Token**
   - 建议每 90 天轮换一次 Token
   - 使用自动化脚本进行轮换
   - 确保轮换过程不影响监控系统运行

2. **最小权限原则**
   - 只授予必要的权限
   - 定期审查权限配置
   - 使用 `kubectl auth can-i` 验证权限

3. **安全存储**
   - 使用 Kubernetes Secrets 存储 Token
   - 避免在代码或配置文件中硬编码
   - 使用 RBAC 控制对 Secret 的访问

4. **监控 Token 使用情况**
   - 记录 Token 的创建和轮换时间
   - 监控异常访问模式
   - 设置告警机制

## 总结

通过本文，我们学习了：
1. 如何创建一个安全的监控 Token
2. 如何正确配置 RBAC 权限
3. 如何验证 Token 的有效性
4. 如何在实际场景中应用
5. 如何排查常见问题
6. 如何遵循最佳实践

记住，安全不是一蹴而就的，而是需要持续维护和改进的过程。定期审查和更新你的安全配置，确保你的 Kubernetes 集群始终处于最佳的安全状态。
