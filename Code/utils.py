import configparser
from datetime import datetime, timedelta

import pytz


def utc_to_local(utc_dt):
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt)


def get_current_time():
    time_today = utc_to_local(datetime.utcnow())
    return time_today


def get_tomorrow_time():
    time_tomorrow = utc_to_local(datetime.utcnow() + timedelta(days=1))
    return time_tomorrow


def get_now_time():
    now_time = utc_to_local(datetime.utcnow())
    return now_time


def get_today():
    today = utc_to_local(datetime.utcnow())
    start = utc_to_local(datetime(today.year, today.month, today.day))
    end = utc_to_local(start + timedelta(1))
    return start, end


def set_timezone(timezone):
    config.set("settings", "timezone", timezone)
    save_config(config)


def get_config():
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config


def save_config(config):
    with open('config.ini', 'w') as configfile:
        config.write(configfile)


config = get_config()
local_tz = pytz.timezone(config.get("settings", "timezone"))
