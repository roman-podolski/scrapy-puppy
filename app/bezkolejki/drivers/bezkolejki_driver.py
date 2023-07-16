from typing import Optional, List, Dict, Union, Any
from app.bezkolejki.drivers import selenium_driver as sd
from time import sleep
from selenium.webdriver.common.by import By
import icecream as ic


class MainPageLocators(object):

    BASE_LINK = "https://www.bezkolejki.eu/luwlodz"
    NEXT_BUTTON = '//*[@id="form-wizard"]/div[3]/div/div/div/button'
    LIST_OF_CHOICE = '//*[@id="form-wizard"]/div[2]/div[2]'


class BezkolejkiDriver(sd.SeleniumBaseFields, MainPageLocators):
    list_of_menu: List[str]

    def __init__(self, with_headless: bool = True):
        super().__init__(base_link=self.BASE_LINK,
                         with_headless=with_headless)

    def get_reservation_menu(self):
        page_menu_choice = self.get_element_by_xpath(self.LIST_OF_CHOICE)
        self.list_of_menu = list(page_menu_choice.text.split("\n"))
        return [elem.lower() for elem in self.list_of_menu]

    def click_reservation_choice(self, choice: int):
        if choice < 1:
            choice = 1
        elif choice > 9:
            choice = 9
        ic.ic(f"Choice: {self.list_of_menu[choice]} selected")
        elem = self.get_element_by_xpath(f'//*[@id="Operacja2"]/div[{choice}]/div/div/button')
        if elem:
            elem.click()
            sleep(10)
        else:
            ic.ic("There is no such element")
    def click_next_button(self):
        next_button = self.get_element_by_xpath(self.NEXT_BUTTON)
        if next_button:
            next_button.click()
            ic.ic("Next button clicked")
            sleep(2)
        else:
            ic.ic("There is no next button")

    def calendar_screenshot(self):
        self.get_element_by_xpath('//*[@id="Dataiczas3"]/div/div[1]/div[2]').screenshot("calendar.png")

    def main(self):
        list_of_choice = self.get_reservation_menu()

# //*[@id="Operacja2"]/div[1]/div/div/button

dd = BezkolejkiDriver()
lista = dd.get_reservation_menu()
dd.click_reservation_choice(1)
dd.scroll_to_the_end()
dd.click_next_button()
dd.calendar_screenshot()

