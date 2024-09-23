from faster_whisper import WhisperModel
from googletrans import Translator

class SharedFunctions:
    def __init__(self, model_size="small"):
        self.whisper_model = WhisperModel(model_size, device="cpu", compute_type="int8")
        self.translator = Translator()

    def transcribe_audio(self, audio_path):
        segments, info = self.whisper_model.transcribe(audio_path, beam_size=5)
        transcription = " ".join([segment.text for segment in segments])
        detected_language = info.language
        return transcription, detected_language

    def translate_text(self, text, src_lang, dest_lang):
        if src_lang == dest_lang:
            return text
        translated = self.translator.translate(text, src=src_lang, dest=dest_lang)
        return translated.text

    @staticmethod
    def get_language_dict():
        return {
            'en': 'English',
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German',
            'it': 'Italian',
            'ja': 'Japanese',
            'ko': 'Korean',
            'zh-cn': 'Chinese (Simplified)',
            'ru': 'Russian',
            'ar': 'Arabic'
        }

    @staticmethod
    def get_language_code(language_name):
        lang_dict = SharedFunctions.get_language_dict()
        return next((code for code, name in lang_dict.items() if name == language_name), None)
