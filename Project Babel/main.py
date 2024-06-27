import tkinter as tk
from tkinter import filedialog, Text, simpledialog, ttk
import whisper
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import threading
import time
import os
from pytube import YouTube
from deep_translator import (GoogleTranslator,
                             ChatGptTranslator,
                             MicrosoftTranslator,
                             PonsTranslator,
                             LingueeTranslator,
                             MyMemoryTranslator,
                             YandexTranslator,
                             PapagoTranslator,
                             DeeplTranslator,
                             QcriTranslator,
                             single_detection,
                             batch_detection)
from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav


preload_models()

def speak_text(text_box, voice_var):
    text = text_box.get("1.0", tk.END)
    selected_voice = voice_var.get()
    audio_array = generate_audio(text, history_prompt=selected_voice)
    write_wav('output.wav', SAMPLE_RATE, audio_array)
    os.system('start output.wav')

class Recorder: 
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
            sd.wait()  
            duration = time.time() - self.start_time
            print("Recording finished. Saving to file...")
            wav.write('output.wav', self.fs, self.myrecording)  
            return 'output.wav', duration

    def cancel_recording(self):
        if self.is_recording:
            self.is_recording = False
            print("Recording cancelled.")

def transcribe_audio():
    model = whisper.load_model("base")
    filename, duration = recorder.stop_recording()
    result = model.transcribe(filename)
    transcript_box.insert(tk.END, result["text"])
    translated_text1 = GoogleTranslator(source='auto', target=language_var1.get()).translate(result["text"])
    translated_box1.insert(tk.END, translated_text1)
    translated_text2 = GoogleTranslator(source='auto', target=language_var2.get()).translate(result["text"])
    translated_box2.insert(tk.END, translated_text2)
    label.config(text=f"Recording duration: {format_duration(duration)}")

def open_audio_file():
    filename = filedialog.askopenfilename(initialdir="/", title="Select Audio File",
                                          filetypes=(("wav files", "*.wav"), ("all files", "*.*")))
    if filename:
        transcribe_audio_file(filename)

def transcribe_audio_file(filename):
    model = whisper.load_model("base")
    result = model.transcribe(filename)
    transcript_box.insert(tk.END, result["text"])
    translated_text1 = GoogleTranslator(source='auto', target=language_var1.get()).translate(result["text"])
    translated_box1.insert(tk.END, translated_text1)
    translated_text2 = GoogleTranslator(source='auto', target=language_var2.get()).translate(result["text"])
    translated_box2.insert(tk.END, translated_text2)

def download_youtube_audio(url):
    yt = YouTube(url)
    stream = yt.streams.filter(only_audio=True).first()
    filename = stream.default_filename
    stream.download(filename=filename)
    return filename

