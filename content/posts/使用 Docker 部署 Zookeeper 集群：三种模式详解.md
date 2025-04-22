---
title: 使用 Docker 部署 Zookeeper 集群：三种模式详解 (fjcanyue/zookeeper 镜像)
date: 2017-03-24 16:36:42
tags: ["docker", "zookeeper", "docker-compose", "cluster", "distributed-systems"]
---

本文档介绍了如何使用 [fjcanyue/docker-zookeeper](https://github.com/fjcanyue/docker-zookeeper) 这个 Docker 镜像来部署 Apache Zookeeper。该镜像支持以下三种常见的部署模式，方便你在不同场景下快速搭建 Zookeeper 服务：

*   **单机模式 (Standalone Mode):** 在单台机器上运行一个独立的 Zookeeper 实例，主要用于开发或测试环境。
*   **伪集群模式 (Pseudo-Distributed Mode):** 在单台机器上运行多个 Zookeeper 实例，模拟一个真实的集群环境，同样适用于开发或测试。
*   **完全分布式模式 (Fully-Distributed Mode):** 将多个 Zookeeper 实例分别部署在不同的物理或虚拟机上，组成一个生产环境级别的高可用集群。

以下将分别介绍如何使用 Docker Compose 配置和启动这三种模式。

### 模式一：单机模式 (Standalone Mode)

此模式下，我们只在一台机器上部署一个 Zookeeper 实例。

**`docker-compose.yml` 配置:**

```yaml:d%3A%5Cprojects%5Cblog%5Cdocker-compose-standalone.yml
version: '2' # 或更高版本，如 '3.8'
services:
  zookeeper: # 服务名称可以自定义
    container_name: zookeeper_standalone # 容器名称
    hostname: zk_standalone # 容器主机名
    image: fjcanyue/zookeeper # 使用指定的 Zookeeper 镜像
    restart: always # 容器退出时总是自动重启
    ports:
      - "2181:2181" # 将主机的 2181 端口映射到容器的 2181 端口 (Zookeeper 客户端端口)
    # environment: # 单机模式下通常不需要特殊环境变量，镜像会默认配置
      # ZOOKEEPER_PORT: 2181 # 默认客户端端口
    volumes:
      # 可选：将数据和日志持久化到宿主机，防止容器删除后数据丢失
      - ./zk-standalone/data:/data
      - ./zk-standalone/datalog:/datalog
```

启动命令: 在包含 docker-compose-standalone.yml 文件的目录下执行：

### 模式二：伪集群模式 (Pseudo-Distributed Mode)
此模式下，我们在 同一台机器 上部署三个 Zookeeper 实例，它们通过内部网络相互通信，组成一个集群。

`docker-compose.yml `配置:

```yaml
version: '2' # 或更高版本
services:
  zookeeper1:
    container_name: zookeeper1
    hostname: zk1 # 容器主机名，用于节点间通信
    image: fjcanyue/zookeeper
    restart: always
    ports:
      - "2181:2181" # 第一个实例的客户端端口映射到主机 2181
    environment:
      ZOOKEEPER_PORT: 2181 # 容器内客户端端口
      ZOOKEEPER_MYID: 1    # 当前实例的唯一 ID (1-255)
      # 定义集群所有节点的地址信息 (server.ID=hostname:peerPort:leaderPort)
      ZOOKEEPER_NODES: server.1=zk1:2888:3888,server.2=zk2:2888:3888,server.3=zk3:2888:3888
    volumes:
      - ./zk-pseudo/zk1/data:/data
      - ./zk-pseudo/zk1/datalog:/datalog
    networks:
      zk_network: # 将所有实例连接到同一个自定义网络

  zookeeper2:
    container_name: zookeeper2
    hostname: zk2
    image: fjcanyue/zookeeper
    restart: always
    ports:
      - "2182:2181" # 第二个实例的客户端端口映射到主机 2182
    environment:
      ZOOKEEPER_PORT: 2181
      ZOOKEEPER_MYID: 2    # 当前实例的唯一 ID
      ZOOKEEPER_NODES: server.1=zk1:2888:3888,server.2=zk2:2888:3888,server.3=zk3:2888:3888
    volumes:
      - ./zk-pseudo/zk2/data:/data
      - ./zk-pseudo/zk2/datalog:/datalog
    networks:
      zk_network:

  zookeeper3:
    container_name: zookeeper3
    hostname: zk3
    image: fjcanyue/zookeeper
    restart: always
    ports:
      - "2183:2181" # 第三个实例的客户端端口映射到主机 2183
    environment:
      ZOOKEEPER_PORT: 2181
      ZOOKEEPER_MYID: 3    # 当前实例的唯一 ID
      ZOOKEEPER_NODES: server.1=zk1:2888:3888,server.2=zk2:2888:3888,server.3=zk3:2888:3888
    volumes:
      - ./zk-pseudo/zk3/data:/data
      - ./zk-pseudo/zk3/datalog:/datalog
    networks:
      zk_network:

# 定义自定义网络，允许容器通过 hostname (zk1, zk2, zk3) 相互访问
networks:
  zk_network:
    driver: bridge
```

启动命令: 在包含 docker-compose-pseudo.yml 文件的目录下执行：

### 模式三：完全分布式模式 (Fully-Distributed Mode)
此模式下，我们将三个 Zookeeper 实例分别部署在 三台不同的机器 上。假设这三台机器的主机名（或 IP 地址）分别是 `machine1` , `machine2` , `machine3` ，并且它们之间网络互通（特别是 2888 和 3888 端口）。

你需要在 每台机器上 分别放置一个 `docker-compose.yml` 文件，并进行相应的配置。

机器 1 ( `machine1` ) 上的 `docker-compose.yml` :

```yaml
version: '2'
services:
  zookeeper1:
    container_name: zookeeper1 # 容器名称
    # hostname: zk1 # 可选，如果网络配置允许通过主机名访问
    image: fjcanyue/zookeeper
    restart: always
    network_mode: "host" # 使用主机网络模式，容器直接使用主机的网络栈和端口
    # ports: # host 模式下不需要再定义端口映射
    #   - "2181:2181"
    #   - "2888:2888"
    #   - "3888:3888"
    environment:
      ZOOKEEPER_PORT: 2181 # 客户端端口
      ZOOKEEPER_MYID: 1    # 当前机器上实例的 ID
      # 定义集群所有节点的地址信息，使用实际的主机名或 IP 地址
      ZOOKEEPER_NODES: server.1=machine1:2888:3888,server.2=machine2:2888:3888,server.3=machine3:2888:3888
    volumes:
      # 将数据持久化到宿主机
      - /path/on/machine1/zk/data:/data
      - /path/on/machine1/zk/datalog:/datalog
```

机器 2 ( `machine2` ) 上的 `docker-compose.yml` :

```yaml
version: '2'
services:
  zookeeper2: # 服务名和容器名建议与 ID 对应
    container_name: zookeeper2
    image: fjcanyue/zookeeper
    restart: always
    network_mode: "host"
    environment:
      ZOOKEEPER_PORT: 2181
      ZOOKEEPER_MYID: 2    # 修改为当前机器实例的 ID
      ZOOKEEPER_NODES: server.1=machine1:2888:3888,server.2=machine2:2888:3888,server.3=machine3:2888:3888 # 集群节点信息保持一致
    volumes:
      - /path/on/machine2/zk/data:/data # 注意修改为本机路径
      - /path/on/machine2/zk/datalog:/datalog # 注意修改为本机路径
```

机器 3 ( `machine3` ) 上的 `docker-compose.yml` :

```yaml
version: '2'
services:
  zookeeper3:
    container_name: zookeeper3
    image: fjcanyue/zookeeper
    restart: always
    network_mode: "host"
    environment:
      ZOOKEEPER_PORT: 2181
      ZOOKEEPER_MYID: 3    # 修改为当前机器实例的 ID
      ZOOKEEPER_NODES: server.1=machine1:2888:3888,server.2=machine2:2888:3888,server.3=machine3:2888:3888 # 集群节点信息保持一致
    volumes:
      - /path/on/machine3/zk/data:/data # 注意修改为本机路径
      - /path/on/machine3/zk/datalog:/datalog # 注意修改为本机路径
```

启动命令: 在 每台 机器上，进入包含对应 docker-compose.yml 文件的目录，执行：

```bash
docker-compose up -d
 ```

**注意事项 (完全分布式模式)**:

- **网络模式**: 推荐使用 `network_mode: "host"` ，这样容器直接使用宿主机的 IP 和端口，简化了节点间通信的配置。如果使用默认的 bridge 网络，你需要确保容器端口（2181, 2888, 3888）正确映射到主机，并且 `ZOOKEEPER_NODES` 中使用的是 主机 IP 或可解析的主机名 。
- **主机名/IP**: `ZOOKEEPER_NODES` 环境变量中的 `machine1` , `machine2` , `machine3` 必须替换为 实际的、相互可访问 的主机名或 IP 地址。
- **防火墙**: 确保每台机器的防火墙允许其他 Zookeeper 节点访问所需的端口 (默认为 2181, 2888, 3888)。
- **数据卷**: 确保每台机器上的 `volumes` 路径指向本机实际存在的目录，用于持久化数据。
选择适合你需求的模式，并根据示例配置进行调整即可快速部署 Zookeeper。
