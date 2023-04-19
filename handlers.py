"""
Модуль обработки сообщений
"""

from loader import *

import states
import other_func
import keyboards

import sqlite3 as sq

# объект основной клавиатуры
main_markup = keyboards.MainKeyboard.main_keyboard()

@dp.message_handler(commands=["start"])
async def start(message):
    mess = f"Привет <b>{message.from_user.first_name}</b>, ваш id: {message.chat.id}\n\nВыберите функцию"
    #  создаем основную клавиатуру
    await bot.send_message(message.chat.id, mess, parse_mode="html", reply_markup=main_markup)

    # добавляем id и name пользователя в таблицу id_telegramm в БД, если id отсутствует в указанной таблице
    with sq.connect("people.db") as con:
        cur = con.cursor()
        if message.chat.id not in [elem[0] for elem in cur.execute(f"SELECT id_t FROM id_telegramm").fetchall()]:
            cur.execute(
                f"INSERT INTO id_telegramm (id_t, name_t) VALUES ({message.chat.id}, '{message.from_user.first_name}')")

@dp.message_handler(commands=["id"])
async def get_id(message):
    await bot.send_message(message.chat.id, f"Ваш id {message.chat.full_name}: <b>\n{message.chat.id}</b>", parse_mode='html')



@dp.message_handler(content_types=["text"])
async def callback_1(message):
    # вызов команд через обычную клавиатуру
    if message.chat.type == "private":  # дальнейший код выполняется, если чат приватный
        if message.text.lower() == "привет":
            await bot.send_message(message.chat.id, f"И вам привет, выберите интересующую Вас функцию", parse_mode='html', reply_markup=main_markup)
        elif message.text.lower() == "💵финансы":
            await bot.send_message(message.chat.id, f"Получение данных, ожидайте...", parse_mode='html')
            await bot.send_message(message.chat.id, f"""$ <b>{other_func.Parser.content_usd_rub()}</b>
€ <b>{other_func.Parser.content_eur_rub()}</b>
Нефть Brent: <b>{other_func.Parser.content_oil_brent()}</b>
Индекс S&P 500: <b>{other_func.Parser.content_spx()}</b>
Индекс Мосбиржи: <b>{other_func.Parser.content_imoex()}</b>
\nИсточник: https://mfd.ru""", parse_mode='html')
        elif message.text.lower() == "⛅погода":
            await bot.send_message(message.chat.id, f"""Погода в Краснодаре: {other_func.Parser.content_weather()}\n
Источник: https://www.gismeteo.ru/weather-krasnodar-5136/now""", parse_mode='html')
        elif message.text.lower() == "🇬🇧перевод":
            await bot.send_message(message.chat.id, f'''<b>Переход в состояние переводчика...</b>

Для перевода отдельного слова - введите слово:''', parse_mode='html')
            await states.Translation.text_input.set()  # переход в состояние ввода слова для перевода


        elif message.text.lower() == "возврат в главное меню":
            await bot.send_message(message.chat.id, f"Выберите функцию", parse_mode="html", reply_markup=main_markup)


        # реализация опции событий
        elif message.text.lower() == "события":
            markup = keyboards.MainKeyboard.events()
            await bot.send_message(message.chat.id, 'Выберите событие', parse_mode='html', reply_markup=markup)

        elif message.text.lower() == "🎁дни рождения":
            markup = keyboards.MainKeyboard.birthdays()
            await bot.send_message(message.chat.id, f'''<b>Переход в состояние поиска Дней Рождений...</b>

- для вывода информации о дне рождения - введите имя и фамилию или просто имя.

- для вывода всего списка - введите: "Все дни рождения."''', parse_mode='html', reply_markup=markup)
            await states.Birthday.name_input.set()  # переход в состояние ввода имени именинника

        elif message.text.lower() == "Годовщины":
            pass

        elif message.text.lower() in other_func.Person.create_names():
            await bot.send_message(message.chat.id, f"Для вывода информации о Днях Рождениях воспользуйтесь соответсвующее функцией", parse_mode='html')



        # реализация опции калькулятора
        elif message.text.lower() == "🧮калькулятор":
            await bot.send_message(message.chat.id, f'''<b>Переход в состояние 🧮Калькулятора...</b>

Допускаются пробелы, а также "." или "," для дробных чисел.

Примеры доступных операций:
5 + 5 (сложение)
5,6 - 4,6 (вычитание)
5,5 * 5 (умножение)
10.5 / 5.5 (деление)
2 ** 3 (возведение в степень)
9 ** 0.5 (квадратный корень)
10 // 3 (целочисленное деление)
10 % 3 (остаток от деления)''', parse_mode='html')
            await states.Calculator.nums_input.set()  # переход в состояние ввода имени цифр для операции калькулятора


        elif message.text.lower() == "🤖chatgpt":
            markup = keyboards.MainKeyboard.chat_gpt()
            await bot.send_message(message.chat.id, f"<b>Переход в состояние 🤖ChatGPT...</b>\n\nНапишите что-нибудь, 🤖ChatGPT готов ответить", parse_mode='html', reply_markup=markup)
            await states.ChatGPT.nums_input.set()  # переход в состояние ChatGPT


        # создаем инлайновую клавиатуру, если ввели неизвестную команду
        else:
            markup = keyboards.InlineKeyboard.inline_keyboard()
            await bot.send_message(message.chat.id, f"Неизвестная команда.\nВведите корректную команду:", reply_markup=markup)



