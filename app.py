import os
from flask import Flask, request, jsonify
import azure.cognitiveservices.speech as speechsdk

app = Flask(__name__)

# 🔑 從環境變數讀取 Key 和 Region
SPEECH_KEY = os.getenv("SPEECH_KEY")
SERVICE_REGION = os.getenv("SERVICE_REGION")

@app.route("/tts", methods=["POST"])
def tts():
    data = request.json
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "請提供文字"}), 400

    speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SERVICE_REGION)
    audio_config = speechsdk.audio.AudioConfig(use_default_speaker=True)
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    synthesizer.speak_text_async(text).get()
    return jsonify({"message": "朗讀完成！"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
