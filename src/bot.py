import os
import time
import json

import requests

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver

from .logger import *


class Bot:
    def __init__(self):
        DATA_LOCAL = "./data"
        DETAILS_LOCAL = f"{DATA_LOCAL}/details.json"
        RESUME_LOCAL = f"{DATA_LOCAL}/resume.pdf"
        COVER_LETTER_LOCAL = f"{DATA_LOCAL}/cover_letter.txt"

        DRIVER_LOCAL = "/opt/drivers/geckodriver"

        self.logger = Logger(filename="debug.log")

        self.sources = ["workable"]

        self.driver = webdriver.Firefox(
            executable_path=DRIVER_LOCAL)

        # self.details = dict()
        with open(DETAILS_LOCAL, 'r') as h:
            self.details = json.load(h)
        self.resume_local = f"{os.environ['PWD']}/{RESUME_LOCAL[2:]}"
        with open(COVER_LETTER_LOCAL, 'r') as h:
            self.cover_letter = h.read()
    def findSourceWorkable(self, link):
        if "apply.workable.com" in link:
            return True
        return False

    def findSource(self, link):
        source = False

        source = self.findSourceWorkable(link)
        if source:
            return "workable"

        source = self.findSourceTeamtailor(link)
        if source:
            return "teamtailor"

        return source

    def findSourceTeamtailor(self, link):
        keyword = "teamtailor"
        page = requests.get(link)
        for line in page.text.split("\n"):
            if keyword in line:
                return True
        return False

    def applyTeamtailor(self, link, details, resume_local, cover_letter):
        try:
            self.driver(link)
            time.sleep(1)
            self.driver.find_element(By.XPATH, "//span[contains(text(), 'Apply for this job").click()
            time.sleep(1)
            self.logger.log(f"[!] Started application {link}\n")
        except:
            self.logger.log(f"[x] Failed to load application {link}\n")
            return 1

        # fill in basic info
        try:
            self.driver.find_element(By.ID, 'candidate_resume_remote_url').send_keys(resume_local)
            self.driver.find_element(By.ID, 'candidate_first_name').send_keys(details['firstname'])
            self.driver.find_element(By.ID, 'candidate_first_name').send_keys(details['lastname'])
            self.driver.find_element(By.ID, 'candidate_email').send_keys(details['email'])
            self.driver.find_element(By.ID, 'candidate_phone').send_keys(details['mobile'])
            self.logger.log(f"[*] Filled basic detailf for application {link}\n")
        except:
            self.logger.log(f"[x] Failed to fill basic details for application {link}\n")
            pass

        # fill resume and cover letter
        try:
            self.driver.find_element(By.ID, 'candidate_job_applications_attributes_0_cover_letter').send_keys(
                cover_letter)
            self.logger.log(f"[*] Filled cover letter for application {link}\n")
        except:
            self.logger.log(f"[x] No cover letter field found for application {link}\n")
            pass

        # consent to data storage
        try:
            self.driver.find_element(By.ID, 'candidate_consent_given').click()
            self.logger.log(f"[*] Accepted data storage consent for application {link}\n")
        except:
            self.logger.log(f"[x] Failed to give data storage consent for application {link}\n")
            pass

        return 0



    def applyWorkable(self, link, details, resume_local, cover_letter):
        # go to application section
        try:
            self.driver.get(f"{link}/apply/")
            time.sleep(1)
            self.logger.log(f"[!] Started application {link}\n")
        except:
            self.logger.log(f"[x] Failed to start application {link}\n")
            return 1

        # upload resume
        self.driver.find_element(By.XPATH, "//input[contains(@id,'input_files_input')]").send_keys(resume_local)

        # fill in name
        try:
            self.driver.find_element(By.ID, "firstname").send_keys(details['first_name'])
            self.driver.find_element(By.ID, "lastname").send_keys(details['last_name'])
            self.logger.log(f"[*] Filled firstname and lastname for application {link}\n")
        except:
            self.logger.log(f"[x] No firstname or lastname field found for application {link}\n")
            pass
        
        # fill in email
        try:
            self.driver.find_element(By.ID, "email").send_keys(details['email'])
            self.logger.log(f"[*] Filled email for application {link}\n")
        except:
            self.logger.log(f"[x] No email field found for application {link}\n")
            pass

        # fill in mobile
        try:
            self.driver.find_element(By.CLASS_NAME, "styles--1EuHm").click()
            wait = WebDriverWait(self.driver, 3)
            mobile = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div/div/div/div/main/form/section[1]/div[2]/div[4]/label/div/div/div/div/input')))
            mobile.send_keys(details['mobile'])
            self.logger.log(f"[*] Filled mobile for application {link}\n")
        except:
            self.logger.log(f"[x] No mobile field found for application {link}\n")
            pass
        
        # fill in summary
        try:
            summary = ""
            for keyword in details['keywords']:
                summary = f"{summary} {keyword}"
            self.driver.find_element(By.ID, "summary").send_keys(summary)
            self.logger.log(f"[*] Filled summary for application {link}\n")
        except:
            self.logger.log(f"[x] No summary field found for application {link}\n")
            pass

        # fill in cover letter
        try:
            self.driver.find_element(By.ID, "cover_letter").send_keys(cover_letter)
            self.logger.log(f"[*] Filled cover letter for application {link}\n")
        except:
            self.logger.log(f"[x] No cover letter field found for application {link}\n")
            pass
        
        # submit application
        time.sleep(1)
        try:
            self.driver.find_element(By.XPATH, "//button[contains(text(),'Submit application')]").click()
            self.logger.log(f"[+] Completed application {link}\n\n")
        except:
            self.logger.log(f"[x] Failed to submit application {link}\n\n")
            pass

        return 0

    def applyLink(self, link, details, resume_local, cover_letter):
        source = self.findSource(link)

        if source == "workable":
            self.applyWorkable(link, details, resume_local, cover_letter)
        elif source == "teamtailor":
            self.applyTeamtailor(link, details, resume_local, cover_letter)
        else:
            return 1

        return 0

    def applyBatch(self, batchfile, details, resume_local, cover_letter):
        with open(batchfile, 'r') as f:
            for link in f.readline():
                self.applyLink(link, details, resume_local, cover_letter)
        return 0

    def test(self):
        self.applyLink("https://careers.atomlearning.com/jobs/2832861-mid-back-end-node-developer", self.details, self.resume_local, self.cover_letter)

    def loginLinkedin(self):
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

    def goToJoblistingLinkedin(self):
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

    def applyAndGetLinksLinkedin(self):
        return 0

    def testLinkedin(self):
        err = self.logger.login()
        if err == 0:
            self.logger.logger.debug(f"[{err}] Login to LinkedIn successfull")
        else:
            self.logger.logger.critical(f"[{err}] Login to LinkedIn failed")

        err = self.goToJoblisting()
        if err == 0:
            self.logger.logger.debug(f"[{err}] Job applications succesfull")
        else:
            self.logger.logger.critical(f"[{err}] Job applications failed")

        return 0
