import os
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
import threading
from vosk import Model
from vosk_manager import MODEL_DIR, AVAILABLE_MODELS, download_and_extract_model
from transcriber import Transcriber
from translator import TranslatorManager
from models_speakers import AVAILABLE_SPEAKERS
from bark_generation import generate_bark_audio

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
        self.conversation_text.tag_configure('italic', font=('Arial', 10, 'italic'))

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
            left_controls, textvariable=self.left_language_var, state="readonly")
        self.left_language_dropdown['values'] = list(AVAILABLE_MODELS.keys())
        self.left_language_dropdown.current(0)
        self.left_language_dropdown.pack(fill=tk.X)

        left_speaker_label = tk.Label(left_controls, text="Their Speaker:")
        left_speaker_label.pack(pady=(10, 0))
        self.left_speaker_var = tk.StringVar()
        self.left_speaker_dropdown = ttk.Combobox(
            left_controls, textvariable=self.left_speaker_var, state="readonly")
        self.left_speaker_dropdown['values'] = self.get_speakers_by_language("English")
        self.left_speaker_dropdown.current(0)
        self.left_speaker_dropdown.pack(fill=tk.X)

        self.left_record_button = tk.Button(
            left_controls, text="Record Their Speech", command=lambda: self.start_recording('left'))
        self.left_record_button.pack()

        self.left_stop_button = tk.Button(
            left_controls, text="Stop Recording", state=tk.DISABLED, command=lambda: self.stop_recording('left'))
        self.left_stop_button.pack(pady=(10, 0))

        # Right side controls
        right_controls = tk.Frame(controls_frame)
        right_controls.pack(side=tk.RIGHT, fill=tk.X, expand=True)

        right_language_label = tk.Label(right_controls, text="Your Language:")
        right_language_label.pack()
        self.right_language_var = tk.StringVar()
        self.right_language_dropdown = ttk.Combobox(
            right_controls, textvariable=self.right_language_var, state="readonly")
        self.right_language_dropdown['values'] = list(AVAILABLE_MODELS.keys())
        self.right_language_dropdown.current(0)
        self.right_language_dropdown.pack(fill=tk.X)

        right_speaker_label = tk.Label(right_controls, text="Your Speaker:")
        right_speaker_label.pack(pady=(10, 0))
        self.right_speaker_var = tk.StringVar()
        self.right_speaker_dropdown = ttk.Combobox(
            right_controls, textvariable=self.right_speaker_var, state="readonly")
        self.right_speaker_dropdown['values'] = self.get_speakers_by_language("English")
        self.right_speaker_dropdown.current(0)
        self.right_speaker_dropdown.pack(fill=tk.X)

        self.right_record_button = tk.Button(
            right_controls, text="Record Your Speech", command=lambda: self.start_recording('right'))
        self.right_record_button.pack()

        self.right_stop_button = tk.Button(
            right_controls, text="Stop Recording", state=tk.DISABLED, command=lambda: self.stop_recording('right'))
        self.right_stop_button.pack(pady=(10, 0))

        # Bind language dropdown changes to update speakers
        self.left_language_dropdown.bind("<<ComboboxSelected>>", lambda event: self.update_speakers('left'))
        self.right_language_dropdown.bind("<<ComboboxSelected>>", lambda event: self.update_speakers('right'))

    def get_speakers_by_language(self, language):
        speakers = [speaker['display'] for speaker in AVAILABLE_SPEAKERS if speaker['language'] == language]
        if not speakers:
            return ["No speakers available"]
        return speakers

    def update_speakers(self, side):
        if side == 'left':
            language = self.left_language_var.get()
            speakers = self.get_speakers_by_language(language)
            self.left_speaker_dropdown['values'] = speakers
            self.left_speaker_dropdown.current(0)
        else:
            language = self.right_language_var.get()
            speakers = self.get_speakers_by_language(language)
            self.right_speaker_dropdown['values'] = speakers
            self.right_speaker_dropdown.current(0)

    def get_lang_code(self, language_name):
        return LANGUAGE_CODES.get(language_name, 'en')

    def start_recording(self, side):
        if side == 'left':
            language_var = self.left_language_var
            record_button = self.left_record_button
            stop_button = self.left_stop_button
            language_dropdown = self.left_language_dropdown
            speaker_dropdown = self.left_speaker_dropdown
        else:
            language_var = self.right_language_var
            record_button = self.right_record_button
            stop_button = self.right_stop_button
            language_dropdown = self.right_language_dropdown
            speaker_dropdown = self.right_speaker_dropdown

        language = language_var.get()

        # Check if the model for the selected language is available or needs downloading
        if language not in self.models:
            url = AVAILABLE_MODELS.get(language)
            if url:
                download_and_extract_model(language, url)
                model_path = os.path.join(MODEL_DIR, language)
                if os.path.exists(model_path):
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

        # Disable the record button and language dropdown, enable stop button
        record_button.config(text="Recording...", state=tk.DISABLED)
        language_dropdown.config(state=tk.DISABLED)
        speaker_dropdown.config(state=tk.DISABLED)
        stop_button.config(state=tk.NORMAL)

        # Store references
        if side == 'left':
            self.left_transcriber = transcriber
            self.left_record_button_ref = record_button
            self.left_stop_button_ref = stop_button
            self.left_language_dropdown_ref = language_dropdown
            self.left_speaker_dropdown_ref = speaker_dropdown
        else:
            self.right_transcriber = transcriber
            self.right_record_button_ref = record_button
            self.right_stop_button_ref = stop_button
            self.right_language_dropdown_ref = language_dropdown
            self.right_speaker_dropdown_ref = speaker_dropdown

    def stop_recording(self, side):
        if side == 'left':
            transcriber = self.left_transcriber
            record_button = self.left_record_button_ref
            stop_button = self.left_stop_button_ref
            language_dropdown = self.left_language_dropdown_ref
            speaker_dropdown = self.left_speaker_dropdown_ref
        else:
            transcriber = self.right_transcriber
            record_button = self.right_record_button_ref
            stop_button = self.right_stop_button_ref
            language_dropdown = self.right_language_dropdown_ref
            speaker_dropdown = self.right_speaker_dropdown_ref

        # Stop the recording process
        transcriber.stop_recording()

        # Re-enable the buttons and dropdowns
        record_button.config(text="Record Speech", state=tk.NORMAL)
        stop_button.config(state=tk.DISABLED)
        language_dropdown.config(state=tk.NORMAL)
        speaker_dropdown.config(state=tk.NORMAL)

    def record_and_transcribe(self, transcriber, side):
        # Start recording and transcribing
        transcriber.start_recording(
            lambda text, partial: self.root.after(0, self.update_conversation, side, text, partial))

    def update_conversation(self, side, text, partial):
        if side == 'left':
            source_lang_var = self.left_language_var
            target_lang_var = self.right_language_var
            record_button_ref = self.left_record_button_ref
            stop_button_ref = self.left_stop_button_ref
            language_dropdown_ref = self.left_language_dropdown_ref
            speaker_dropdown_ref = self.left_speaker_dropdown_ref
            transcriber = self.left_transcriber
            alignment = 'left'
            speaker_label = "Them"
        else:
            source_lang_var = self.right_language_var
            target_lang_var = self.left_language_var
            record_button_ref = self.right_record_button_ref
            stop_button_ref = self.right_stop_button_ref
            language_dropdown_ref = self.right_language_dropdown_ref
            speaker_dropdown_ref = self.right_speaker_dropdown_ref
            transcriber = self.right_transcriber
            alignment = 'right'
            speaker_label = "You"

        source_lang = source_lang_var.get()
        target_lang = target_lang_var.get()

        src_lang_code = self.get_lang_code(source_lang)
        dest_lang_code = self.get_lang_code(target_lang)

        if partial:
            # Update typing indicator (optional)
            pass  # Implement a typing indicator if desired
        else:
            # Display original text with speaker label
            self.conversation_text.insert(tk.END, f"{speaker_label}: ", ('bold', alignment))
            self.conversation_text.insert(tk.END, f"{text}\n", alignment)

            # Translate the text
            translated = self.translator_manager.translate_text(text, src_lang_code, dest_lang_code)

            # Display translated text with prefix "Translated: "
            self.conversation_text.insert(tk.END, f"Translated: {translated}\n", (alignment, 'italic'))

            # Add a blank line for spacing
            self.conversation_text.insert(tk.END, "\n")

            self.conversation_text.see(tk.END)

            # Reset recording buttons
            transcriber.stop_recording()
            record_button_ref.config(text=f"Record {speaker_label}'s Speech", state=tk.NORMAL)
            stop_button_ref.config(state=tk.DISABLED)
            language_dropdown_ref.config(state=tk.NORMAL)
            speaker_dropdown_ref.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = RealTimeTranslatorApp(root)
    root.mainloop()
