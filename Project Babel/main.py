import tkinter as tk
from tkinter import filedialog, Text
import whisper
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import threading
import time

class Recorder: # This the Timer thing/recorder
    def __init__(self):
        self.fs = 44100 
        self.is_recording = False
        self.start_time = None
        self.myrecording = None

    def start_recording(self): 
        self.is_recording = True
        self.start_time = time.time()
        self.myrecording = sd.rec(int(10 * self.fs), samplerate=self.fs, channels=2)

    def stop_recording(self):
        if self.is_recording:
            self.is_recording = False
            sd.wait()  # Wait until recording is finished
            duration = time.time() - self.start_time
            print("Recording finished. Saving to file...")
            wav.write('output.wav', self.fs, self.myrecording)  # Save as WAV file 
            return 'output.wav', duration

    def cancel_recording(self):
        if self.is_recording:
            self.is_recording = False
            print("Recording cancelled.")

def transcribe_audio():
    model = whisper.load_model("base")
    filename, duration = recorder.stop_recording()
    result = model.transcribe(filename)
    with open("transcription.txt", "w") as f:
        f.write(result["text"])
    label.config(text=f"Recording duration: {format_duration(duration)}")
    transcript_box.insert(tk.END, result["text"])

def format_duration(seconds):
    minutes, seconds = divmod(seconds, 60)
    return f"{int(minutes)}:{int(seconds):02d}"

def update_label():
    if recorder.is_recording:
        duration = time.time() - recorder.start_time
        label.config(text=f"Recording... Duration: {format_duration(duration)}")
        root.after(1000, update_label)

recorder = Recorder()

root = tk.Tk()
start_button = tk.Button(root, text="Start Recording", command=lambda: [recorder.start_recording(), update_label()])
start_button.pack()
stop_button = tk.Button(root, text="Stop and Transcribe Audio", command=transcribe_audio)
stop_button.pack()
cancel_button = tk.Button(root, text="Cancel Recording", command=recorder.cancel_recording)
cancel_button.pack()
label = tk.Label(root, text="")
label.pack()
transcript_box = Text(root)
transcript_box.pack()

root.mainloop()
