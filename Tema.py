from selenium import webdriver
import cv2
import numpy as np
import pyautogui
import time

from selenium.webdriver.common.by import By

######### INREGISTRAREA ECRANULUI ##########

# display screen resolution, get it from your OS settings
SCREEN_SIZE = (1920, 1080)
# define the codec
fourcc = cv2.VideoWriter_fourcc(*"XVID")
# create the video write object
out = cv2.VideoWriter("output.avi", fourcc, 20.0, (SCREEN_SIZE))

start_time = time.time()
seconds = 30
prev = 0
fps = 60

while True:
    current_time = time.time()
    elapsed_time = current_time - start_time
    # make a screenshot
    img = pyautogui.screenshot()
    # convert these pixels to a proper numpy array to work with OpenCV
    frame = np.array(img)
    # convert colors from BGR to RGB
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # write the frame
    out.write(frame)
    if elapsed_time > seconds:
        break
    # show the frame
    # cv2.imshow("screenshot", frame)

# while True:
#     elapsed_time = time.time() - prev
#     img = pyautogui.screenshot()
#
#     if elapsed_time > 1.0/fps:
#         prev = time.time()
#         frame = np.array(img)
#         frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         out.write(frame)
#
#     cv2.waitKey(100)
#     if prev - start_time > seconds:
#         break



########## Deschide Youtube ############
driver = webdriver.Chrome()
driver.get('https://www.youtube.com/')
driver.maximize_window()

# Apasa butonul I AGREE
element = driver.find_element(By.LINK_TEXT ,"I AGREE")
element.click()

# Face click pe primul video recomandat
first_video = driver.find_element(By.CSS_SELECTOR, "#dismissible > ytd-thumbnail")
first_video.click()


# make sure everything is closed when exited
cv2.destroyAllWindows()
out.release()