# вызов команд через инлайновую клавиатуру  ############################################################################
@dp.callback_query_handler(text_startswith="q")
async def callback_2(call: types.callback_query):
    if call.data == "q1":
        await bot.send_message(call.message.chat.id, f"Получение данных, ожидайте...", parse_mode='html')
        await bot.send_message(call.message.chat.id, f"""$ <b>{other_func.Parser.content_usd_rub()}</b>
€ <b>{other_func.Parser.content_eur_rub()}</b>
Нефть Brent: <b>{other_func.Parser.content_oil_brent()}</b>
Индекс S&P 500: <b>{other_func.Parser.content_spx()}</b>
Индекс Мосбиржи: <b>{other_func.Parser.content_imoex()}</b>
\nИсточник: https://ru.investing.com""", parse_mode='html')
    elif call.data == "q2":
        await bot.send_message(call.message.chat.id, f"""Погода в Краснодаре: {other_func.Parser.content_weather()}\n
Источник: https://www.gismeteo.ru/weather-krasnodar-5136/now""", parse_mode='html')
    elif call.data == "q3":
        await bot.send_message(call.message.chat.id, f'''<b>Переход в состояние переводчика...</b>

Для перевода отдельного слова - введите слово:''', parse_mode='html')
        await states.Translation.text_input.set()  # переход в состояние ввода слова для перевода
    elif call.data == "q4":
        await bot.send_message(call.message.chat.id, f'''<b>Переход в состояние ДР...</b>

Для вывода информации о дне рождения - введите имя:\n\nДля вывода всего списка - введите: "все ДР."''',
                               parse_mode='html')
        await states.Birthday.name_input.set()  # переход в состояние ДР
    elif call.data == "q5":
        await bot.send_message(call.message.chat.id, f'''<b>Переход в состояние калькулятора...</b>

Допускаются пробелы, а также "." или "," для дробных чисел.

Примеры доступных операций:
5 + 5 (сложение)
5,6 - 4,6 (вычитание)
5,5 * 5 (умножение)
10.5 / 5.5 (деление)
2 ** 3 (возведение в степень)
9 ** 0.5 (квадратный корень)
10 // 3 (целочисленное деление)
10 % 3 (остаток от деления)''', parse_mode='html')
        await states.Calculator.nums_input.set()  # переход в состояние ввода имени цифр для операция калькулятора