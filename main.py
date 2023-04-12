from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import executor
from handlers import *


# реализация уведомлений о ДР и событиях ###############################################################################
async def send_message_birthdays_events():
    with sq.connect("people.db") as con:
        today = datetime.today()  # получение текущей даты
        cur = con.cursor()
        birthdays = {elem[0]: elem[1:] for elem in cur.execute(f"SELECT name, birthdate, name_declension FROM p1").fetchall()}
        events = {elem[0]: elem[1:] for elem in cur.execute(f"SELECT name, date, access FROM p2").fetchall()}

        async def check_birthdays_and_events(dct):
            for key, value in dct.items():
                d, m = map(int, value[0].split(".")[:2])
                dr = datetime(today.year, m, d)
                delta = dr - today
                if delta.days < 0:  # если ДР уже прошел - значит следующий - в следующем году, поэтому добавляем 1 год
                    dr = datetime(today.year + 1, m, d)
                    delta = dr - today
                if delta.days <= 2:  # если до ДР остается меньше двух дней происходит рассылка сообщений пользователям, id
                    # которых добавлены в таблицу id_telegramm в БД
                    if dct == birthdays:
                        for id_t in cur.execute(f"SELECT id_t FROM id_telegramm").fetchall():
                            await bot.send_message(id_t[0], f"<b>Уведомление о ДР 🍼🍺🍷🥃</b>\n"
                                                            f"Чувствую я, что близится...\n"
                                                            f"День Рождения {value[1]}\n"
                                                            f"<b>{value[0]}</b>", parse_mode='html')
                    elif dct == events:
                        for id_t in cur.execute(f"SELECT id_t FROM id_telegramm").fetchall():
                            if value[1] == 'all' or id_t[0] in value[1]:
                                await bot.send_message(id_t[0], f"<b>Уведомление о событии</b>\n"
                                                                f"{key}\n<b>{value[0]}</b>", parse_mode='html')

        await check_birthdays_and_events(birthdays)
        await check_birthdays_and_events(events)


scheduler = AsyncIOScheduler(timezone="Europe/Moscow")  # запуск уведомлений
scheduler.add_job(send_message_birthdays_events, trigger="interval", hours=8)
scheduler.start()



executor.start_polling(dp)






