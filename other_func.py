from datetime import date
import sqlite3 as sq


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
    def create_names():
        with sq.connect("people.db") as con:
            cur = con.cursor()
            names = [name.split(",") for elem in cur.execute("SELECT other_name FROM p1").fetchall() for name in elem]
            return [name for elem in names for name in elem]

    # обращение к таблице p1 (БД people.db) для последующего создания объекта класса Person и вывода информации
    # об имени, др и возрасте
    @classmethod
    def create_person(cls, mes):
        with sq.connect("people.db") as con:
            cur = con.cursor()
            if mes in ["все др"]:
                return [Person(elem[0], elem[1].split(".")) for elem in
                        cur.execute(f"SELECT name, birthdate FROM p1").fetchall()]
            else:
                for _id in cur.execute(f"SELECT id FROM p1").fetchall():
                    name, other_name, birthdate = cur.execute(f"SELECT name, other_name, birthdate FROM p1 WHERE id = {_id[0]}").fetchall()[0]
                    if mes in [name, *other_name.split(",")]:
                        return cls(name, birthdate.split("."))
