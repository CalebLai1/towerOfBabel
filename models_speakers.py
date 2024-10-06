# models_speakers.py

# Define available models
AVAILABLE_MODELS = {
    'English': 'en',
    'Chinese': 'zh-cn',
    'French': 'fr',
    'German': 'de',
    'Hindi': 'hi',
    'Italian': 'it',
    'Japanese': 'ja',
    'Korean': 'ko',
    'Polish': 'pl',
    'Portuguese': 'pt',
    'Russian': 'ru',
    'Spanish': 'es',
    'Turkish': 'tr',
    # Add other languages as needed
}

# Define comprehensive speakers list
# Replace the list below with your complete speakers data
# Define comprehensive speakers list
AVAILABLE_SPEAKERS = [
    # English Speakers
    {"id": "v2/en_speaker_0", "display": "Speaker 0 (EN) - English - Male", "language": "English", "gender": "Male"},
    {"id": "v2/en_speaker_1", "display": "Speaker 1 (EN) - English - Male", "language": "English", "gender": "Male"},
    {"id": "v2/en_speaker_2", "display": "Speaker 2 (EN) - English - Male", "language": "English", "gender": "Male"},
    {"id": "v2/en_speaker_3", "display": "Speaker 3 (EN) - English - Male", "language": "English", "gender": "Male"},
    {"id": "v2/en_speaker_4", "display": "Speaker 4 (EN) - English - Male", "language": "English", "gender": "Male"},
    {"id": "v2/en_speaker_5", "display": "Speaker 5 (EN) - English - Male (Grainy)", "language": "English", "gender": "Male", "tags": ["Grainy"]},
    {"id": "v2/en_speaker_6", "display": "Speaker 6 (EN) - English - Male (Suno Favorite)", "language": "English", "gender": "Male", "tags": ["Suno Favorite"]},
    {"id": "v2/en_speaker_7", "display": "Speaker 7 (EN) - English - Male", "language": "English", "gender": "Male"},
    {"id": "v2/en_speaker_8", "display": "Speaker 8 (EN) - English - Male", "language": "English", "gender": "Male"},
    {"id": "v2/en_speaker_9", "display": "Speaker 9 (EN) - English - Female", "language": "English", "gender": "Female"},
    
    # Chinese Speakers
    {"id": "v2/zh_speaker_0", "display": "Speaker 0 (ZH) - Chinese (Simplified) - Male", "language": "Chinese (Simplified)", "gender": "Male"},
    {"id": "v2/zh_speaker_1", "display": "Speaker 1 (ZH) - Chinese (Simplified) - Male", "language": "Chinese (Simplified)", "gender": "Male"},
    {"id": "v2/zh_speaker_2", "display": "Speaker 2 (ZH) - Chinese (Simplified) - Male", "language": "Chinese (Simplified)", "gender": "Male"},
    {"id": "v2/zh_speaker_3", "display": "Speaker 3 (ZH) - Chinese (Simplified) - Male", "language": "Chinese (Simplified)", "gender": "Male"},
    {"id": "v2/zh_speaker_4", "display": "Speaker 4 (ZH) - Chinese (Simplified) - Female", "language": "Chinese (Simplified)", "gender": "Female"},
    {"id": "v2/zh_speaker_5", "display": "Speaker 5 (ZH) - Chinese (Simplified) - Male", "language": "Chinese (Simplified)", "gender": "Male"},
    {"id": "v2/zh_speaker_6", "display": "Speaker 6 (ZH) - Chinese (Simplified) - Female (Background Noise)", "language": "Chinese (Simplified)", "gender": "Female", "tags": ["Background Noise"]},
    {"id": "v2/zh_speaker_7", "display": "Speaker 7 (ZH) - Chinese (Simplified) - Female", "language": "Chinese (Simplified)", "gender": "Female"},
    {"id": "v2/zh_speaker_8", "display": "Speaker 8 (ZH) - Chinese (Simplified) - Male", "language": "Chinese (Simplified)", "gender": "Male"},
    {"id": "v2/zh_speaker_9", "display": "Speaker 9 (ZH) - Chinese (Simplified) - Female", "language": "Chinese (Simplified)", "gender": "Female"},
    
    # French Speakers
    {"id": "v2/fr_speaker_0", "display": "Speaker 0 (FR) - French - Male", "language": "French", "gender": "Male"},
    {"id": "v2/fr_speaker_1", "display": "Speaker 1 (FR) - French - Female", "language": "French", "gender": "Female"},
    {"id": "v2/fr_speaker_2", "display": "Speaker 2 (FR) - French - Female", "language": "French", "gender": "Female"},
    {"id": "v2/fr_speaker_3", "display": "Speaker 3 (FR) - French - Male", "language": "French", "gender": "Male"},
    {"id": "v2/fr_speaker_4", "display": "Speaker 4 (FR) - French - Male", "language": "French", "gender": "Male"},
    {"id": "v2/fr_speaker_5", "display": "Speaker 5 (FR) - French - Female", "language": "French", "gender": "Female"},
    {"id": "v2/fr_speaker_6", "display": "Speaker 6 (FR) - French - Male", "language": "French", "gender": "Male"},
    {"id": "v2/fr_speaker_7", "display": "Speaker 7 (FR) - French - Male", "language": "French", "gender": "Male"},
    {"id": "v2/fr_speaker_8", "display": "Speaker 8 (FR) - French - Male", "language": "French", "gender": "Male"},
    {"id": "v2/fr_speaker_9", "display": "Speaker 9 (FR) - French - Male (Auditorium)", "language": "French", "gender": "Male", "tags": ["Auditorium"]},
    
    # German Speakers
    {"id": "v2/de_speaker_0", "display": "Speaker 0 (DE) - German - Male", "language": "German", "gender": "Male"},
    {"id": "v2/de_speaker_1", "display": "Speaker 1 (DE) - German - Male", "language": "German", "gender": "Male"},
    {"id": "v2/de_speaker_2", "display": "Speaker 2 (DE) - German - Male", "language": "German", "gender": "Male"},
    {"id": "v2/de_speaker_3", "display": "Speaker 3 (DE) - German - Female", "language": "German", "gender": "Female"},
    {"id": "v2/de_speaker_4", "display": "Speaker 4 (DE) - German - Male", "language": "German", "gender": "Male"},
    {"id": "v2/de_speaker_5", "display": "Speaker 5 (DE) - German - Male", "language": "German", "gender": "Male"},
    {"id": "v2/de_speaker_6", "display": "Speaker 6 (DE) - German - Male", "language": "German", "gender": "Male"},
    {"id": "v2/de_speaker_7", "display": "Speaker 7 (DE) - German - Male", "language": "German", "gender": "Male"},
    {"id": "v2/de_speaker_8", "display": "Speaker 8 (DE) - German - Female", "language": "German", "gender": "Female"},
    {"id": "v2/de_speaker_9", "display": "Speaker 9 (DE) - German - Male", "language": "German", "gender": "Male"},
    
    # Hindi Speakers
    {"id": "v2/hi_speaker_0", "display": "Speaker 0 (HI) - Hindi - Female", "language": "Hindi", "gender": "Female"},
    {"id": "v2/hi_speaker_1", "display": "Speaker 1 (HI) - Hindi - Female (Background Noise)", "language": "Hindi", "gender": "Female", "tags": ["Background Noise"]},
    {"id": "v2/hi_speaker_2", "display": "Speaker 2 (HI) - Hindi - Male", "language": "Hindi", "gender": "Male"},
    {"id": "v2/hi_speaker_3", "display": "Speaker 3 (HI) - Hindi - Female", "language": "Hindi", "gender": "Female"},
    {"id": "v2/hi_speaker_4", "display": "Speaker 4 (HI) - Hindi - Female (Background Noise)", "language": "Hindi", "gender": "Female", "tags": ["Background Noise"]},
    {"id": "v2/hi_speaker_5", "display": "Speaker 5 (HI) - Hindi - Male", "language": "Hindi", "gender": "Male"},
    {"id": "v2/hi_speaker_6", "display": "Speaker 6 (HI) - Hindi - Male", "language": "Hindi", "gender": "Male"},
    {"id": "v2/hi_speaker_7", "display": "Speaker 7 (HI) - Hindi - Male", "language": "Hindi", "gender": "Male"},
    {"id": "v2/hi_speaker_8", "display": "Speaker 8 (HI) - Hindi - Male", "language": "Hindi", "gender": "Male"},
    {"id": "v2/hi_speaker_9", "display": "Speaker 9 (HI) - Hindi - Female", "language": "Hindi", "gender": "Female"},
    
    # Italian Speakers
    {"id": "v2/it_speaker_0", "display": "Speaker 0 (IT) - Italian - Male", "language": "Italian", "gender": "Male"},
    {"id": "v2/it_speaker_1", "display": "Speaker 1 (IT) - Italian - Male", "language": "Italian", "gender": "Male"},
    {"id": "v2/it_speaker_2", "display": "Speaker 2 (IT) - Italian - Female", "language": "Italian", "gender": "Female"},
    {"id": "v2/it_speaker_3", "display": "Speaker 3 (IT) - Italian - Male", "language": "Italian", "gender": "Male"},
    {"id": "v2/it_speaker_4", "display": "Speaker 4 (IT) - Italian - Male (Suno Favorite)", "language": "Italian", "gender": "Male", "tags": ["Suno Favorite"]},
    {"id": "v2/it_speaker_5", "display": "Speaker 5 (IT) - Italian - Male", "language": "Italian", "gender": "Male"},
    {"id": "v2/it_speaker_6", "display": "Speaker 6 (IT) - Italian - Male", "language": "Italian", "gender": "Male"},
    {"id": "v2/it_speaker_7", "display": "Speaker 7 (IT) - Italian - Female", "language": "Italian", "gender": "Female"},
    {"id": "v2/it_speaker_8", "display": "Speaker 8 (IT) - Italian - Male", "language": "Italian", "gender": "Male"},
    {"id": "v2/it_speaker_9", "display": "Speaker 9 (IT) - Italian - Female", "language": "Italian", "gender": "Female"},
    
    # Japanese Speakers
    {"id": "v2/ja_speaker_0", "display": "Speaker 0 (JA) - Japanese - Female", "language": "Japanese", "gender": "Female"},
    {"id": "v2/ja_speaker_1", "display": "Speaker 1 (JA) - Japanese - Female (Background Noise)", "language": "Japanese", "gender": "Female", "tags": ["Background Noise"]},
    {"id": "v2/ja_speaker_2", "display": "Speaker 2 (JA) - Japanese - Male", "language": "Japanese", "gender": "Male"},
    {"id": "v2/ja_speaker_3", "display": "Speaker 3 (JA) - Japanese - Female", "language": "Japanese", "gender": "Female"},
    {"id": "v2/ja_speaker_4", "display": "Speaker 4 (JA) - Japanese - Female", "language": "Japanese", "gender": "Female"},
    {"id": "v2/ja_speaker_5", "display": "Speaker 5 (JA) - Japanese - Female", "language": "Japanese", "gender": "Female"},
    {"id": "v2/ja_speaker_6", "display": "Speaker 6 (JA) - Japanese - Male", "language": "Japanese", "gender": "Male"},
    {"id": "v2/ja_speaker_7", "display": "Speaker 7 (JA) - Japanese - Female", "language": "Japanese", "gender": "Female"},
    {"id": "v2/ja_speaker_8", "display": "Speaker 8 (JA) - Japanese - Female", "language": "Japanese", "gender": "Female"},
    {"id": "v2/ja_speaker_9", "display": "Speaker 9 (JA) - Japanese - Female", "language": "Japanese", "gender": "Female"},
    
    # Korean Speakers
    {"id": "v2/ko_speaker_0", "display": "Speaker 0 (KO) - Korean - Female", "language": "Korean", "gender": "Female"},
    {"id": "v2/ko_speaker_1", "display": "Speaker 1 (KO) - Korean - Male", "language": "Korean", "gender": "Male"},
    {"id": "v2/ko_speaker_2", "display": "Speaker 2 (KO) - Korean - Male", "language": "Korean", "gender": "Male"},
    {"id": "v2/ko_speaker_3", "display": "Speaker 3 (KO) - Korean - Male", "language": "Korean", "gender": "Male"},
    {"id": "v2/ko_speaker_4", "display": "Speaker 4 (KO) - Korean - Male", "language": "Korean", "gender": "Male"},
    {"id": "v2/ko_speaker_5", "display": "Speaker 5 (KO) - Korean - Male", "language": "Korean", "gender": "Male"},
    {"id": "v2/ko_speaker_6", "display": "Speaker 6 (KO) - Korean - Male", "language": "Korean", "gender": "Male"},
    {"id": "v2/ko_speaker_7", "display": "Speaker 7 (KO) - Korean - Male", "language": "Korean", "gender": "Male"},
    {"id": "v2/ko_speaker_8", "display": "Speaker 8 (KO) - Korean - Male", "language": "Korean", "gender": "Male"},
    {"id": "v2/ko_speaker_9", "display": "Speaker 9 (KO) - Korean - Male", "language": "Korean", "gender": "Male"},
    
    # Polish Speakers
    {"id": "v2/pl_speaker_0", "display": "Speaker 0 (PL) - Polish - Male", "language": "Polish", "gender": "Male"},
    {"id": "v2/pl_speaker_1", "display": "Speaker 1 (PL) - Polish - Male", "language": "Polish", "gender": "Male"},
    {"id": "v2/pl_speaker_2", "display": "Speaker 2 (PL) - Polish - Male", "language": "Polish", "gender": "Male"},
    {"id": "v2/pl_speaker_3", "display": "Speaker 3 (PL) - Polish - Male", "language": "Polish", "gender": "Male"},
    {"id": "v2/pl_speaker_4", "display": "Speaker 4 (PL) - Polish - Female", "language": "Polish", "gender": "Female"},
    {"id": "v2/pl_speaker_5", "display": "Speaker 5 (PL) - Polish - Male", "language": "Polish", "gender": "Male"},
    {"id": "v2/pl_speaker_6", "display": "Speaker 6 (PL) - Polish - Female", "language": "Polish", "gender": "Female"},
    {"id": "v2/pl_speaker_7", "display": "Speaker 7 (PL) - Polish - Male", "language": "Polish", "gender": "Male"},
    {"id": "v2/pl_speaker_8", "display": "Speaker 8 (PL) - Polish - Male", "language": "Polish", "gender": "Male"},
    {"id": "v2/pl_speaker_9", "display": "Speaker 9 (PL) - Polish - Female", "language": "Polish", "gender": "Female"},
    
    # Portuguese Speakers
    {"id": "v2/pt_speaker_0", "display": "Speaker 0 (PT) - Portuguese - Male", "language": "Portuguese", "gender": "Male"},
    {"id": "v2/pt_speaker_1", "display": "Speaker 1 (PT) - Portuguese - Male", "language": "Portuguese", "gender": "Male"},
    {"id": "v2/pt_speaker_2", "display": "Speaker 2 (PT) - Portuguese - Male", "language": "Portuguese", "gender": "Male"},
    {"id": "v2/pt_speaker_3", "display": "Speaker 3 (PT) - Portuguese - Male", "language": "Portuguese", "gender": "Male"},
    {"id": "v2/pt_speaker_4", "display": "Speaker 4 (PT) - Portuguese - Male", "language": "Portuguese", "gender": "Male"},
    {"id": "v2/pt_speaker_5", "display": "Speaker 5 (PT) - Portuguese - Male", "language": "Portuguese", "gender": "Male"},
    {"id": "v2/pt_speaker_6", "display": "Speaker 6 (PT) - Portuguese - Male (Background Noise)", "language": "Portuguese", "gender": "Male", "tags": ["Background Noise"]},
    {"id": "v2/pt_speaker_7", "display": "Speaker 7 (PT) - Portuguese - Male", "language": "Portuguese", "gender": "Male"},
    {"id": "v2/pt_speaker_8", "display": "Speaker 8 (PT) - Portuguese - Male", "language": "Portuguese", "gender": "Male"},
    {"id": "v2/pt_speaker_9", "display": "Speaker 9 (PT) - Portuguese - Male", "language": "Portuguese", "gender": "Male"},
    
    # Russian Speakers
    {"id": "v2/ru_speaker_0", "display": "Speaker 0 (RU) - Russian - Male", "language": "Russian", "gender": "Male"},
    {"id": "v2/ru_speaker_1", "display": "Speaker 1 (RU) - Russian - Male (Echoes)", "language": "Russian", "gender": "Male", "tags": ["Echoes"]},
    {"id": "v2/ru_speaker_2", "display": "Speaker 2 (RU) - Russian - Male (Echoes)", "language": "Russian", "gender": "Male", "tags": ["Echoes"]},
    {"id": "v2/ru_speaker_3", "display": "Speaker 3 (RU) - Russian - Male", "language": "Russian", "gender": "Male"},
    {"id": "v2/ru_speaker_4", "display": "Speaker 4 (RU) - Russian - Male", "language": "Russian", "gender": "Male"},
    {"id": "v2/ru_speaker_5", "display": "Speaker 5 (RU) - Russian - Female", "language": "Russian", "gender": "Female"},
    {"id": "v2/ru_speaker_6", "display": "Speaker 6 (RU) - Russian - Female (Grainy)", "language": "Russian", "gender": "Female", "tags": ["Grainy"]},
    {"id": "v2/ru_speaker_7", "display": "Speaker 7 (RU) - Russian - Male", "language": "Russian", "gender": "Male"},
    {"id": "v2/ru_speaker_8", "display": "Speaker 8 (RU) - Russian - Male (Grainy)", "language": "Russian", "gender": "Male", "tags": ["Grainy"]},
    {"id": "v2/ru_speaker_9", "display": "Speaker 9 (RU) - Russian - Female (Grainy)", "language": "Russian", "gender": "Female", "tags": ["Grainy"]},
    
    # Spanish Speakers
    {"id": "v2/es_speaker_0", "display": "Speaker 0 (ES) - Spanish - Male", "language": "Spanish", "gender": "Male"},
    {"id": "v2/es_speaker_1", "display": "Speaker 1 (ES) - Spanish - Male", "language": "Spanish", "gender": "Male"},
    {"id": "v2/es_speaker_2", "display": "Speaker 2 (ES) - Spanish - Male (Background Noise)", "language": "Spanish", "gender": "Male", "tags": ["Background Noise"]},
    {"id": "v2/es_speaker_3", "display": "Speaker 3 (ES) - Spanish - Male (Background Noise)", "language": "Spanish", "gender": "Male", "tags": ["Background Noise"]},
    {"id": "v2/es_speaker_4", "display": "Speaker 4 (ES) - Spanish - Male", "language": "Spanish", "gender": "Male"},
    {"id": "v2/es_speaker_5", "display": "Speaker 5 (ES) - Spanish - Male (Background Noise)", "language": "Spanish", "gender": "Male", "tags": ["Background Noise"]},
    {"id": "v2/es_speaker_6", "display": "Speaker 6 (ES) - Spanish - Male", "language": "Spanish", "gender": "Male"},
    {"id": "v2/es_speaker_7", "display": "Speaker 7 (ES) - Spanish - Male", "language": "Spanish", "gender": "Male"},
    {"id": "v2/es_speaker_8", "display": "Speaker 8 (ES) - Spanish - Female", "language": "Spanish", "gender": "Female"},
    {"id": "v2/es_speaker_9", "display": "Speaker 9 (ES) - Spanish - Female", "language": "Spanish", "gender": "Female"},
    
    # Turkish Speakers
    {"id": "v2/tr_speaker_0", "display": "Speaker 0 (TR) - Turkish - Male", "language": "Turkish", "gender": "Male"},
    {"id": "v2/tr_speaker_1", "display": "Speaker 1 (TR) - Turkish - Male", "language": "Turkish", "gender": "Male"},
    {"id": "v2/tr_speaker_2", "display": "Speaker 2 (TR) - Turkish - Male", "language": "Turkish", "gender": "Male"},
    {"id": "v2/tr_speaker_3", "display": "Speaker 3 (TR) - Turkish - Male", "language": "Turkish", "gender": "Male"},
    {"id": "v2/tr_speaker_4", "display": "Speaker 4 (TR) - Turkish - Female", "language": "Turkish", "gender": "Female"},
    {"id": "v2/tr_speaker_5", "display": "Speaker 5 (TR) - Turkish - Female", "language": "Turkish", "gender": "Female"},
    {"id": "v2/tr_speaker_6", "display": "Speaker 6 (TR) - Turkish - Male", "language": "Turkish", "gender": "Male"},
    {"id": "v2/tr_speaker_7", "display": "Speaker 7 (TR) - Turkish - Male (Grainy)", "language": "Turkish", "gender": "Male", "tags": ["Grainy"]},
    {"id": "v2/tr_speaker_8", "display": "Speaker 8 (TR) - Turkish - Male", "language": "Turkish", "gender": "Male"},
    {"id": "v2/tr_speaker_9", "display": "Speaker 9 (TR) - Turkish - Male", "language": "Turkish", "gender": "Male"},
]

