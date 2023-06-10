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


CONTENT_SYSTEM = "Ты полезный ассистент с ИИ, который готов помочь своему пользователю."



# реализация FSM для модуля дней рождений  #############################################################################
class Birthday(StatesGroup):
    name_input = State()


@dp.message_handler(state=Birthday.name_input)
async def answer_birthday(message, state: FSMContext):
    async def search_for_name():
        person_obj = other_func.Person.create_person(message.text.lower())
        await bot.send_message(message.chat.id, f"<b>{person_obj.name}</b>\n{person_obj.birthday}\n"
                                                f"возраст: {person_obj.get_age()}", parse_mode="html")

    if message.text.lower() in other_func.Person.create_names():
        await search_for_name()
        markup = keyboards.MainKeyboard.birthdays()
        await bot.send_message(message.chat.id, f"Для вывода информации о дне рождения - введите имя и фамилию "
                                                f"или просто имя", parse_mode="html", reply_markup=markup)

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
        await bot.send_message(message.chat.id, f"Указанного имени нет в списке, попробуйте еще раз, введите имя и фамилию "
                                                f"или просто имя", parse_mode="html", reply_markup=markup)


# реализация FSM для модуля перевода  ##################################################################################
class Translation(StatesGroup):
    text_input = State()


@dp.message_handler(state=Translation.text_input)
async def answer_translation(message, state: FSMContext):
    # реализация перевода Ru_En
    if all([True if letter in ascii_letters + digits else False for letter in message.text.lower()]):
        await bot.send_message(message.chat.id, f"https://translate.google.com/?hl=ru&tab=TT&sl=en&tl=ru&text={message.text}&op=translate", parse_mode="html")
    # реализация перевода En_Ru
    elif all([True if letter in "абвгдежзийклмнопрстуфхцчшщъыьэюя" + digits else False for letter in
              message.text.lower()]):
        await bot.send_message(message.chat.id, f"https://translate.google.com/?hl=en&tab=TT&sl=ru&tl=en&text={message.text}&op=translate", parse_mode="html")
    else:
        await bot.send_message(message.chat.id,f"Введены недопустимые символы.\n"
                                               f"Допускается вводить только rus или eng буквы, а также цифры.\n"
                                               f"Выход из состояния поиска имени...", parse_mode="html")
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
        await bot.send_message(message.chat.id, f"{eval(f'{num1}{operator}{num2}', {}, {})}\n\n"
                                                f"<b>Выход из состояния калькулятора...</b>", parse_mode="html")
    except:
        await bot.send_message(message.chat.id, (f"<b>Недопустимый формат ввода значений...</b>\n\n"
                                                 f"Введите значения в формате:\n"
                                                 f"5 + 5 (сложение)\n"
                                                 f"5,6 - 4,6 (вычитание)\n"
                                                 f"5,5 * 5 (умножение)\n"
                                                 f"10.5 / 5.5 (деление)\n"
                                                 f"2 ** 3 (возведение в степень)\n"
                                                 f"9 ** 0.5 (квадратный корень)\n"
                                                 f"10 // 3 (целочисленное деление)\n"
                                                 f"10 % 3 (остаток от деления)\n\n"
                                                 f"<b>Выход из состояния калькулятора...</b>"), parse_mode="html")
    await state.finish()  # выход из состояния калькулятора



# реализация FSM для модуля ChatGPT  ###################################################################################
class ChatGPT(StatesGroup):
    text_input = State()
    ChatGPTSystemRole = State()


