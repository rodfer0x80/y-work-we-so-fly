import os
import sys
import time
from bs4 import BeautifulSoup
import urllib.request
import re
import time
import json

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from .logger import *


class Bot:
    def __init__(self):
        DATA_LOCAL = "./data"
        DETAILS_LOCAL = f"{DATA_LOCAL}/details.json"
        DRIVER_LOCAL = "/opt/drivers/geckodriver"

        self.logger = Logger(filename="debug.log")

        self.driver = webdriver.Firefox(
            executable_path=DRIVER_LOCAL)

        # self.details = dict()
        with open(DETAILS_LOCAL, 'r') as h:
            self.details = json.load(h)

    def login(self):
        url = f"https://linkedin.com/in/{self.details['linkedin_username']}"
        self.driver.get(url)
        time.sleep(1)

        try:
            self.driver.find_element(By.CLASS_NAME,
                                     "sign-in-modal__outlet-btn").click()
        except:
            return 1
        try:
            self.driver.find_element(By.ID,
                                     "public_profile_contextual-sign-in_sign-in-modal_session_key").send_keys(self.details['email'])
        except:
            return 2
        try:
            self.driver.find_element(By.ID,
                                     "public_profile_contextual-sign-in_sign-in-modal_session_password").send_keys(self.details['linkedin_passwd'])
        except:
            return 3
        try:
            self.driver.find_element(By.CLASS_NAME,
                                     "sign-in-form__submit-btn--full-width").click()
            time.sleep(1)
        except:
            return 4

        return 0

    def goToJoblisting(self):
        for keyword in self.details['keywords']:
            try:
                self.driver.get(
                    "https://www.linkedin.com/jobs/search/?currentJobId=1/")
                time.sleep(5)
            except:
                return 1
            try:
                self.driver.find_element(
                    By.CSS_SELECTOR, "input.jobs-search-box__keyboard-text-input").click()
                time.sleep(1)
                self.driver.find_element(
                    By.CSS_SELECTOR, "input.jobs-search-box__keyboard-text-input").send_keys(keyword)
            except:
                return 2
            try:
                self.driver.find_element(
                    By.CSS_SELECTOR, "button.jobs-search-box__submit-button").click()
                time.sleep(5)
                self.applyAndGetLinks()
            except:
                return 3
        return 0

    def applyAndGetLinks(self):
        return 0

    def test(self):
        err = self.login()
        if err == 0:
            self.logger.debug(f"[{err}] Login to LinkedIn successfull")
        else:
            self.logger.critical(f"[{err}] Login to LinkedIn failed")

        err = self.goToJoblisting()
        if err == 0:
            self.logger.debug(f"[{err}] Job applications succesfull")
        else:
            self.logger.critical(f"[{err}] Job applications failed")

        return 0
