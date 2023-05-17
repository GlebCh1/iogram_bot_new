from datetime import datetime
import pytz

# Определяем желаемый часовой пояс
timezone = pytz.timezone('Europe/Moscow')

# Получаем текущую дату и время в указанном часовом поясе
current_time = datetime.now(timezone)

# Выводим текущее время
s = current_time.strftime("%d.%m.%Y, %H:%M:%S")
pass
