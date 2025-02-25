from datetime import datetime

def greeting(date: str) -> str:
    """
    Функция принимает дату в формате строки YYYY-MM-DD HH-MM-SS
    Возвращает строку приветствия в зависимости от времени:
    22.00 - 04.00 - Доброй ночи
    04.00 - 10.00 - Доброе утро
    10.00 - 16.00 - Добрый день
    16.00 - 22.00 - Добрый вечер
    """
    date_obj = datetime.strptime(date, "%Y-%m-d %H-%M-%S")
    hour = date_obj.hour
    if hour > 21 or hour < 4:
        return "Доброй ночи!"
    elif 3 < hour < 10:
        return "Доброе утро!"
    elif 9 < hour < 16:
        return "Добрый день!"
    else:
        return "Добрый вечер!"
