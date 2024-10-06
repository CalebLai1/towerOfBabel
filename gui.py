import os
import tkinter as tk
from tkinter import ttk, messagebox
import threading
from vosk import Model
from vosk_manager import MODEL_DIR, AVAILABLE_MODELS, download_and_extract_model
from transcriber import Transcriber
from translator import TranslatorManager
from modelSpeakers import AVAILABLE_SPEAKERS
from bark_generation import generate_bark_audio
from playsound import playsound
from pathlib import Path

LANGUAGE_CODES = {
    'English': 'en',
    'Chinese (Simplified)': 'zh-CN',
    'Dutch': 'nl',
    'French': 'fr',
    'German': 'de',
    'Italian': 'it',
    'Spanish': 'es',
    'Russian': 'ru',
    'Portuguese': 'pt',
    'Turkish': 'tr',
    'Japanese': 'ja',
    'Korean': 'ko',
    'Arabic': 'ar',
    'Hindi': 'hi',
    'Bengali': 'bn',
    'Swedish': 'sv',
    'Norwegian': 'no',
    'Finnish': 'fi',
    'Danish': 'da',
    'Greek': 'el',
    'Hebrew': 'he',
    'Polish': 'pl',
    'Czech': 'cs',
    'Hungarian': 'hu',
    'Thai': 'th',
    'Vietnamese': 'vi',
}

class RealTimeTranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Real-Time Translator and Transcriber")
        self.models = {}
        self.translator_manager = TranslatorManager()
        self.create_widgets()

    def create_widgets(self):
        conversation_frame = tk.Frame(self.root)
        conversation_frame.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(conversation_frame, borderwidth=0)
        scrollbar = ttk.Scrollbar(conversation_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        controls_frame = tk.Frame(self.root)
        controls_frame.pack(fill=tk.X)

        left_controls = tk.Frame(controls_frame)
        left_controls.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=10)

        left_language_label = tk.Label(left_controls, text="Their Language:")
        left_language_label.pack()
        self.left_language_var = tk.StringVar()
        self.left_language_dropdown = ttk.Combobox(
            left_controls, textvariable=self.left_language_var, state="readonly")
        self.left_language_dropdown['values'] = list(AVAILABLE_MODELS.keys())
        self.left_language_dropdown.current(0)
        self.left_language_dropdown.pack(fill=tk.X)

        self.left_record_button = tk.Button(
            left_controls, text="Record Their Speech", command=lambda: self.start_recording('left'))
        self.left_record_button.pack(pady=(10, 0))

        self.left_stop_button = tk.Button(
            left_controls, text="Stop Recording", state=tk.DISABLED, command=lambda: self.stop_recording('left'))
        self.left_stop_button.pack(pady=(5, 0))

        right_controls = tk.Frame(controls_frame)
        right_controls.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=10, pady=10)

        right_language_label = tk.Label(right_controls, text="Your Language:")
        right_language_label.pack()
        self.right_language_var = tk.StringVar()
        self.right_language_dropdown = ttk.Combobox(
            right_controls, textvariable=self.right_language_var, state="readonly")
        self.right_language_dropdown['values'] = list(AVAILABLE_MODELS.keys())
        self.right_language_dropdown.current(0)
        self.right_language_dropdown.pack(fill=tk.X)

        self.right_record_button = tk.Button(
            right_controls, text="Record Your Speech", command=lambda: self.start_recording('right'))
        self.right_record_button.pack(pady=(10, 0))

        self.right_stop_button = tk.Button(
            right_controls, text="Stop Recording", state=tk.DISABLED, command=lambda: self.stop_recording('right'))
        self.right_stop_button.pack(pady=(5, 0))

        self.left_language_dropdown.bind("<<ComboboxSelected>>", lambda event: self.update_model('left'))
        self.right_language_dropdown.bind("<<ComboboxSelected>>", lambda event: self.update_model('right'))

    def update_model(self, side):
        language = self.get_language(side)
        if language not in self.models:
            url = AVAILABLE_MODELS.get(language)
            if url:
                download_and_extract_model(language, url)
                model_path = Path(MODEL_DIR) / language
                if model_path.exists():
                    for item in model_path.iterdir():
                        if item.is_dir():
                            self.models[language] = Model(str(item))
                            break
                    else:
                        messagebox.showerror("Error", f"Model for {language} not found.")
                        return
                else:
                    messagebox.showerror("Error", f"Failed to download model for {language}.")
                    return
            else:
                messagebox.showerror("Error", f"No model URL found for {language}")
                return

    def get_lang_code(self, language_name):
        return LANGUAGE_CODES.get(language_name, 'en')

    def get_language(self, side):
        if side == 'left':
            return self.left_language_var.get()
        else:
            return self.right_language_var.get()

    def start_recording(self, side):
        if side == 'left':
            language_var = self.left_language_var
            record_button = self.left_record_button
            stop_button = self.left_stop_button
            language_dropdown = self.left_language_dropdown
        else:
            language_var = self.right_language_var
            record_button = self.right_record_button
            stop_button = self.right_stop_button
            language_dropdown = self.right_language_dropdown

        language = language_var.get()

        if language not in self.models:
            self.update_model(side)
            if language not in self.models:
                return

        transcriber = Transcriber(self.models[language])

        threading.Thread(target=self.record_and_transcribe, args=(transcriber, side), daemon=True).start()

        record_button.config(text="Recording...", state=tk.DISABLED)
        language_dropdown.config(state=tk.DISABLED)
        stop_button.config(state=tk.NORMAL)

        if side == 'left':
            self.left_transcriber = transcriber
            self.left_record_button_ref = record_button
            self.left_stop_button_ref = stop_button
            self.left_language_dropdown_ref = language_dropdown
        else:
            self.right_transcriber = transcriber
            self.right_record_button_ref = record_button
            self.right_stop_button_ref = stop_button
            self.right_language_dropdown_ref = language_dropdown

    def stop_recording(self, side):
        if side == 'left':
            transcriber = self.left_transcriber
            record_button = self.left_record_button_ref
            stop_button = self.left_stop_button_ref
            language_dropdown = self.left_language_dropdown_ref
        else:
            transcriber = self.right_transcriber
            record_button = self.right_record_button_ref
            stop_button = self.right_stop_button_ref
            language_dropdown = self.right_language_dropdown_ref

        transcriber.stop_recording()

        record_button.config(text="Record Speech", state=tk.NORMAL)
        stop_button.config(state=tk.DISABLED)
        language_dropdown.config(state=tk.NORMAL)

    def record_and_transcribe(self, transcriber, side):
        transcriber.start_recording(
            lambda text, partial: self.root.after(0, self.update_conversation, side, text, partial)
        )

    def update_conversation(self, side, text, partial):
        if side == 'left':
            source_lang_var = self.left_language_var
            target_lang_var = self.right_language_var
            transcriber = self.left_transcriber
            speaker_label = "Them"
            target_language = self.right_language_var.get()
        else:
            source_lang_var = self.right_language_var
            target_lang_var = self.left_language_var
            transcriber = self.right_transcriber
            speaker_label = "You"
            target_language = self.left_language_var.get()

        source_lang = source_lang_var.get()
        target_lang = target_lang_var.get()

        src_lang_code = self.get_lang_code(source_lang)
        dest_lang_code = self.get_lang_code(target_lang)

        if not partial:
            original_frame = tk.Frame(self.scrollable_frame, pady=5)
            original_frame.pack(fill=tk.X, anchor='w' if side == 'left' else 'e', padx=10)

            speaker_label_widget = tk.Label(
                original_frame,
                text=f"{speaker_label}: ",
                font=('Arial', 10, 'bold'),
                fg='blue' if side == 'left' else 'green'
            )
            speaker_label_widget.pack(side=tk.LEFT)

            original_text_widget = tk.Label(
                original_frame,
                text=text,
                wraplength=500,
                justify='left'
            )
            original_text_widget.pack(side=tk.LEFT)

            translated = self.translator_manager.translate_text(text, src_lang_code, dest_lang_code)

            translated_frame = tk.Frame(self.scrollable_frame, pady=5)
            translated_frame.pack(fill=tk.X, anchor='w' if side == 'left' else 'e', padx=10)

            translated_label = tk.Label(
                translated_frame,
                text="Translated: ",
                font=('Arial', 10, 'italic'),
                fg='gray'
            )
            translated_label.pack(side=tk.LEFT)

            translated_text_widget = tk.Label(
                translated_frame,
                text=translated,
                wraplength=500,
                justify='left'
            )
            translated_text_widget.pack(side=tk.LEFT)

            speaker_selection_frame = tk.Frame(self.scrollable_frame, pady=5)
            speaker_selection_frame.pack(fill=tk.X, anchor='w' if side == 'left' else 'e', padx=10)

            speaker_label_widget = tk.Label(
                speaker_selection_frame,
                text="Select Speaker: ",
                font=('Arial', 10)
            )
            speaker_label_widget.pack(side=tk.LEFT)

            speaker_var = tk.StringVar()
            speaker_dropdown = ttk.Combobox(
                speaker_selection_frame,
                textvariable=speaker_var,
                state="readonly"
            )

            available_speakers = AVAILABLE_SPEAKERS

            if not available_speakers:
                speaker_dropdown['values'] = ["No speakers available"]
                speaker_dropdown.current(0)
                speaker_dropdown.config(state="disabled")
            else:
                speaker_dropdown['values'] = [speaker['display'] for speaker in available_speakers]
                max_length = max(len(speaker['display']) for speaker in available_speakers)
                min_width = 20
                final_width = max(max_length + 2, min_width)
                speaker_dropdown.config(width=final_width)
                speaker_dropdown.current(0)

            speaker_dropdown.pack(side=tk.LEFT, fill=tk.X, expand=True)

            button_frame = tk.Frame(self.scrollable_frame, pady=5)
            button_frame.pack(fill=tk.X, anchor='w' if side == 'left' else 'e', padx=10)

            generate_button = tk.Button(
                button_frame,
                text="Generate Bark Audio",
                command=lambda: self.generate_audio_with_speaker(
                    translated,
                    dest_lang_code,
                    available_speakers,
                    speaker_var.get(),
                    play_button
                )
            )
            generate_button.pack(side=tk.LEFT, padx=(0, 5))

            play_button = tk.Button(
                button_frame,
                text="Play Audio",
                state=tk.DISABLED,
                command=lambda: self.play_audio(play_button.filepath) if hasattr(play_button, 'filepath') else None
            )
            play_button.pack(side=tk.LEFT)

            spacer = tk.Frame(self.scrollable_frame, height=10)
            spacer.pack()

            self.scrollable_frame.update_idletasks()
            self.root.update_idletasks()

            self.scrollable_frame.master.yview_moveto(1.0)

            transcriber.stop_recording()
            if side == 'left':
                self.left_record_button_ref.config(text=f"Record {speaker_label}'s Speech", state=tk.NORMAL)
                self.left_stop_button_ref.config(state=tk.DISABLED)
                self.left_language_dropdown_ref.config(state=tk.NORMAL)
            else:
                self.right_record_button_ref.config(text=f"Record {speaker_label}'s Speech", state=tk.NORMAL)
                self.right_stop_button_ref.config(state=tk.DISABLED)
                self.right_language_dropdown_ref.config(state=tk.NORMAL)

    def generate_audio_with_speaker(self, text, dest_lang_code, available_speakers, selected_speaker_display, play_button):
        if not available_speakers:
            messagebox.showerror("Error", "No available speakers for the selected language.")
            return

        selected_speaker = next((s for s in available_speakers if s['display'] == selected_speaker_display), None)
        if not selected_speaker:
            messagebox.showerror("Error", "Selected speaker not found.")
            return

        self.generate_audio_thread(text, dest_lang_code, selected_speaker['id'], play_button)

    def generate_audio_thread(self, text, dest_lang_code, speaker_id, play_button):
        threading.Thread(target=self.generate_audio, args=(text, dest_lang_code, speaker_id, play_button), daemon=True).start()

    def generate_audio(self, text, dest_lang_code, speaker_id, play_button):
        filepath = generate_bark_audio(text, dest_lang_code, speaker_id)
        filepath = Path(filepath).resolve()
        if filepath.exists():
            self.root.after(0, lambda: self.enable_play_button(play_button, filepath))
            self.root.after(0, lambda: messagebox.showinfo("Success", f"Audio saved to {filepath}"))
        else:
            self.root.after(0, lambda: messagebox.showerror("Error", "Failed to generate audio."))

    def enable_play_button(self, play_button, filepath):
        play_button.config(state=tk.NORMAL)
        play_button.filepath = str(filepath)

    def play_audio(self, filepath):
        filepath = Path(filepath)
        if not filepath.exists():
            messagebox.showerror("Error", "Audio file not found.")
            return

        try:
            playsound(str(filepath))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to play audio: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RealTimeTranslatorApp(root)
    root.geometry("800x600")
    root.mainloop()
