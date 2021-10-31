import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import socket
import time

logger = logging.getLogger(__name__)


class YoutubeNav():
    def __init__(self):
        self.seconds = 120
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()


    def connection(self):
        try:
            appsocket = socket.socket()
            appsocket.connect(("8.8.8.8", 53))
            return True
        except socket.error:
            return False

    def navigation(self):
        try:
            if self.connection():
                self.driver.get('https://www.youtube.com/')
                # self.driver.implicitly_wait(5)
            else:
                self.navigation()
        except WebDriverException as error:
            logger.critical(error.msg + "\n")
            raise

        self.agree_button()
        self.select_video()

        # Apasa butonul I AGREE

    def agree_button(self):
        for _ in range(3):
            try:
                if self.connection():
                    element = WebDriverWait(self.driver, 5).until(
                        EC.visibility_of_element_located((By.LINK_TEXT, "I AGREE")))
                    element.click()
                    break
                else:
                    logger.error("Internet connection failed. Couldn't click the agree button\n")
                    continue
            except TimeoutException:
                logger.warning("Couldn't find the agree button")
                break
            except ElementClickInterceptedException:
                logger.error("Couldn't press agree button\n")
                raise


        # Face click pe primul video recomandat
        # first_video = self.driver.find_element(By.CSS_SELECTOR, "#dismissible > ytd-thumbnail")
        # first_video.click()

    def select_video(self):
        number = 0
        try:
            if self.connection():
                video = self.driver.find_element(By.CSS_SELECTOR, "#dismissible > ytd-thumbnail")
                # if len(videos) == 0:
                #     raise NoSuchElementException
                video.click()
            else:
                raise socket.error
        except TimeoutException:
            logger.critical("Element is not clickable\n")
            raise
        except NoSuchElementException:
            logger.warning("Path of the video might be wrong\n")
            raise
        except IndexError:
            logger.critical("The element you are trying to select is not in the array of elements\n")
            raise
        except socket.error:
            logger.error("Internet connection failed. Couldn't select video\n")
            raise


    def recording_time(self):
        start_time = time.time()
        while time.time() - start_time < self.seconds:
            if not self.connection():
                logger.error("Internet connection failed")
                break
            else:
                continue
        logger.info("Connection was successful")


    def start(self):
        yt_thead = threading.Thread(target= self.navigation())
        yt_thead.start()

        logger.info("The browser and the Youtube page are opened")

    def stop(self):
        self.driver.close()
