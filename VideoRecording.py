import cv2
import threading
import time
import numpy as np
import pyautogui
import logging
import errno

logger = logging.getLogger(__name__)

class VideoRecorder():
    def __init__(self):
        self.open = True
        self.fps = 16
        self.screen_size = (1920,1080)
        self.fourcc = cv2.VideoWriter_fourcc(*"XVID")
        self.out = cv2.VideoWriter("temp_video.avi", self.fourcc, 16.0, (self.screen_size))
        self.start_time = time.time()
        self.seconds = 120

    def record(self):

        try:
            logger.info("Screen recording started")
            const = int(self.fps * self.seconds)
            for i in range(const):
                # make a screenshot
                img = pyautogui.screenshot()
                # convert these pixels to a proper numpy array to work with OpenCV
                frame = np.array(img)
                # convert colors from BGR to RGB
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # write the frame
                self.out.write(frame)

            self.stop()
            logger.info("Screen recording finished")
        except OSError as e:
            if e.errno == errno.ENOSPC:
                logger.error("Couldn't compile screen recording file. Disk space is fulll.")
                raise
            else:
                logger.error(e)
                raise
        finally:
            self.out.release()


    def stop(self):
        self.out.release()
        cv2.destroyAllWindows()


    def start(self):
        video_tread = threading.Thread(target=self.record)
        video_tread.start()

