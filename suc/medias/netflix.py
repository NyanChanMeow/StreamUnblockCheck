# -*- coding: utf-8 -*-

import json
import logging
from selenium import webdriver
from selenium.webdriver.webkitgtk.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from .media_base import MediaBaseSelenium
from ..types.errors.requests import ResponseInvalid


class NetflixSelenium(MediaBaseSelenium):
    def __init__(self, config: dict = {}):
        super().__init__(config)
        self._invalid_error_codes = ["F7111-5059"]
        self._email = config["email"]
        self._password = config["password"]
        self._profile_uri = config["profile_uri"]
        self._test_url = config["test_url"]
        self._dns_server = config.get("dns", "1.0.0.1")
        self._cookies_file = config.get("cookies_file", "netflix_cookies.json")

        self._ff_profile = webdriver.FirefoxProfile()
        self._ff_profile.set_preference("general.warnOnAboutConfig", False)
        self._ff_profile.set_preference(
            "browser.aboutConfig.showWarning", False)

        self._ff_options = webdriver.FirefoxOptions()
        self._ff_options.headless = config.get("headless", False)

    def _login_via_pwd(self):
        self._webdri.get("https://netflix.com/login")

        login_id_ele = None
        try:
            login_id_ele = self._webdri.find_element_by_xpath(
                r'//*[@id="id_userLoginId"]')
        except NoSuchElementException:
            raise ResponseInvalid("Login ID element not found")
        login_id_ele.send_keys(self._email)
        logging.info("Email entered")

        login_pwd_ele = None
        try:
            login_pwd_ele = self._webdri.find_element_by_xpath(
                r'//*[@id="id_password"]')
        except NoSuchElementException:
            raise ResponseInvalid("Login Password element not found")
        login_pwd_ele.send_keys(self._password)
        logging.info("Password entered")

        login_btn_ele = None
        try:
            login_btn_ele = self._webdri.find_element_by_xpath(
                r'/html/body/div[1]/div/div[3]/div/div/div[1]/form/button')
        except NoSuchElementException:
            raise ResponseInvalid("Login Button element not found")
        login_btn_ele.click()
        logging.info("Login button clicked")

        # waiting for login
        logging.info("Waiting for login")
        wait = WebDriverWait(self._webdri, 15)
        wait.until(lambda webdri: self._webdri.current_url ==
                   "https://www.netflix.com/browse")
        logging.info("Logged in")

        # switch profile
        logging.info("Switching profile")
        self._webdri.get("https://www.netflix.com" + self._profile_uri)
        self._webdri.get("https://www.netflix.com/browse")
        logging.info("Profile switched")

    def _login_via_cookie(self):
        self._webdri.get("https://netflix.com/")
        with open(self._cookies_file, "r+") as f:
            cookies = json.load(f)
        for cookie in cookies:
            self._webdri.add_cookie(cookie)

    def _save_login_cookies(self):
        logging.info("Saving netflix login cookies")
        with open(self._cookies_file, "w+") as f:
            json.dump(self._webdri.get_cookies(), f)

    def run(self) -> bool:
        try:
            logging.info("Starting firefox")
            self._webdri = webdriver.Firefox(
                firefox_profile=self._ff_profile, firefox_options=self._ff_options)
            logging.info("Firefox started")

            try:
                logging.info("Logging via cookies")
                self._login_via_cookie()
                self._webdri.get("https://netflix.com/login")
                if self._webdri.current_url != "https://www.netflix.com/browse":
                    logging.error("Failed to login via cookies")
                    self._login_via_pwd()
                else:
                    logging.info("Logged in via cookies")
            except Exception as e:
                logging.error("Failed to login via cookies, {}".format(str(e)))
                self._login_via_pwd()

            # Change DNS Server
            logging.info("Setting up DNS to {}".format(self._dns_server))
            self._set_string_preferce(
                "network.dns.forceResolve", self._dns_server)

            # start test
            logging.info("Performing test")
            self._webdri.get(self._test_url)
            # self._webdri.get(
            #    "https://www.netflix.com/watch/80186864?trackId=254015180")
            try:
                judge_ele = WebDriverWait(self._webdri, 120).until(
                    _netflix_judge_element_found(
                        (By.XPATH,
                         r'/html/body/div[1]/div/div/div[1]/div/div/div[2]/div/div[2]/div/div[2]/span/strong'),
                        (By.XPATH,
                         r'/html/body/div[1]/div/div/div[1]/div/div/div[2]')
                    )
                )
                if judge_ele.tag_name == "strong":
                    if judge_ele.text in self._invalid_error_codes:
                        logging.info("Invalid Code: {}".format(judge_ele.text))
                        return False
                    else:
                        logging.info("Valid Code: {}".format(judge_ele.text))
                        return True
                elif judge_ele.tag_name == "div":
                    logging.info(judge_ele.get_attribute("class"))
                    return True
                else:
                    raise ResponseInvalid(
                        "Invalid element {}".format(judge_ele.text))

            except TimeoutException:
                raise ResponseInvalid("Wait element timeout")
        except Exception as e:
            raise e
        finally:
            self._save_login_cookies()
            self._webdri.quit()


class _netflix_judge_element_found(object):
    def __init__(self, locator_errcode: tuple, locator_success: tuple):
        self.locator_errcode = locator_errcode
        self.locator_success = locator_success

    def __call__(self, driver: WebDriver):
        element_errcode = driver.find_element(*self.locator_errcode)
        if element_errcode is not None:
            return element_errcode

        element_success = driver.find_element(*self.locator_success)
        if element_success is not None:
            return element_success

        return False
