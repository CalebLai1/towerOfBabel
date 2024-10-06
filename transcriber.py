import pyaudio
import json
import threading
from vosk import KaldiRecognizer, Model
import re

class Transcriber:
    def __init__(self, model):
        self.model = model
        self.recognizer = None
        self.is_recording = False

    def start_recording(self, callback):
        self.is_recording = True
        self.recognizer = KaldiRecognizer(self.model, 16000)
        self.recognizer.SetWords(True)
        self.recognizer.SetPartialWords(True)

        def record():
            mic = pyaudio.PyAudio()
            stream = mic.open(format=pyaudio.paInt16, channels=1,
                              rate=16000, input=True, frames_per_buffer=16000)
            stream.start_stream()
            try:
                while self.is_recording:
                    data = stream.read(8000, exception_on_overflow=False)
                    if self.recognizer.AcceptWaveform(data):
                        result = self.recognizer.Result()
                        text = json.loads(result).get('text', '')
                        text = re.sub(r'\s+', ' ', text).strip()
                        callback(text, False)
                    else:
                        partial = self.recognizer.PartialResult()
                        text = json.loads(partial).get('partial', '')
                        callback(text, True)
            finally:
                stream.stop_stream()
                stream.close()
                mic.terminate()

        threading.Thread(target=record, daemon=True).start()

    def stop_recording(self):
        self.is_recording = False
