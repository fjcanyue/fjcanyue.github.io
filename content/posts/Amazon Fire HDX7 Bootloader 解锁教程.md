---
title: Amazon Fire HDX7 Bootloader 解锁教程
date: 2016-11-02 19:45:55
tags: ["android", "bootloader", "kindle fire hdx", "root", "twrp", "cyanogenmod"]
---

最近入手了亚马逊 Fire HDX 7 平板，想刷入第三方 ROM (如 CyanogenMod/LineageOS) 以获得更自由的体验。解锁 Bootloader 是第一步。本文参考了 [XDA 论坛的教程](http://forum.xda-developers.com/kindle-fire-hdx/general/thor-unlocking-bootloader-firmware-t3463982)，并结合我自己的实践经验，整理了一份更详细、清晰的解锁流程，希望能帮助到大家。

**重要提示：** 解锁 Bootloader 会清除设备上的所有数据，并可能导致设备失去保修。请在操作前务必备份好重要数据，并仔细阅读所有步骤。操作有风险，请谨慎进行。

## 第一步：准备工作与 Root

1.  **获取 Root 权限：**
    解锁过程需要 Root 权限。你可以使用以下任一工具尝试获取 Root：
    *   [KingoRoot](http://www.kingoapp.com)
    *   [KingRoot](https://kingroot.net)
    下载并安装对应的 App 或 PC 软件，按照提示进行一键 Root 操作。

2.  **安装 ADB 和 Fastboot 驱动：**
    电脑需要正确识别你的设备才能执行后续命令。
    *   **下载驱动：** 访问 [此 Google Drive 链接](https://drive.google.com/open?id=0B2twXJIOgv-UMGxXMUZPZTlZTUk) (原教程提供，请自行确认链接有效性)，进入 `Non_English` 文件夹下载适用于你系统的驱动文件。
    *   **(Windows) 禁用驱动程序强制签名：** Windows 8/10/11 通常需要禁用驱动强制签名才能安装未签名的驱动。
        a. 按住 `SHIFT` 键，然后点击“开始”菜单中的“重启”。
        b. 重启后，依次选择“疑难解答” -> “高级选项” -> “启动设置”，然后点击“重启”。
        c. 电脑再次重启后，会显示启动设置菜单，按 `F7` 键选择“禁用驱动程序强制签名”。
        d. 进入系统后，驱动签名验证就被临时禁用了。
    *   **安装驱动：** 解压下载的驱动文件，找到 `dpinst.exe` (或类似安装程序)，以管理员身份运行。如果提供的是 `.inf` 文件，可以通过设备管理器手动安装。原教程提供的命令 `dpinst.exe /EL` 可能是特定安装包的参数，请根据实际下载的文件调整安装方式。
    *   **验证安装：** 连接平板到电脑，打开开发者选项并启用 USB 调试。在电脑上打开命令提示符 (CMD) 或 PowerShell，输入 `adb devices`。如果看到设备序列号，表示 ADB 驱动安装成功。

<!-- more -->

## 第二步：获取设备硬件信息

解锁需要用到设备的唯一识别码。

1.  **连接设备：** 确保平板通过 USB 连接到电脑，并且 USB 调试已开启。
2.  **打开 ADB Shell：** 在电脑的命令提示符或 PowerShell 中输入：
    ```bash
    adb shell
    ```
3.  **查询硬件信息：** 在 `adb shell` 环境下，依次输入以下两条命令：
    ```bash
    cat /sys/block/mmcblk0/device/manfid
    cat /sys/block/mmcblk0/device/serial
    ```
4.  **记录结果：** 你会得到类似下面的输出：
    ```
    # cat /sys/block/mmcblk0/device/manfid
    0x0000mm  <-- mm 是你的 manfid 值
    # cat /sys/block/mmcblk0/device/serial
    0xssssssss <-- ssssssss 是你的 serial 值
    ```
    将这两个值组合成 `0xmmssssssss` 的格式（例如，如果 manfid 是 `0x000015`，serial 是 `0x1234abcd`，则组合结果为 `0x151234abcd`）。**请务必记下这个组合后的值**，后面会用到。
5.  **退出 ADB Shell：** 输入 `exit` 并回车。

## 第三步：生成解锁文件 (`.unlock`)

需要使用 Python 脚本来生成解锁 Bootloader 所需的文件。

1.  **安装 Python：** 如果你的电脑没有安装 Python，请从 [Python 官网](https://www.python.org) 下载并安装 (建议选择 Python 2.7 或兼容版本，根据脚本要求)。确保将 Python 添加到系统环境变量 (PATH)。
2.  **安装 gmpy2 库：** `cuberHDX.py` 脚本依赖 `gmpy2` 库。打开命令提示符或 PowerShell，使用 pip 安装：
    ```bash
    pip install gmpy2
    ```
    *注意：* 在 Windows 上安装 `gmpy2` 可能需要预编译的二进制文件或额外的编译环境。你可以尝试从 [这里](https://www.lfd.uci.edu/~gohlke/pythonlibs/#gmpy2) 下载对应 Python 版本的 `.whl` 文件，然后使用 `pip install gmpy2-xxxx.whl` 安装。
3.  **下载 cuberHDX 脚本：** 从 [XDA 帖子](http://forum.xda-developers.com/showpost.php?p=58864282&postcount=46) 下载 `cuberHDX.py` 脚本文件，并将其保存到电脑上一个方便访问的位置。
4.  **生成解锁文件：** 打开命令提示符或 PowerShell，切换到 `cuberHDX.py` 脚本所在的目录，然后运行以下命令（将 `0xmmssssssss` 替换为 **你在第二步中记下的那个值**）：
    ```bash
    python cuberHDX.py 0xmmssssssss
    ```
    如果一切顺利，脚本会在当前目录下生成一个名为 `0xmmssssssss.unlock` 的文件。这就是你的解锁文件。

## 第四步：刷入旧版 aboot 和 TWRP Recovery

为了能够成功解锁，需要先刷入一个存在漏洞的旧版 `aboot` (引导加载程序的一部分) 和一个定制的 TWRP Recovery。

1.  **下载所需文件：** 再次访问 [此 Google Drive 链接](https://drive.google.com/open?id=0B2twXJIOgv-UMGxXMUZPZTlZTUk) (原教程提供)，下载 `aboot_vuln.mbn` 和 `twrp_cubed.img` 这两个文件。
2.  **传输文件到设备：** 将下载好的 `aboot_vuln.mbn` 和 `twrp_cubed.img` 文件复制到平板的内部存储空间根目录 (通常是 `/sdcard/`)。
3.  **刷入 TWRP Recovery：**
    *   打开 `adb shell`：
        ```bash
        adb shell
        ```
    *   获取 Root 权限 (如果 `adb shell` 默认不是 root 用户)：
        ```bash
        su
        ```
        (此时平板上可能会弹出授权请求，请允许)
    *   使用 `dd` 命令刷入 TWRP (请**极其小心**，确保命令无误！)：
        ```bash
        dd if=/sdcard/twrp_cubed.img of=/dev/block/platform/msm_sdcc.1/by-name/recovery
        ```
    *   刷入完成后，输入 `exit` 两次退出 `adb shell`。
4.  **刷入旧版 aboot：** (原教程似乎遗漏了刷入 `aboot_vuln.mbn` 的步骤，但根据 XDA 流程通常需要这一步。请参考 XDA 原帖确认是否需要以及如何刷入，通常也是通过 `dd` 命令刷入到 `aboot` 分区，例如 `dd if=/sdcard/aboot_vuln.mbn of=/dev/block/platform/msm_sdcc.1/by-name/aboot`。**刷写 aboot 风险极高，请务必确认无误再操作！** 如果不确定，请严格按照 XDA 最新教程操作。)

## 第五步：执行解锁命令

现在可以正式解锁 Bootloader 了。

1.  **进入 Fastboot 模式：**
    *   先将平板完全关机。
    *   按住 **音量加键** 不放，同时连接 USB 数据线到电脑。设备屏幕应该会停留在 Kindle Fire Logo 界面，这就是 Fastboot 模式。
    *   或者，在 `adb shell` 中执行 `reboot bootloader` 命令。
2.  **验证 Fastboot 连接：** 在电脑的命令提示符或 PowerShell 中输入：
    ```bash
    fastboot -i 0x1949 devices
    ```
    如果看到设备序列号，表示 Fastboot 连接成功。(`-i 0x1949` 是指定 Amazon 设备的 Vendor ID)。
3.  **刷入解锁文件：** 确保你的命令提示符或 PowerShell 当前目录是之前生成 `.unlock` 文件的目录。然后执行以下命令 (将 `0xmmssssssss` 替换为 **你的那个值**)：
    ```bash
    fastboot -i 0x1949 flash unlock 0xmmssssssss.unlock
    ```
4.  **检查结果：** 如果命令执行成功，你应该会看到类似 `unlock code is correct` 的提示。这表示你的 Bootloader 已经成功解锁！
5.  **重启设备：**
    ```bash
    fastboot -i 0x1949 reboot
    ```

## 第六步：刷入自定义 ROM (例如 CM13)

Bootloader 解锁后，你就可以刷入第三方 Recovery (如果之前刷入的 TWRP 不是最新版，建议更新) 和自定义 ROM 了。

1.  **下载 ROM：** 前往 [CyanogenMod 下载页面 (或其他 ROM 提供方)](http://download.cyanogenmod.org/?device=thor) 下载适用于 Fire HDX 7 (代号 thor) 的 CM13 (或其他你选择的 ROM) 的 zip 文件，以及对应的 GApps (Google 应用包，如果需要的话)。
2.  **传输文件：** 将下载好的 ROM zip 文件和 GApps zip 文件复制到平板的内部存储空间。
3.  **进入 Recovery 模式：**
    *   关机状态下，按住 **音量减键** 和 **电源键**，直到看到 TWRP Recovery 界面。
    *   或者在 `adb shell` 中执行 `reboot recovery`。
4.  **刷入 ROM：**
    *   在 TWRP 中，建议先进行 **Wipe (清除)** 操作，选择 "Advanced Wipe"，勾选 Dalvik/ART Cache, System, Data, Cache，然后滑动确认清除 (不要清除 Internal Storage)。
    *   返回主菜单，选择 **Install (安装)**。
    *   找到你之前复制到设备的 ROM zip 文件，选择它，然后滑动确认刷入。
    *   刷入 GApps (如果需要)，步骤同上。
    *   完成后，返回主菜单，选择 **Reboot (重启)** -> **System (系统)**。

首次启动新系统可能会比较慢，请耐心等待。恭喜你，现在你的 Fire HDX 7 已经解锁并运行自定义 ROM 了！
