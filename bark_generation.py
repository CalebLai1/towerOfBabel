import os
import soundfile as sf
from bark import SAMPLE_RATE, generate_audio, preload_models

preload_models()

def generate_bark_audio(text, dest_lang_code, speaker_id):
    try:
        if not speaker_id:
            raise ValueError("Invalid speaker_id provided.")

        audio_array = generate_audio(text, history_prompt=speaker_id)

        output_dir = "bark_audio"
        os.makedirs(output_dir, exist_ok=True)
        filename = f"{len(os.listdir(output_dir)) + 1}_{dest_lang_code}.wav"
        filepath = os.path.join(output_dir, filename)

        sf.write(filepath, audio_array, SAMPLE_RATE)
        print(f"Audio saved to {filepath}")
        return filepath

    except Exception as e:
        print(f"Error generating audio: {e}")
        return None
