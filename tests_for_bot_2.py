from datetime import datetime
import pytz
import sqlite3 as sq

# Определяем желаемый часовой пояс
timezone = pytz.timezone('Europe/Moscow')

# Получаем текущую дату и время в указанном часовом поясе
current_time = datetime.now(timezone)

# Выводим текущее время
s = current_time.strftime("%d.%m.%Y, %H:%M:%S")
with sq.connect('people.db') as con:
    cur = con.cursor()
    dialog_history = cur.execute(f'SELECT GPT_dialog_history FROM chatGPT_dialog_history WHERE id_t={message.chat.id}')