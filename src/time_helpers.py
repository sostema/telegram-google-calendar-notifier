from datetime import datetime, timedelta

import pytz

from src.utils import setup_logger

logger = setup_logger("time_helpers")
local_timezone = pytz.timezone("Europe/Moscow")


class Date:
    def __init__(
        self, dt=datetime.utcnow(), full_day=True, local_timezone=local_timezone
    ):
        self.local_timezone = local_timezone
        self.full_day = full_day

        self.date = None
        self.datetime_begin = None
        self.datetime_end = None

        self.init_delta(dt)

    def init_delta(self, dt):
        dt = dt.astimezone(self.local_timezone)

        if self.full_day:
            self.date = datetime(dt.year, dt.month, dt.day)
            self.datetime_begin = self.date
            self.datetime_end = self.date + timedelta(1)
        else:
            self.date = datetime(dt.year, dt.month, dt.day)
            self.datetime_begin = dt
            self.datetime_end = self.date + timedelta(1)

        return self

    def parse_datetime(self, string):
        try:
            dt = datetime.strptime(string, "%Y/%m/%d")
            return self.init_delta(dt)
        except Exception as e:
            try:
                this_year = str(datetime.now(self.local_timezone).year)
                string = this_year + "/" + string
                dt = datetime.strptime(string, "%Y/%m/%d")
                return self.init_delta(dt)
            except Exception as e:
                logger.debug(e)
                raise e

    def __str__(self):
        weekdays_ru = {
            0: "Понедельник",
            1: "Вторник",
            2: "Среда",
            3: "Четверг",
            4: "Пятница",
            5: "Суббота",
            6: "Воскресенье",
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
            12: "Декабря",
        }
        weekdays_to_str = weekdays_ru
        months_to_str = months_ru
        dt_str = (
            weekdays_to_str[self.date.weekday()]
            + ", "
            + str(self.date.day)
            + " "
            + months_to_str[self.date.month]
            + " "
            + str(self.date.year)
            + " года "
        )
        return dt_str

    def isoformat(self):
        return self.date.replace(tzinfo=self.local_timezone).isoformat()
