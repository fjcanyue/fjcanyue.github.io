---
title: Markdown 秒变 PPT：神器 Marp for VS Code 教程
date: 2020-07-07 23:19:23
tags: ["markdown", "ppt", "vscode", "marp", "presentation"]
---

对于习惯使用 Markdown 写作的朋友来说，如果能将写好的文档快速转换成 PPT 演示文稿，especially 对样式要求不高的场合，那绝对是一种高效的体验。今天就向大家推荐一款 VS Code 插件神器：**Marp for VS Code**，它可以轻松帮你实现这个目标！

<!-- more -->

# Marp for VS Code 核心功能

*   **实时预览：** 在 VS Code 中直接预览幻灯片效果，所见即所得。
*   **多格式导出：** 支持将 Markdown 导出为 HTML、PDF、PPTX (PowerPoint) 文件。
*   **图片导出：** 支持将幻灯片导出为 PNG 或 JPEG 图片（注意：免费版通常**仅支持导出第一页**）。
*   **主题支持：** 内置多种主题，并支持用户自定义 CSS 主题。
*   **Markdown 扩展：** 支持标准的 Markdown 语法，并增加了一些用于幻灯片的特殊指令 (Directives)。
*   **代码折叠：** 编辑器中可以方便地折叠单张幻灯片的代码。
*   **HTML 嵌入：** 允许在 Markdown 中直接嵌入 HTML 代码，实现更复杂的布局或效果。

# 安装步骤

安装过程非常简单：

1.  打开 Visual Studio Code。
2.  点击左侧边栏的 **扩展** 图标 (Extensions)。
3.  在搜索框中输入 `Marp`。
4.  找到 **Marp for VS Code** 插件。
5.  点击 **安装** (Install) 按钮。

# 使用方法

## 基础操作

1.  **启用 Marp：**
    *   **方法一 (推荐):** 在你的 Markdown 文件**最顶部**添加 YAML Front Matter 声明 `marp: true`。
        ```markdown
        ---
        marp: true
        ---

        # 你的第一页标题
        ```
    *   **方法二:** 打开命令面板 (Ctrl+Shift+P 或 Cmd+Shift+P)，输入 `Marp: Toggle Marp preview` 并执行，为当前文件临时启用/禁用 Marp 预览。

2.  **分隔幻灯片：** 使用 Markdown 的水平分割线 `---` 来分隔不同的幻灯片页面。
    ```markdown
    ---
    marp: true
    ---

    # 第一页

    这是第一页的内容。

    ---

    # 第二页

    这是第二页的内容。
    ```

3.  **开启实时预览：**
    *   点击 VS Code 编辑器右上角的 **预览** 图标 (通常是一个带有 Markdown 标志和眼睛的图标)。
    *   或者，打开命令面板 (Ctrl+Shift+P)，输入 `Markdown: Open Preview to the Side` (Markdown: 打开侧边预览) 并执行。

4.  **导出幻灯片：**
    *   点击 VS Code 编辑器右上角的 **Marp 图标** (通常是一个带有 Marp Logo 的图标)。
    *   在弹出的菜单中选择 **Export Slide Deck...** (导出幻灯片...)。
    *   选择你想要的导出格式，例如 **PowerPoint document (.pptx)**。
    *   根据提示选择保存位置，点击 **Export** (导出) 按钮。搞定！✌️

## 自定义主题

如果你觉得内置主题不够用，可以创建自己的主题。

1.  **创建 CSS 主题文件：**
    *   在你的项目工作区 (workspace) 内创建一个 CSS 文件，例如命名为 `my-theme.css`。
    *   在 CSS 文件顶部，使用 `/* @theme 主题名称 */` 来声明你的主题名称，例如 `/* @theme fjcanyue */`。
    *   使用 `@import 'default';` 或 `@import 'uncover';` 来继承一个内置主题的样式，然后在此基础上进行修改。
    *   编写你的自定义 CSS 规则。

    ```css:d%3A%5Cprojects%5Cblog%5Cmy-theme.css
    /* @theme fjcanyue */ /* 声明主题名称 */

    @import 'default'; /* 继承默认主题样式 */

    /* 自定义 section (幻灯片页面) 样式 */
    section {
        width: 1280px;    /* 页面宽度 */
        height: 720px;     /* 页面高度 (改为常见的16:9) */
        font-size: 32px;   /* 默认字体大小 */
        padding: 40px;     /* 内边距 */
        background: #f0f0f0; /* 页面背景色 */
        color: #333;       /* 默认文字颜色 */
    }

    /* 自定义 h1 标题样式 */
    h1 {
        font-size: 60px;
        color: #007acc;    /* 蓝色标题 */
        text-align: center; /* 标题居中 */
        margin-bottom: 40px;
    }

    /* 自定义 h2 标题样式 */
    h2 {
        font-size: 48px;
        color: #4a4a4a;
    }

    /* 示例：为带有 'invert' class 的页面设置反色效果 */
    section.invert {
      background: #333;
      color: #f0f0f0;
    }
    section.invert h1 {
      color: #fff;
    }
    ```

2.  **在 VS Code 中注册自定义主题：**
    *   打开 VS Code 的 **设置** (Settings)。可以通过 `文件` -> `首选项` -> `设置` (File > Preferences > Settings) 或快捷键 `Ctrl+,` 打开。
    *   切换到 **工作区** (Workspace) 设置选项卡。
    *   在搜索框中输入 `markdown.marp.themes`。
    *   找到 "Markdown › Marp: Themes" 设置项，点击 **在 settings.json 中编辑** (Edit in settings.json)。
    *   在 `settings.json` 文件中，添加你的 CSS 文件相对于工作区根目录的路径。如果 `settings.json` 不存在，VS Code 会在 `.vscode` 目录下创建它。

    ```json:d%3A%5Cprojects%5Cblog%5C.vscode%5Csettings.json
    {
        "markdown.marp.themes": [
            "./my-theme.css" // 添加你的自定义主题文件路径
        ]
    }
    ```
    *   保存 `settings.json` 文件。

3.  **在 Markdown 中使用自定义主题：**
    在 Markdown 文件的 YAML Front Matter 中，将 `theme` 指令设置为你定义的 CSS 主题名称 (即 `@theme` 后面的名字)。

    ```markdown:d%3A%5Cprojects%5Cblog%5Ccontent%5Cposts%5CMarkdown%E7%A7%92%E5%8F%98PPT.md
    ---
    marp: true
    theme: fjcanyue # 使用你自定义的主题名称
    ---

    # 使用自定义主题的第一页

    内容...

    ---
    <!-- _class: invert --> <!-- 可以为单页应用特定样式 -->

    # 使用自定义主题的第二页 (反色)

    内容...
    ```

现在，你的 Marp 预览和导出的文件就会应用你自定义的主题样式了！
