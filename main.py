from aiogram import Bot, Dispatcher, executor, types
import config
import my_parser
import other_func
from string import ascii_letters, digits, printable

# FSM import  ##########################################################################################################
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

# FSM  #################################################################################################################
storage = MemoryStorage()
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot, storage=storage)


# реализация FSM для модуля дней рождений
class Birthday(StatesGroup):
    name_input = State()


@dp.message_handler(state=Birthday.name_input)
async def answer_birthday(message, state: FSMContext):
    async def search_for_name():
        for key in other_func.dict_obj:
            if message.text.lower() in key:
                await bot.send_message(message.chat.id,
                                       f"\n{other_func.dict_obj[key].birthday}\nвозраст: {other_func.dict_obj[key].get_age()}",
                                       parse_mode='html')
                await state.finish()  # выход из состояния поиска имени

    if message.text.lower() in other_func.names:
        await search_for_name()
    elif message.text.lower() in ["все др"]:
        for elem in sorted(other_func.lst_person, key=lambda x: x.birthday.split(".")[1]):  # сортировка
            await bot.send_message(message.chat.id, f"{elem.name}\n{elem.birthday}\nвозраст: {elem.get_age()}",
                                   parse_mode='html')
            await state.finish()  # выход из состояния поиска имени
    else:
        await bot.send_message(message.chat.id, f"Указанного имени нет в списке, выход из состояния поиска имени...",
                               parse_mode='html')
        await state.finish()  # выход из состояния поиска имени


# реализация FSM для модуля перевода
class Translation(StatesGroup):
    text_input = State()


@dp.message_handler(state=Translation.text_input)
async def answer_translation(message, state: FSMContext):
    # реализация перевода Ru_En
    if all([True if letter in ascii_letters + digits else False for letter in message.text.lower()]):
        await bot.send_message(message.chat.id,
                               f"https://translate.google.com/?hl=ru&tab=TT&sl=en&tl=ru&text={message.text}&op=translate",
                               parse_mode='html')
        await state.finish()  # выход из состояния поиска имени
    # реализация перевода En_Ru
    elif all([True if letter in "абвгдежзийклмнопрстуфхцчшщъыьэюя" + digits else False for letter in
              message.text.lower()]):
        await bot.send_message(message.chat.id,
                               f"https://translate.google.com/?hl=en&tab=TT&sl=ru&tl=en&text={message.text}&op=translate",
                               parse_mode='html')
        await state.finish()  # выход из состояния поиска имени
    else:
        await bot.send_message(message.chat.id,
                               f"Введены недопустимые символы.\nДопускается вводить только rus или eng буквы, а также цифры.\nВыход из состояния поиска имени...",
                               parse_mode='html')
        await state.finish()


# реализация FSM для модуля калькулятора
class Calculator(StatesGroup):
    nums_input = State()


@dp.message_handler(state=Calculator.nums_input)
async def answer_calculator(message, state: FSMContext):
    try:
        operator = "".join([elem for elem in message.text if elem in ["+", "-", "*", "/", "%"]])
        working_line = message.text.replace(",", ".").split(operator)
        num1, num2 = map(lambda num: int(num.strip()) if "." not in num else float(num.strip()), working_line)
        if operator == "+":
            await bot.send_message(message.chat.id, f"{num1 + num2}\n\n<b>Выход из состояния калькулятора...</b>", parse_mode='html')
        elif operator == "-":
            await bot.send_message(message.chat.id, f"{num1 - num2}\n\n<b>Выход из состояния калькулятора...</b>", parse_mode='html')
        elif operator == "*":
            await bot.send_message(message.chat.id, f"{num1 * num2}\n\n<b>Выход из состояния калькулятора...</b>", parse_mode='html')
        elif operator == "/":
            await bot.send_message(message.chat.id, f"{num1 / num2}\n\n<b>Выход из состояния калькулятора...</b>", parse_mode='html')
        elif operator == "**":
            await bot.send_message(message.chat.id, f"{num1 ** num2}\n\n<b>Выход из состояния калькулятора...</b>", parse_mode='html')
        elif operator == "//":
            await bot.send_message(message.chat.id, f"{num1 // num2}\n\n<b>Выход из состояния калькулятора...</b>", parse_mode='html')
        elif operator == "%":
            await bot.send_message(message.chat.id, f"{num1 % num2}\n\n<b>Выход из состояния калькулятора...</b>", parse_mode='html')
    except ValueError:
        await bot.send_message(message.chat.id, f'''<b>Недопустимый формат ввода значений...</b>
        
Введите значения в формате:
5 + 5 (сложение)
5,6 - 4,6 (вычитание)
5,5 * 5 (умножение)
10.5 / 5.5 (деление)
2 ** 3 (возведение в степень)
9 ** 0.5 (квадратный корень)
10 // 3 (целочисленное деление)
10 % 3 (остаток от деления)

<b>Выход из состояния калькулятора...</b>''', parse_mode='html')
    await state.finish()


