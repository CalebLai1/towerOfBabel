# gui.py

import os
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
import threading
from vosk import Model
from vosk_manager import MODEL_DIR, AVAILABLE_MODELS, download_and_extract_model
from transcriber import Transcriber
from translator import TranslatorManager

LANGUAGE_CODES = {
    'English': 'en',
    'Chinese': 'zh-cn',
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
        # Main frame for the conversation
        conversation_frame = tk.Frame(self.root)
        conversation_frame.pack(fill=tk.BOTH, expand=True)

        # Conversation text box
        self.conversation_text = ScrolledText(conversation_frame, wrap=tk.WORD)
        self.conversation_text.pack(fill=tk.BOTH, expand=True)

        # Configure text tags for alignment and styling
        self.conversation_text.tag_configure('left', justify='left', foreground='blue')
        self.conversation_text.tag_configure('right', justify='right', foreground='green')
        self.conversation_text.tag_configure('system', justify='center', foreground='gray')
        self.conversation_text.tag_configure('bold', font=('Arial', 10, 'bold'))

        # Bottom frame for controls
        controls_frame = tk.Frame(self.root)
        controls_frame.pack(fill=tk.X)

        # Left side controls
        left_controls = tk.Frame(controls_frame)
        left_controls.pack(side=tk.LEFT, fill=tk.X, expand=True)

        left_language_label = tk.Label(left_controls, text="Their Language:")
        left_language_label.pack()
        self.left_language_var = tk.StringVar()
        self.left_language_dropdown = ttk.Combobox(
            left_controls, textvariable=self.left_language_var)
        self.left_language_dropdown['values'] = list(AVAILABLE_MODELS.keys())
        self.left_language_dropdown.current(0)
        self.left_language_dropdown.pack()

        self.left_record_button = tk.Button(
            left_controls, text="Record Their Speech", command=lambda: self.start_recording('left'))
        self.left_record_button.pack()

        # Right side controls
        right_controls = tk.Frame(controls_frame)
        right_controls.pack(side=tk.RIGHT, fill=tk.X, expand=True)

        right_language_label = tk.Label(right_controls, text="Your Language:")
        right_language_label.pack()
        self.right_language_var = tk.StringVar()
        self.right_language_dropdown = ttk.Combobox(
            right_controls, textvariable=self.right_language_var)
        self.right_language_dropdown['values'] = list(AVAILABLE_MODELS.keys())
        self.right_language_dropdown.current(0)
        self.right_language_dropdown.pack()

        self.right_record_button = tk.Button(
            right_controls, text="Record Your Speech", command=lambda: self.start_recording('right'))
        self.right_record_button.pack()

    def get_lang_code(self, language_name):
        return LANGUAGE_CODES.get(language_name, 'en')

    def start_recording(self, side):
        if side == 'left':
            language_var = self.left_language_var
            record_button = self.left_record_button
            language_dropdown = self.left_language_dropdown
        else:
            language_var = self.right_language_var
            record_button = self.right_record_button
            language_dropdown = self.right_language_dropdown

        language = language_var.get()
        if language not in self.models:
            url = AVAILABLE_MODELS.get(language)
            if url:
                download_and_extract_model(language, url)
                model_path = os.path.join(MODEL_DIR, language)
                if os.path.exists(model_path):
                    # Find the actual model directory
                    for item in os.listdir(model_path):
                        item_path = os.path.join(model_path, item)
                        if os.path.isdir(item_path):
                            self.models[language] = Model(item_path)
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

        # Create a new transcriber for this recording
        transcriber = Transcriber(self.models[language])

        # Start recording in a separate thread
        threading.Thread(target=self.record_and_transcribe, args=(transcriber, side)).start()

        # Disable the record button and language dropdown
        record_button.config(text="Recording...", state=tk.DISABLED)
        language_dropdown.config(state=tk.DISABLED)

        # Store references
        if side == 'left':
            self.left_transcriber = transcriber
            self.left_record_button_ref = record_button
            self.left_language_dropdown_ref = language_dropdown
        else:
            self.right_transcriber = transcriber
            self.right_record_button_ref = record_button
            self.right_language_dropdown_ref = language_dropdown

    def record_and_transcribe(self, transcriber, side):
        # Start recording and transcribing
        transcriber.start_recording(
            lambda text, partial: self.root.after(0, self.update_conversation, side, text, partial))

    def update_conversation(self, side, text, partial):
        if side == 'left':
            source_lang_var = self.left_language_var
            target_lang_var = self.right_language_var
            record_button_ref = self.left_record_button_ref
            language_dropdown_ref = self.left_language_dropdown_ref
            transcriber = self.left_transcriber
            alignment = 'left'
            speaker_label = "Them"
        else:
            source_lang_var = self.right_language_var
            target_lang_var = self.left_language_var
            record_button_ref = self.right_record_button_ref
            language_dropdown_ref = self.right_language_dropdown_ref
            transcriber = self.right_transcriber
            alignment = 'right'
            speaker_label = "You"

        source_lang = source_lang_var.get()
        target_lang = target_lang_var.get()

        src_lang_code = self.get_lang_code(source_lang)
        dest_lang_code = self.get_lang_code(target_lang)

        if partial:
            # Update typing indicator (optional)
            pass  # We can choose to implement a typing indicator if desired
        else:
            # Display original text with speaker label
            self.conversation_text.insert(tk.END, f"{speaker_label}: ", ('bold', alignment))
            self.conversation_text.insert(tk.END, f"{text}\n", alignment)
            self.conversation_text.see(tk.END)

            # Translate the text
            translated = self.translator_manager.translate_text(text, src_lang_code, dest_lang_code)

            # Display translated text on the opposite side
            other_alignment = 'right' if alignment == 'left' else 'left'
            other_speaker_label = "You" if speaker_label == "Them" else "Them"
            self.conversation_text.insert(tk.END, f"{other_speaker_label} (Translated): ", ('bold', other_alignment))
            self.conversation_text.insert(tk.END, f"{translated}\n", other_alignment)
            self.conversation_text.see(tk.END)

            # Reset recording buttons
            transcriber.stop_recording()
            record_button_ref.config(text=f"Record {speaker_label}'s Speech", state=tk.NORMAL)
            language_dropdown_ref.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = RealTimeTranslatorApp(root)
    root.mainloop()
