import tkinter as tk
from tkinter import ttk, Text, filedialog, simpledialog
from shared_functions import Recorder, format_duration, download_youtube_audio, transcribe_audio_file, translate_text, get_language_choices
from voice_options import VOICE_OPTIONS

class OfflineMode:
    def __init__(self, notebook):
        self.frame = ttk.Frame(notebook)
        notebook.add(self.frame, text="Offline Mode")

        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(3, weight=1)

        self.create_widgets()
        self.recorder = Recorder()

    def create_widgets(self):
        # Voice selection
        voice_frame = ttk.Frame(self.frame)
        voice_frame.grid(row=0, column=0, pady=10, sticky="ew")
        voice_frame.columnconfigure((0, 1), weight=1)

        self.voice_var1 = tk.StringVar(value=VOICE_OPTIONS[0])
        voice_menu1 = ttk.Combobox(voice_frame, textvariable=self.voice_var1, values=VOICE_OPTIONS)
        voice_menu1.grid(row=0, column=0, padx=5, sticky="ew")

        self.voice_var2 = tk.StringVar(value=VOICE_OPTIONS[0])
        voice_menu2 = ttk.Combobox(voice_frame, textvariable=self.voice_var2, values=VOICE_OPTIONS)
        voice_menu2.grid(row=0, column=1, padx=5, sticky="ew")

        # Language selection
        lang_frame = ttk.Frame(self.frame)
        lang_frame.grid(row=1, column=0, pady=10, sticky="ew")
        lang_frame.columnconfigure((0, 1), weight=1)

        self.language_var1 = tk.StringVar(value="english")
        language_menu1 = ttk.Combobox(lang_frame, textvariable=self.language_var1, values=get_language_choices())
        language_menu1.grid(row=0, column=0, padx=5, sticky="ew")

        self.language_var2 = tk.StringVar(value="english")
        language_menu2 = ttk.Combobox(lang_frame, textvariable=self.language_var2, values=get_language_choices())
        language_menu2.grid(row=0, column=1, padx=5, sticky="ew")

        # Text boxes
        text_frame = ttk.Frame(self.frame)
        text_frame.grid(row=3, column=0, sticky="nsew", pady=10)
        text_frame.columnconfigure((0, 1, 2), weight=1)
        text_frame.rowconfigure(0, weight=1)

        self.translated_box1 = Text(text_frame, wrap="word")
        self.translated_box1.grid(row=0, column=0, sticky="nsew", padx=5)

        self.transcript_box = Text(text_frame, wrap="word")
        self.transcript_box.grid(row=0, column=1, sticky="nsew", padx=5)

        self.translated_box2 = Text(text_frame, wrap="word")
        self.translated_box2.grid(row=0, column=2, sticky="nsew", padx=5)

        # Buttons
        button_frame = ttk.Frame(self.frame)
        button_frame.grid(row=4, column=0, pady=10, sticky="ew")

        ttk.Button(button_frame, text="Start Recording", command=self.start_recording).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Stop and Transcribe", command=self.stop_and_transcribe).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Cancel Recording", command=self.cancel_recording).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Open Audio File", command=self.open_audio_file).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Open YouTube Video", command=self.open_youtube_video).pack(side="left", padx=5)

        # Status label
        self.status_label = ttk.Label(self.frame, text="")
        self.status_label.grid(row=5, column=0, pady=10)


    def get_language_choices(self):
        from deep_translator import GoogleTranslator
        return GoogleTranslator(source='auto', target='english').get_supported_languages()

    def start_recording(self):
        self.recorder.start_recording()
        self.status_label.config(text="Recording...")
        self.frame.after(1000, self.update_recording_duration)

    def stop_and_transcribe(self):
        filename, duration = self.recorder.stop_recording()
        self.transcribe_audio_file(filename)
        self.status_label.config(text=f"Recording duration: {format_duration(duration)}")

    def cancel_recording(self):
        self.recorder.cancel_recording()
        self.status_label.config(text="Recording cancelled.")

    def open_audio_file(self):
        filename = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav"), ("All files", "*.*")])
        if filename:
            self.transcribe_audio_file(filename)

    def open_youtube_video(self):
        url = simpledialog.askstring("YouTube Video URL", "Enter the URL of the YouTube video:")
        if url:
            filename = download_youtube_audio(url)
            self.transcribe_audio_file(filename)

    def transcribe_audio_file(self, filename):
        result = transcribe_audio_file(filename)
        self.transcript_box.delete("1.0", tk.END)
        self.transcript_box.insert(tk.END, result)
        self.translate_text()

    def translate_text(self):
        text = self.transcript_box.get("1.0", tk.END).strip()
        translated_text1, translated_text2 = translate_text(text, self.language_var1.get(), self.language_var2.get())
        
        self.translated_box1.delete("1.0", tk.END)
        self.translated_box1.insert(tk.END, translated_text1)
        
        self.translated_box2.delete("1.0", tk.END)
        self.translated_box2.insert(tk.END, translated_text2)

    def update_recording_duration(self):
        if self.recorder.is_recording:
            duration = self.recorder.get_recording_duration()
            self.status_label.config(text=f"Recording... Duration: {format_duration(duration)}")
            self.frame.after(1000, self.update_recording_duration)