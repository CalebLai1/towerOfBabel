from deep_translator import GoogleTranslator

class TranslatorManager:

    def translate_text(self, text, src_lang_code, dest_lang_code):
        try:
            if not text.strip():
                return ''

            translator = GoogleTranslator(source=src_lang_code, target=dest_lang_code)
            
            translated_text = translator.translate(text)
            return translated_text

        except Exception as e:
            return f"Translation Error: {e}"

