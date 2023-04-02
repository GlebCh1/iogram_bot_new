from loader import *

import states
import other_func
import keyboards

import sqlite3 as sq

# ОБРАБОТЧИКИ СООБЩЕНИЙ  ###############################################################################################
@dp.message_handler(commands=["start"])
async def start(message):
    mess = f'''Привет <b>{message.from_user.first_name}</b>, ваш id: {message.chat.id}\n\nВведите корректную команду, например:\n\n"финансы"\n"погода"\n"перевод\n"ДР".\n
Для просмотра доступных команд - введите любой символ.'''

    #  создаем основную клавиатуру
    markup = keyboards.MainKeyboard.main_keyboard()
    await bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)

    # добавляем id и name пользователя в таблицу id_telegramm в БД, если id отсутствует в указанной таблице
    with sq.connect("people.db") as con:
        cur = con.cursor()
        if message.chat.id not in [elem[0] for elem in cur.execute(f"SELECT id_t FROM id_telegramm").fetchall()]:
            cur.execute(
                f"INSERT INTO id_telegramm (id_t, name_t) VALUES ({message.chat.id}, '{message.from_user.first_name}')")


@dp.message_handler(content_types=["text"])
async def callback_1(message):
    # вызов команд через обычную клавиатуру
    if message.chat.type == "private":  # дальнейший код выполняется, если чат приватный
        if message.text.lower() in ["id", "узнать id", "мой id"]:
            await bot.send_message(message.chat.id, f"твой id: {message.chat.id}", parse_mode='html')
        elif message.text.lower() == "привет":
            await bot.send_message(message.chat.id, f'''И вам привет, введите корректную команду, например:
\n"финансы"\n"погода"\n"перевод\n"ДР".
\nДля просмотра доступных команд - введите любой символ.
Для создания основной клавиатуры - введите: /start''', parse_mode='html')
        elif message.text.lower() in ["💵финансы", "финансы", "/финансы"]:
            await bot.send_message(message.chat.id, f"Получение данных, ожидайте...", parse_mode='html')
            await bot.send_message(message.chat.id, f"""$ <b>{other_func.Parser.content_usd_rub()}</b>
€ <b>{other_func.Parser.content_eur_rub()}</b>
Нефть Brent: <b>{other_func.Parser.content_oil_brent()}</b>
Индекс S&P 500: <b>{other_func.Parser.content_spx()}</b>
Индекс Мосбиржи: <b>{other_func.Parser.content_imoex()}</b>
\nИсточник: https://mfd.ru""", parse_mode='html')
        elif message.text.lower() in ["⛅погода", "погода", "/погода", "погода краснодар", "погода в краснодаре"]:
            await bot.send_message(message.chat.id, f"""Погода в Краснодаре: {other_func.Parser.content_weather()}\n
Источник: https://www.gismeteo.ru/weather-krasnodar-5136/now""", parse_mode='html')
        elif message.text.lower() in ["🇬🇧перевод", "перевод"]:
            await bot.send_message(message.chat.id, f'''<b>Переход в состояние переводчика...</b>

Для перевода отдельного слова - введите слово:''', parse_mode='html')
            await states.Translation.text_input.set()  # переход в состояние ввода слова для перевода

        # реализация модуля с ДР
        elif message.text.lower() in ["🎁др", "др", "/др"]:
            await bot.send_message(message.chat.id, f'''<b>Переход в состояние ДР...</b>

Для вывода информации о дне рождения - введите имя:\n\nДля вывода всего списка - введите: "все ДР."''',
                                   parse_mode='html')
            await states.Birthday.name_input.set()  # переход в состояние ввода имени именинника

        elif message.text.lower() in other_func.Person.create_names():
            await bot.send_message(message.chat.id,
                                   f'Для вывода информации о дне рождения - введите "ДР" или воспользуйтесь соотвествующей кнопкой.\n\nДля вывода всего списка - введите: "все ДР".',
                                   parse_mode='html')

        elif message.text.lower() == "все др":
            for elem in sorted(other_func.Person.create_person(message.text.lower()),
                               key=lambda x: x.birthday.split(".")[1]):  # сортировка
                await bot.send_message(message.chat.id,
                                       f"<b>{elem.name}</b>\n{elem.birthday}\nвозраст: {elem.get_age()}",
                                       parse_mode='html')
        elif message.text.lower() == "события":
            markup = keyboards.MainKeyboard.events()
            await bot.send_message(message.chat.id, 'Выберите событие', parse_mode='html', reply_markup=markup)

        # реализация модуля с калькулятором
        elif message.text.lower() in ["🧮калькулятор", "калькулятор"]:
            await bot.send_message(message.chat.id, f'''<b>Переход в состояние калькулятора...</b>

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