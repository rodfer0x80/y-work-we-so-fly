import os
import sys
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from .logger import *


class Bot:
    def __init__(self):
        DATA_LOCAL = "./data"
        self.logger = Logger(filename="debug.log")

    def test(self):
        self.logger.debug("test")
        self.logger.info("test")
        self.logger.warning("test")
        self.logger.error("test")
        self.logger.critical("test")
        print("bot")
        return 0
