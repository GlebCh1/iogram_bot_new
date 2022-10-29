import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

URL_1_usd_rub = "https://mfd.ru/marketdata/ticker/?id=2287"
URL_2_eur_rub = "https://mfd.ru/marketdata/ticker/?id=2282"
URL_3_oil_brent = "https://mfd.ru/marketdata/ticker/?id=1*"
URL_4_spx = "https://mfd.ru/marketdata/ticker/?id=1977"
URL_5_imoex = "https://mfd.ru/marketdata/ticker/?id=140335"
URL_6_weather = "https://www.gismeteo.ru/weather-krasnodar-5136/now"
USER = {"user-agent": UserAgent().random}


class Parser:
    @staticmethod
    def all_quotes(html):
        soup = BeautifulSoup(html, 'html.parser')
        item_1 = soup.find('div', class_='m-companytable-last')
        quote = item_1.text
        return quote

    @classmethod
    def content_usd_rub(cls):
        html = requests.get(URL_1_usd_rub, headers=USER).text
        return cls.all_quotes(html)

    @classmethod
    def content_eur_rub(cls):
        html = requests.get(URL_2_eur_rub, headers=USER).text
        return cls.all_quotes(html)

    @classmethod
    def content_oil_brent(cls):
        html = requests.get(URL_3_oil_brent, headers=USER).text
        return cls.all_quotes(html)

    @classmethod
    def content_spx(cls):
        html = requests.get(URL_4_spx, headers=USER).text
        return cls.all_quotes(html)

    @classmethod
    def content_imoex(cls):
        html = requests.get(URL_5_imoex, headers=USER).text
        return cls.all_quotes(html)

    @staticmethod
    def content_weather():
        html = requests.get(URL_6_weather, headers=USER).text
        soup = BeautifulSoup(html, 'html.parser')
        item_1 = soup.find('span', class_='unit unit_temperature_c')
        item_2 = soup.find('a', class_='weathertab weathertab-block tooltip')
        weather = f"""{item_1.text.strip()}
{item_2.attrs['data-text']}"""
        return weather.lower()


# a = Parser.content_usd_rub()
# b = Parser.content_eur_rub()
# c = Parser.content_imoex()
# d = Parser.content_spx()
# e = Parser.content_oil_brent()
# pass
# pass
# pass