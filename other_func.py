from datetime import date
import sqlite3 as sq

import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup


# парсинг данных
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



# класс для реализации модуля дней рождений
class Person:

    def __init__(self, name, birthday):
        self.__name = name
        self.__birthday = birthday
        if date.today().month > int(birthday[1]):
            self.__age = date.today().year - int(birthday[2])
        elif date.today().month < int(birthday[1]):
            self.__age = date.today().year - int(birthday[2]) - 1
        else:
            if date.today().day >= int(birthday[0]):
                self.__age = date.today().year - int(birthday[2])
            else:
                self.__age = date.today().year - int(birthday[2]) - 1

    @property
    def name(self):
        return self.__name

    @property
    def birthday(self):
        return ".".join(self.__birthday)

    def get_age(self):
        return self.__age

    # получение в виде списка всех имен из таблицы p1 (БД people.db)
    @staticmethod
    def create_names() -> list:
        """
        Возвращает список имен (name) и псевдонимов(other_name) из БД (таблица p1)
        :return: ['аня', 'анна', 'анечка', 'никита', 'рита', 'маргарита'...]
        """
        with sq.connect("people.db") as con:
            cur = con.cursor()
            names = [name.split(", ") for elem in cur.execute("SELECT other_name FROM p1").fetchall() for name in elem]
            return [name for elem in names for name in elem]

    @classmethod
    def create_person(cls, mes: str):
        """
        Обращение к БД (таблица p1) для последующего создания объекта класса Person и вывода информации
        об имени, др и возрасте
        :param mes: message.text.lower()
        :return: Person()
        """
        with sq.connect("people.db") as con:
            cur = con.cursor()
            if mes == "все др":
                return [Person(elem[0], elem[1].split(".")) for elem in
                        cur.execute(f"SELECT name, birthdate FROM p1").fetchall()]
            else:
                for _id in cur.execute(f"SELECT id FROM p1").fetchall():
                    name, other_name, birthdate = cur.execute(f"SELECT name, other_name, birthdate FROM p1 WHERE id = {_id[0]}").fetchall()[0]
                    if mes in [name, *other_name.split(", ")]:
                        return cls(name, birthdate.split("."))
