from os import devnull
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.common.exceptions as SeleniumExceptions

# Firefox
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.firefox import GeckoDriverManager

from pyassist import Utilities
import logging
import time

# Contains Process/ Subprocess related Functions
class Selenium(Utilities):

    driver = ""
    By = By
    EC = EC
    Keys = Keys
    ActionChains = ActionChains
    WebDriverWait = WebDriverWait
    exceptions = SeleniumExceptions

    def __init__(self, **kwargs):
        if "name" not in kwargs:
            kwargs["name"] = (f"{__class__}".split("'")[1])
        self.get_logger(**kwargs)
        self.debug(f"Initialized: {kwargs['name']}")

        # Disable Proxy by default and also set Loggin level as warning for Unwanted Class
        self.proxy_enabled = False
        for class_ in ["selenium.webdriver.common.service", 'selenium.webdriver.remote.remote_connection', "WDM"]:
            logger = logging.getLogger(class_)
            logger.setLevel(logging.WARNING)

    def set_proxy(self, proxy):
        self.proxy = proxy

    def enable_proxy(self):
        self.proxy_enabled = True

    def get_firefox_proxy(self):
        proxy_obj = self.proxy()
        proxy = Proxy()
        proxy.http_proxy = proxy_obj["http"].replace("http://", "")
        proxy.proxy_type = ProxyType.MANUAL
        if "https" in proxy_obj:
            proxy.ssl_proxy = proxy_obj["https"].replace("https://", "")
        print(f"Firefox Proxy: {proxy}")
        if not proxy:
            time.sleep(2)
            return self.__get_firefox_driver()
        return proxy

    def __get_firefox_driver(self):
        options = FirefoxOptions()
        # options.headless = True
        if self.proxy_enabled:
            options.proxy = self.get_proxy()
        driver = webdriver.Firefox(
                                    service=FirefoxService(GeckoDriverManager().install()),
                                    options=options,
                                )
        # else:
        #     driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

        return driver

    def set_firefox_driver(self):
        print("FIREFOX DRIVER")
        try:
            self.get_driver = self.__get_firefox_driver
            self.get_proxy = self.get_firefox_proxy
        except Exception as e:
            print(f"Exception getting driver {e}")

    def run_function_within_webdriver(self, function_name, **kwargs):
        try:
            with self.get_driver() as driver:
                self.sleep(sleep_time=3, message="Giving time to Initialize Driver")
                output = function_name(driver, **kwargs)
            return output
        except Exception as e:
            print(f"Exception: {e}")
    
    def find_nth_ancestor_selenium(self, element, n):
        for i in range(n):
            element = element.find_element(By.XPATH, "./..")
        return element

    def find_nth_sibling_selenium(self, element, n):
        for i in range(n):
            element = element.find_element(By.XPATH, ".//following-sibling::*")
        return element

    def wait_by_class_name(self, driver, classname, waittime=10):
        self.WebDriverWait(driver, waittime).until(self.EC.presence_of_all_elements_located((self.By.CLASS_NAME, classname)))


