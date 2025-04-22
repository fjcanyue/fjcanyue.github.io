---
title: GitLab CE 汉化版 Docker 镜像升级与迁移指南 (从 twang2218/gitlab-ce-zh 迁移)
date: 2020-05-13 11:59:23
tags: ["gitlab", "docker", "docker-compose", "migration", "upgrade", "chinese"]
---

## 背景说明

许多用户之前可能使用了 `twang2218/gitlab-ce-zh` 这个 Docker 镜像来运行 GitLab 社区版的汉化版本。然而，该镜像的维护者已停止更新，导致用户无法升级到较新的 GitLab 版本。

直接切换到 GitLab 官方的 Docker 镜像 (`gitlab/gitlab-ce:latest`) 进行升级时，可能会因为中文环境的 locale 配置问题导致升级失败或数据迁移出错。

为了解决这个问题，我们提供了一个基于官方镜像并处理了 locale 兼容性的新镜像 `fjcanyue/gitlab-ce-zh`，旨在帮助大家顺利地从旧的汉化版镜像迁移和升级到更新的 GitLab 版本。

## 如何使用新镜像进行升级/迁移

核心步骤非常简单：**只需将你现有的 Docker 或 Docker Compose 配置中的镜像名称替换为 `fjcanyue/gitlab-ce-zh:latest` (或指定版本号) 即可。**

### 场景一：使用 Docker Compose

如果你的 GitLab 是通过 Docker Compose 部署的，请修改你的 `docker-compose.yml` 文件：

1.  找到 `services` -> `gitlab` -> `image` 这一行。
2.  将其值从 `twang2218/gitlab-ce-zh:xxx` 或其他旧镜像，**更改为 `fjcanyue/gitlab-ce-zh:latest`**。

修改后的 `docker-compose.yml` 文件示例：

```yaml:d%3A%5Cprojects%5Cblog%5Cdocker-compose.yml
version: '2' # 或者 '3' 等你的版本
services:
    gitlab:
      # --- 修改这里 ---
      # image: 'twang2218/gitlab-ce-zh:some-old-version' # 旧镜像
      image: 'fjcanyue/gitlab-ce-zh:latest'             # 替换为新镜像
      # --- 修改结束 ---

      restart: unless-stopped
      hostname: 'gitlab.example.com' # 替换为你的 GitLab 访问域名
      environment:
        TZ: 'Asia/Shanghai'
        GITLAB_OMNIBUS_CONFIG: |
          # --- 保留你原有的配置 ---
          external_url 'http://gitlab.example.com' # 替换为你的 GitLab 访问 URL
          gitlab_rails['time_zone'] = 'Asia/Shanghai'
          # 需要配置到 gitlab.rb 中的配置可以在这里配置，每个配置一行，注意缩进。
          # 比如下面的电子邮件的配置：
          # gitlab_rails['smtp_enable'] = true
          # gitlab_rails['smtp_address'] = "smtp.exmail.qq.com"
          # gitlab_rails['smtp_port'] = 465
          # gitlab_rails['smtp_user_name'] = "xxxx@xx.com"
          # gitlab_rails['smtp_password'] = "password"
          # gitlab_rails['smtp_authentication'] = "login"
          # gitlab_rails['smtp_enable_starttls_auto'] = true
          # gitlab_rails['smtp_tls'] = true
          # gitlab_rails['gitlab_email_from'] = 'xxxx@xx.com'
          # --- 保留你原有的配置结束 ---
      ports:
        # --- 保留你原有的端口映射 ---
        - '80:80'
        - '443:443'
        - '22:22' # 如果需要 SSH 访问，请保留
      volumes:
        # --- 确保 Volumes 映射保持不变，指向你现有的数据目录 ---
        - config:/etc/gitlab
        - data:/var/opt/gitlab
        - logs:/var/log/gitlab

# --- 确保 Volumes 定义保持不变 ---
volumes:
    config:
      # external: true # 如果你使用的是外部 volume，请保留相应配置
    data:
      # external: true
    logs:
      # external: true
```

