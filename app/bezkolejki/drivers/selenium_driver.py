from selenium import webdriver
from selenium.webdriver.common.by import By
from typing import Optional, List, Dict, Union, Any
import icecream as ic


#
#
# WEB_DRIVERS = {
#     'edge': webdriver.Edge(),
#     'chrome': webdriver.Chrome(),
#     'firefox': webdriver.Firefox()
# }

class ChromeOptions:
    def __init__(self, with_headless: bool = True):
        self.chrome_options = webdriver.ChromeOptions()
        self.with_headless = with_headless

    def chrome_option(self):
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--window-size=1920,1080')

        if self.with_headless:
            self.chrome_options.add_argument('--headless')
            self.chrome_options.add_argument('--disable-gpu')

        return self.chrome_options


class SeleniumBaseFields(ChromeOptions):
    def __init__(self,
                 base_link: str, with_headless: bool = True):
        super().__init__(with_headless=with_headless)
        self.driver = webdriver.Chrome(options=self.chrome_option())

        ic.ic(f"Driver: {self.driver} started")
        self.driver.get(base_link)
        ic.ic(f"Serching for: {base_link}")
        self.driver.implicitly_wait(10)

    def close(self):
        self.driver.close()

    def driver_status(self):
        pass

    def get_elements_by_css(self, css: str):
        ic.ic(f"Searching for: {css=}")
        return self.driver.find_element(By.CSS_SELECTOR, css)

    def get_element_by_xpath(self, xpath: str):
        ic.ic(f"Searching for: {xpath=}")
        return self.driver.find_element(By.XPATH, xpath)

    def get_elements_by_id(self, id: str):
        ic.ic(f"Searching for: {id=}")
        return self.driver.find_elements(By.ID, id)

    def get_elements_by_class(self, class_name: str):
        ic.ic(f"Searching for: {class_name=}")
        return self.driver.find_elements(By.CLASS_NAME, class_name)

    def scroll_to_the_end(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        ic.ic("Scrolling to the end of the page")
