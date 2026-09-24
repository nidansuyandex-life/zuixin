from pathlib import Path

root = Path('android/app/src/main/java/com/healthlife/app')
root.mkdir(parents=True, exist_ok=True)
main = root / 'MainActivity.java'

main.write_text(r'''package com.healthlife.app;

import android.Manifest;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.speech.RecognitionListener;
import android.speech.RecognizerIntent;
import android.speech.SpeechRecognizer;
import android.webkit.JavascriptInterface;

import androidx.annotation.NonNull;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import com.getcapacitor.BridgeActivity;

import org.json.JSONObject;

import java.util.ArrayList;
import java.util.Locale;

public class MainActivity extends BridgeActivity {
    private static final int REQ_RECORD_AUDIO = 9001;
    private SpeechRecognizer speechRecognizer;
    private boolean waitingForPermission = false;
    private boolean listening = false;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        getBridge().getWebView().addJavascriptInterface(new AndroidVoiceBridge(), "AndroidBridge");
        createSpeechRecognizer();
    }

    private void createSpeechRecognizer() {
        if (!SpeechRecognizer.isRecognitionAvailable(this)) {
            speechRecognizer = null;
            return;
        }
        speechRecognizer = SpeechRecognizer.createSpeechRecognizer(this);
        speechRecognizer.setRecognitionListener(new RecognitionListener() {
            @Override public void onReadyForSpeech(Bundle params) {
                listening = true;
                sendState("started");
            }
            @Override public void onBeginningOfSpeech() {
                listening = true;
                sendState("started");
            }
            @Override public void onRmsChanged(float rmsdB) {}
            @Override public void onBufferReceived(byte[] buffer) {}
            @Override public void onEndOfSpeech() {
                listening = false;
                sendState("ended");
            }
            @Override public void onError(int error) {
                listening = false;
                sendError(errorMessage(error));
                sendState("ended");
            }
            @Override public void onResults(Bundle results) {
                listening = false;
                ArrayList<String> matches = results == null ? null :
                        results.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION);
                if (matches != null && !matches.isEmpty() && matches.get(0) != null && !matches.get(0).trim().isEmpty()) {
                    sendResult(matches.get(0).trim());
                } else {
                    sendError("没有识别到内容，请说完后再松口");
                }
                sendState("ended");
            }
            @Override public void onPartialResults(Bundle partialResults) {}
            @Override public void onEvent(int eventType, Bundle params) {}
        });
    }

    private String errorMessage(int error) {
        switch (error) {
            case SpeechRecognizer.ERROR_AUDIO:
                return "录音启动失败，请检查手机麦克风权限";
            case SpeechRecognizer.ERROR_CLIENT:
                return "语音识别启动失败，请重新点击麦克风";
            case SpeechRecognizer.ERROR_INSUFFICIENT_PERMISSIONS:
                return "麦克风权限未授予，请在系统设置中允许麦克风";
            case SpeechRecognizer.ERROR_NETWORK:
            case SpeechRecognizer.ERROR_NETWORK_TIMEOUT:
                return "语音识别网络异常，请检查网络后重试";
            case SpeechRecognizer.ERROR_NO_MATCH:
                return "没有识别到内容，请说完整一句话后再停顿";
            case SpeechRecognizer.ERROR_RECOGNIZER_BUSY:
                return "语音识别正在使用中，请稍后再试";
            case SpeechRecognizer.ERROR_SERVER:
                return "系统语音识别服务异常，请稍后重试";
            case SpeechRecognizer.ERROR_SPEECH_TIMEOUT:
                return "等待说话超时，请点击麦克风后直接说话";
            default:
                return "语音识别失败（错误码 " + error + "）";
        }
    }

    private void startNativeVoice() {
        if (speechRecognizer == null) {
            createSpeechRecognizer();
        }
        if (speechRecognizer == null) {
            sendError("当前手机没有可用的系统语音识别服务");
            return;
        }
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO)
                != PackageManager.PERMISSION_GRANTED) {
            waitingForPermission = true;
            ActivityCompat.requestPermissions(this,
                    new String[]{Manifest.permission.RECORD_AUDIO}, REQ_RECORD_AUDIO);
            return;
        }

        try {
            speechRecognizer.cancel();
        } catch (Exception ignored) {}

        Intent intent = new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
        intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM);
        intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE, "zh-CN");
        intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_PREFERENCE, "zh-CN");
        intent.putExtra(RecognizerIntent.EXTRA_PARTIAL_RESULTS, false);
        // Give the user substantially more time to speak than WebView's default.
        intent.putExtra(RecognizerIntent.EXTRA_SPEECH_INPUT_MINIMUM_LENGTH_MILLIS, 15000L);
        intent.putExtra(RecognizerIntent.EXTRA_SPEECH_INPUT_COMPLETE_SILENCE_LENGTH_MILLIS, 5000L);
        intent.putExtra(RecognizerIntent.EXTRA_SPEECH_INPUT_POSSIBLY_COMPLETE_SILENCE_LENGTH_MILLIS, 4000L);

        listening = true;
        sendState("started");
        try {
            speechRecognizer.startListening(intent);
        } catch (Exception e) {
            listening = false;
            sendError("无法启动系统语音识别：" + e.getMessage());
            sendState("ended");
        }
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == REQ_RECORD_AUDIO) {
            boolean granted = grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED;
            if (granted && waitingForPermission) {
                waitingForPermission = false;
                new Handler(Looper.getMainLooper()).postDelayed(this::startNativeVoice, 200);
            } else {
                waitingForPermission = false;
                sendError("麦克风权限未授予，请允许后再试");
            }
        }
    }

    private void sendResult(final String text) {
        final String js = "window.onNativeSpeechResult && window.onNativeSpeechResult(" + JSONObject.quote(text) + ");";
        runOnUiThread(() -> getBridge().getWebView().evaluateJavascript(js, null));
    }

    private void sendError(final String message) {
        final String js = "window.onNativeSpeechError && window.onNativeSpeechError(" + JSONObject.quote(message) + ");";
        runOnUiThread(() -> getBridge().getWebView().evaluateJavascript(js, null));
    }

    private void sendState(final String status) {
        final String js = "window.onNativeSpeechState && window.onNativeSpeechState(" + JSONObject.quote(status) + ");";
        runOnUiThread(() -> getBridge().getWebView().evaluateJavascript(js, null));
    }

    @Override
    public void onDestroy() {
        if (speechRecognizer != null) {
            try { speechRecognizer.destroy(); } catch (Exception ignored) {}
            speechRecognizer = null;
        }
        super.onDestroy();
    }

    private class AndroidVoiceBridge {
        @JavascriptInterface
        public boolean isSpeechAvailable() {
            return SpeechRecognizer.isRecognitionAvailable(MainActivity.this);
        }

        @JavascriptInterface
        public void startVoice() {
            runOnUiThread(MainActivity.this::startNativeVoice);
        }
    }
}
''', encoding='utf-8')
print(f'Wrote {main}')
