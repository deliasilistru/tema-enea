import cv2
import threading
import time
import numpy as np
import pyautogui

class VideoRecorder():
    def __init__(self):
        self.open = True
        self.fps = 100
        self.screen_size = (1920,1080)
        self.fourcc = cv2.VideoWriter_fourcc(*"XVID")
        self.out = cv2.VideoWriter("temp_video.avi", self.fourcc, 16.0, (self.screen_size))
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