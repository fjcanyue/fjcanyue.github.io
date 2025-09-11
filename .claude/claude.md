# 项目说明
- **类型：** Hugo 静态博客
- **目标：** 稳定、可维护、可持续写作的个人/团队博客，专注清晰信息架构、良好 SEO、易部署。
- **优先级顺序：** 内容质量 > 架构与可维护性 > 性能与可访问性 > 视觉细节。
- **你应当：** 在任何修改前读完此文件；所有变更均需解释理由并给出可回滚的最小改动集。

---

# 代码与目录约定
- **配置文件：** 使用 `config.toml`（如已有 `yaml/json` 不强迁移，仅保持一致）
- **标准结构：**
  - `/content` 文章内容（按语言子目录分组：`/content/zh`, `/content/en`）
  - `/archetypes` 文章原型（默认 `default.md`；必要时新增 `post.md`, `note.md`）
  - `/layouts` 模板（`_default/baseof.html`, `list.html`, `single.html`；分区模板按需覆盖）
  - `/layouts/partials` 公共局部（`head.html`, `header.html`, `footer.html`, `seo.html`）
  - `/layouts/shortcodes` 短代码
  - `/static` 静态资源（不经管道处理）
  - `/assets` 可经 Hugo Pipes 处理的 SASS/JS/图片等
  - `/themes` 主题（若使用第三方主题，避免直接改主题；在 `layouts` 覆盖）
  - `/i18n` 多语言翻译
- **不做直接修改：** 第三方主题目录。通过项目 `layouts` 层叠覆盖。

---

# 内容与前言块规范
- **文件命名：** 小写短横线（例如 `building-hugo-blog.md`）
- **路径：** `/content/<lang>/<section>/<slug>/index.md`（资源 colocate 在同目录）
- **前言块最小集：**
  - `title`：简短明确，60 字符内
  - `date`：创建时间；`lastmod` 自动或手动维护
  - `draft`：初稿设为 `true`
  - `description`：一句话摘要
  - `tags`/`categories`：从受控词表中选（见下）
  - `slug`：可选；默认用文件名
  - `aliases`：重命名或迁移时设旧链接
  - `toc`：按需开启目录
- **受控词表：**
  - `categories`: [`tech`, `life`, `notes`, `reading`, `opinion`]
  - `tags`: 自由但建议每篇 ≤ 5 个；避免同义重复
- **草稿与发布：**
  - 草稿：`draft=true`；本地预览 `hugo server -D`
  - 发布：移除或设 `draft=false`；必要时添加 `publishDate`

---

# 多语言与路由
- **默认语言：** 在 `config.toml` 中设 `defaultContentLanguage = "zh"`
- **语言路径：** `defaultContentLanguageInSubdir = true` 时，中文路径为 `/zh/...`
- **翻译策略：**
  - 跨语言文章使用相同目录结构与 `slug`，用不同语言内容文件
  - 导航、按钮、多语言 UI 文案在 `/i18n/*.toml` 维护
- **链接：** 避免硬编码站点域名，用 `relURL`/`absURL` 或 `relref`/`ref`

---

# 模板与短代码
- **基座模板：** `_default/baseof.html` 统一包含 `partials/head.html`, `header.html`, `footer.html`, `scripts.html`
- **列表/文章模板：** `_default/list.html`, `_default/single.html`，按 section 定制覆盖
- **短代码规范：**
  - 命名：语义化、短小（如 `note`, `warn`, `img`, `codecaption`）
  - 参数：具名参数优先；提供合理默认值
  - 文档：每个短代码在注释首行说明用法
- **图片处理：** 使用 Page Bundle + `.Resources`，配合 `resources.Fingerprint` 与 Hugo 图像管道 `Fit/Fill/Resize`
- **Mermaid：** 使用 `{{< mermaid >}}` <mermaid 代码> `{{< /mermaid >}}` 格式编写 Mermaid 流程图

---

# 主题与样式
- **主题选择：** 可用第三方主题；若改动较多，建议自建最小样式层
- **覆盖策略：**
  - 不改主题源；使用项目 `layouts` 与 `assets` 覆盖
  - CSS 使用 SASS，在 `assets/scss`；入口单文件（如 `main.scss`），通过 Hugo Pipes 构建与指纹
