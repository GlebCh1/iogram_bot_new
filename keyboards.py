"""
Модуль управления клавиатурами
"""

from loader import types


# класс управления основной клавиатурой
class MainKeyboard:

    @staticmethod
    def main_keyboard() -> types.ReplyKeyboardMarkup:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, is_persistent=True)
        btn1 = types.KeyboardButton("💵Финансы")
        btn2 = types.KeyboardButton("⛅Погода")
        btn3 = types.KeyboardButton("🇬🇧Перевод")
        btn4 = types.KeyboardButton("События")
        btn5 = types.KeyboardButton("🧮Калькулятор")
        btn6 = types.KeyboardButton("🤖ChatGPT")
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6)  # добавляем созданные кнопки в разметку (markup)
        return markup

    @staticmethod
    def events() -> types.ReplyKeyboardMarkup:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, is_persistent=True)
        btn1 = types.KeyboardButton("🎁Дни рождения")
        btn2 = types.KeyboardButton("Годовщины")
        btn3 = types.KeyboardButton("Дни памяти")
        btn4 = types.KeyboardButton("Прочие события")
        btn5 = types.KeyboardButton("Возврат в главное меню")
        markup.add(btn1, btn2, btn3, btn4, btn5)  # добавляем созданные кнопки в разметку (markup)
        return markup

    @staticmethod
    def birthdays() -> types.ReplyKeyboardMarkup:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, is_persistent=True)
        btn1 = types.KeyboardButton("Все дни рождения")
        btn2 = types.KeyboardButton("Выход из состояния / возврат в главное меню")
        markup.add(btn1, btn2)  # добавляем созданные кнопки в разметку (markup)
        return markup

    @staticmethod
    def chat_gpt() -> types.ReplyKeyboardMarkup:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, is_persistent=True)
        btn1 = types.KeyboardButton("Назначение системной роли ChatGPT")
        btn2 = types.KeyboardButton("Выход из состояния / возврат в главное меню")
        markup.add(btn1, btn2)  # добавляем созданные кнопки в разметку (markup)
        return markup

    @staticmethod
    def chat_gpt_system_role():
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, is_persistent=True)
        btn1 = types.KeyboardButton("Информация о текущей системной роли")
        btn2 = types.KeyboardButton("Возврат системной роли, используемой по-умолчанию")
        btn3 = types.KeyboardButton("Выход из состояния / возврат в предыдущее меню")
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