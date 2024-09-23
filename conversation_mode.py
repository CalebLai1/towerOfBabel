import tkinter as tk
from tkinter import ttk
import pyaudio
import wave
import os
import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, lfilter
import threading

class ConversationMode(ttk.Frame):
    def __init__(self, parent, shared):
        super().__init__(parent)
        self.shared = shared
        self.is_recording = False
        self.audio_thread = None
        self.current_speaker = None
        self.stop_requested = False

        self.create_widgets()

    def create_widgets(self):
        self.conversation_frame = ttk.Frame(self)
        self.conversation_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.conversation_frame)
        self.scrollbar = ttk.Scrollbar(self.conversation_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((400, 0), window=self.scrollable_frame, anchor="n")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side="right", fill="y")

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

        self.volume_meter = ttk.Progressbar(control_frame, orient="horizontal", length=200, mode="determinate")
        self.volume_meter.grid(row=2, column=0, columnspan=4, pady=5)

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

        frames = []

        while self.is_recording and not self.stop_requested:
            data = stream.read(CHUNK)
            frames.append(np.frombuffer(data, dtype=np.int16))
            
            volume = np.max(np.abs(np.frombuffer(data, dtype=np.int16))) / 32767 * 100
            self.update_volume_meter(volume)

        stream.stop_stream()
        stream.close()
        p.terminate()

        self.is_recording = False
        self.stop_requested = False

        audio_data = np.concatenate(frames)
        audio_data = self.reduce_noise(audio_data, RATE)
        wavfile.write(WAVE_OUTPUT_FILENAME, RATE, audio_data.astype(np.int16))

        try:
            transcription, detected_language = self.shared.transcribe_audio(WAVE_OUTPUT_FILENAME)
            
            if transcription.strip():
                your_lang_code = self.shared.get_language_code(self.your_lang.get())
                other_lang_code = self.shared.get_language_code(self.other_lang.get())

                if self.current_speaker == "you":
                    translated_text = self.shared.translate_text(transcription, your_lang_code, other_lang_code)
                    self.add_message(transcription, "right", your_lang_code)
                    self.add_message(translated_text, "left", other_lang_code)
                else:
                    translated_text = self.shared.translate_text(transcription, other_lang_code, your_lang_code)
                    self.add_message(transcription, "left", other_lang_code)
                    self.add_message(translated_text, "right", your_lang_code)
        except Exception as e:
            print(f"An error occurred during transcription or translation: {e}")
        finally:
            if os.path.exists(WAVE_OUTPUT_FILENAME):
                try:
                    os.remove(WAVE_OUTPUT_FILENAME)
                except Exception as e:
                    print(f"Error removing temporary file: {e}")

        if self.current_speaker == "you":
            self.your_button.config(text="Start Your Turn", state="normal")
            self.other_button.config(state="normal")
        else:
            self.other_button.config(text="Start Other's Turn", state="normal")
            self.your_button.config(state="normal")

    def add_message(self, text, side, lang_code):
        frame = ttk.Frame(self.scrollable_frame, width=700)
        frame.pack(pady=5)
        frame.pack_propagate(False)

        message_frame = ttk.Frame(frame, style=f"{side}.TFrame")
        message_frame.pack(side=side, padx=10)

        label = ttk.Label(message_frame, text=f"{text}\n({lang_code})", wraplength=300, justify="left", style=f"{side}.TLabel")
        label.pack(padx=10, pady=5)

        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1.0)

    def update_volume_meter(self, volume):
        self.volume_meter["value"] = volume
        self.update_idletasks()

    def detect_voice_activity(self, audio_data, threshold=0.01):
        return np.max(np.abs(audio_data)) > threshold

    def reduce_noise(self, audio_data, sample_rate):
        cutoff = 1000  # Cutoff frequency of 1000 Hz
        nyquist = 0.5 * sample_rate
        normal_cutoff = cutoff / nyquist
        order = 6
        b, a = butter(order, normal_cutoff, btype='high', analog=False)
        
        filtered_audio = lfilter(b, a, audio_data)
        return filtered_audio