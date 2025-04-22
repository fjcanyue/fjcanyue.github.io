---
title: MCP评析：Anthropic的新接口探讨
date: 2025-03-28 14:59:23
tags: ["ai", "mcp"]
thumbnail: thumb-anthropic-mcp.jpg
---

Anthropic的MCP（Model Control Protocol）作为一种新型接口，旨在让大语言模型与外部工具交互。我使用它一段时间后，有了一些思考。虽然它代表了AI领域的创新尝试，但也存在一些值得商榷的设计决策。本文将从实用角度分析MCP的优缺点，帮助你了解这一技术的现状。

<!-- more -->

### 什么是MCP？
简单来说，MCP是Anthropic开发的一种协议，让Claude等大语言模型能够与外部工具和服务进行标准化交互。它就像是AI与外部世界之间的"翻译官"，使模型能够调用各种API和服务来完成复杂任务。

![Anthropic  Model Context Protocol (MCP)](https://www.descope.com/_next/image?url=https%3A%2F%2Fimages.ctfassets.net%2Fxqb1f63q68s1%2F2x3R1j8peZzdnweb5m1RK3%2Fa8628561358334a605e7f291560fc7cc%2FMCP_learning_center_image_1-min__1_.png&w=1920&q=75)

## 设计复杂性：是否必要？
### 过度工程化的问题
MCP的Python SDK设计让人感觉过于复杂。查看代码后，我发现它充斥着层层嵌套的包装器、访问器和装饰器，这些可能只需几行JSON和一个简单字典就能实现。

```python
# MCP Python SDK示例 - 复杂性展示
from anthropic.mcp import MCPClient, MCPServer, MCPTool
from anthropic.mcp.decorators import tool_definition

@tool_definition
def simple_calculator(a: int, b: int, operation: str) -> int:
    """一个简单的计算器工具"""
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    # ... existing code ...
```

这种复杂性让人想起Java或TypeScript的开发风格，而不是Python的简洁哲学。对于许多开发者来说，这种设计增加了不必要的学习成本和使用门槛。

### 为什么要重新发明轮子？
一个核心问题是：为什么需要创建一个新服务器来包装已存在的API？我们已经有了REST和Swagger/OpenAPI这样成熟的API规范，为什么不直接利用这些现有技术？

从实用角度看，从Swagger规范生成简化的JSON模式，使其与常用的工具定义对齐，会容易得多。这种方法可以减少代码重复，并利用已经存在的标准和工具。

## API集成的痛点
### 现有API难以复用
如果我想让大语言模型使用现有服务，为什么不让模型直接消费API呢？MCP要求我们为每个API创建新的包装层，这不仅增加了工作量，还引入了新的潜在故障点。

更令人担忧的是，我没有看到太多关于安全性、访问控制的内容，这让人难以放心将MCP服务器暴露给大语言模型。虽然这是一项正在进行的工作，但感觉在为每个API创建新服务器上浪费了很多精力。

### 更简单的替代方案
直接利用现有的API规范（如OpenAPI）可能是一种更高效的方法：

1. 从现有API的Swagger/OpenAPI规范生成简化的JSON模式
2. 使这些模式与常用的工具定义对齐
3. 让模型直接调用这些API，而不是通过额外的中间层
这种方法不仅简化了开发流程，还能更好地利用现有的API生态系统。

## 架构不匹配：持久连接的问题
### 与现代云架构的冲突
MCP被设计为面向连接和有状态的接口，这与现代无状态云服务的架构理念不符。许多API现在运行在AWS Lambda或Cloudflare Workers等无状态环境中，而MCP的设计似乎没有充分考虑这一点。

虽然Anthropic选择使用服务器发送事件（SSE）是个不错的决定，但即使去除网络组件，本地MCP服务器作为单独进程运行的方式仍然感觉臃肿且资源浪费。

### 安全隐患
将MCP服务器作为子进程运行引发了潜在的安全问题，特别是在权限控制和资源隔离方面。这种设计需要更严格的安全措施来防止可能的漏洞利用。

## 上下文拥挤：选项过多
### 模型上下文浪费
在实际测试中，我发现MCP倾向于将所有可能的选项都塞入模型上下文。这不仅浪费了宝贵的tokens，还可能导致模型行为不稳定。

例如，一个MCP服务器可能暴露以下所有功能：

- 数据检索功能
- 数据处理功能
- 文件操作功能
- API调用功能
- 数据库查询功能
- 图像处理功能
- 文本分析功能
- ...更多功能
即使当前任务只需要其中一两个功能，所有这些选项都会被塞入模型上下文，这显然是不高效的。

### 智能路由的缺失
MCP似乎缺少某种形式的"路由"或逐步、选择性暴露选项的机制。一个理想的解决方案应该能够根据当前任务的需求，只向模型暴露相关的工具和功能，这将大大提高效率和准确性。

## 结论：期待更好的解决方案
目前，MCP相比"标准"工具调用并没有显著优势。对于API集成，agents.json和围绕端点发现的概念可能是更自然的选择。

当然，AI和大语言模型领域正处于快速发展阶段，最佳实践和标准还在不断演化。作为开发者，我们需要保持开放的心态，但也要对新技术保持健康的批判精神。

虽然MCP代表了一种尝试标准化LLM与外部工具交互的努力，但其当前实现中的复杂性和设计决策使其难以在实际应用中广泛采用。随着这一领域的不断发展，我们可能会看到更简洁、更实用的解决方案出现。

## 关于作者

### Rui Carmo

技术专家，对AI和大语言模型有深入研究。本文是他对Anthropic的MCP接口的个人评析和思考。
