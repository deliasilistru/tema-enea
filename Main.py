import threading
import time
import os
from AudioRecording import AudioRecorder
from VideoRecording import VideoRecorder
from YoutubeNavigation import YoutubeNav

def start_YTVRecording(filename):
    global video_thread
    global yt_thread
    global audio_thread

    video_thread = VideoRecorder()
    audio_thread = AudioRecorder()
    yt_thread = YoutubeNav()

    video_thread.start()
    yt_thread.start()
    audio_thread.start()

    return filename


def stop_YTRecording(filename):
    video_thread.stop()
    audio_thread.stop()
    yt_thread.stop()

    # Makes sure the threads have finished
    while threading.active_count() > 1:
        time.sleep(1)


# Required and wanted processing of final files
def file_manager(filename):
    local_path = os.getcwd()

    if os.path.exists(str(local_path) + "/temp_audio.wav"):
        os.remove(str(local_path) + "/temp_audio.wav")

    if os.path.exists(str(local_path) + "/temp_video.avi"):
        os.remove(str(local_path) + "/temp_video.avi")

    if os.path.exists(str(local_path) + "/" + filename + ".avi"):
        os.remove(str(local_path) + "/" + filename + ".avi")


if __name__ == "__main__":
    filename = "Default_user"
    file_manager(filename)

    start_YTVRecording(filename)

    time.sleep(120)

    stop_YTRecording(filename)

    print("Done")