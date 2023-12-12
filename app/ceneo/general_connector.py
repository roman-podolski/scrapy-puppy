from typing import Optional
from app.logs.api_logger import logger
from bs4 import BeautifulSoup, PageElement, ResultSet
import requests
import pandas as pd

text = requests.get('https://www.ceneo.pl/2674616')


def ddd(clasa: str):
    print(clasa.replace(" ", "."))
    return clasa.replace(" ", ".")


def get_ceneo_info(url: str) -> pd.DataFrame:
    text = requests.get(url)
    dane = []
    soup = BeautifulSoup(text.content, 'html.parser')
    offers = soup.find_all("li", attrs={"class": "product-offers__list__item js_productOfferGroupItem"})
    for offer in offers:
        offer_detail = {}
        name = offer.find("span", attrs={'class': 'short-name__txt'}).text
        price = offer.find("a", attrs={'class': 'product-price go-to-shop'})
        if price:
            price = price.find("span", attrs={'class': 'price-format nowrap'}).text.replace("zł", "").replace(" ", "")
        seller_name = offer.find("li", attrs={'class': 'offer-shop-opinions'}).text
        if seller_name:
            seller_name = seller_name.replace("\n", "").replace("Dane i opinie o ", "")

        offer_detail['name'] = name
        offer_detail['price'] = price
        offer_detail['seller_name'] = seller_name
        dane.append(offer_detail)
    data = pd.DataFrame(dane)
    return data

class CeneoInfoById:
    def __init__(self, url: str):
        self.url = url
        self.page_content: BeautifulSoup = self.get_page_content()

    def get_page_content(self) -> BeautifulSoup:

        if "ceneo" not in self.url:
            raise ValueError("This is not ceneo url")

        text = requests.get(self.url)
        soup = BeautifulSoup(text.content, 'html.parser')
        return soup

    def get_page_info(self) -> pd.DataFrame:
        offers: ResultSet = self.page_content.find_all("li", attrs={"class": "product-offers__list__item js_productOfferGroupItem"})
        frame: pd.DataFrame = pd.DataFrame()
        for offer in offers:
            offer_detail = {}
            name = self.get_product_name(offer)
            price = self.get_product_price(offer)
            seller_name = self.get_seller_name(offer)
            availability = self.get_product_availability(offer)
            delivery_price = self.delivery_price(offer)
            # go_to_shop_url = self.get_go_to_shop_url(offer)

            offer_detail['name'] = name
            offer_detail['price'] = price
            offer_detail['seller_name'] = seller_name
            offer_detail['availability'] = availability
            offer_detail['delivery_price'] = delivery_price
            # offer_detail['go_to_shop_url'] = go_to_shop_url
            offer_detail['is_promoted'] = False
            offer_detail['ceneo_id'] = self.url.split("/")[-1]
            frame = frame._append(offer_detail, ignore_index=True)
        return frame

    def get_product_name(self, result: PageElement) -> Optional[str]:
        product_name = result.find("span", attrs={'class': 'short-name__txt'})
        if not product_name:
            return None
        return product_name.text

    def get_product_price(self, result: PageElement) -> Optional[float]:
        price = result.find("div", attrs={'class': 'product-offer__product__price'})
        if price:
            price = price.find("span", attrs={'class': 'price-format nowrap'}).text.replace("zł", "").replace(" ", "")
            return float(price.replace(",", "."))
        return None

    def get_seller_name(self, result: PageElement) -> Optional[str]:

        seller_name = result.find("li", attrs={'class': 'offer-shop-opinions'})
        if seller_name:
            seller_name = seller_name.text
            seller_name = seller_name.replace("\n", "").replace("Dane i opinie o ", "")
            return seller_name
        return None

    def get_product_availability(self, result: PageElement) -> bool:
        availability = result.find("div", attrs={'class': 'product-availability'})
        if availability:
            availability = availability.text
            if availability and availability.lower().replace("\n","") == "dostępny":
                return True
            return False

    def delivery_price(self, result: PageElement) -> Optional[float]:
        delivery_price = result.find("div", attrs={'class': 'product-offer__product__delivery-section'})
        if delivery_price:
            delivery_price = delivery_price.text
            if "darmowa" in delivery_price.lower():
                return 0.0
            delivery_price = delivery_price.lower().replace("z wysyłką od", "").replace("zł", "").replace("\n", "")
            return float(delivery_price.replace(",", "."))
        return None


    def get_go_to_shop_url(self, result: PageElement) -> Optional[str]:
        url = result.find("a", attrs={'class': 'button button--primary button--flex go-to-shop'})
        if url:
            return url['href']
        return None


obj = CeneoInfoById("https://www.ceneo.pl/89330169")
dane = obj.get_page_info().sort_values(by=['delivery_price'])
avg_price = dane['delivery_price'].median(skipna=True)
dane['price_deviation'] = round((dane['delivery_price'] - avg_price)/avg_price * 100, 2)
print(dane.to_markdown())
print(f"Average price: {avg_price}")

# dane.to_excel("/Users/romanpodolski/Documents/GitHub/scrapy-puppy/app/ceneo/ceneo.xlsx")