- **暗色模式：** 使用 `prefers-color-scheme`，并提供手动切换（localStorage 记忆）

---

# SEO、社交与可访问性
- **Head 与元信息：** `partials/seo.html` 输出 `title`、`meta description`、`canonical`、`og:*`、`twitter:*`
- **结构化数据：** 文章页输出 `Article` JSON-LD，首页/作者页输出 `WebSite/Person`
- **站点地图与 robots：** 启用 `sitemap`；提供 `robots.txt`
- **链接：** 站内相对、站外 `rel="noopener noreferrer"`；死链检查在 CI
- **可访问性：**
  - 所有图片必须有 `alt`
  - 颜色对比满足 WCAG AA
  - 键盘可达与焦点可见
  - 语义化标签（`main`, `nav`, `article`, `aside`, `footer`）

---

# 性能与构建
- **构建命令：**
  - 开发：`hugo server -D`（含草稿）
  - 生产：`hugo --minify`
- **静态资源：**
  - 通过 Hugo Pipes 压缩、合并、指纹
  - 使用 `integrity` 与 `crossorigin` 输出 `<link>`/`<script>`
  - 延迟加载：`loading="lazy"`；非关键 JS `defer`
- **图像：** 生成多尺寸、`srcset`，存储为 WebP 优先，必要时回退
- **缓存：** 使用指纹版本化，避免手工改查询参数

---

# 部署与环境
- **环境变量：** 使用 `.env`（不入库）；Hugo 可用 `--environment` 或 `HUGO_ENV`
- **常见目标：**
  - Netlify：自动部署；设置 `HUGO_VERSION` 与 构建命令
  - Vercel：输出到 `public`（默认 `hugo` 输出），设置框架为其它静态
  - GitHub Pages：构建产物在 `gh-pages` 分支；CI 使用 `peaceiris/actions-hugo`
- **预览链接：** PR 必须生成预览部署，便于验收

---

# 开发工作流
1. **新建内容：** `hugo new <section>/<slug>/index.md`（从 archetype 生成）
2. **本地预览：** `hugo server -D`，检查布局、链接、图片、目录、暗黑模式
3. **提交规范：** `feat(content): zh post about ...`；范围使用 `content/layouts/assets/build`
4. **PR 检查：**
   - ✅ 构建通过
   - ✅ 链接无错
   - ✅ 图片 alt 完整
   - ✅ SEO 元信息齐全
   - ✅ 多语言路径正确
5. **合并与发布：** squash 合并；生产部署完成后检查站点地图与关键页面

---

# 安全与合规
- **不包含：** 私密密钥、访问令牌、内网地址、个人隐私信息
- **外链脚本：** 白名单制；CDN 需支持 SRI；拒绝未知统计脚本
- **GDPR/隐私：** 若使用分析工具，提供弹窗/设置开关与隐私声明链接

---


# 常用 archetypes（archetypes/post.md）
```markdown
---
title: "{{ replace .Name "-" " " | title }}"
date: {{ .Date }}
lastmod: {{ .Date }}
draft: true
description: ""
categories: []
tags: []
toc: true
---

> 摘要：用 1–2 句说明本文结论或核心观点。

<!-- 正文从此开始 -->
```

# 质量清单（提交前自检）
- **内容：** 结构清晰、无错别字、外链可靠、引文有来源
- **前言块：** `title/description/tags/categories` 完整，`aliases` 处理重定向
- **可访问性：** 图片 `alt`、标题层级不跳级、颜色对比合规
- **SEO：** 标题 ≤ 60 字符，描述 120–160 字符，唯一 H1
- **性能：** 图片使用管道处理，资源已指纹，懒加载生效
- **多语言：** 路径/导航/翻译项对应完整
- **部署：** 预览链接可用，无 404/500

---

# 你在此项目中的行为准则
- **最小改动：** 在不破坏现有结构的前提下实现目标；提出多种方案并标注取舍
- **可回滚：** 每次 PR 仅做一类变更，附变更点概览与回滚步骤
- **可读性：** 模板中加入简短注释；短代码首行注释用法
- **对话风格：** 回答具体、给出可执行命令与路径；必要时请求缺失信息
```

