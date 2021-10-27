import threading
import pyaudio
import wave
import audioop

class AudioRecorder():
    def __init__(self):
        self.open = True
        self.rate = 44100
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 2
        self.audio_filename = "temp_audio.wav"
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format= self.format,
                                      channels = self.channels,
                                      rate = self.rate,
                                      input = True,
                                      output = True,
                                      frames_per_buffer = self.chunk)
        self.frames = []

    def record(self):
        self.stream.start_stream()
        while(self.open == True):
            data = self.stream.read(self.chunk)
            self.frames.append(data)
            if self.open == False:
                break

    def stop(self):
        if self.open == True:
            self.open = False
            self.stream.stop_stream()
            self.stream.close()
            self.audio.terminate()

            waveFile = wave.open(self.audio_filename, "wb")
            waveFile.setnchannels(self.channels)
            waveFile.setsampwidth(self.audio.get_sample_size(self.format))
            waveFile.setframerate(self.rate)
            waveFile.writeframes(b"".join(self.frames))
            waveFile.close()

        pass

    def start(self):
        audio_thread = threading.Thread(target = self.record)
        audio_thread.start()

