import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import os
from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav
import torch

class VoiceGenerationPage(ttk.Frame):
    def __init__(self, parent, shared, device):
        super().__init__(parent)
        self.shared = shared
        self.device = device  
        self.speaker_prompts = [
            "v2/en_speaker_0", "v2/en_speaker_1", "v2/en_speaker_2", "v2/en_speaker_3",
            "v2/en_speaker_4", "v2/en_speaker_5", "v2/en_speaker_6", "v2/en_speaker_7",
            "v2/en_speaker_8", "v2/en_speaker_9"
        ]
        self.create_widgets()

    def create_widgets(self):
        self.text_box = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=80, height=10)
        self.text_box.pack(padx=10, pady=10)

        control_frame = ttk.Frame(self)
        control_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(control_frame, text="Select Voice:").grid(row=0, column=0, padx=5, pady=5)
        self.voice_combo = ttk.Combobox(control_frame, values=self.speaker_prompts)
        self.voice_combo.set(self.speaker_prompts[0])
        self.voice_combo.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(control_frame, text="Generate Audio", command=self.generate_audio).grid(row=1, column=0, columnspan=2, pady=10)

        self.status_label = ttk.Label(control_frame, text="")
        self.status_label.grid(row=2, column=0, columnspan=2, pady=5)

        self.device_label = ttk.Label(control_frame, text=f"Using device: {self.device}")
        self.device_label.grid(row=3, column=0, columnspan=2, pady=5)

        self.progress_bar = ttk.Progressbar(control_frame, orient="horizontal", length=300, mode="indeterminate")
        self.progress_bar.grid(row=4, column=0, columnspan=2, pady=5)

    def generate_audio(self):
        text = self.text_box.get("1.0", tk.END).strip()
        if not text:
            self.status_label.config(text="Please enter some text to generate audio.")
            return

        self.status_label.config(text="Generating audio...")
        self.progress_bar.start()

        threading.Thread(target=self._generate_audio_thread, args=(text,)).start()

    def _generate_audio_thread(self, text):
        try:
            preload_models(self.device)
            
            audio_array = generate_audio(text, history_prompt=self.voice_combo.get(), device=self.device)

            output_path = "generated_audio.wav"
            write_wav(output_path, SAMPLE_RATE, audio_array)

            self.status_label.config(text=f"Audio generated and saved as {output_path}")
        except Exception as e:
            self.status_label.config(text=f"Error generating audio: {str(e)}")
        finally:
            self.progress_bar.stop()

    def clear_text(self):
        self.text_box.delete('1.0', tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Voice Generation")

    shared = {} 
    device = "cuda" if torch.cuda.is_available() else "cpu"
    app = VoiceGenerationPage(root, shared, device)
    app.pack(expand=True, fill=tk.BOTH)

    root.mainloop()
