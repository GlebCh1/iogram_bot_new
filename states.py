"""
Модуль реализации состояний
"""
from datetime import datetime
from pytz import timezone
from string import ascii_letters, digits
import sqlite3 as sq
import openai

from loader import *
import keyboards
import other_func


from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State


# реализация FSM для модуля дней рождений  #############################################################################
class Birthday(StatesGroup):
    name_input = State()


@dp.message_handler(state=Birthday.name_input)
async def answer_birthday(message, state: FSMContext):
    async def search_for_name():
        person_obj = other_func.Person.create_person(message.text.lower())
        await bot.send_message(message.chat.id,
                               f"<b>{person_obj.name}</b>\n{person_obj.birthday}\nвозраст: {person_obj.get_age()}",
                               parse_mode='html')

    if message.text.lower() in other_func.Person.create_names():
        await search_for_name()
        markup = keyboards.MainKeyboard.birthdays()
        await bot.send_message(message.chat.id, f"Для вывода информации о дне рождения - введите имя и фамилию или просто имя", parse_mode='html', reply_markup=markup)

    elif message.text.lower() == "все дни рождения":
        for elem in sorted(other_func.Person.create_person(message.text.lower()), key=lambda x: x.birthday.split(".")[1]):  # сортировка
            await bot.send_message(message.chat.id, f"{elem.name}\n{elem.birthday}\nвозраст: {elem.get_age()}", parse_mode="html")

    elif message.text.lower() == "выход из состояния / возврат в главное меню":
        markup = keyboards.MainKeyboard.main_keyboard()
        await bot.send_message(message.chat.id, f"Выберите функцию", parse_mode="html", reply_markup=markup)
        await state.finish()  # выход из состояния поиска имени

    elif message.text.lower() == "/start":
        markup = keyboards.MainKeyboard.main_keyboard()
        await bot.send_message(message.chat.id, f"Выберите функцию", parse_mode="html", reply_markup=markup)
        await state.finish()  # выход из состояния поиска имени

    else:
        markup = keyboards.MainKeyboard.birthdays()
        await bot.send_message(message.chat.id, f"Указанного имени нет в списке, попробуйте еще раз, введите имя и фамилию или просто имя", parse_mode='html', reply_markup=markup)


# реализация FSM для модуля перевода  ##################################################################################
class Translation(StatesGroup):
    text_input = State()


@dp.message_handler(state=Translation.text_input)
async def answer_translation(message, state: FSMContext):
    # реализация перевода Ru_En
    if all([True if letter in ascii_letters + digits else False for letter in message.text.lower()]):
        await bot.send_message(message.chat.id,
                               f"https://translate.google.com/?hl=ru&tab=TT&sl=en&tl=ru&text={message.text}&op=translate",
                               parse_mode='html')
    # реализация перевода En_Ru
    elif all([True if letter in "абвгдежзийклмнопрстуфхцчшщъыьэюя" + digits else False for letter in
              message.text.lower()]):
        await bot.send_message(message.chat.id,
                               f"https://translate.google.com/?hl=en&tab=TT&sl=ru&tl=en&text={message.text}&op=translate",
                               parse_mode='html')
    else:
        await bot.send_message(message.chat.id,
                               f"Введены недопустимые символы.\nДопускается вводить только rus или eng буквы, а также цифры.\nВыход из состояния поиска имени...",
                               parse_mode='html')
    await state.finish()  # выход из состояния поиска имени


# реализация FSM для модуля калькулятора  ##############################################################################
class Calculator(StatesGroup):
    nums_input = State()


@dp.message_handler(state=Calculator.nums_input)
async def answer_calculator(message, state: FSMContext):
    try:
        operator = "".join([elem for elem in message.text if elem in ["+", "-", "*", "/", "%"]])
        working_line = message.text.replace(",", ".").split(operator)
        num1, num2 = map(lambda num: int(num.strip()) if "." not in num else float(num.strip()), working_line)
        await bot.send_message(message.chat.id,
                               f"{eval(f'{num1}{operator}{num2}', {}, {})}\n\n<b>Выход из состояния калькулятора...</b>",
                               parse_mode="html")
    except:
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