@dp.message_handler(state=ChatGPT.text_input)
async def answer_chatgpt(message, state: FSMContext):

    # Добавляем id и name пользователя в таблицу chatGPT_dialog_history в БД, если id отсутствует в указанной таблице
    with sq.connect("people.db") as con:
        cur = con.cursor()
        # Если пользователя с данным id нет в таблице chatGPT_dialog_history
        if message.chat.id not in [elem[0] for elem in cur.execute(f"SELECT id_t FROM chatGPT_dialog_history").fetchall()]:
            cur.execute(f"INSERT INTO chatGPT_dialog_history (id_t, name_t, GPT_dialog_history, content_system) VALUES (?, ?, ?, ?)", (message.chat.id, message.from_user.first_name, "", CONTENT_SYSTEM))

    if message.text.lower() == "назначение системной роли chatgpt":
        markup = keyboards.MainKeyboard.chat_gpt_system_role()
        await bot.send_message(message.chat.id, f"<b>Переход в состояние выбора системной роли...\n"
                                                f"Отправьте сообщение и тем самым назначьте системную роль ChatGPT.</b>\n\n"
                                                f"Пример использования: <i>\"Тебе зовут Шелдон.\n"
                                                f"Ты должен отвечать как программист Python.\n"
                                                f"Когда я задаю тебе вопросы про программирование - ты отвечаешь подробно и по существу, "
                                                f"при этом не затрагивая посторонние темы\".</i>", parse_mode="html", reply_markup=markup)
        await ChatGPT.ChatGPTSystemRole.set()  # переход в состояние назначения системной роли

    elif message.text.lower() == "выход из состояния / возврат в главное меню":
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
        with sq.connect("people.db") as con: # Через менеджер контекста вновь подключаемся к БД и получаем системную роль...
            # пользователя из таблицы chatGPT_dialog_history
            cur = con.cursor()

            content_system = cur.execute(f"SELECT content_system FROM chatGPT_dialog_history WHERE id_t = {message.chat.id}").fetchall()[0][0]
            if not content_system:
                content_system = CONTENT_SYSTEM

            content_user = "Привет, можешь ли ты мне помочь?"
            content_assistant = "Здравствуйте, да, что Вас интересует?"
            openai_messages = [
                {"role": "system", "content": content_system},
                {"role": "user", "content": content_user},
                {"role": "assistant", "content": content_assistant}
            ]

            # Определяем желаемый часовой пояс
            tz = timezone("Europe/Moscow")

            # Получаем текущую дату и время в указанном часовом поясе
            current_time = datetime.now(tz)

            # Получаем текущую дату и время
            date_time = current_time.strftime("%d.%m.%Y, %H:%M:%S")

            # Получаем историю диалога
            dialog_history = cur.execute(f"SELECT GPT_dialog_history FROM chatGPT_dialog_history WHERE id_t = {message.chat.id}").fetchall()[0][0]
            # Формируем в user_message сообщение от пользователя с указанием текущей даты и времени
            user_message = f"{date_time}\nMessage from user with id {message.chat.id}:\n{message.text}"

            # Формируем в content объект строки в виде истории сообщений и сообщения от пользователя для дальнейшего...
            # формирования словаря {'role': 'user', 'content': content}
            content = f"{dialog_history}\n\n\n{user_message}"

            # Добавляем словарь, где content - это история сообщений и сообщение от пользователя, в список контекста
            openai_messages.append({"role": "user", "content": content})

            # Проверяем ответ ChatGPT на ошибки
            try:
                completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=openai_messages)

            # Автоматически очищаем историю диалога, если возникла ошибка превышения лимита токенов (4097 токенов всего доступно)
            except openai.error.InvalidRequestError as error:
                if error.code == "context_length_exceeded":
                    await bot.send_message(message.chat.id, f"🤖<b>История диалога очищена, поскольку исчерпан лимит токенов...</b>"
                                                            f"\n\nОтветы на последующие сообщения будут представлены без учета предыдущего диалога", parse_mode="html")

                    # Через менеджер контекста вновь подключаемся к БД и удаляем все данные в поле GPT_dialog_history
                    with sq.connect("people.db") as con:
                        cur = con.cursor()
                        cur.execute("UPDATE chatGPT_dialog_history SET GPT_dialog_history = ? WHERE id_t = ?", ("", message.chat.id))

                    # Обновляем значение переменной, так, чтобы она ссылалась на пустую строку
                    dialog_history = ""

                    # Меняем последний элемент списка openai_messages на словарь, где ключ 'content' указывает просто на ...
                    # сообщение пользователя, т.е. не передается история диалога
                    openai_messages[-1] = {"role": "user", "content": user_message}
                    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=openai_messages)

            answer_chat_gpt = completion.choices[0].message.content

        # Обновляем историю диалога, с учетом полученного ответа
        dialog = f"{user_message}\n\nResponse from ChatGPT:\n{answer_chat_gpt} \n\n\n"
        dialog_history += dialog
        print(dialog_history)

        # Через менеджер контекста вновь подключаемся к БД и обновляем историю диалога, с учетом полученного ответа
        with sq.connect("people.db") as con:
            cur = con.cursor()
            cur.execute("UPDATE chatGPT_dialog_history SET GPT_dialog_history = ? WHERE id_t = ?", (dialog_history, message.chat.id))

        await bot.send_message(message.chat.id, answer_chat_gpt, parse_mode=None)



