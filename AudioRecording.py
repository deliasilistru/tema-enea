import threading
import pyaudio
import wave
import audioop
import logging
import errno

logger = logging.getLogger(__name__)


class AudioRecorder():
    def __init__(self):
        self.seconds = 120
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
        # try:
        #     logger.info("Audio recording started")
        #     self.stream.start_stream()
        #     for _ in range(int(44100 / (self.chunk * self.seconds))):
        #         data = self.stream.read(self.chunk)
        #         self.frames.append(data)
        #     self.stop()
        #     logger.info("Audio recording finished")
        # except OSError as e:
        #     if e.errno == errno.ENOSPC:
        #         logger.error("Couldn't compile screen recording file. Disk space is fulll.")
        #         raise
        #     else:
        #         logger.error(e)
        #         raise
        # finally:
        #     self.out.release()
        logger.info("Audio recording started")
        self.stream.start_stream()
        while (self.open == True):
            data = self.stream.read(self.chunk)
            self.frames.append(data)
            if self.open == False:
                break
        logger.info("Audio recording finished")

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

