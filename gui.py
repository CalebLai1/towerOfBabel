import os
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
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

        # Frames for layout
        left_frame = tk.Frame(self.root)
        right_frame = tk.Frame(self.root)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Left side (Person you're talking to)
        left_language_label = tk.Label(left_frame, text="Their Language:")
        left_language_label.pack()
        self.left_language_var = tk.StringVar()
        self.left_language_dropdown = ttk.Combobox(
            left_frame, textvariable=self.left_language_var)
        self.left_language_dropdown['values'] = list(AVAILABLE_MODELS.keys())
        self.left_language_dropdown.current(0)
        self.left_language_dropdown.pack()

        self.left_text = ScrolledText(left_frame, wrap=tk.WORD)
        self.left_text.pack(fill=tk.BOTH, expand=True)

        self.left_record_button = tk.Button(
            left_frame, text="Record", command=lambda: self.start_recording('left'))
        self.left_record_button.pack()

        # Right side (You)
        right_language_label = tk.Label(right_frame, text="Your Language:")
        right_language_label.pack()
        self.right_language_var = tk.StringVar()
        self.right_language_dropdown = ttk.Combobox(
            right_frame, textvariable=self.right_language_var)
        self.right_language_dropdown['values'] = list(AVAILABLE_MODELS.keys())
        self.right_language_dropdown.current(0)
        self.right_language_dropdown.pack()

        self.right_text = ScrolledText(right_frame, wrap=tk.WORD)
        self.right_text.pack(fill=tk.BOTH, expand=True)

        self.right_record_button = tk.Button(
            right_frame, text="Record", command=lambda: self.start_recording('right'))
        self.right_record_button.pack()

        # Configure text tags for alignment and styling
        for text_widget in [self.left_text, self.right_text]:
            text_widget.tag_configure('left', justify='left', foreground='blue')
            text_widget.tag_configure('right', justify='right', foreground='green')
            text_widget.tag_configure('typing', foreground='gray')
            text_widget.tag_configure('error', foreground='red')

    def get_lang_code(self, language_name):
        return LANGUAGE_CODES.get(language_name, 'en')

    def start_recording(self, side):
        if side == 'left':
            language_var = self.left_language_var
            text_widget = self.left_text
            record_button = self.left_record_button
            language_dropdown = self.left_language_dropdown
            other_text_widget = self.right_text
        else:
            language_var = self.right_language_var
            text_widget = self.right_text
            record_button = self.right_record_button
            language_dropdown = self.right_language_dropdown
            other_text_widget = self.left_text

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

        # Start recording
        transcriber.start_recording(
            lambda text, partial: self.root.after(0, self.update_text, side, text, partial))

        # Disable the record button and language dropdown
        record_button.config(text="Recording...", state=tk.DISABLED)
        language_dropdown.config(state=tk.DISABLED)

        # Store references
        if side == 'left':
            self.left_transcriber = transcriber
            self.left_record_button_ref = record_button
            self.left_language_dropdown_ref = language_dropdown
            self.left_text_widget = text_widget
            self.right_text_widget = other_text_widget
        else:
            self.right_transcriber = transcriber
            self.right_record_button_ref = record_button
            self.right_language_dropdown_ref = language_dropdown
            self.right_text_widget = text_widget
            self.left_text_widget = other_text_widget

    def update_text(self, side, text, partial):
        if side == 'left':
            source_lang_var = self.left_language_var
            target_lang_var = self.right_language_var
            text_widget = self.left_text_widget
            other_text_widget = self.right_text_widget
            record_button_ref = self.left_record_button_ref
            language_dropdown_ref = self.left_language_dropdown_ref
            transcriber = self.left_transcriber
        else:
            source_lang_var = self.right_language_var
            target_lang_var = self.left_language_var
            text_widget = self.right_text_widget
            other_text_widget = self.left_text_widget
            record_button_ref = self.right_record_button_ref
            language_dropdown_ref = self.right_language_dropdown_ref
            transcriber = self.right_transcriber

        source_lang = source_lang_var.get()
        target_lang = target_lang_var.get()

        src_lang_code = self.get_lang_code(source_lang)
        dest_lang_code = self.get_lang_code(target_lang)

        if partial:
            # Update the typing indicator
            text_widget.delete('end-2l', tk.END)
            text_widget.insert(tk.END, f"Typing: {text}\n", 'typing')
            text_widget.see(tk.END)
        else:
            # Append the final recognized text
            # Display original text
            text_widget.insert(tk.END, f"You: {text}\n", 'right' if side == 'right' else 'left')

            # Translate the text
            translated = self.translator_manager.translate_text(text, src_lang_code, dest_lang_code)

            # Check if translation was successful
            if translated.startswith("Translation Error:"):
                # Display error message
                other_text_widget.insert(tk.END, f"{translated}\n", 'error')
            else:
                # Display translated text in the other user's text widget
                other_text_widget.insert(tk.END, f"Translated: {translated}\n", 'left' if side == 'right' else 'right')
                other_text_widget.see(tk.END)

            # Reset recording buttons
            transcriber.stop_recording()
            record_button_ref.config(text="Record", state=tk.NORMAL)
            language_dropdown_ref.config(state=tk.NORMAL)