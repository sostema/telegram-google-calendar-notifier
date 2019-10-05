from datetime import datetime

from Code.CalendarAPI.calendar import GoogleCalendar


def setup_calendar_from_config(config):
    api_key = config.get("credentials", "api_key")
    cal_id = config.get("credentials", "cal_id")
    calendar = GoogleCalendar(api_key, cal_id)
    return calendar


def parse_google_event_datetime(event_datetime):
    return datetime.fromisoformat(event_datetime).strftime('%H:%M')
