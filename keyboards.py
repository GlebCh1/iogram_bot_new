"""
Модуль управления клавиатурами
"""

from loader import types

# класс управления основной клавиатурой
class MainKeyboard:

    @staticmethod
    def main_keyboard() -> types.ReplyKeyboardMarkup:
        markup = types.ReplyKeyboardMarkup()
        btn1 = types.KeyboardButton("💵Финансы")
        btn2 = types.KeyboardButton("⛅Погода")
        btn3 = types.KeyboardButton("🇬🇧Перевод")
        btn4 = types.KeyboardButton("События")
        btn5 = types.KeyboardButton("🧮Калькулятор")
        markup.add(btn1, btn2, btn3, btn4, btn5)  # добавляем созданные кнопки в разметку (markup)
        return markup

    @staticmethod
    def events():
        markup = types.ReplyKeyboardMarkup()
        btn1 = types.KeyboardButton("🎁Дни рождения")
        btn2 = types.KeyboardButton("Годовщины")
        btn3 = types.KeyboardButton("Прочие события")
        markup.add(btn1, btn2, btn3)  # добавляем созданные кнопки в разметку (markup)
        return markup

# класс управления инлайновой клавиатурой
class InlineKeyboard:

    @staticmethod
    def inline_keyboard() -> types.InlineKeyboardMarkup():
        markup = types.InlineKeyboardMarkup(row_width=3)
        btn1 = types.InlineKeyboardButton("💵Финансы", callback_data="q1")
        btn2 = types.InlineKeyboardButton("⛅Погода", callback_data="q2")
        btn3 = types.InlineKeyboardButton("🇬🇧Перевод", callback_data="q3")
        btn4 = types.InlineKeyboardButton("События", callback_data="q4")
        btn5 = types.KeyboardButton("🧮Калькулятор", callback_data="q5")
        markup.add(btn1, btn2, btn3, btn4, btn5)  # добавляем созданные кнопки в разметку (markup)
        return markup