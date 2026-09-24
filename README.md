# 健康生活 Android App

这是把 `www/index.html` 直接封装成 Android APK 的 GitHub Actions 项目。

## GitHub 使用方法

1. 把本目录中的**全部文件和文件夹**上传到 GitHub 仓库的**根目录**。
2. 确认仓库根目录可以直接看到：
   - `package.json`
   - `package-lock.json`
   - `capacitor.config.json`
   - `www/index.html`
   - `.github/workflows/android.yml`
3. 打开 GitHub → **Actions** → **Build Android APK** → **Run workflow**。
4. 编译完成后打开本次运行记录，在 **Artifacts** 下载 `健康生活-Android-APK`。
5. 解压后得到 `app-debug.apk`，安装到 Android 手机即可。

## 重要

不要把整个 `BuildFixed` 文件夹再套一层上传。如果 GitHub 仓库根目录叫 `health-life-app`，那么 `package.json` 必须直接位于：

`health-life-app/package.json`

而不是：

`health-life-app/Build/package.json`

项目使用 `npm ci`，所以已经包含 `package-lock.json`，可以满足 GitHub Actions 的 npm cache 要求。
