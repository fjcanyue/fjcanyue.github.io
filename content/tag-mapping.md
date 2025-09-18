# Tag标准化映射表

本文档记录了现有非规范tag到标准化tag的映射关系，用于指导tag标准化工作。

## 映射规则

1. 同义词统一：如"AI"、"ai"、"人工智能"统一为`ai`
2. 中英文统一：优先使用英文tag，中文tag仅在必要时保留
3. 合并近义词：如"Agent"、"AI Agent"、"智能体"统一为`agent`
4. 简化复合词：如"Tool Engineering"简化为`tooling`

## Tag映射列表

| 原始Tag | 标准化Tag | 说明 |
|---------|-----------|------|
| AI | ai | 统一为小写 |
| ai | ai | 标准形式 |
| Agent | agent | 统一为小写 |
| AI Agent | agent | 合并到agent |
| LLM | llm | 标准形式 |
| Reliability | - | 删除，可通过内容体现 |
| Cost | - | 删除，可通过内容体现 |
| Tool Engineering | tooling | 归类到工具链 |
| Human-in-the-loop | - | 删除，可通过内容体现 |
| AI Hype | - | 删除，可通过内容体现 |
| Agent Lifecycle | agent | 归类到agent |
| AgentOps | agent | 归类到agent |
| Architecture | architecture | 标准形式 |
| ChatOps | - | 删除，特定概念 |
| best-practices | best-practices | 标准形式 |
| ai-tool | ai | 归类到ai |
| coding | development | 归类到开发 |
| android | - | 删除，可通过内容体现 |
| bootloader | - | 删除，可通过内容体现 |
| root | - | 删除，可通过内容体现 |
| 监控 | - | 删除，可通过内容体现 |
| RBAC | security | 归类到安全 |
| DevOps | devops | 标准形式 |
| faiss | - | 删除，特定库 |
| library | - | 删除，可通过内容体现 |
| mcp | mcp | 标准形式 |
| 技术趋势 | - | 删除，可通过内容体现 |
| macos | linux | 合并到操作系统类别 |
| apm | - | 删除，可通过内容体现 |
| apache-httpclient | java | 归类到编程语言 |
| mns | - | 删除，特定服务 |
| template-engine | java | 归类到编程语言 |
| benchmark | performance | 归类到性能 |
| thymeleaf | java | 归类到编程语言 |
| freemarker | java | 归类到编程语言 |
| velocity | java | 归类到编程语言 |
| rocker | java | 归类到编程语言 |
| migration | - | 删除，可通过内容体现 |
| upgrade | - | 删除，可通过内容体现 |
| chinese | - | 删除，语言相关 |
| cli | development | 归类到开发 |
| markdown | - | 删除，可通过内容体现 |
| ppt | - | 删除，可通过内容体现 |
| marp | - | 删除，特定工具 |
| presentation | - | 删除，可通过内容体现 |
| tradecraft | development | 归类到开发 |
| vm | - | 删除，可通过内容体现 |
| virtualbox | - | 删除，可通过内容体现 |
| windows | - | 删除，操作系统相关 |
| design | - | 删除，可通过内容体现 |
| ux | - | 删除，可通过内容体现 |
| sensory design | - | 删除，可通过内容体现 |
| Agentic Systems | agent | 归类到agent |
| Shopify | - | 删除，特定平台 |
| 检索增强 | rag | 归类到rag |
| 大语言模型 | llm | 归类到llm |
| 企业应用 | - | 删除，可通过内容体现 |
| 知识库 | - | 删除，可通过内容体现 |
| 自动化 | - | 删除，可通过内容体现 |
| cot | - | 删除，特定概念 |
| react | - | 删除，特定框架（与前端框架react区分） |
| 人工智能 | ai | 归类到ai |
| cluster | - | 删除，可通过内容体现 |
| distributed-systems | - | 删除，可通过内容体现 |
| 树莓派 | - | 删除，特定硬件 |
| microSD | - | 删除，特定硬件 |
| 存储可靠性 | - | 删除，可通过内容体现 |
| 硬件选购 | - | 删除，可通过内容体现 |
| 数据安全 | security | 归类到安全 |
| 高耐久度 | - | 删除，可通过内容体现 |
| 闪存 | - | 删除，可通过内容体现 |
| 单板计算机 | - | 删除，可通过内容体现 |
| programming | development | 归类到开发 |
| visual-programming | development | 归类到开发 |
| yarnpkg | javascript | 归类到编程语言 |
| hadoop | - | 删除，特定框架 |
| yarn | - | 删除，名称冲突项 |
| command-line | development | 归类到开发 |
| path | - | 删除，特定概念 |
| conflict | - | 删除，可通过内容体现 |
| mysql | database | 归类到数据库 |
| 性能调优 | performance | 归并到性能 |
| 参数配置 | - | 删除，可通过内容体现 |
| innodb | database | 归类到数据库 |
| 游戏产业 | - | 删除，领域相关 |
| Valve | - | 删除，特定公司 |
| Steam | - | 删除，特定平台 |
| 半条命 | - | 删除，特定产品 |
| 创新 | - | 删除，可通过内容体现 |
| 科技人物 | - | 删除，可通过内容体现 |
| 游戏开发 | - | 删除，可通过内容体现 |
| 数字发行 | - | 删除，可通过内容体现 |
| ai tool | ai | 归类到ai |
| animation | - | 删除，可通过内容体现 |
| video | - | 删除，可通过内容体现 |
| 人物 | - | 删除，可通过内容体现 |

## 标准化Tag词表

### 技术领域类
- `ai` - 人工智能相关
- `llm` - 大语言模型
- `agent` - AI代理/智能体
- `rag` - 检索增强生成
- `mcp` - 模型上下文协议
- `devops` - 开发运维
- `kubernetes` - Kubernetes容器编排
- `docker` - Docker容器技术
- `database` - 数据库技术
- `java` - Java编程语言
- `python` - Python编程语言
- `javascript` - JavaScript编程语言
- `git` - Git版本控制
- `linux` - Linux操作系统

### 应用场景类
- `best-practices` - 最佳实践
- `troubleshooting` - 故障排查
- `performance` - 性能优化
- `security` - 安全相关
- `architecture` - 系统架构
- `development` - 软件开发
- `tooling` - 工具链

### 产品工具类
- `cursor` - Cursor AI编程工具
- `github` - GitHub平台
- `gitlab` - GitLab平台
- `vscode` - Visual Studio Code编辑器
- `zookeeper` - Zookeeper分布式协调服务