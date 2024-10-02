import os
import urllib.request
import zipfile
import shutil

# Directory to store models
MODEL_DIR = "vosk_models"

# Ensure the model directory exists
if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)

AVAILABLE_MODELS = {
    'English': 'https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip',
    'Chinese': 'https://alphacephei.com/vosk/models/vosk-model-small-cn-0.22.zip',
    'Dutch': 'https://alphacephei.com/vosk/models/vosk-model-small-nl-0.22.zip',
    'French': 'https://alphacephei.com/vosk/models/vosk-model-small-fr-0.22.zip',
    'German': 'https://alphacephei.com/vosk/models/vosk-model-small-de-0.15.zip',
    'Italian': 'https://alphacephei.com/vosk/models/vosk-model-small-it-0.22.zip',
    'Spanish': 'https://alphacephei.com/vosk/models/vosk-model-small-es-0.42.zip',
    'Russian': 'https://alphacephei.com/vosk/models/vosk-model-small-ru-0.22.zip',
    'Portuguese': 'https://alphacephei.com/vosk/models/vosk-model-small-pt-0.3.zip',
    'Turkish': 'https://alphacephei.com/vosk/models/vosk-model-small-tr-0.3.zip',
    'Japanese': 'https://alphacephei.com/vosk/models/vosk-model-small-ja-0.22.zip',
    'Korean': 'https://alphacephei.com/vosk/models/vosk-model-small-ko-0.22.zip',
    'Arabic': 'https://alphacephei.com/vosk/models/vosk-model-ar-mgb2-0.4.zip',
    'Arabic Tunisian': 'https://alphacephei.com/vosk/models/vosk-model-ar-tn-0.1-linto.zip',
    'Farsi': 'https://alphacephei.com/vosk/models/vosk-model-fa-0.5.zip',
    'Filipino': 'https://alphacephei.com/vosk/models/vosk-model-tl-ph-generic-0.6.zip',
    'Ukrainian': 'https://alphacephei.com/vosk/models/vosk-model-uk-v3.zip',
    'Kazakh': 'https://alphacephei.com/vosk/models/vosk-model-kz-0.15.zip',
    'Swedish': 'https://alphacephei.com/vosk/models/vosk-model-small-sv-rhasspy-0.15.zip',
    'Esperanto': 'https://alphacephei.com/vosk/models/vosk-model-small-eo-0.42.zip',
    'Hindi': 'https://alphacephei.com/vosk/models/vosk-model-hi-0.22.zip',
    'Czech': 'https://alphacephei.com/vosk/models/vosk-model-small-cs-0.4-rhasspy.zip',
    'Polish': 'https://alphacephei.com/vosk/models/vosk-model-small-pl-0.22.zip',
    'Uzbek': 'https://alphacephei.com/vosk/models/vosk-model-small-uz-0.22.zip',
    'Breton': 'https://alphacephei.com/vosk/models/vosk-model-br-0.8.zip',
    'Gujarati': 'https://alphacephei.com/vosk/models/vosk-model-gu-0.42.zip',
    'Tajik': 'https://alphacephei.com/vosk/models/vosk-model-tg-0.22.zip',
    'Speaker Identification': 'https://alphacephei.com/vosk/models/vosk-model-spk-0.4.zip',
}


def download_and_extract_model(language, url):
    model_path = os.path.join(MODEL_DIR, language)
    if not os.path.exists(model_path):
        print(f"Downloading and extracting model for {language}...")
        zip_path = os.path.join(MODEL_DIR, f"{language}.zip")
        try:
            urllib.request.urlretrieve(url, zip_path)
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(model_path)
            os.remove(zip_path)
            print(f"Model for {language} downloaded and extracted successfully.")
        except Exception as e:
            print(f"Error downloading model for {language}: {e}")
            if os.path.exists(zip_path):
                os.remove(zip_path)
    else:
        print(f"Model for {language} already exists.")

def download_all_models():
    for lang, url in AVAILABLE_MODELS.items():
        download_and_extract_model(lang, url)
