import time
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import whisper
from pytube import YouTube
from bark import SAMPLE_RATE, generate_audio
from scipy.io.wavfile import write as write_wav
import os
import speech_recognition as sr
from deep_translator import GoogleTranslator

def preload_models():
    from bark import preload_models
    preload_models()

class Recorder:
    def __init__(self):
        self.fs = 44100
        self.is_recording = False
        self.start_time = None
        self.myrecording = None

    def start_recording(self):
        self.is_recording = True
        self.start_time = time.time()
        self.myrecording = sd.rec(int(10 * self.fs), samplerate=self.fs, channels=2)

    def stop_recording(self):
        if self.is_recording:
            self.is_recording = False
            sd.wait()
            duration = time.time() - self.start_time
            wav.write('output.wav', self.fs, self.myrecording)
            return 'output.wav', duration

    def cancel_recording(self):
        if self.is_recording:
            self.is_recording = False
            print("Recording cancelled.")

    def get_recording_duration(self):
        if self.is_recording:
            return time.time() - self.start_time
        return 0

def format_duration(seconds):
    minutes, seconds = divmod(seconds, 60)
    return f"{int(minutes)}:{int(seconds):02d}"

def download_youtube_audio(url):
    yt = YouTube(url)
    stream = yt.streams.filter(only_audio=True).first()
    filename = stream.default_filename
    stream.download(filename=filename)
    return filename

def transcribe_audio_file(filename):
    model = whisper.load_model("base")
    result = model.transcribe(filename)
    return result["text"]

def translate_text(text, target_lang1, target_lang2):
    translated_text1 = GoogleTranslator(source='auto', target=target_lang1).translate(text)
    translated_text2 = GoogleTranslator(source='auto', target=target_lang2).translate(text)
    return translated_text1, translated_text2

def generate_and_save_audio(text, voice, filename, person, is_input=True):
    # Create directory structure if it doesn't exist
    base_dir = 'audio'
    io_dir = 'input' if is_input else 'output'
    person_dir = f'person{person}'
    full_dir = os.path.join(base_dir, io_dir, person_dir)
    os.makedirs(full_dir, exist_ok=True)

    # Generate and save audio
    audio_array = generate_audio(text, history_prompt=voice)
    full_path = os.path.join(full_dir, filename)
    write_wav(full_path, SAMPLE_RATE, audio_array)

def speak_text(text, voice):
    audio_array = generate_audio(text, history_prompt=voice)
    write_wav('temp_output.wav', SAMPLE_RATE, audio_array)
    os.system('start temp_output.wav')

def realtime_transcribe_translate(app):
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            while app.is_recording_realtime:
                audio = r.listen(source, phrase_time_limit=5)
                try:
                    text = r.recognize_google(audio)
                    # Detect the language
                    detected_lang = GoogleTranslator().detect(text)
                    app.frame.after(0, app.update_realtime_text, text, detected_lang)
                except sr.UnknownValueError:
                    print("Speech recognition could not understand audio")
                except sr.RequestError as e:
                    print(f"Could not request results from speech recognition service; {e}")
    except AttributeError:
        print("Error: PyAudio is not installed. Real-time transcription is not available.")
        app.frame.after(0, app.update_status, "Error: PyAudio is not installed. Real-time transcription is not available.")

def get_language_choices():
    return GoogleTranslator(source='auto', target='english').get_supported_languages()