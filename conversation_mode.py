import tkinter as tk
from tkinter import ttk, scrolledtext
import pyaudio
import wave
import os
import numpy as np
from scipy.io import wavfile
import threading
import torch
from bark import SAMPLE_RATE, generate_audio, preload_models
import sounddevice as sd

class ConversationMode(ttk.Frame):
    def __init__(self, parent, shared):
        super().__init__(parent)
        self.shared = shared
        self.is_recording = False
        self.audio_thread = None
        self.current_speaker = None
        self.stop_requested = False

        if torch.cuda.is_available():
            print("GPU available. Forcing Bark to use GPU.")
            os.environ["CUDA_VISIBLE_DEVICES"] = "0"  
            torch.cuda.set_device(0)
        else:
            print("GPU not available. Bark will use CPU.")

        preload_models()

        self.create_widgets()

    def create_widgets(self):
        self.text_box = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=80, height=20)
        self.text_box.pack(padx=10, pady=10)

        control_frame = ttk.Frame(self)
        control_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(control_frame, text="Your Language:").grid(row=0, column=0, padx=5, pady=5)
        self.your_lang = ttk.Combobox(control_frame, values=list(self.shared.get_language_dict().values()))
        self.your_lang.set("English")
        self.your_lang.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(control_frame, text="Other Person's Language:").grid(row=0, column=2, padx=5, pady=5)
        self.other_lang = ttk.Combobox(control_frame, values=list(self.shared.get_language_dict().values()))
        self.other_lang.set("Spanish")
        self.other_lang.grid(row=0, column=3, padx=5, pady=5)

        self.your_button = ttk.Button(control_frame, text="Start Your Turn", command=lambda: self.toggle_recording("you"))
        self.your_button.grid(row=1, column=0, columnspan=2, pady=10)

        self.other_button = ttk.Button(control_frame, text="Start Other's Turn", command=lambda: self.toggle_recording("other"))
        self.other_button.grid(row=1, column=2, columnspan=2, pady=10)

        self.clear_button = ttk.Button(control_frame, text="Clear Text", command=self.clear_text)
        self.clear_button.grid(row=2, column=0, columnspan=4, pady=10)

        self.volume_meter = ttk.Progressbar(control_frame, orient="horizontal", length=200, mode="determinate")
        self.volume_meter.grid(row=3, column=0, columnspan=4, pady=5)

    def toggle_recording(self, speaker):
        if self.is_recording:
            self.stop_requested = True
            self.your_button.config(state="disabled")
            self.other_button.config(state="disabled")
        else:
            self.is_recording = True
            self.stop_requested = False
            self.current_speaker = speaker
            if speaker == "you":
                self.your_button.config(text="Stop Your Turn")
                self.other_button.config(state="disabled")
            else:
                self.other_button.config(text="Stop Other's Turn")
                self.your_button.config(state="disabled")
            self.audio_thread = threading.Thread(target=self.record_and_transcribe)
            self.audio_thread.start()

    def record_and_transcribe(self):
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        WAVE_OUTPUT_FILENAME = "temp_audio.wav"

        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        print("Started recording...")
        frames = []

        while self.is_recording and not self.stop_requested:
            data = stream.read(CHUNK)
            frames.append(np.frombuffer(data, dtype=np.int16))
            
            volume = np.max(np.abs(np.frombuffer(data, dtype=np.int16))) / 32767 * 100
            self.update_volume_meter(volume)

        print("Stopped recording...")
        stream.stop_stream()
        stream.close()
        p.terminate()

        self.is_recording = False
        self.stop_requested = False

        audio_data = np.concatenate(frames)
        wavfile.write(WAVE_OUTPUT_FILENAME, RATE, audio_data.astype(np.int16))

        print(f"Audio file saved: {os.path.abspath(WAVE_OUTPUT_FILENAME)}")
        print(f"File size: {os.path.getsize(WAVE_OUTPUT_FILENAME)} bytes")

        try:
            print("Starting transcription...")
            transcription, detected_language = self.shared.transcribe_audio(WAVE_OUTPUT_FILENAME)
            print(f"Transcription completed. Detected language: {detected_language}")
            print(f"Transcription text: {transcription}")
            
            if transcription.strip():
                your_lang_code = self.shared.get_language_code(self.your_lang.get())
                other_lang_code = self.shared.get_language_code(self.other_lang.get())

                if self.current_speaker == "you":
                    translated_text = self.shared.translate_text(transcription, your_lang_code, other_lang_code)
                    self.add_message(f"You ({your_lang_code}): {transcription}")
                    self.add_message(f"You (translated to {other_lang_code}): {translated_text}")
                    self.generate_speech(translated_text, other_lang_code)
                else:
                    translated_text = self.shared.translate_text(transcription, other_lang_code, your_lang_code)
                    self.add_message(f"Other ({other_lang_code}): {transcription}")
                    self.add_message(f"Other (translated to {your_lang_code}): {translated_text}")
                    self.generate_speech(translated_text, your_lang_code)
            else:
                print("Transcription was empty.")
        except Exception as e:
            print(f"An error occurred during transcription or translation: {e}")
        finally:
            if os.path.exists(WAVE_OUTPUT_FILENAME):
                try:
                    os.remove(WAVE_OUTPUT_FILENAME)
                    print(f"Temporary file {WAVE_OUTPUT_FILENAME} removed.")
                except Exception as e:
                    print(f"Error removing temporary file: {e}")

        if self.current_speaker == "you":
            self.your_button.config(text="Start Your Turn", state="normal")
            self.other_button.config(state="normal")
        else:
            self.other_button.config(text="Start Other's Turn", state="normal")
            self.your_button.config(state="normal")

    def generate_speech(self, text, language_code):
        print(f"Generating speech for: {text[:50]}... in language {language_code}")
        
        voice_preset = self.get_voice_preset(language_code)
        
        audio_array = generate_audio(text, history_prompt=voice_preset)
        
        output_filename = "generated_speech.wav"
        wavfile.write(output_filename, SAMPLE_RATE, audio_array)
        
        print(f"Speech generated and saved as {output_filename}")
        
        sd.play(audio_array, SAMPLE_RATE)
        sd.wait()

    def get_voice_preset(self, language_code):
        voice_presets = {
            "en": "v2/en_speaker_6",
            "es": "v2/es_speaker_6",
        }
        return voice_presets.get(language_code, "v2/en_speaker_6")  

    def add_message(self, text):
        self.text_box.insert(tk.END, f"{text}\n\n")
        self.text_box.see(tk.END)
        print(f"Message added to text box: {text[:50]}...")

    def update_volume_meter(self, volume):
        self.volume_meter["value"] = volume
        self.update_idletasks()

    def clear_text(self):
        self.text_box.delete('1.0', tk.END)

    def detect_voice_activity(self, audio_data, threshold=0.01):
        return np.max(np.abs(audio_data)) > threshold

class SharedResources:
    def __init__(self):
        pass

    def get_language_dict(self):
        return {
            "en": "English",
            "es": "Spanish",
        }

    def get_language_code(self, language_name):
        lang_dict = {v: k for k, v in self.get_language_dict().items()}
        return lang_dict.get(language_name, "en") 
    def transcribe_audio(self, audio_file):
        print(f"Transcribing audio file: {audio_file}")
        return "This is a placeholder transcription.", "en"

    def translate_text(self, text, source_lang, target_lang):
        print(f"Translating from {source_lang} to {target_lang}: {text[:50]}...")
        return f"Translated: {text}"

def main():
    root = tk.Tk()
    root.title("Conversation Mode")
    shared = SharedResources()
    app = ConversationMode(root, shared)
    app.pack(expand=True, fill=tk.BOTH)
    root.mainloop()

if __name__ == "__main__":
    main()