# реализация FSM для модуля назначения системной роли ChatGPT  #########################################################
@dp.message_handler(state=ChatGPT.ChatGPTSystemRole)
async def answer_chatgpt_system_role(message, state: FSMContext):
    if message.text.lower() == "информация о текущей системной роли":
        with sq.connect("people.db") as con:
            cur = con.cursor()

            answer = cur.execute(f"SELECT content_system FROM chatGPT_dialog_history WHERE id_t = {message.chat.id}").fetchall()[0][0]
            if not answer:
                answer = CONTENT_SYSTEM

                cur.execute("UPDATE chatGPT_dialog_history SET content_system = ? WHERE id_t = ?", (CONTENT_SYSTEM, message.chat.id))

            await bot.send_message(message.chat.id, f"<b>У Вас назначена следующая системная роль:</b>\n\n"
                                                    f"<i>{answer}</i>\n\n"
                                                    f"<b>Назначьте новую системную роль</b>.", parse_mode="html")

    elif message.text.lower() == "возврат системной роли, используемой по-умолчанию":
        with sq.connect("people.db") as con:
            cur = con.cursor()

            cur.execute("UPDATE chatGPT_dialog_history SET content_system = ? WHERE id_t = ?", (CONTENT_SYSTEM, message.chat.id))

            await bot.send_message(message.chat.id, f"<b>Назначена системная роль, используемая по-умолчанию:</b>\n\n"
                                                    f"<i>{CONTENT_SYSTEM}</i>", parse_mode="html")

    elif message.text.lower() == "выход из состояния / возврат в предыдущее меню":
        markup = keyboards.MainKeyboard.chat_gpt()
        await bot.send_message(message.chat.id, f"<b>🤖Возврат в состояние ChatGPT...</b>\n\n"
                                                f"Напишите что-нибудь, 🤖ChatGPT готов ответить", parse_mode="html", reply_markup=markup)

        # выход из состояния ChatGPTSystemRole и возврат в состояние ChatGPT
        await ChatGPT.text_input.set()

    elif message.text.lower() == "/start":
        markup = keyboards.MainKeyboard.main_keyboard()
        await bot.send_message(message.chat.id, f"Выберите функцию", parse_mode="html", reply_markup=markup)
        await state.finish()  # выход из состояния ChatGPTSystemRole

    else:
        markup = keyboards.MainKeyboard.chat_gpt()
        with sq.connect("people.db") as con:
            cur = con.cursor()

            cur.execute("UPDATE chatGPT_dialog_history SET content_system = ? WHERE id_t = ?", (message.text, message.chat.id))

            await bot.send_message(message.chat.id, f"<b>Изменения системной роли сохранены.</b>\n\n"
                                                    f"<b>🤖Возврат в состояние ChatGPT...</b>\n\n"
                                                    f"Напишите что-нибудь, 🤖ChatGPT готов ответить", parse_mode="html", reply_markup=markup)

            # выход из состояния ChatGPTSystemRole и возврат в состояние ChatGPT
            await ChatGPT.text_input.set()
