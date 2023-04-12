from string import ascii_letters, digits

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

    elif message.text.lower() == "возврат в главное меню":
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
                               parse_mode='html')
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

<b>Выход из состояния калькулятора...</b>''', parse_mode='html')
    await state.finish()  # выход из состояния калькулятора