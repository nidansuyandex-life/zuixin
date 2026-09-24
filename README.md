# 健康生活 Android App（GitHub 自动生成 APK）

这是基于原始 `www/index.html` 的 Capacitor Android 项目。

## 本版本特别修复：手机没有“麦克风”权限

App 的 AI 语音记账使用网页端 `SpeechRecognition / webkitSpeechRecognition`。Android WebView 要使用麦克风，需要 Android 原生 Manifest 声明 `RECORD_AUDIO`；同时 Android 11+ 对系统语音识别服务需要声明 `RecognitionService` 查询。

GitHub Actions 在 `npx cap add android` 后自动执行 `patch-android-permissions.py`，为生成的 Android 工程加入：

- `android.permission.RECORD_AUDIO`
- `android.permission.MODIFY_AUDIO_SETTINGS`
- `android.speech.RecognitionService` 查询

Capacitor 自带的 `BridgeWebChromeClient` 会处理 WebView 的 `AUDIO_CAPTURE` 权限请求；因此这版不需要改你的 HTML 语音记账逻辑。

## GitHub 使用方式

把 ZIP 解压后，将**里面的所有内容**上传到 GitHub 仓库根目录。仓库根目录必须直接看到：

```text
package.json
package-lock.json
capacitor.config.json
www/
.github/
patch-android-permissions.py
```

然后：

1. 打开 GitHub → Actions
2. 选择 `Build Android APK`
3. 点击 `Run workflow`
4. 等待完成
5. 在该次运行底部 `Artifacts` 下载 `health-life-android-apk`
6. 解压得到 `app-debug.apk`

安装新 APK 后：

**手机设置 → 应用 → 健康生活 → 权限**

此时应该能看到：

**麦克风 → 允许（仅在使用应用时）**

第一次点击 AI 语音记账时，如果 Android 弹出麦克风授权框，请选择“允许”。

## 注意

不要安装旧版本 APK 测试麦克风权限；需要安装本版本重新编译出来的 APK。
