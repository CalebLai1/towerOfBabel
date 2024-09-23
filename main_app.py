import tkinter as tk
from tkinter import ttk
from shared_functions import SharedFunctions
from conversation_mode import ConversationMode
from transcription_mode import TranscriptionMode
from voice_clone_page import VoiceGenerationPage
import os

class TranscriptionApp:
    def __init__(self, master):
        self.master = master
        master.title("Multilingual Transcription and Voice Generation App")
        master.geometry("800x600")

        base_model_path = os.path.join(os.path.dirname(__file__), "vosk_models")
        self.shared = SharedFunctions(base_model_path)

        self.device = self.shared.get_device_info()

        self.notebook = ttk.Notebook(master)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.transcription_tab = TranscriptionMode(self.notebook, self.shared)
        self.conversation_tab = ConversationMode(self.notebook, self.shared)
        self.voice_generation_tab = VoiceGenerationPage(self.notebook, self.shared, self.device)

        self.notebook.add(self.transcription_tab, text="Transcription")
        self.notebook.add(self.conversation_tab, text="Conversation")
        self.notebook.add(self.voice_generation_tab, text="Voice Generation")

        self.status_label = ttk.Label(master, text="")
        self.status_label.pack(pady=5)

        self.device_label = ttk.Label(master, text=f"Using: {self.device}")
        self.device_label.pack(pady=5)

        self.language_var = tk.StringVar(value="English")
        self.language_menu = ttk.Combobox(master, textvariable=self.language_var, 
                                          values=list(self.shared.get_language_dict().values()))
        self.language_menu.pack(pady=5)
        self.language_menu.bind("<<ComboboxSelected>>", self.on_language_change)

        self.model_label = ttk.Label(master, text="No model loaded")
        self.model_label.pack(pady=5)

    def on_language_change(self, event):
        lang_name = self.language_var.get()
        lang_code = self.shared.get_language_code(lang_name)
        self.shared.ensure_model(lang_code)
        self.model_label.config(text=f"Model loaded for: {lang_name}")

    def update_status(self, message):
        self.status_label.config(text=message)
        self.master.update_idletasks()

if __name__ == "__main__":
    root = tk.Tk()
    app = TranscriptionApp(root)
    root.mainloop()