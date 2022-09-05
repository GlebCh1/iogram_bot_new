from datetime import date


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


# создаем список объектов класса Person
lst_person = [Person("Глеб", ["25", "05", "1989"]),
              Person("Аня", ["16", "09", "1988"]),
              Person("Никита", ["27", "09", "1987"]),
              Person("Рита", ["17", "06", "1992"]),
              Person("Мама", ["08", "04", "1961"]),
              Person("Папа", ["03", "01", "1966"]),
              Person("Ксюша", ["12", "01", "2001"]),
              Person("Стас", ["22", "04", "1994"]),
              Person("Данил", ["08", "07", "2016"]),
              Person("Марк", ["04", "08", "2014"]),
              Person("Татьяна Петровна", ["13", "09", "1955"])]

# словарь со сслыкой на объекты класса Person (создан для дальнешего поиска с учетом различных примеров ввода)
dict_obj = {("глеб", "глебчик"): lst_person[0],
            ("анна", "аня", "анечка"): lst_person[1],
            ("никита",): lst_person[2],
            ("рита",): lst_person[3],
            ("мама", "ольга", "ольга ивановна"): lst_person[4],
            ("папа", "александр", "батюшка", "отец александр"): lst_person[5],
            ("ксюша", "ксения"): lst_person[6],
            ("стас",): lst_person[7],
            ("даня", "данил"): lst_person[8],
            ("марк",): lst_person[9],
            ("татьяна петровна",): lst_person[10]}

# в names распаковываются и хранятся в виде списка все имена (ключи) из dict_obj
names = [elem for key in dict_obj for elem in key]
pass

