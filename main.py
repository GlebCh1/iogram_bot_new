from aiogram import Bot, Dispatcher, executor, types
import config
import my_parser
import other_func
import fsm
from string import ascii_letters


# FSM import  ##########################################################################################################
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State


# FSM  #################################################################################################################
storage = MemoryStorage()
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot, storage=storage)


class Birthday(StatesGroup):
    name_input = State()


@dp.message_handler(state=Birthday.name_input)
async def answer_dr(message, state: FSMContext):
    async def search_for_name():
        for key in other_func.dict_obj:
            if message.text.lower() in key:
                await bot.send_message(message.chat.id,
                                       f"\n{other_func.dict_obj[key].birthday}\nвозраст: {other_func.dict_obj[key].get_age()}",
                                       parse_mode='html')
                await state.finish()  # выход из состояния поиска имени

    if message.text.lower() in other_func.names:
        await search_for_name()
    elif message.text.lower() not in other_func.names:
        await bot.send_message(message.chat.id, f"Указанного имени нет в списке, выход из состояния поиска имени...", parse_mode='html')
        await state.finish()  # выход из состояния поиска имени


########################################################################################################################
@dp.message_handler(commands=["start"])
async def start(message):
    mess = f'''Привет <b>{message.from_user.first_name}</b>, ваш id: {message.chat.id}\n\nВведите корректную команду, например:\n\n"финансы"\n"погода"\n"перевод\n"ДР".\n
Для просмотра доступных комманд - введите любой символ.'''
    #  создаем обычную клавиатуру
    markup = types.ReplyKeyboardMarkup()
    r_btn1 = types.KeyboardButton("Финансы")
    r_btn2 = types.KeyboardButton("Погода")
    r_btn3 = types.KeyboardButton("Перевод")
    r_btn4 = types.KeyboardButton("ДР")
    markup.add(r_btn1, r_btn2, r_btn3, r_btn4)  # добавляем созданные кнопки
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
\nДля просмотра доступных команд - введите любой символ.''', parse_mode='html')
        elif message.text.lower() in ["финансы", "/финансы"]:
            await bot.send_message(message.chat.id, f"Получение данных, ожидайте...", parse_mode='html')
            await bot.send_message(message.chat.id, f"""{my_parser.Parser.content_usd_rub()} за $
{my_parser.Parser.content_eur_rub()} за €
Нефть Brent: {my_parser.Parser.content_oil_brent()}
Индекс S&P 500: {my_parser.Parser.content_spx()}
Индекс Мосбиржи: {my_parser.Parser.content_imoex()}
\nИсточник: https://ru.investing.com""", parse_mode='html')
        elif message.text.lower() in ["погода", "/погода", "погода краснодар", "погода в краснодаре"]:
            await bot.send_message(message.chat.id, f"""Погода в Краснодаре: {my_parser.Parser.content_weather()}\n
Источник: https://www.gismeteo.ru/weather-krasnodar-5136/now""", parse_mode='html')
        elif message.text.lower() in ["перевод"]:
            await bot.send_message(message.chat.id,
                                   f'Для перевода отдельного слова - напишите в чат данное слово в виде: "=слово"')
        # реализация перевода Ru_En
        elif message.text[0] == "=" and len(message.text) >= 2 and message.text[1] not in ascii_letters:
            await bot.send_message(message.chat.id,
                                   f"https://translate.google.com/?hl=ru&tab=TT&sl=ru&tl=en&text={message.text[1:]}&op=translate",
                                   parse_mode='html')
        # реализация перевода En_Ru
        elif message.text[0] == "=" and len(message.text) >= 2 and message.text[1] in ascii_letters:
            await bot.send_message(message.chat.id,
                                   f"https://translate.google.com/?hl=en&tab=TT&sl=ru&tl=ru&text={message.text[1:]}&op=translate",
                                   parse_mode='html')
        # реализация модуля с ДР
        elif message.text.lower() in ["др", "/др"]:
            await bot.send_message(message.chat.id, f'Введите имя будущего именинника:', parse_mode='html')
            await Birthday.name_input.set()  # переход в состояние ввода имени

        elif message.text.lower() in other_func.names:
            await bot.send_message(message.chat.id,
                                   f'Для вывода информации о дне рождения - введите "ДР" или воспользуйтесь соотвествующей кнопкой.\n\nДля вывода всего списка - введите: "все ДР".',
                                   parse_mode='html')

        elif message.text.lower() == "все др":
            for elem in sorted(other_func.lst_person, key=lambda x: x.birthday.split(".")[1]):  # сортировка
                await bot.send_message(message.chat.id, f"{elem.name}\n{elem.birthday}\nвозраст: {elem.get_age()}",
                                       parse_mode='html')

        # cоздаем инлайновую клавиатуру, если ввели неизвестную комманду
        else:
            markup = types.InlineKeyboardMarkup(row_width=3)
            btn1 = types.InlineKeyboardButton("Финансы", callback_data="q1")
            btn2 = types.InlineKeyboardButton("Погода", callback_data="q2")
            btn3 = types.InlineKeyboardButton("Перевод", callback_data="q3")
            btn4 = types.InlineKeyboardButton("ДР", callback_data="q4")
            markup.add(btn1, btn2, btn3, btn4)  # добавляем кнопки
            await bot.send_message(message.chat.id, f"Неизвестная комманда или имя.\nВведите корректную комманду:",
                                   reply_markup=markup)


# вызов команд через инлайновую клавиатуру
@dp.callback_query_handler(text_startswith="q")
async def callback_2(call: types.callback_query):
    if call.data == "q1":
        await bot.send_message(call.message.chat.id, f"Получение данных, ожидайте...", parse_mode='html')
        await bot.send_message(call.message.chat.id, f"""{my_parser.Parser.content_usd_rub()} за $
{my_parser.Parser.content_eur_rub()} за €
Нефть Brent: {my_parser.Parser.content_oil_brent()}
Индекс S&P 500: {my_parser.Parser.content_spx()}
Индекс Мосбиржи: {my_parser.Parser.content_imoex()}
\nИсточник: https://ru.investing.com""", parse_mode='html')
    elif call.data == "q2":
        await bot.send_message(call.message.chat.id, f"""Погода в Краснодаре: {my_parser.Parser.content_weather()}\n
Источник: https://www.gismeteo.ru/weather-krasnodar-5136/now""", parse_mode='html')
    elif call.data == "q3":
        await bot.send_message(call.message.chat.id,
                               f'Для перевода отдельного слова - напишите в чат данное слово в виде: "=слово"',
                               parse_mode='html')
    elif call.data == "q4":
        await bot.send_message(call.message.chat.id,
                               f'Для вывода информации о дне рождения - введите имя.\n\nДля вывода всего списка - введите: "все ДР."',
                               parse_mode='html')
        await Birthday.name_input.set()


executor.start_polling(dp)
