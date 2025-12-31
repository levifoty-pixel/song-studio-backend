from flask import Flask, request, jsonify
from transcribe.audio_downloader import download_audio
from transcribe.basic_pitch_runner import transcribe_audio
from transcribe.midi_to_tab import midi_to_tab

app = Flask(__name__)

@app.route("/")
def home():
    return "Backend is running"

@app.route("/transcribe", methods=["POST"])
def transcribe():
    data = request.json
    youtube_url = data.get("youtube_url")

    if not youtube_url:
        return jsonify({"error": "youtube_url is required"}), 400

    # Step 1: Download audio
    audio_path = download_audio(youtube_url)

    # Step 2: Transcribe audio → MIDI
    midi_path = transcribe_audio(audio_path)

    # Step 3: Convert MIDI → placeholder tab
    tab_data = midi_to_tab(midi_path)

    return jsonify({
        "status": "success",
        "tab": tab_data
    })

if __name__ == "__main__":
    app.run()
