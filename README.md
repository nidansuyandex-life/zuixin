# 健康生活 Android App（GitHub 自动编译版）

这是一套把 `www/index.html` 包装成 Android APK 的 Capacitor 项目。

## GitHub 使用方法

1. 解压本压缩包。
2. 将压缩包**里面的全部内容**上传到 GitHub 仓库根目录。
3. 确认仓库根目录直接看到：
   - `package.json`
   - `package-lock.json`
   - `capacitor.config.json`
   - `www/index.html`
   - `.github/workflows/android.yml`
4. 打开 GitHub → Actions。
5. 选择 **Build Android APK**。
6. 点击 **Run workflow**。
7. 编译完成后打开本次运行记录，在 **Artifacts** 下载 `health-life-android-apk`。

## 本版针对之前的错误做的修复

之前日志已经成功通过 SDK license 接受阶段，但 `android-actions/setup-android@v3` 后执行 `sdkmanager tools` 时失败：

`Warning Failed to find package 'tools'`

因此本版**完全移除了 `android-actions/setup-android@v3`**，不再安装已经废弃的 `tools` 包。

GitHub Runner 自带 Android SDK，本版直接使用 Runner 中的 `sdkmanager`，只安装：
- platform-tools
- platforms;android-35
- build-tools;35.0.0

同时保留 `package-lock.json`，避免 `actions/setup-node` 的 npm cache 检查报 “Dependencies lock file is not found”。

## 注意

请把本压缩包中的文件直接放到仓库根目录，不要再套一层 `Build` 文件夹。
