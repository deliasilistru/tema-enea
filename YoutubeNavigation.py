import threading
from selenium import webdriver
from selenium.webdriver.common.by import By


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
