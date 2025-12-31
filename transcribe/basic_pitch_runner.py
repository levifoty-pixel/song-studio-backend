from basic_pitch.inference import predict
import os

def transcribe_audio(audio_path):
    midi_path = audio_path.replace(".wav", ".mid")

    # Run Basic Pitch
    _, midi_data, _ = predict(audio_path)

    # Save MIDI file
    midi_data.write(midi_path)

    return midi_path