<b>Выход из состояния калькулятора...</b>''', parse_mode="html")
    await state.finish()  # выход из состояния калькулятора


# реализация FSM для модуля ChatGPT  ###################################################################################
class ChatGPT(StatesGroup):
    text_input = State()


@dp.message_handler(state=ChatGPT.text_input)
async def answer_chatgpt(message, state: FSMContext):

    if message.text.lower() == "выход из состояния / возврат в главное меню":
        markup = keyboards.MainKeyboard.main_keyboard()
        await bot.send_message(message.chat.id, f"Выберите функцию", parse_mode="html", reply_markup=markup)
        await state.finish()  # выход из состояния ChatGPT

    elif message.text.lower() == "/start":
        markup = keyboards.MainKeyboard.main_keyboard()
        await bot.send_message(message.chat.id, f"Выберите функцию", parse_mode="html", reply_markup=markup)
        await state.finish()  # выход из состояния ChatGPT

    else:
        openai.api_key = config.OPENAI_API_KEY

        # Задаем параметры общего контекста диалога
        content_system = """Свои ответы никогда не начинай со слов: "Response from ChatGPT:".
Ты полезный ассистент с ИИ женского пола, который готов помочь своему пользователю.
Отвечай мне в стиле гопника, используй всякие жаргонные выражения, тюремную лексику.
"""
# Если я попрошу тебя что-то сделать, что можно сделать с помощью программы на python, ты присылаешь мне код программы без объяснений.
# Если программа должна возвращать какой-то результат, то выводи его с помощью print.
# Затем я запущу этот код и скажу тебе результат, после чего ты сделаешь ответ из этого результата.
# Если при выполнении кода возникнет ошибка, я тебе её пришлю и ты исправишь код. Просто пришли мне исправленный код без пояснений.
# Если ты увидишь, что результат выполнения кода не соответствует твоим ожиданиям, то просто пришли новую версию кода.
# Если тебе нужна какая-то информация, то получай её из интернета с помощью python и обрабатывай с помощью кода.
# Не используй код, который требует использование ключей для доступа к api
# Для написания кода используй специальную библиотеку, которая называется gpt_utils. Она содержит следующие функции:
# gpt_utils.send_message_to_all(text) - отправляет сообщение всем пользователям
# Используй библиотеку yfinance для доступа к ценам акций
# Для работы с вопросами о погоде используй python_weather
        content_user = 'Привет, можешь ли ты мне помочь?'
        content_assistant = 'Здравствуйте, да, что Вас интересует?'

        openai_messages = [
            {'role': 'system', 'content': content_system},
            {'role': 'user', 'content': content_user},
            {'role': 'assistant', 'content': content_assistant}
        ]

        # Добавляем id и name пользователя в таблицу chatGPT_dialog_history в БД, если id отсутствует в указанной таблице
        with sq.connect('people.db') as con:
            cur = con.cursor()

            # Если пользователя с данным id нет в таблице chatGPT_dialog_history
            if message.chat.id not in [elem[0] for elem in cur.execute(f"SELECT id_t FROM chatGPT_dialog_history").fetchall()]:
                cur.execute(f"INSERT INTO chatGPT_dialog_history (id_t, name_t) VALUES ({message.chat.id}, '{message.from_user.first_name}')")

            # Определяем желаемый часовой пояс
            tz = timezone('Europe/Moscow')

            # Получаем текущую дату и время в указанном часовом поясе
            current_time = datetime.now(tz)

            # Получаем текущую дату и время
            date_time = current_time.strftime('%d.%m.%Y, %H:%M:%S')

            # Получаем историю диалога
            dialog_history = cur.execute(f'SELECT GPT_dialog_history FROM chatGPT_dialog_history WHERE id_t = {message.chat.id}').fetchall()[0][0]

            # Формируем в user_message сообщение от пользователя с указанием текущей даты и времени
            user_message = f'{date_time}\nMessage from user with id {message.chat.id}:\n{message.text}'

            # Формируем в content объект строки в виде истории сообщений и сообщения от пользователя для дальнейшего...
            # формирования словаря {'role': 'user', 'content': content}
            content = f'{dialog_history}\n\n\n{user_message}'

            print()
            print('*******************************************')
            print(content)
            print('*******************************************')
            print()

            # Добавляем словарь, где content - это история сообщений и сообщение от пользователя, в список контекста
            openai_messages.append({'role': 'user', 'content': content})
            completion = openai.ChatCompletion.create(model='gpt-3.5-turbo', messages=openai_messages)
            answer_chat_gpt = completion.choices[0].message.content

            # Обновляем историю диалогов, с учетом полученного ответа
            dialog = f'\n\n{date_time}\nMessage from user with id {message.chat.id}:\n{message.text}\n\nResponse from ChatGPT:\n{answer_chat_gpt}'
            dialog_history += dialog

            cur.execute('UPDATE chatGPT_dialog_history SET GPT_dialog_history = ? WHERE id_t = ?', (dialog_history, message.chat.id))

            print()
            print('-------------------------------------------')
            print(dialog_history)
            print('-------------------------------------------')
            print()

        await bot.send_message(message.chat.id, answer_chat_gpt, parse_mode=None)
