---
title: 解决 Pinpoint 监控 Apache HTTP Client 异步请求时的 SocketTimeoutException 问题
date: 2017-05-10 14:50:20
tags: ["pinpoint", "apm", "apache-httpclient", "java", "troubleshooting", "mns"]
---

## 问题背景

在使用分布式应用性能管理 (APM) 工具 [Pinpoint](https://github.com/pinpoint-apm/pinpoint) 对 Java 应用进行监控时，我们发现在调用某些基于 Apache HTTP Client (特别是其异步 NIO 客户端) 的服务时，偶尔会出现诡异的 `SocketTimeoutException` 错误。具体场景是我们的应用通过 Apache HTTP Client 调用阿里云消息服务 (MNS)。

## 错误现象

启用 Pinpoint Agent 后，相关调用链在 Pinpoint UI 上可能显示正常或超时，同时应用程序日志中出现类似以下的堆栈信息：

```java
Caused by: java.net.SocketTimeoutException
	at org.apache.http.nio.protocol.HttpAsyncRequestExecutor.timeout(HttpAsyncRequestExecutor.java:351)
	at org.apache.http.impl.nio.client.InternalIODispatch.onTimeout(InternalIODispatch.java:92)
	at org.apache.http.impl.nio.client.InternalIODispatch.onTimeout(InternalIODispatch.java:39)
	at org.apache.http.impl.nio.reactor.AbstractIODispatch.timeout(AbstractIODispatch.java:177)
	at org.apache.http.impl.nio.reactor.BaseIOReactor.sessionTimedOut(BaseIOReactor.java:265)
	at org.apache.http.impl.nio.reactor.AbstractIOReactor.timeoutCheck(AbstractIOReactor.java:494)
	at org.apache.http.impl.nio.reactor.BaseIOReactor.validate(BaseIOReactor.java:215)
	at org.apache.http.impl.nio.reactor.AbstractIOReactor.execute(AbstractIOReactor.java:282)
	at org.apache.http.impl.nio.reactor.BaseIOReactor.execute(BaseIOReactor.java:106)
	at org.apache.http.impl.nio.reactor.AbstractMultiworkerIOReactor$Worker.run(AbstractMultiworkerIOReactor.java:590)
	... more
```

这个超时异常看起来像是网络问题或服务端处理慢，但奇怪的是，禁用 Pinpoint Agent 后问题就消失了，这表明问题很可能与 Pinpoint 的监控插桩有关。

## 问题分析：HttpEntity 的可重复性 (Repeatability)
经过排查，我们发现问题根源在于 Pinpoint 对 Apache HTTP Client 请求体 (HttpEntity) 的处理方式以及 HttpEntity 自身的可重复性特性。

Pinpoint 为了能在调用链追踪中记录 HTTP 请求的详细信息（例如 POST 请求的参数），会尝试读取请求体的内容。然而，Apache HTTP Client 中的 HttpEntity 分为几种类型，其中一种是 流式实体 (Streamed Entity) 。

根据 Apache HttpCore 的官方文档说明：

- 流式 (streamed): 内容从流中接收，或动态生成。特别是，从连接接收的实体属于此类。 流式实体通常是不可重复读取的 (not repeatable) 。
- 自包含 (self-contained): 内容在内存中，或通过独立于连接或其他实体的方式获取。 自包含实体通常是可重复读取的 (repeatable) 。
- 包装 (wrapping): 内容从另一个实体获取。

当 HttpEntity 是一个 不可重复读取 的流式实体时（例如，直接来自输入流或者某些动态生成的内容），它内部的数据流只能被消费一次。如果 Pinpoint 为了记录请求参数而尝试读取这个流，那么当 Apache HTTP Client 真正要发送请求时，流可能已经到达末尾或处于无效状态，导致无法正确发送请求内容，最终可能表现为连接异常或超时。

在我们的场景中，调用阿里云 MNS SDK 时，其内部使用的 Apache HTTP Client 可能创建了不可重复读取的 HttpEntity 。Pinpoint 的默认配置会尝试读取这种实体，从而干扰了正常的请求发送流程。

## 解决方案
要解决这个问题，我们需要调整 Pinpoint Agent 的配置文件 pinpoint.config (或 pinpoint-env.config )， 禁止 Pinpoint 尝试读取可能不可重复的请求体 。

找到以下配置项：

将其值修改为 false ：

修改说明：

- profiler.apache.httpclient4.entity 这个配置项控制 Pinpoint 是否尝试记录 Apache HTTP Client 4.x 发出的 POST 或 PUT 请求的实体内容。
- 虽然注释中提到 "Limited to entities where HttpEntity.isRepeatable() == true"，但在某些复杂或特定实现下，Pinpoint 的判断或读取操作仍可能干扰不可重复的流。
- 将其设置为 false 后，Pinpoint 将不再尝试读取请求体内容，从而避免了与不可重复实体的冲突。缺点是在 Pinpoint UI 上可能无法看到具体的 POST/PUT 请求参数，但可以保证业务调用的正常进行。
修改配置后， 重启 你的 Java 应用使配置生效。之后，调用 MNS 或其他类似服务的 SocketTimeoutException 问题应该就能得到解决。

## 总结
Pinpoint 是一个强大的 APM 工具，但在监控某些特定库（如 Apache HTTP Client 的异步调用）时，其默认配置可能与库的内部机制（如 HttpEntity 的可重复性）产生冲突。遇到类似问题时，除了检查网络和服务端，也应考虑 APM 工具本身的配置和插桩行为。通过调整 profiler.apache.httpclient4.entity 配置，可以有效解决因读取不可重复请求体导致的超时或其他异常。