# ОСНОВНОЙ КОД  ########################################################################################################
@dp.message_handler(commands=["start"])
async def start(message):
    mess = f'''Привет <b>{message.from_user.first_name}</b>, ваш id: {message.chat.id}\n\nВведите корректную команду, например:\n\n"финансы"\n"погода"\n"перевод\n"ДР".\n
Для просмотра доступных команд - введите любой символ.'''
    #  создаем обычную клавиатуру
    markup = types.ReplyKeyboardMarkup()
    r_btn1 = types.KeyboardButton("💵Финансы")
    r_btn2 = types.KeyboardButton("⛅Погода")
    r_btn3 = types.KeyboardButton("🇬🇧Перевод")
    r_btn4 = types.KeyboardButton("🎁ДР")
    r_btn5 = types.KeyboardButton("🧮Калькулятор")
    markup.add(r_btn1, r_btn2, r_btn3, r_btn4, r_btn5)  # добавляем созданные кнопки
    await bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)


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
            await bot.send_message(message.chat.id, f"""$ <b>{my_parser.Parser.content_usd_rub()}</b>
€ <b>{my_parser.Parser.content_eur_rub()}</b>
Нефть Brent: <b>{my_parser.Parser.content_oil_brent()}</b>
Индекс S&P 500: <b>{my_parser.Parser.content_spx()}</b>
Индекс Мосбиржи: <b>{my_parser.Parser.content_imoex()}</b>
\nИсточник: https://ru.investing.com""", parse_mode='html')
        elif message.text.lower() in ["⛅погода", "погода", "/погода", "погода краснодар", "погода в краснодаре"]:
            await bot.send_message(message.chat.id, f"""Погода в Краснодаре: {my_parser.Parser.content_weather()}\n
Источник: https://www.gismeteo.ru/weather-krasnodar-5136/now""", parse_mode='html')
        elif message.text.lower() in ["🇬🇧перевод", "перевод"]:
            await bot.send_message(message.chat.id, f"Для перевода отдельного слова - введите слово:",
                                   parse_mode='html')
            await Translation.text_input.set()  # переход в состояние ввода слова для перевода

        # реализация модуля с ДР
        elif message.text.lower() in ["🎁др", "др", "/др"]:
            await bot.send_message(message.chat.id,
                                   f'Для вывода информации о дне рождения - введите имя:\n\nДля вывода всего списка - введите: "все ДР."',
                                   parse_mode='html')
            await Birthday.name_input.set()  # переход в состояние ввода имени именниника

        elif message.text.lower() in other_func.names:
            await bot.send_message(message.chat.id,
                                   f'Для вывода информации о дне рождения - введите "ДР" или воспользуйтесь соотвествующей кнопкой.\n\nДля вывода всего списка - введите: "все ДР".',
                                   parse_mode='html')

        elif message.text.lower() == "все др":
            for elem in sorted(other_func.lst_person, key=lambda x: x.birthday.split(".")[1]):  # сортировка
                await bot.send_message(message.chat.id, f"{elem.name}\n{elem.birthday}\nвозраст: {elem.get_age()}",
                                       parse_mode='html')

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
            await Calculator.nums_input.set()  # переход в состояние ввода имени цифр для операция калькулятора

        # cоздаем инлайновую клавиатуру, если ввели неизвестную команду
        else:
            markup = types.InlineKeyboardMarkup(row_width=3)
            btn1 = types.InlineKeyboardButton("💵Финансы", callback_data="q1")
            btn2 = types.InlineKeyboardButton("⛅Погода", callback_data="q2")
            btn3 = types.InlineKeyboardButton("🇬🇧Перевод", callback_data="q3")
            btn4 = types.InlineKeyboardButton("🎁ДР", callback_data="q4")
            btn5 = types.KeyboardButton("🧮Калькулятор", callback_data="q5")
            markup.add(btn1, btn2, btn3, btn4, btn5)  # добавляем кнопки
            await bot.send_message(message.chat.id, f"Неизвестная команда.\nВведите корректную команду:",
                                   reply_markup=markup)


# вызов команд через инлайновую клавиатуру
@dp.callback_query_handler(text_startswith="q")
async def callback_2(call: types.callback_query):
    if call.data == "q1":
        await bot.send_message(call.message.chat.id, f"Получение данных, ожидайте...", parse_mode='html')
        await bot.send_message(call.message.chat.id, f"""$ <b>{my_parser.Parser.content_usd_rub()}</b>
€ <b>{my_parser.Parser.content_eur_rub()}</b>
Нефть Brent: <b>{my_parser.Parser.content_oil_brent()}</b>
Индекс S&P 500: <b>{my_parser.Parser.content_spx()}</b>
Индекс Мосбиржи: <b>{my_parser.Parser.content_imoex()}</b>
\nИсточник: https://ru.investing.com""", parse_mode='html')
    elif call.data == "q2":
        await bot.send_message(call.message.chat.id, f"""Погода в Краснодаре: {my_parser.Parser.content_weather()}\n
Источник: https://www.gismeteo.ru/weather-krasnodar-5136/now""", parse_mode='html')
    elif call.data == "q3":
        await bot.send_message(call.message.chat.id, f"Для перевода отдельного слова - введите слово:",
                               parse_mode='html')
        await Translation.text_input.set()  # переход в состояние ввода слова для перевода
    elif call.data == "q4":
        await bot.send_message(call.message.chat.id,
                               f'Для вывода информации о дне рождения - введите имя:\n\nДля вывода всего списка - введите: "все ДР."',
                               parse_mode='html')
        await Birthday.name_input.set()
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
        await Calculator.nums_input.set()  # переход в состояние ввода имени цифр для операция калькулятора


executor.start_polling(dp)
