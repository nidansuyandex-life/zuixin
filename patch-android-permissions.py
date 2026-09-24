from pathlib import Path

manifest = Path('android/app/src/main/AndroidManifest.xml')
text = manifest.read_text(encoding='utf-8')

perm_lines = [
    '    <uses-permission android:name="android.permission.RECORD_AUDIO" />',
    '    <uses-permission android:name="android.permission.MODIFY_AUDIO_SETTINGS" />',
]
for line in perm_lines:
    if line not in text:
        text = text.replace('<application', line + '\n\n    <application', 1)

if 'android.speech.RecognitionService' not in text:
    query = '''    <queries>\n        <intent>\n            <action android:name="android.speech.RecognitionService" />\n        </intent>\n    </queries>\n\n'''
    text = text.replace('<application', query + '    <application', 1)

manifest.write_text(text, encoding='utf-8')
print('Patched AndroidManifest.xml for microphone and speech recognition.')
