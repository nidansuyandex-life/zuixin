# 健康生活 Android App - GitHub Actions 构建版

这个版本将 `www/index.html` 原网页打包为 Capacitor Android App，并针对“点击麦克风后还没来得及说话就识别失败”增加了**原生 Android 系统语音识别桥接**。

## 本次语音修复

GitHub Actions 构建时会自动：

1. 添加 `RECORD_AUDIO`、`MODIFY_AUDIO_SETTINGS` 权限；
2. 添加 Android 11+ 语音识别服务查询；
3. 写入原生 `MainActivity.java`，通过 Android `SpeechRecognizer` 接收中文语音；
4. 设置中文 `zh-CN`；
5. 将最低语音输入时长设置为 15 秒，并允许更长的停顿；
6. 识别结果自动回传网页现有的 `window.onNativeSpeechResult()`，所以不需要重新设计记账页面；
7. 如果识别失败，会把具体原因返回到页面，而不是统一显示“识别失败”。

## GitHub 使用

将压缩包里的内容直接放到 GitHub 仓库根目录，确保仓库根目录能看到：

- `package.json`
- `package-lock.json`
- `capacitor.config.json`
- `www/index.html`
- `patch-android-permissions.py`
- `patch-native-voice.py`
- `.github/workflows/android.yml`

然后进入 GitHub：`Actions` → `Build Android APK` → `Run workflow`。

构建完成后，在 Actions 的 Artifacts 中下载 `health-life-android-apk`，安装新的 `app-debug.apk`。

## 使用语音记账

安装新版 APK 后：

1. 第一次点击麦克风时允许麦克风权限；
2. 等页面显示“聆听中”；
3. 直接说完整一句，例如：`今天午餐花了三十五元`；
4. 说完自然停顿，系统会把识别文字回传到记账页面。

注意：这个版本不再依赖 Android WebView 自己的 Web Speech API 作为主要语音路径，而是优先走原生 Android `SpeechRecognizer`。
