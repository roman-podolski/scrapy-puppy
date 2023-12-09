from typing import Optional, List, Dict, Union, Any
from app.bezkolejki.drivers import selenium_driver as sd
from time import sleep
from selenium.webdriver.common.by import By
import icecream as ic
from datetime import datetime, time
import os
from bs4 import BeautifulSoup
# soup = BeautifulSoup(html_doc, 'html.parser')

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


    def is_free_visit(self):
        reservation_elem = self.get_element_by_xpath('//*[@id="Dataiczas3"]/div/div[1]/div[1]/div/h5')
        reservation_text = reservation_elem.text.lower()
        if "brak" in reservation_text:
            ic.ic(f"There is no free visit: {reservation_text}")
            return False
        else:
            ic.ic(f"There is free visit: {reservation_text}")
            return True

    def calendar_screenshot(self):
        screenshot_name = f"calendar {datetime.now()}"

        self.get_element_by_xpath('//*[@id="Dataiczas3"]/div/div[1]/div[2]').\
            screenshot(f"screenshots/{str(screenshot_name)}.png")

        if os.path.exists(f"screenshots/{str(screenshot_name)}.png"):
            ic.ic(f"Screenshot {screenshot_name} saved")
        else:
            ic.ic(f"Screenshot {screenshot_name} not saved")

    def print_free_visits_dates(self):
        calendar_box = self.get_elements_by_xpath("//span[@aria-disabled='false']")
        free_dates = []
        for date in calendar_box:
            free_date = date.click()
            self.driver.get(free_date)
            ic.ic(free_date)
            free_dates.append(free_date)
        ic.ic(f"Poszło {free_dates}")


def main():
    dd = BezkolejkiDriver()
    dd.get_reservation_menu()
    dd.click_reservation_choice(4)
    dd.scroll_to_the_end()
    dd.click_next_button()
    if dd.is_free_visit():
        dd.calendar_screenshot()
    dd.print_free_visits_dates()


if __name__ == "__main__":
    main()


