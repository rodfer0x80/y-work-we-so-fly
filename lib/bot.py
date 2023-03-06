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
