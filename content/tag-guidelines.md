# Tag使用规范

本文档定义了本博客项目中Tag的使用规范，以确保Tag的一致性和可维护性。

## 1. 基本原则

1. **数量限制**：每篇文章的Tag数量不应超过5个
2. **语义明确**：每个Tag应具有明确的技术含义
3. **避免重复**：避免使用同义或近义的Tag
4. **标准化命名**：使用小写字母和连字符分隔单词

## 2. Tag分类

### 2.1 技术领域类Tag
这些Tag表示文章涉及的技术领域：

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

### 2.2 应用场景类Tag
这些Tag表示文章的应用场景或主题：

- `best-practices` - 最佳实践
- `troubleshooting` - 故障排查
- `performance` - 性能优化
- `security` - 安全相关
- `architecture` - 系统架构
- `development` - 软件开发
- `tooling` - 工具链

### 2.3 产品工具类Tag
这些Tag表示文章涉及的具体产品或工具：

- `cursor` - Cursor AI编程工具
- `github` - GitHub平台
- `gitlab` - GitLab平台
- `vscode` - Visual Studio Code编辑器
- `zookeeper` - Zookeeper分布式协调服务

## 3. 使用指南

### 3.1 选择Tag的原则

1. **相关性优先**：选择与文章内容最相关的Tag
2. **抽象层次**：优先选择抽象层次适中的Tag，避免过于宽泛或过于具体
3. **技术栈导向**：优先选择能体现技术栈的Tag

### 3.2 Tag组合示例

- AI相关文章：`ai`, `llm`, `agent`（根据具体内容选择）
- 技术教程：`best-practices`, `troubleshooting`（根据文章性质选择）
- 工具使用：`tooling`, `cursor`, `github`（根据涉及的工具选择）

### 3.3 避免使用的Tag

以下类型的Tag应避免使用：

1. **过于宽泛**：如"技术"、"编程"等
2. **过于具体**：如特定版本号、特定配置项等
3. **同义重复**：如同时使用"AI"和"人工智能"
4. **时效性过强**：如特定年份、特定活动等

## 4. 维护机制

1. **定期审查**：每季度审查Tag使用情况，更新受控词表
2. **新Tag引入**：引入新Tag前需经过团队讨论
3. **废弃Tag处理**：对于不再使用的Tag，应制定迁移计划

## 5. 自动化工具

项目提供了一个自动化脚本`scripts/standardize-tags.py`，可用于：

1. 批量标准化现有文章的Tag
2. 检查Tag是否符合规范
3. 生成Tag使用报告

使用方法：
```bash
python scripts/standardize-tags.py
```

## 6. 违规处理

对于不符合规范的Tag使用：

1. **轻微违规**：通过PR评论提醒作者修改
2. **严重违规**：要求修改后重新提交PR
3. **重复违规**：在团队内进行规范培训