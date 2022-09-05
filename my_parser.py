import requests
from bs4 import BeautifulSoup

URL_1_usd_rub = "https://ru.investing.com/currencies/usd-rub"
URL_2_eur_rub = "https://ru.investing.com/currencies/eur-rub"
URL_3_oil_brent = "https://ru.investing.com/commodities/brent-oil"
URL_4_spx = "https://ru.investing.com/indices/us-spx-500"
URL_5_imoex = "https://ru.investing.com/indices/mcx"
URL_6_weather = "https://www.gismeteo.ru/weather-krasnodar-5136/now"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}


class Parser:

    @staticmethod
    def content_usd_rub():
        html = requests.get(URL_1_usd_rub, headers=HEADERS).text
        soup = BeautifulSoup(html, 'html.parser')
        item_1 = soup.find('span', class_='text-2xl')
        usd_rub = item_1.text
        return usd_rub

    @staticmethod
    def content_eur_rub():
        html = requests.get(URL_2_eur_rub, headers=HEADERS).text
        soup = BeautifulSoup(html, 'html.parser')
        item_1 = soup.find('span', class_='text-2xl')
        eur_rub = item_1.text
        return eur_rub

    @staticmethod
    def content_oil_brent():
        html = requests.get(URL_3_oil_brent, headers=HEADERS).text
        soup = BeautifulSoup(html, 'html.parser')
        item_1 = soup.find('span', class_='text-2xl')
        oil_brent = item_1.text
        return oil_brent

    @staticmethod
    def content_spx():
        html = requests.get(URL_4_spx, headers=HEADERS).text
        soup = BeautifulSoup(html, 'html.parser')
        item_1 = soup.find('span', class_='text-2xl')
        spx = item_1.text
        return spx

    @staticmethod
    def content_imoex():
        html = requests.get(URL_5_imoex, headers=HEADERS).text
        soup = BeautifulSoup(html, 'html.parser')
        item_1 = soup.find('span', class_='text-2xl')
        imoex = item_1.text
        return imoex

    @staticmethod
    def content_weather():
        html = requests.get(URL_6_weather, headers=HEADERS).text
        soup = BeautifulSoup(html, 'html.parser')
        item_1 = soup.find('span', class_='unit unit_temperature_c')
        item_2 = soup.find('a', class_='weathertab weathertab-block tooltip')
        weather = f"""{item_1.text.strip()}
{item_2.attrs['data-text']}"""
        return weather.lower()
