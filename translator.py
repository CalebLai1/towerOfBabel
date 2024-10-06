from deep_translator import GoogleTranslator

class TranslatorManager:
    def __init__(self):
        # No need to initialize the translator here since source and target languages are dynamic
        pass

    def translate_text(self, text, src_lang_code, dest_lang_code):
        try:
            # Ensure text is not empty
            if not text.strip():
                return ''

            # Initialize GoogleTranslator with dynamic source and target languages
            translator = GoogleTranslator(source=src_lang_code, target=dest_lang_code)
            
            # Perform the translation
            translated_text = translator.translate(text)
            return translated_text

        except Exception as e:
            return f"Translation Error: {e}"

