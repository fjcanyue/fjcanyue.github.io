---
title: 解决 Windows 环境下 Yarn (JS 包管理器) 与 Hadoop YARN 的 `yarn` 命令冲突问题
date: 2016-11-30 18:09:11
tags: ["yarnpkg", "hadoop", "yarn", "command-line", "path", "windows", "conflict"]
---

[Yarn](https://yarnpkg.com/) 是一个流行的 JavaScript 包管理器，由 Facebook (现 Meta) 开发，旨在替代 npm 提供更快、更可靠的依赖管理。
[Hadoop YARN](https://hadoop.apache.org/docs/current/hadoop-yarn/hadoop-yarn-site/YARN.html) (Yet Another Resource Negotiator) 则是 Apache Hadoop 生态系统中的资源管理器和作业调度器。

问题在于，这两款完全不同的工具，其命令行可执行文件都可能被命名为 `yarn` (或 `yarn.cmd` 在 Windows 上)。

如果你在同一台机器（尤其是 Windows）上同时安装了 Yarn (JS 包管理器) 和 Hadoop，并且两者的安装路径都被添加到了系统的 `PATH` 环境变量中，那么当你尝试在命令行中执行 `yarn` 命令时，系统可能会错误地调用 Hadoop YARN 的命令，导致意外的错误。

<!--more-->

## 冲突症状

当你期望运行 Yarn (JS 包管理器) 的命令时，例如检查版本：

```bash
yarn --version
```

你可能会遇到以下 并非来自 Yarn (JS 包管理器) 的错误信息：

```plaintext
Unrecognized option: --version
Error: Could not create the Java Virtual Machine.
Error: A fatal exception has occurred. Program will exit.
```

错误原因分析： 这个错误信息实际上是 Hadoop YARN 抛出的。因为系统根据 PATH 环境变量的顺序，先找到了 Hadoop 的 yarn.cmd 。Hadoop YARN 是一个 Java 程序，它不识别 --version 这个命令行参数，并且在尝试启动 Java 虚拟机 (JVM) 时可能因为错误的参数或其他配置问题而失败，最终导致程序退出。

## 根本原因
问题的根源在于：

1. 命令名称冲突： 两个不同的程序使用了相同的 yarn 命令名。
2. PATH 环境变量顺序： Windows (或其他操作系统) 在执行命令时，会按照 PATH 环境变量中列出的目录顺序查找可执行文件。如果 Hadoop 的 bin 目录在 PATH 中排在了 Yarn (JS 包管理器) 的 bin 目录之前，那么系统就会优先执行 Hadoop 的 yarn.cmd 。
## 解决方案
有几种方法可以解决这个冲突：

### 方案一：使用 yarnpkg 别名 (官方推荐)
Yarn (JS 包管理器) 的开发者意识到了这个冲突，并提供了一个备用命令名 yarnpkg 。在大多数情况下，你可以直接使用 yarnpkg 来代替 yarn 执行所有命令。

例如，检查版本：

```bash
yarnpkg --version
 ```

安装依赖：

```bash
yarnpkg install
 ```

添加依赖：

```bash
yarnpkg add <package_name>
 ```

这是最简单、最推荐的解决方案，因为它不需要修改系统环境。

### 方案二：调整 PATH 环境变量顺序 (Windows)
如果你更希望直接使用 yarn 命令来调用 JS 包管理器，可以通过调整系统 `PATH` 环境变量，让 Yarn (JS 包管理器) 的路径 优先于 Hadoop 的路径。

步骤 (以 Windows 10/11 为例)：

1. 在 Windows 搜索栏中搜索“环境变量”，选择“编辑系统环境变量”。
2. 在“系统属性”对话框中，点击“高级”选项卡下的“环境变量(N)...”按钮。
3. 在“环境变量”对话框的“系统变量(S)”（或“用户变量”，取决于你的安装方式）区域，找到名为 `Path` (或 `PATH` ) 的变量，选中它，然后点击“编辑(E)...”。
4. 在“编辑环境变量”对话框中，你会看到一个路径列表。找到包含 Yarn (JS 包管理器) 的 `bin` 目录的路径（例如 C:\Program Files (x86)\Yarn\bin 或 C:\Users\<YourUsername>\AppData\Local\Yarn\bin ）。
5. 找到包含 Hadoop 的 `bin` 目录的路径（例如 C:\hadoop\bin ）。
6. 选中 Yarn 的路径，使用右侧的“上移(U)”按钮，将其移动到 Hadoop 路径的 上方 。
7. 点击“确定”保存所有打开的对话框。
8. 重要： 关闭所有已打开的命令行窗口（如 CMD, PowerShell, VS Code 终端等），然后 重新打开 一个新的命令行窗口，使 `PATH` 的更改生效。
现在，当你在新的命令行窗口中输入 `yarn` 时，系统应该会优先找到并执行 Yarn (JS 包管理器) 的命令。

### 方案三：修改 Hadoop 的启动脚本 (不推荐)
理论上也可以修改 Hadoop 的 `yarn.cmd` 脚本名称，但这可能会影响 Hadoop 的正常使用或升级，因此 不推荐 这样做。

## 相关讨论
这个问题在 Yarn 的 GitHub 仓库中有过讨论： [Issue #673](https://github.com/yarnpkg/yarn/issues/673) 。虽然曾有人提议将 Yarn (JS) 命令改名为 `nyarn` 等，但最终官方选择提供 `yarnpkg` 别名作为主要的解决方案。

## 总结
Yarn (JS 包管理器) 和 Hadoop YARN 的 yarn 命令冲突是由于命名相同以及 `PATH` 环境变量顺序引起的。推荐使用官方提供的 `yarnpkg` 别名来调用 JS 包管理器，或者通过调整 `PATH` 环境变量的顺序来解决此问题。
