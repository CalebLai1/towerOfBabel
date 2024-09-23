import tkinter as tk
from tkinter import ttk, scrolledtext
import pyaudio
import wave
import os
import threading

class TranscriptionMode(ttk.Frame):
    def __init__(self, parent, shared):
        super().__init__(parent)
        self.shared = shared
        self.is_recording = False
        self.audio_thread = None

        self.create_widgets()

    def create_widgets(self):
        self.text_box = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=80, height=20)
        self.text_box.pack(padx=10, pady=10)

        button_frame = ttk.Frame(self)
        button_frame.pack(pady=5)

        self.start_button = ttk.Button(button_frame, text="Start Recording", command=self.toggle_recording)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = ttk.Button(button_frame, text="Clear Text", command=self.clear_text)
        self.clear_button.pack(side=tk.LEFT, padx=5)

        language_frame = ttk.Frame(self)
        language_frame.pack(pady=5)

        ttk.Label(language_frame, text="Transcription Language:").pack(side=tk.LEFT, padx=5)
        self.transcription_lang = ttk.Combobox(language_frame, values=list(self.shared.get_language_dict().values()))
        self.transcription_lang.set("English")
        self.transcription_lang.pack(side=tk.LEFT, padx=5)

    def toggle_recording(self):
        if self.is_recording:
            self.is_recording = False
            self.start_button.config(text="Start Recording")
        else:
            self.is_recording = True
            self.start_button.config(text="Stop Recording")
            self.audio_thread = threading.Thread(target=self.record_and_transcribe)
            self.audio_thread.start()

    def record_and_transcribe(self):
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 16000
        WAVE_OUTPUT_FILENAME = "temp_audio.wav"

        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        frames = []

        while self.is_recording:
            data = stream.read(CHUNK)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

        transcription, detected_language = self.shared.transcribe_audio(WAVE_OUTPUT_FILENAME)
        target_language_code = self.shared.get_language_code(self.transcription_lang.get())
        translated_text = self.shared.translate_text(transcription, detected_language, target_language_code)

        self.text_box.insert(tk.END, f"Original ({detected_language}): {transcription}\n")
        self.text_box.insert(tk.END, f"Translated ({target_language_code}): {translated_text}\n\n")
        self.text_box.see(tk.END)

        os.remove(WAVE_OUTPUT_FILENAME)

    def clear_text(self):
        self.text_box.delete('1.0', tk.END)
