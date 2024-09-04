import tkinter as tk
from tkinter import ttk, Text
import threading
import time
from shared_functions import generate_and_save_audio, speak_text, realtime_transcribe_translate, get_language_choices
from voice_options import VOICE_OPTIONS
from deep_translator import GoogleTranslator
from gtts import gTTS
import os
from playsound import playsound

class RealtimeMode:
    def __init__(self, notebook):
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Realtime Mode")

        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)

        self.create_widgets()
        self.is_recording_realtime = False
        self.audio_counter = {"person1": 1, "person2": 1}

    def create_widgets(self):
        # Conversation area
        conv_frame = ttk.Frame(self.frame)
        conv_frame.grid(row=0, column=0, sticky="nsew", pady=10)
        conv_frame.columnconfigure((0, 2), weight=1)
        conv_frame.rowconfigure(1, weight=1)

        # Left language column
        left_frame = ttk.Frame(conv_frame)
        left_frame.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=5)
        left_frame.columnconfigure(0, weight=1)
        left_frame.rowconfigure(2, weight=1)

        # Left voice and language selection
        left_config_frame = ttk.Frame(left_frame)
        left_config_frame.grid(row=0, column=0, sticky="ew", pady=5)
        left_config_frame.columnconfigure((0, 1), weight=1)

        self.left_voice_var = tk.StringVar(value=VOICE_OPTIONS[0])
        ttk.Combobox(left_config_frame, textvariable=self.left_voice_var, values=VOICE_OPTIONS).grid(row=0, column=0, padx=5, sticky="ew")

        self.left_lang_var = tk.StringVar(value="english")
        ttk.Combobox(left_config_frame, textvariable=self.left_lang_var, values=get_language_choices()).grid(row=0, column=1, padx=5, sticky="ew")

        ttk.Label(left_frame, text="Original Text").grid(row=1, column=0, sticky="w", pady=(10, 0))
        self.left_original = Text(left_frame, wrap="word", height=10)
        self.left_original.grid(row=2, column=0, sticky="nsew")
        self.left_original.config(bg="white")

        ttk.Label(left_frame, text="Translated Text").grid(row=3, column=0, sticky="w", pady=(10, 0))
        self.left_translated = Text(left_frame, wrap="word", height=10)
        self.left_translated.grid(row=4, column=0, sticky="nsew")
        self.left_translated.config(bg="lightblue")

        ttk.Button(left_frame, text="Speak", command=lambda: self.speak_realtime_text("left")).grid(row=5, column=0, pady=5)

        # Microphone button and recording indicator
        mic_frame = ttk.Frame(conv_frame)
        mic_frame.grid(row=1, column=1, padx=10)
        self.mic_button = ttk.Button(mic_frame, text="🎤", command=self.toggle_realtime_recording, width=5)
        self.mic_button.pack(pady=5)
        
        self.canvas = tk.Canvas(mic_frame, width=50, height=50)
        self.canvas.pack()
        self.indicator = self.canvas.create_oval(5, 5, 45, 45, fill="gray")
        self.indicator_ring = self.canvas.create_arc(0, 0, 50, 50, start=0, extent=0, fill="")

        # Right language column
        right_frame = ttk.Frame(conv_frame)
        right_frame.grid(row=0, column=2, rowspan=2, sticky="nsew", padx=5)
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(2, weight=1)

        # Right voice and language selection
        right_config_frame = ttk.Frame(right_frame)
        right_config_frame.grid(row=0, column=0, sticky="ew", pady=5)
        right_config_frame.columnconfigure((0, 1), weight=1)

        self.right_voice_var = tk.StringVar(value=VOICE_OPTIONS[0])
        ttk.Combobox(right_config_frame, textvariable=self.right_voice_var, values=VOICE_OPTIONS).grid(row=0, column=0, padx=5, sticky="ew")

        self.right_lang_var = tk.StringVar(value="spanish")
        ttk.Combobox(right_config_frame, textvariable=self.right_lang_var, values=get_language_choices()).grid(row=0, column=1, padx=5, sticky="ew")

        ttk.Label(right_frame, text="Original Text").grid(row=1, column=0, sticky="w", pady=(10, 0))
        self.right_original = Text(right_frame, wrap="word", height=10)
        self.right_original.grid(row=2, column=0, sticky="nsew")
        self.right_original.config(bg="white")

        ttk.Label(right_frame, text="Translated Text").grid(row=3, column=0, sticky="w", pady=(10, 0))
        self.right_translated = Text(right_frame, wrap="word", height=10)
        self.right_translated.grid(row=4, column=0, sticky="nsew")
        self.right_translated.config(bg="lightblue")

        ttk.Button(right_frame, text="Speak", command=lambda: self.speak_realtime_text("right")).grid(row=5, column=0, pady=5)

    def toggle_realtime_recording(self):
        if not self.is_recording_realtime:
            self.start_realtime_recording()
        else:
            self.stop_realtime_recording()

    def start_realtime_recording(self):
        self.is_recording_realtime = True
        self.mic_button.config(text="⏹")
        self.canvas.itemconfig(self.indicator, fill="red")
        threading.Thread(target=self.realtime_transcribe_translate_wrapper, daemon=True).start()
        threading.Thread(target=self.update_recording_indicator, daemon=True).start()

    def stop_realtime_recording(self):
        self.is_recording_realtime = False
        self.mic_button.config(text="🎤")
        self.canvas.itemconfig(self.indicator, fill="gray")
        self.canvas.itemconfig(self.indicator_ring, extent=0)

    def update_recording_indicator(self):
        angle = 0
        while self.is_recording_realtime:
            angle = (angle + 10) % 360
            self.canvas.itemconfig(self.indicator_ring, start=angle, extent=90)
            time.sleep(0.1)

    def realtime_transcribe_translate_wrapper(self):
        realtime_transcribe_translate(self)

    def update_realtime_text(self, text, detected_lang):
        left_lang = self.left_lang_var.get()
        right_lang = self.right_lang_var.get()

        if detected_lang == left_lang:
            original_side = "left"
            translation_side = "right"
            target_lang = right_lang
        elif detected_lang == right_lang:
            original_side = "right"
            translation_side = "left"
            target_lang = left_lang
        else:
            print(f"Detected language {detected_lang} doesn't match either side. Defaulting to left.")
            original_side = "left"
            translation_side = "right"
            target_lang = right_lang

        # Update original text
        getattr(self, f"{original_side}_original").insert(tk.END, text + " ")
        getattr(self, f"{original_side}_original").see(tk.END)

        # Translate and update translated text
        translated_text = self.translate_text(text, detected_lang, target_lang)
        getattr(self, f"{translation_side}_translated").insert(tk.END, translated_text + " ")
        getattr(self, f"{translation_side}_translated").see(tk.END)

        # Speak the translated text
        tts = gTTS(text=translated_text, lang=target_lang)
        tts.save("temp.mp3")
        playsound("temp.mp3")
        os.remove("temp.mp3")

        # Generate and save audio for both languages
        self.generate_and_save_audio(text, "1" if original_side == "left" else "2", is_input=True)
        self.generate_and_save_audio(translated_text, "2" if original_side == "left" else "1", is_input=False)

    def generate_and_save_audio(self, text, person, is_input):
        voice = self.left_voice_var.get() if person == "1" else self.right_voice_var.get()
        filename = f"AudioFile{self.audio_counter[f'person{person}']}.wav"
        generate_and_save_audio(text, voice, filename, person, is_input)
        self.audio_counter[f'person{person}'] += 1

    def speak_realtime_text(self, side):
        text = getattr(self, f"{side}_translated").get("1.0", tk.END).strip()
        voice = getattr(self, f"{side}_voice_var").get()
        speak_text(text, voice)

    def translate_text(self, text, source_lang, target_lang):
        return GoogleTranslator(source=source_lang, target=target_lang).translate(text)