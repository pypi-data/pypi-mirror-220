from bs4 import BeautifulSoup
from pyassist import Utilities
import requests

class BS4(Utilities):

    soup = ""
    
    def __init__(self, **kwargs):
        if "name" not in kwargs:
            kwargs["name"] = (f"{__class__}".split("'")[1])
        self.get_logger(**kwargs)
        self.debug(f"Initialized: {kwargs['name']}")

    def soup(self, text, unicode="UTF-8", parser="html.parser"):
        return BeautifulSoup(text.encode(unicode).decode(unicode), parser)

    def find_nth_anchestor_bs4(self, element, n):
        for i in range(n + 1):
            element = element.parent
        return element

    def find_nth_sibling_bs4(self, element, n):
        for i in range(n + 1):
            element = element.nextSibling
        return element

    def find_nth_successor_bs4(self, element, n):
        for i in range(n + 1):
            element = element.findChildren()[0]
        return element
    
    def find_by_classname(self, soup, classname, element="div"):
        return soup.find(element, {"class": classname})

    def findall_by_classname(self, soup, classname, element="div"):
        return soup.find_all(element, {"class": classname})

    def selenium_webpage_to_soup(self, driver):
        text = driver.execute_script("return document.body.innerHTML")
        return self.soup(text)

    def request_url_to_soup(self, url):
        response = requests.get(url)
        try:
            content = response.content.decode("utf-8")
            return self.soup(content)
        except Exception as e:
            print(f"Exception: {e}")

    def get_clear_text_from_element(self, element):
        texts = element.text.replace("  "," ").strip().split()
        texts = [text for text in texts if text]
        return " ".join(texts)