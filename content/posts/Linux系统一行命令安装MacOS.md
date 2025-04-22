---
title: Linux系统一行命令安装MacOS
date: 2020-07-24 14:59:23
tags: ["docker", "macos", "linux"]
---

想体验 MacOS 系统但苦于没有苹果设备？通过 Docker 容器技术，我们可以在 Linux 系统上轻松运行 MacOS！这个方案不仅适用于 Intel CPU，AMD CPU 同样可以使用，让我们一起来看看具体怎么操作。

<!-- more -->

# 准备工作

在开始之前，请确保你的系统满足以下条件：

## 系统环境要求
* 支持的 Linux 发行版：
  - Arch / Manjaro
  - Ubuntu / Debian
  - CentOS / RHEL / Fedora
* BIOS 已开启虚拟化功能（CPU Virtualization）

## 安装必要软件

1. 安装 QEMU 和相关依赖
```shell
# Arch/Manjaro 用户运行：
sudo pacman -S qemu libvirt dnsmasq virt-manager bridge-utils flex bison ebtables edk2-ovmf

# Ubuntu/Debian 用户运行：
sudo apt install qemu qemu-kvm libvirt-clients libvirt-daemon-system bridge-utils virt-manager

# CentOS/RHEL/Fedora 用户运行：
sudo yum install libvirt qemu-kvm -y
```

2. 启用必要的系统服务
```shell
sudo systemctl enable libvirtd.service
sudo systemctl enable virtlogd.service
sudo modprobe kvm
```

3. 确保已安装 Docker

# 安装步骤
## 1. 启动 MacOS 容器
打开终端，运行以下命令：
```shell
docker run \
-e RAM=8 \
-e CORES=4 \
--privileged -e "DISPLAY=${DISPLAY:-:0.0}" \
-v /tmp/.X11-unix:/tmp/.X11-unix sickcodes/docker-osx:latest
```

参数说明：

- RAM=8 ：分配 8GB 内存（可根据实际情况调整）
- CORES=4 ：分配 4 核 CPU（可根据实际情况调整）

## 2. 系统安装
1. 在启动界面选择 "Disk Utility"
2. 找到容量最大的磁盘，点击 "Erase"（抹除）
3. 关闭 Disk Utility，点击 "Reinstall macOS" 开始安装系统
# 日常使用
## 启动已安装的系统
首次安装完成后，如果想再次使用，请按以下步骤操作：

1. 查找已安装的容器 ID
```shell
docker ps --all
```

2. 使用容器 ID 启动系统
```shell
docker start <容器ID>
```
例如： `docker start abc123xyz567`

# 高级配置
## 扩展磁盘空间
默认磁盘大小为 200GB。如需更大空间，请在首次启动前执行：

```shell
docker build -t docker-osx:latest --build-arg SIZE=500G
 ```
```

此命令将创建一个 500GB 的磁盘空间（可根据需求调整）。