import logging
from datetime import datetime, timedelta

import pytz

local_timezone = pytz.timezone('Europe/Moscow')


def get_local_datetime(dt: datetime):
    return dt.replace(tzinfo=local_timezone)


def get_local_isoformat(dt: datetime):
    return dt.replace(tzinfo=local_timezone).isoformat()


def get_datetime_from_string(str_date):
    dt = None
    try:
        dt = datetime.strptime(str_date, "%Y/%-m/%-d")
    except Exception as e:
        logging.debug(e)
    else:
        try:
            dt = datetime.strptime(str_date, "%-m/%-d")
        except Exception as e:
            logging.debug(e)
    return dt


def get_datetime_delta(dt):
    begin_of_dt = datetime(dt.year, dt.month, dt.day)
    end_dt = begin_of_dt + timedelta(1)
    local_begin_dt = get_local_datetime(dt)
    local_end_dt = get_local_datetime(end_dt)
    return local_begin_dt, local_end_dt


def get_today_date():
    dt = datetime.utcnow()
    today_date = get_local_datetime(dt)
    return today_date


def get_tomorrow_date():
    dt = datetime.utcnow() + timedelta(1)
    tomorrow_dt = get_local_datetime(dt)
    return tomorrow_dt


def get_date_string(today_date: datetime):
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
    today_date_str = weekdays_to_str[today_date.weekday()] + ", " + str(today_date.day) + " " + months_to_str[
        today_date.month] + " " + str(today_date.year) + " года"
    return today_date_str
