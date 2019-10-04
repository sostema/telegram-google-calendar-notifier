from datetime import datetime, timedelta

import pytz

local_timezone = pytz.timezone('Europe/Moscow')


def get_local_datetime(dt: datetime):
    return dt.replace(tzinfo=local_timezone)


def get_local_isoformat(dt: datetime):
    return dt.replace(tzinfo=local_timezone).isoformat()


def get_today_datetime():
    today_dt = datetime.utcnow()
    today_begin_dt = datetime(today_dt.year, today_dt.month, today_dt.day)
    today_end_dt = today_begin_dt + timedelta(days=1)
    local_today_begin_dt = get_local_datetime(today_begin_dt)
    local_today_end_dt = get_local_datetime(today_end_dt)
    return local_today_begin_dt, local_today_end_dt


def get_tomorrow_datetime():
    local_today_begin_dt, local_today_end_dt = get_today_datetime()
    local_tomorrow_begin_dt = local_today_begin_dt + timedelta(1)
    local_tomorrow_end_dt = local_today_end_dt + timedelta(1)
    return local_tomorrow_begin_dt, local_tomorrow_end_dt


def get_today_date():
    today_date = datetime.utcnow()
    today_date = get_local_datetime(today_date)
    return today_date


def today_date_string(today_date: datetime):
    weekdays_ru = {
        0: "Понедельник",
        1: "Вторник",
        2: "Среда",
        3: "Четверг",
        4: "Пятница",
        5: "Суббота",
        6: "Воскресенье"
    }
    months_ru = {
        1: "Января",
        2: "Февраля",
        3: "Марта",
        4: "Апреля",
        5: "Мая",
        6: "Июня",
        7: "Июля",
        8: "Августа",
        9: "Сентября",
        10: "Октября",
        11: "Ноября",
        12: "Декабря"
    }
    weekdays_to_str = weekdays_ru
    months_to_str = months_ru
    today_date_str = weekdays_to_str[today_date.weekday()] + ", " + str(today_date.date) + " " + months_to_str[
        today_date.month]
    return today_date_str
