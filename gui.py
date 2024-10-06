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

# Mapping of language names to their respective codes
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
        self.models = {}  # To store loaded Vosk models
        self.translator_manager = TranslatorManager()  # Initialize the translator manager
        self.create_widgets()  # Setup the GUI components

    def create_widgets(self):
        """
        Create and layout all the widgets in the GUI.
        """
        # Main frame for the conversation with a scrollbar
        conversation_frame = tk.Frame(self.root)
        conversation_frame.pack(fill=tk.BOTH, expand=True)

        # Create a canvas and a vertical scrollbar for it
        canvas = tk.Canvas(conversation_frame, borderwidth=0)
        scrollbar = ttk.Scrollbar(conversation_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas)

        # Configure the scrollable frame
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        # Add the scrollable frame to the canvas
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack the canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bottom frame for controls
        controls_frame = tk.Frame(self.root)
        controls_frame.pack(fill=tk.X)

        # Left side controls (Their Language and Recording)
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

        # Right side controls (Your Language and Recording)
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

        # Bind language dropdown changes to model updates
        self.left_language_dropdown.bind("<<ComboboxSelected>>", lambda event: self.update_model('left'))
        self.right_language_dropdown.bind("<<ComboboxSelected>>", lambda event: self.update_model('right'))

    def update_model(self, side):
        """
        Update the Vosk model for the selected language side ('left' or 'right').
        Downloads and loads the model if not already loaded.
        """
        language = self.get_language(side)
        print(f"[DEBUG] Updating model for {side} side with language: {language}")
        if language not in self.models:
            url = AVAILABLE_MODELS.get(language)
            if url:
                print(f"[DEBUG] Downloading model for language: {language} from {url}")
                download_and_extract_model(language, url)
                model_path = Path(MODEL_DIR) / language
                if model_path.exists():
                    # Find the first directory inside the model path
                    for item in model_path.iterdir():
                        if item.is_dir():
                            self.models[language] = Model(str(item))
                            print(f"[DEBUG] Loaded model from: {item}")
                            break
                    else:
                        messagebox.showerror("Error", f"Model for {language} not found.")
                        print(f"[ERROR] Model directory for {language} not found.")
                        return
                else:
                    messagebox.showerror("Error", f"Failed to download model for {language}.")
                    print(f"[ERROR] Model path does not exist: {model_path}")
                    return
            else:
                messagebox.showerror("Error", f"No model URL found for {language}")
                print(f"[ERROR] No model URL found for language: {language}")
                return

    def get_lang_code(self, language_name):
        """
        Retrieve the language code based on the language name.
        Defaults to 'en' if not found.
        """
        return LANGUAGE_CODES.get(language_name, 'en')

    def get_language(self, side):
        """
        Get the selected language for the specified side ('left' or 'right').
        """
        if side == 'left':
            return self.left_language_var.get()
        else:
            return self.right_language_var.get()

    def start_recording(self, side):
        """
        Initiate the recording and transcription process for the specified side.
        """
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
        print(f"[DEBUG] Starting recording for {side} side with language: {language}")

        # Check if the model is available; if not, update/load it
        if language not in self.models:
            self.update_model(side)
            if language not in self.models:
                print(f"[ERROR] Model for language '{language}' could not be loaded.")
                return

        # Create a new transcriber for this recording
        transcriber = Transcriber(self.models[language])

        # Start recording in a separate thread
        threading.Thread(target=self.record_and_transcribe, args=(transcriber, side), daemon=True).start()

        # Update UI elements
        record_button.config(text="Recording...", state=tk.DISABLED)
        language_dropdown.config(state=tk.DISABLED)
        stop_button.config(state=tk.NORMAL)

        # Store references for later use
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
        """
        Stop the recording and transcription process for the specified side.
        """
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

        print(f"[DEBUG] Stopping recording for {side} side.")
        # Stop the recording process
        transcriber.stop_recording()

        # Update UI elements
        record_button.config(text="Record Speech", state=tk.NORMAL)
        stop_button.config(state=tk.DISABLED)
        language_dropdown.config(state=tk.NORMAL)

    def record_and_transcribe(self, transcriber, side):
        """
        Handle the recording and transcription process.
        """
        transcriber.start_recording(
            lambda text, partial: self.root.after(0, self.update_conversation, side, text, partial)
        )

    def update_conversation(self, side, text, partial):
        """
        Update the conversation frame with the transcribed and translated text.
        """
        if side == 'left':
            source_lang_var = self.left_language_var
            target_lang_var = self.right_language_var
            transcriber = self.left_transcriber
            speaker_label = "Them"
            available_speakers = [s for s in AVAILABLE_SPEAKERS if s['language'].lower() == self.right_language_var.get().lower()]
        else:
            source_lang_var = self.right_language_var
            target_lang_var = self.left_language_var
            transcriber = self.right_transcriber
            speaker_label = "You"
            available_speakers = [s for s in AVAILABLE_SPEAKERS if s['language'].lower() == self.left_language_var.get().lower()]

        source_lang = source_lang_var.get()
        target_lang = target_lang_var.get()

        src_lang_code = self.get_lang_code(source_lang)
        dest_lang_code = self.get_lang_code(target_lang)

        if partial:
            # Optionally implement a typing indicator or real-time display
            pass
        else:
            print(f"[DEBUG] Received transcribed text: {text} for {side} side.")

            # Display original text with speaker label
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

            # Translate the text
            translated = self.translator_manager.translate_text(text, src_lang_code, dest_lang_code)
            print(f"[DEBUG] Translated text: {translated}")

            # Display translated text with "Translated:" prefix
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

            # Create a frame for the buttons
            button_frame = tk.Frame(self.scrollable_frame, pady=5)
            button_frame.pack(fill=tk.X, anchor='w' if side == 'left' else 'e', padx=10)

            # Create the "Generate Bark Audio" button
            generate_button = tk.Button(
                button_frame,
                text="Generate Bark Audio",
                command=lambda: self.generate_audio_with_speaker(translated, dest_lang_code, available_speakers, play_button)
            )
            generate_button.pack(side=tk.LEFT, padx=(0, 5))

            # Create the "Play Audio" button, initially disabled
            play_button = tk.Button(
                button_frame,
                text="Play Audio",
                state=tk.DISABLED,
                command=lambda: self.play_audio(play_button.filepath) if hasattr(play_button, 'filepath') else None
            )
            play_button.pack(side=tk.LEFT)

            # Add a blank line for spacing
            spacer = tk.Frame(self.scrollable_frame, height=10)
            spacer.pack()

            self.scrollable_frame.update_idletasks()
            self.root.update_idletasks()

            # Scroll to the bottom
            self.scrollable_frame.master.yview_moveto(1.0)

            # Reset recording buttons
            transcriber.stop_recording()
            if side == 'left':
                self.left_record_button_ref.config(text=f"Record {speaker_label}'s Speech", state=tk.NORMAL)
                self.left_stop_button_ref.config(state=tk.DISABLED)
                self.left_language_dropdown_ref.config(state=tk.NORMAL)
            else:
                self.right_record_button_ref.config(text=f"Record {speaker_label}'s Speech", state=tk.NORMAL)
                self.right_stop_button_ref.config(state=tk.DISABLED)
                self.right_language_dropdown_ref.config(state=tk.NORMAL)

    def generate_audio_with_speaker(self, text, dest_lang_code, available_speakers, play_button):
        """
        Handle the generation of audio and enable the Play Audio button upon success.
        """
        if not available_speakers:
            messagebox.showerror("Error", "No available speakers for the selected language.")
            print("[ERROR] No available speakers for the selected language.")
            return

        # For this example, we'll take the first available speaker
        selected_speaker = available_speakers[0]
        print(f"[DEBUG] Selected speaker ID: {selected_speaker['id']}")
        # Start the audio generation in a separate thread, passing the play_button reference
        self.generate_audio_thread(text, dest_lang_code, selected_speaker['id'], play_button)

    def generate_audio_thread(self, text, dest_lang_code, speaker_id, play_button):
        """
        Start a new thread to generate audio to prevent blocking the GUI.
        """
        threading.Thread(target=self.generate_audio, args=(text, dest_lang_code, speaker_id, play_button), daemon=True).start()

    def generate_audio(self, text, dest_lang_code, speaker_id, play_button):
        """
        Generate Bark audio using the provided text, language code, and speaker ID.
        """
        print(f"[DEBUG] Generating audio with speaker_id: {speaker_id}, language code: {dest_lang_code}, text: {text}")
        filepath = generate_bark_audio(text, dest_lang_code, speaker_id)
        # Handle path correctly using pathlib
        filepath = Path(filepath).resolve()
        if filepath.exists():
            print(f"[DEBUG] Audio successfully saved to {filepath}")
            # Update the Play Audio button in the main thread
            self.root.after(0, lambda: self.enable_play_button(play_button, filepath))
            self.root.after(0, lambda: messagebox.showinfo("Success", f"Audio saved to {filepath}"))
        else:
            print("[ERROR] Failed to generate audio.")
            self.root.after(0, lambda: messagebox.showerror("Error", "Failed to generate audio."))

    def enable_play_button(self, play_button, filepath):
        """
        Enable the Play Audio button and store the filepath.
        """
        play_button.config(state=tk.NORMAL)
        play_button.filepath = str(filepath)  # Convert Path to string
        print(f"[DEBUG] Play Audio button enabled with filepath: {filepath}")

    def play_audio(self, filepath):
        """
        Play the generated audio file.
        """
        filepath = Path(filepath)
        if not filepath.exists():
            messagebox.showerror("Error", "Audio file not found.")
            print("[ERROR] Audio file not found.")
            return

        print(f"[DEBUG] Playing audio from: {filepath}")
        try:
            # Ensure the path uses forward slashes or is an absolute path
            playsound(str(filepath))
            print("[DEBUG] Audio playback completed.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to play audio: {e}")
            print(f"[ERROR] Failed to play audio: {e}")

if __name__ == "__main__":
    # Initialize the main Tkinter window
    root = tk.Tk()
    app = RealTimeTranslatorApp(root)
    root.geometry("800x600")  # Set a default window size
    root.mainloop()
