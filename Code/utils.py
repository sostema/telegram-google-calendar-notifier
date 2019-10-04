import configparser
import datetime

import pytz


def utc_to_local(utc_dt):
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt)


def get_current_time():
    time_today = utc_to_local(datetime.datetime.utcnow())
    return time_today


def get_tomorrow_time():
    time_tomorrow = utc_to_local(datetime.datetime.utcnow() + datetime.timedelta(days=1))
    return time_tomorrow


def get_now_time():
    now_time = utc_to_local(datetime.datetime.utcnow())
    return now_time


def get_today():
    today = utc_to_local(datetime.datetime.utcnow())
    start = utc_to_local(datetime.datetime(today.year, today.month, today.day))
    end = utc_to_local(start + datetime.timedelta(1))
    return start, end


def get_date():
    weekdays = {
        0: "Понедельник",
        1: "Вторник",
        2: "Среда",
        3: "Четверг",
        4: "Пятница",
        5: "Суббота",
        6: "Воскресенье"
    }
    months = {
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
    today = utc_to_local(datetime.datetime.today())
    return "Сегодня " + str(today.day) + " " + months[today.month] + ", " + weekdays[today.weekday()]


def set_timezone(timezone):
    config.set("settings", "timezone", timezone)
    save_config(config)


def get_config():
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config


def save_config(config):
    config.write("config.ini")


config = get_config()
local_tz = pytz.timezone(config.get("settings", "timezone"))
