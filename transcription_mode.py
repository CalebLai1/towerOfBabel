import tkinter as tk
from tkinter import ttk, scrolledtext
import pyaudio
import threading
import queue

class TranscriptionMode(ttk.Frame):
    def __init__(self, parent, shared):
        super().__init__(parent)
        self.shared = shared
        self.is_recording = False
        self.audio_queue = queue.Queue()

        self.create_widgets()

    def create_widgets(self):
        self.text_box = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=80, height=20)
        self.text_box.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

        controls_frame = ttk.Frame(self)
        controls_frame.pack(pady=5)

        self.lang_var = tk.StringVar(value="English")
        lang_label = ttk.Label(controls_frame, text="Language:")
        lang_label.pack(side=tk.LEFT, padx=5)
        lang_combo = ttk.Combobox(controls_frame, textvariable=self.lang_var, 
                                  values=list(self.shared.get_language_dict().values()))
        lang_combo.pack(side=tk.LEFT, padx=5)

        self.start_button = ttk.Button(controls_frame, text="Start", command=self.toggle_recording)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = ttk.Button(controls_frame, text="Clear", command=self.clear_text)
        self.clear_button.pack(side=tk.LEFT, padx=5)

    def toggle_recording(self):
        if self.is_recording:
            self.is_recording = False
            self.start_button.config(text="Start")
        else:
            self.is_recording = True
            self.start_button.config(text="Stop")
            threading.Thread(target=self.record_audio, daemon=True).start()
            threading.Thread(target=self.process_audio, daemon=True).start()

    def record_audio(self):
        CHUNK = 4000
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 16000

        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                        input=True, frames_per_buffer=CHUNK)

        while self.is_recording:
            data = stream.read(CHUNK)
            self.audio_queue.put(data)

        stream.stop_stream()
        stream.close()
        p.terminate()

    def process_audio(self):
        while self.is_recording:
            if not self.audio_queue.empty():
                audio_data = self.audio_queue.get()
                lang_code = self.shared.get_language_code(self.lang_var.get())
                text = self.shared.transcribe_audio(audio_data, lang_code)
                if text:
                    self.text_box.insert(tk.END, text + " ")
                    self.text_box.see(tk.END)

    def clear_text(self):
        self.text_box.delete('1.0', tk.END)