from googletrans import Translator

class TranslatorManager:
    def __init__(self):
        self.translator = Translator(service_urls=[
            'translate.google.com',
            'translate.google.co.kr',
        ])

    def translate_text(self, text, src_lang_code, dest_lang_code):
        try:
            # Ensure text is not empty
            if not text.strip():
                return ''
            # Perform translation
            translated = self.translator.translate(
                text, src=src_lang_code, dest=dest_lang_code)
            return translated.text
        except Exception as e:
            return f"Translation Error: {e}"
