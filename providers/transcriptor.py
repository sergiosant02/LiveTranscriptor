import queue
import threading
import numpy as np
import time
import scipy.io.wavfile
import sounddevice as sd
from faster_whisper import WhisperModel
import scipy.io.wavfile
from typing import Callable
import torch

print(sd.query_devices())


for i in sd.query_devices():
    if i["name"] == "BlackHole 2ch":
        DEVICE_ID = i["index"]


audio_queue = queue.Queue()

class Transcriptor: 
    
    device_id = 1
    SAMPLE_RATE = 16_000
    CHANNELS = 1
    WINDOW_SEC = 3
    
    @property
    def max_length(self):
        return int(2 * self.WINDOW_SEC * self.SAMPLE_RATE)
    
    working: bool = False
    audio_queue = queue.Queue()
    t1: threading.Thread
    t2: threading.Thread
    
    def record_audio(self, audio_duration:int = 3):
        i = 0

        while self.working:
            print(f"Recording from system audio... Device index {self.device_id}, audio_duration: {audio_duration}")
            recording = sd.rec(int(audio_duration * self.SAMPLE_RATE), samplerate=self.SAMPLE_RATE,
                            channels=self.CHANNELS, dtype='float32',
                            device=self.device_id)
            sd.wait()
            scipy.io.wavfile.write(f"system_audio{i}.wav", self.SAMPLE_RATE, recording)
            recording = np.squeeze(recording)
            audio_queue.put(recording)
            i +=1

    def transcript_audio(self, fn: Callable | None = None, model_size="distil-large-v3", compute_type="int8"):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model = WhisperModel(model_size, device=device, compute_type=compute_type)
        buffer = np.zeros((0,), dtype=np.float32)
        partible = False
        while True:
            audio = audio_queue.get()
            
            if audio is None:
                break
            try:
                buffer = np.concatenate((buffer,audio))
                print(len(buffer))
                if len(buffer) > self.max_length:
                    buffer = buffer[-self.max_length:]
                segments, _ = model.transcribe(buffer, beam_size=5, language="en", condition_on_previous_text=False)
                segments = list(segments)
                if partible:
                    partition = len(segments) // 3
                    segments = segments[partition:]
                full_text = "".join([s.text for s in segments])
                print(f"Transcription: {full_text}")
                if fn:
                    fn(full_text)
                partible = True
            except Exception as e:
                print("Error:", e)
                
    def stop(self):
        self.audio_queue.put(None)
        self.working = False
        #self.t1.join()
        #self.t2.join()
                
    def start(self, fn: Callable | None = None, device="cpu", model_size="distil-large-v3", compute_type="int8"):
        self.working = True
        self.t1 = threading.Thread(group=None, target=self.record_audio, daemon=True)
        self.t2 = threading.Thread(group=None, target=self.transcript_audio, args=(fn,model_size,compute_type,), daemon=True)
        self.t1.start()
        self.t2.start()

if __name__ == "__main__":
    transcriptor = Transcriptor()
    transcriptor.start()
    print("Real-time translator running... Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        transcriptor.stop()
        print("Stopping...")
    