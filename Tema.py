import cv2
import threading
import time
import subprocess
import os
import numpy as np
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
import pyaudio
import wave
import ffmpeg


class VideoRecorder():
    def __init__(self):
        self.open = True
        self.fps = 100
        self.screen_size = (1920,1080)
        self.fourcc = cv2.VideoWriter_fourcc(*"XVID")
        self.out = cv2.VideoWriter("temp_video.avi", self.fourcc, 16.5, (self.screen_size))
        self.start_time = time.time()
        self.seconds = 120

    def record(self):
        timer_start = time.time();
        while(self.open == True):
            # make a screenshot
            img = pyautogui.screenshot()
            # convert these pixels to a proper numpy array to work with OpenCV
            frame = np.array(img)
            # convert colors from BGR to RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # write the frame
            self.out.write(frame)


    def stop(self):
        if self.open == True:
            self.open = False
            self.out.release()
            cv2.destroyAllWindows()
        else:
            pass

    def start(self):
        video_tread = threading.Thread(target=self.record)
        video_tread.start()


class YoutubeNav():
    def __init__(self):
        self.driver = webdriver.Chrome()

    def navigation(self):
        self.driver.get('https://www.youtube.com/')
        self.driver.maximize_window()
        # Apasa butonul I AGREE
        element = self.driver.find_element(By.LINK_TEXT, "I AGREE")
        element.click()

        # Face click pe primul video recomandat
        first_video = self.driver.find_element(By.CSS_SELECTOR, "#dismissible > ytd-thumbnail")
        first_video.click()

        #time.sleep(120)

    def start(self):
        yt_thead = threading.Thread(target= self.navigation())
        yt_thead.start()

    def stop(self):
        self.driver.close()

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





def start_YTVRecording(filename):
    global video_thread
    global yt_thread
    global audio_thread

    video_thread = VideoRecorder()
    audio_thread = AudioRecorder()
    yt_thread = YoutubeNav()

    video_thread.start()
    audio_thread.start()
    yt_thread.start()

    return filename


# def start_video_recording(filename):
#     global video_thread
#
#     video_thread = VideoRecorder()
#     video_thread.start()
#
#     return filename


def stop_YTRecording(filename):
    video_thread.stop()
    audio_thread.stop()
    yt_thread.stop()

    # Makes sure the threads have finished
    while threading.active_count() > 1:
        time.sleep(1)

    cmd = "ffmpeg -ac 2 -channel_layout stereo -i temp_audio.wav -i temp_video.avi -pix_fmt yuv420p " + filename + ".avi"
    subprocess.call(cmd, shell=True)




# Required and wanted processing of final files
def file_manager(filename):
    local_path = os.getcwd()

    if os.path.exists(str(local_path) + "/temp_audio.wav"):
        os.remove(str(local_path) + "/temp_audio.wav")

    if os.path.exists(str(local_path) + "/temp_video.avi"):
        os.remove(str(local_path) + "/temp_video.avi")

    if os.path.exists(str(local_path) + "/temp_video2.avi"):
        os.remove(str(local_path) + "/temp_video2.avi")

    if os.path.exists(str(local_path) + "/" + filename + ".avi"):
        os.remove(str(local_path) + "/" + filename + ".avi")


if __name__ == "__main__":
    filename = "Default_user"
    file_manager(filename)

    start_YTVRecording(filename)

    time.sleep(120)

    stop_YTRecording(filename)

    print("Done")
