import torch
from vosk import Model, KaldiRecognizer
import json
import os
import requests
import zipfile

class SharedFunctions:
    def __init__(self, base_model_path=None):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Initializing on {self.device}")
        
        if base_model_path is None:
            base_model_path = os.path.join(os.path.dirname(__file__), "vosk_models")
        self.base_model_path = base_model_path
        os.makedirs(self.base_model_path, exist_ok=True)
        
        self.model = None
        self.current_lang = None

    def ensure_model(self, lang="en-us"):
        model_path = os.path.join(self.base_model_path, f"vosk-model-small-{lang}")
        if not os.path.exists(model_path):
            self.download_model(lang)
        
        if self.current_lang != lang:
            self.model = Model(model_path)
            self.current_lang = lang

    def download_model(self, lang):
        model_url = f"https://alphacephei.com/vosk/models/vosk-model-small-{lang}.zip"
        model_path = os.path.join(self.base_model_path, f"vosk-model-small-{lang}")
        zip_path = os.path.join(self.base_model_path, f"vosk-model-small-{lang}.zip")
        
        print(f"Downloading model for {lang}...")
        response = requests.get(model_url)
        with open(zip_path, 'wb') as f:
            f.write(response.content)
        
        print("Extracting model...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(self.base_model_path)
        
        os.remove(zip_path)
        print("Model downloaded and extracted successfully.")

    def transcribe_audio(self, audio_data, lang="en-us"):
        self.ensure_model(lang)
        recognizer = KaldiRecognizer(self.model, 16000)
        recognizer.SetWords(True)
        if recognizer.AcceptWaveform(audio_data):
            result = json.loads(recognizer.Result())
            return result['text']
        return None

    def get_device_info(self):
        if self.device == "cuda":
            return f"GPU: {torch.cuda.get_device_name(0)}"
        else:
            return "CPU"

    @staticmethod
    def get_language_dict():
        return {
            'en-us': 'English',
            'es-es': 'Spanish',
            'fr-fr': 'French',
            'de-de': 'German',
            'it-it': 'Italian',
            'ja-jp': 'Japanese',
            'ko-kr': 'Korean',
            'zh-cn': 'Chinese (Simplified)',
            'ru-ru': 'Russian',
            'ar-eg': 'Arabic'
        }

    @staticmethod
    def get_language_code(language_name):
        lang_dict = SharedFunctions.get_language_dict()
        return next((code for code, name in lang_dict.items() if name == language_name), None)