def open_youtube_video():
    url = simpledialog.askstring("YouTube Video URL", "Enter the URL of the YouTube video:")
    if url:
        filename = download_youtube_audio(url)
        transcribe_audio_file(filename)

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
voice_options = [
    "v2/en_speaker_0", "v2/en_speaker_1", "v2/en_speaker_2", "v2/en_speaker_3", "v2/en_speaker_4",
    "v2/en_speaker_5", "v2/en_speaker_6", "v2/en_speaker_7", "v2/en_speaker_8", "v2/en_speaker_9",
    "v2/zh_speaker_0", "v2/zh_speaker_1", "v2/zh_speaker_2", "v2/zh_speaker_3", "v2/zh_speaker_4",
    "v2/zh_speaker_5", "v2/zh_speaker_6", "v2/zh_speaker_7", "v2/zh_speaker_8", "v2/zh_speaker_9",
    "v2/fr_speaker_0", "v2/fr_speaker_1", "v2/fr_speaker_2", "v2/fr_speaker_3", "v2/fr_speaker_4",
    "v2/fr_speaker_5", "v2/fr_speaker_6", "v2/fr_speaker_7", "v2/fr_speaker_8", "v2/fr_speaker_9",
    "v2/de_speaker_0", "v2/de_speaker_1", "v2/de_speaker_2", "v2/de_speaker_3", "v2/de_speaker_4",
    "v2/de_speaker_5", "v2/de_speaker_6", "v2/de_speaker_7", "v2/de_speaker_8", "v2/de_speaker_9",
    "v2/hi_speaker_0", "v2/hi_speaker_1", "v2/hi_speaker_2", "v2/hi_speaker_3", "v2/hi_speaker_4",
    "v2/hi_speaker_5", "v2/hi_speaker_6", "v2/hi_speaker_7", "v2/hi_speaker_8", "v2/hi_speaker_9",
    "v2/it_speaker_0", "v2/it_speaker_1", "v2/it_speaker_2", "v2/it_speaker_3", "v2/it_speaker_4",
    "v2/it_speaker_5", "v2/it_speaker_6", "v2/it_speaker_7", "v2/it_speaker_8", "v2/it_speaker_9",
    "v2/ja_speaker_0", "v2/ja_speaker_1", "v2/ja_speaker_2", "v2/ja_speaker_3", "v2/ja_speaker_4",
    "v2/ja_speaker_5", "v2/ja_speaker_6", "v2/ja_speaker_7", "v2/ja_speaker_8", "v2/ja_speaker_9",
    "v2/ko_speaker_0", "v2/ko_speaker_1", "v2/ko_speaker_2", "v2/ko_speaker_3", "v2/ko_speaker_4",
    "v2/ko_speaker_5", "v2/ko_speaker_6", "v2/ko_speaker_7", "v2/ko_speaker_8", "v2/ko_speaker_9",
    "v2/pl_speaker_0", "v2/pl_speaker_1", "v2/pl_speaker_2", "v2/pl_speaker_3", "v2/pl_speaker_4",
    "v2/pl_speaker_5", "v2/pl_speaker_6", "v2/pl_speaker_7", "v2/pl_speaker_8", "v2/pl_speaker_9",
    "v2/pt_speaker_0", "v2/pt_speaker_1", "v2/pt_speaker_2", "v2/pt_speaker_3", "v2/pt_speaker_4",
    "v2/pt_speaker_5", "v2/pt_speaker_6", "v2/pt_speaker_7", "v2/pt_speaker_8", "v2/pt_speaker_9",
    "v2/ru_speaker_0", "v2/ru_speaker_1", "v2/ru_speaker_2", "v2/ru_speaker_3", "v2/ru_speaker_4",
    "v2/ru_speaker_5", "v2/ru_speaker_6", "v2/ru_speaker_7", "v2/ru_speaker_8", "v2/ru_speaker_9",
    "v2/es_speaker_0", "v2/es_speaker_1", "v2/es_speaker_2", "v2/es_speaker_3", "v2/es_speaker_4",
    "v2/es_speaker_5", "v2/es_speaker_6", "v2/es_speaker_7", "v2/es_speaker_8", "v2/es_speaker_9",
    "v2/tr_speaker_0", "v2/tr_speaker_1", "v2/tr_speaker_2", "v2/tr_speaker_3", "v2/tr_speaker_4",
    "v2/tr_speaker_5", "v2/tr_speaker_6", "v2/tr_speaker_7", "v2/tr_speaker_8", "v2/tr_speaker_9"
]
voice_var = tk.StringVar(root)
voice_var.set(voice_options[0])  # default value
voice_menu = ttk.Combobox(root, textvariable=voice_var, values=voice_options)
voice_menu.pack()
speak_button1 = tk.Button(root, text="Speak Translated Text 1", command=lambda: speak_text(translated_box1, voice_var))
speak_button1.pack(side=tk.LEFT)
speak_button2 = tk.Button(root, text="Speak Translated Text 2", command=lambda: speak_text(translated_box2, voice_var))
speak_button2.pack(side=tk.RIGHT)
start_button = tk.Button(root, text="Start Recording", command=lambda: [recorder.start_recording(), update_label()])
start_button.pack()
stop_button = tk.Button(root, text="Stop and Transcribe Audio", command=transcribe_audio)
stop_button.pack()
cancel_button = tk.Button(root, text="Cancel Recording", command=recorder.cancel_recording)
cancel_button.pack()
open_file_button = tk.Button(root, text="Open Audio File", command=open_audio_file)
open_file_button.pack()
youtube_button = tk.Button(root, text="Open YouTube Video", command=open_youtube_video)
youtube_button.pack()
label = tk.Label(root, text="")
label.pack()

# Dropdown menus for language selection
translator = GoogleTranslator(source='auto', target='english')
language_var1 = tk.StringVar(root)
language_var1.set("english")  # default value
language_choices = translator.get_supported_languages()
language_menu1 = ttk.Combobox(root, textvariable=language_var1, values=language_choices)
language_menu1.pack(side=tk.LEFT)

language_var2 = tk.StringVar(root)
language_var2.set("english")  # default value
language_menu2 = ttk.Combobox(root, textvariable=language_var2, values=language_choices)
language_menu2.pack(side=tk.RIGHT)

# Three text boxes for original and translated text
translated_box1 = Text(root)
translated_box1.pack(side=tk.LEFT)
transcript_box = Text(root)
transcript_box.pack(side=tk.LEFT)
translated_box2 = Text(root)
translated_box2.pack(side=tk.RIGHT)

root.mainloop()