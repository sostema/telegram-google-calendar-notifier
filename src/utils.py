import configparser
import logging
import pathlib
from datetime import datetime, timedelta

import pytz


def setup_logger(logger_name=__name__):
    console_handler = logging.StreamHandler()
    (pathlib.Path("./app/Logs")).mkdir(parents=True, exist_ok=True)
    file_handler = logging.FileHandler(f"./app/Logs/{logger_name}_logging.log")
    logger_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s"
    )
    console_handler.setFormatter(logger_formatter)
    file_handler.setFormatter(logger_formatter)

    logger = logging.getLogger(f"{logger_name}")
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger


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
    _config = configparser.ConfigParser()
    _config.read("config.ini")
    return _config


def save_config(_config):
    with open("config.ini", "w") as configfile:
        _config.write(configfile)


config = get_config()
local_tz = pytz.timezone(config.get("settings", "timezone"))
default_logger = setup_logger("default")
