# bark_generation.py

import os
import soundfile as sf
from bark import SAMPLE_RATE, generate_audio, preload_models

# Preload models to speed up audio generation
preload_models()

def generate_bark_audio(text, dest_lang_code, speaker_id):
    try:
        # Generate audio using Bark with the selected speaker
        audio_array = generate_audio(text, history_prompt=speaker_id)

        # Define the output file path
        output_dir = "bark_audio"
        os.makedirs(output_dir, exist_ok=True)
        filename = f"{len(os.listdir(output_dir)) + 1}_{dest_lang_code}.wav"
        filepath = os.path.join(output_dir, filename)

        # Save the audio to a WAV file
        sf.write(filepath, audio_array, SAMPLE_RATE)
        print(f"Audio saved to {filepath}")

    except Exception as e:
        print(f"Error generating audio: {e}")
