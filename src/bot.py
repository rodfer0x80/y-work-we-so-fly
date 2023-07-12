import os
import time
import json

import requests

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options as FirefoxOptions
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

        ## Headless
        options = FirefoxOptions()
        #options.add_argument("--headless")
        options.add_argument("--window-size=1920x1080")

        self.driver = webdriver.Firefox(
            executable_path=DRIVER_LOCAL, options=options)

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

        source = self.findSourceAshby(link)
        if source:
            return "ashby"

        return source

    def findSourceTeamtailor(self, link):
        keyword = "teamtailor"
        page = requests.get(link)
        for line in page.text.split("\n"):
            if keyword in line:
                return True
        return False

    def findSourceAshby(self, link):
        if "jobs.ashbyhq.com" in link:
            return True
        return False

    def applyAshby(self, link, details, resume_local, cover_letter):
        try:
            self.driver.get(f"{link}/application")
            self.logger.info(f"[!] Started application {link}\n")
            time.sleep(3)
        except:
            self.logger.error(f"[x] Failed to load application {link}\n")
            return 1

        try:
            self.driver.find_element(By.XPATH, "//input[@name='_systemfield_name']").send_keys(f"{details['first_name']} {details['last_name']}")
            self.logger.info(f"[*] Filled name field for application {link}\n")
        except:
            self.logger.warning(f"[x] Fail to fill name field for application {link}\n")
            pass

        try:
            self.driver.find_element(By.XPATH, "//input[@name='_systemfield_email']").send_keys(details['email'])
            self.logger.info(f"[*] Filled email field for application {link}\n")
        except:
            self.logger.warning(f"[x] Fail to fill email field for application {link}\n")
            pass

        try:
            self.driver.find_element(By.XPATH, "//textarea[@rows='4']").send_keys(cover_letter)
            self.logger.info(f"[*] Filled cover letter field for application {link}\n")
        except:
            self.logger.warning(f"[x] Fail to fill cover letter field for application {link}\n")
            pass

        try:
            self.driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[2]/div/div/div[5]/div/input").send_keys(resume_local)
            self.logger.info(f"[*] Uploaded resume for application {link}\n")
            time.sleep(3)
        except:
            self.logger.warning(f"[x] Failed to upload resume for application {link}\n")
        pass

        try:
            self.driver.find_element(By.CLASS_NAME, 'ashby-application-form-submit-button').click()
            self.logger.info(f"[!] Submited application {link}\n")
        except:
            self.logger.error(f"[x] Failed to submit application {link}\n")
            return 2

        return 0


    def applyTeamtailor(self, link, details, resume_local, cover_letter):
        try:
            self.driver.get(link)
            time.sleep(1)
            self.logger.info(f"[!] Started application {link}\n")
        except:
            self.logger.error(f"[x] Failed to load application {link}\n")
            return 1

        # disable cookies
        try:
            self.driver.find_element(By.XPATH, "//button[@class='careersite-button w-full' and contains(text(), 'Disable all')]").click()
            self.logger.info(f"[*] Disabled cookies for application {link}\n")
        except:
            self.logger.warning(f"[x] Failed to disable cookies for application {link}\n")
            pass

        try:
            self.driver.find_element(By.CLASS_NAME, 'truncate').click()
            time.sleep(1)
            self.logger.info(f"[*] Loaded form for application {link}\n")
        except:
            self.logger.warning(f"[x] Failed to load form for application {link}\n")
            return 2


        # fill in basic info
        try:
            self.driver.find_element(By.ID, 'candidate_first_name').send_keys(details['first_name'])
            self.driver.find_element(By.ID, 'candidate_last_name').send_keys(details['last_name'])
            self.driver.find_element(By.ID, 'candidate_email').send_keys(details['email'])
            self.driver.find_element(By.ID, 'candidate_phone').send_keys(details['mobile'])
            self.logger.info(f"[*] Filled basic details for application {link}\n")
        except:
            self.logger.warning(f"[x] Failed to fill basic details for application {link}\n")
            pass

        # fill resume
        try:
            self.driver.find_element(By.ID, 'candidate_resume_remote_url').send_keys(resume_local)
            time.sleep(1)
            self.logger.info(f"[*] Uploaded resume for application {link}\n")
        except:
            self.logger.warning(f"[x] Failed to upload resume for application {link}\n")
            pass

        try:
            self.driver.find_element(By.ID, 'candidate_job_applications_attributes_0_cover_letter').send_keys(
                cover_letter)
            time.sleep(1)
            cover_letter = self.driver.find_element(By.ID, 'candidate_job_applications_attributes_0_cover_letter')
            time.sleep(1)
            self.logger.info(f"[*] Filled cover letter for application {link}\n")
        except:
            self.logger.warning(f"[x] No cover letter field found for application {link}\n")
            pass


        # scroll down
        try:
            self.driver.execute_script("arguments[0].scrollIntoView();", cover_letter)
            self.logger.info(f"[*] Scroll down in application {link}\n")
        except:
            self.logger.warning(f"[!] Failed to scroll down in application {link}\n")
            pass

        # consent to data storage
        try:
            self.driver.find_element(By.ID, 'candidate_consent_given').click()
            checkbox = self.driver.find_element(By.ID, 'candidate_consent_given')
            self.logger.info(f"[*] Accepted data storage consent for application {link}\n")
        except:
            self.logger.warning(f"[x] Failed to give data storage consent for application {link}\n")
            pass

        # scroll down
        try:
            self.driver.execute_script("arguments[0].scrollIntoView();", checkbox)
            self.logger.info(f"[*] Scroll down in application {link}\n")
        except:
            self.logger.warning(f"[!] Failed to scroll down in application {link}\n")
            pass

        # submit application
        try:
            self.driver.find_element(By.XPATH, "//input[@type='submit']").click()
            self.logger.info(f"[+] Completed application {link}\n\n")
        except:
            self.logger.error(f"[x] Failed to submit application {link}\n\n")
            return 3

        return 0



    def applyWorkable(self, link, details, resume_local, cover_letter):
        # go to application section
        if link[-1] == "/":
            link = f"{link}apply"
        else:
            link = f"{link}/apply"
        try:
            self.driver.get(link)
            self.logger.info(f"[!] Started application {link}\n")
            time.sleep(2)
        except:
            self.logger.error(f"[x] Failed to start application {link}\n")
            return 1

        # fill in name
        try:
            self.driver.find_element(By.ID, "firstname").send_keys(details['first_name'])
            self.driver.find_element(By.ID, "lastname").send_keys(details['last_name'])
            self.logger.info(f"[*] Filled firstname and lastname for application {link}\n")
        except:
            self.logger.warning(f"[x] No firstname or lastname field found for application {link}\n")
            pass

        # fill in email
        try:
            self.driver.find_element(By.ID, "email").send_keys(details['email'])
            self.logger.info(f"[*] Filled email for application {link}\n")
        except:
            self.logger.warning(f"[x] No email field found for application {link}\n")
            pass

        # fill in mobile
        try:
            self.driver.find_element(By.XPATH, "/html/body/div/div/div/div/main/form/section[1]/div[2]/div[5]/label/div/div/div/div/input").click()
            wait = WebDriverWait(self.driver, 3)
            mobile = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div/div/div/div/main/form/section[1]/div[2]/div[5]/label/div/div/div/div/input')))
            mobile.send_keys(details['mobile'])
            self.logger.info(f"[*] Filled mobile for application {link}\n")
            time.sleep(1)
        except:
            self.logger.warning(f"[x] No mobile field found for application {link}\n")
            pass

        # fill in address
        try:
            self.driver.find_element(By.ID, "address").send_keys(details['address'])
            self.logger.info(f"[*] Filled address for application {link}\n")
            time.sleep(1)
        except:
            self.logger.warning(f"[x] No address field found for application {link}\n")
            pass

        # scroll down
        try:
            summary_box = self.driver.find_element(By.ID, "summary")
            self.driver.execute_script("arguments[0].scrollIntoView();", summary_box)
            self.logger.info(f"[*] Scroll down in application {link}\n")
        except:
            self.logger.warning(f"[!] Failed to scroll down in application {link}\n")
            pass

        # fill in summary
        try:
            summary = ""
            for keyword in details['keywords']:
                summary = f"{summary} {keyword}"
            self.driver.find_element(By.ID, "summary").send_keys(summary)
            self.logger.info(f"[*] Filled summary for application {link}\n")
        except:
            self.logger.warning(f"[x] No summary field found for application {link}\n")
            pass

        # scroll down
        try:
            resume_field = self.driver.find_element(By.XPATH, "//input[contains(@id,'input_files_input')]")
            self.driver.execute_script("arguments[0].scrollIntoView();", resume_field)
            self.logger.info(f"[*] Scroll down in application {link}\n")
        except:
            self.logger.warning(f"[!] Failed to scroll down in application {link}\n")
            pass

        # upload resume
        try:
            self.driver.find_element(By.XPATH, "//input[contains(@id,'input_files_input')]").send_keys(resume_local)
            self.logger.info(f"[*] Uploaded resume for application {link}\n")
        except:
            self.logger.warning(f"[x] Failed to upload resume for application {link}\n")
            pass

        # scroll down
        try:
            resume_field = self.driver.find_element(By.ID, "cover_letter")
            self.driver.execute_script("arguments[0].scrollIntoView();", resume_field)
            self.logger.info(f"[*] Scroll down in application {link}\n")
        except:
            self.logger.warning(f"[!] Failed to scroll down in application {link}\n")
            pass

        # fill in cover letter
        try:
            self.driver.find_element(By.ID, "cover_letter").send_keys(cover_letter)
            self.logger.info(f"[*] Filled cover letter for application {link}\n")
        except:
            self.logger.warning(f"[x] No cover letter field found for application {link}\n")
            pass

        # check questions
        try:
            self.driver.find_element(By.XPATH, "//input[contains(text(), 'What is your notice period/availablity?')]").send_keys(details['motivation'])
            self.logger.info(f"[*] Filled question motivation for application {link}\n")
        except:
            self.logger.warning(f"[x] No field motivation found for application {link}\n")
            pass
        try:
            self.driver.find_element(By.XPATH, "//input[contains(text(), 'What are your salary expectations?')]").send_keys(details['salary_predict'])
            self.logger.info(f"[*] Filled question salary prediction for application {link}\n")
        except:
            self.logger.warning(f"[x] No field salary prediction found for application {link}\n")
            pass
        try:
            self.driver.find_element(By.XPATH,
                                     "//span[@class='styles--33WZ1' and contains(text(), 'yes')]")\
                .click()
            self.logger.info(f"[*] Confirmed right to work for application {link}\n")
        except:
            self.logger.warning(f"[X] Failed to confirm right to work for application {link}\n")
            pass

        # submit application
        time.sleep(1)
        try:
            self.driver.find_element(By.XPATH,
                                     '/html/body/div/div/div/div/main/form/section[4]/div/div/div/label/label/div/input')\
                .click()
            self.driver.find_element(By.XPATH,
                                     '/html/body/div/div/div/div/main/form/section[4]/div/div/div/label/label/div/input')\
                .send_keys("1")
            self.logger.info(f"[*] Confirmed GDPR notice for application {link}\n")
        except:
            self.logger.warning(f"[X] Failed to confirm GDPR notice for application {link}\n")
        time.sleep(1)
        try:
            self.driver.find_element(By.XPATH, "//button[contains(text(),'Submit application')]").click()
            self.logger.info(f"[+] Completed application {link}\n\n")
        except:
            self.logger.error(f"[x] Failed to submit application {link}\n\n")
            return 2

        return 0

    def applyLink(self, link, details, resume_local, cover_letter):
        source = self.findSource(link)

        if source == "workable":
            self.applyWorkable(link, details, resume_local, cover_letter)
        elif source == "teamtailor":
            self.applyTeamtailor(link, details, resume_local, cover_letter)
        elif source == "ashby":
            self.applyAshby(link, details, resume_local, cover_letter)
        else:
            return 1

        return 0

    def applyBatch(self, batchfile):
        with open(batchfile, 'r') as f:
            for link in f.read().splitlines():
                self.applyLink(link, self.details, self.resume_local, self.cover_letter)
        return 0

    def test(self):
        self.applyLink("https://jobs.ashbyhq.com/safi/83c5a967-b72d-42ae-9889-86e3bbba6da6", self.details, self.resume_local, self.cover_letter)
        return 0

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
