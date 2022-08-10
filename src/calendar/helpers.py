from datetime import datetime

from src.calendar.calendar import GoogleCalendar, CalendarEvent


def parse_google_event(event: dict):
    calendar_event = CalendarEvent()
    calendar_event.name = event["summary"]
    calendar_event.description = event.setdefault("description", None)
    if "start" in event:
        calendar_event.begin_date = parse_google_event_datetime(
            event["start"]["dateTime"]
        )
    else:
        calendar_event.begin_date = None
    if "end" in event:
        calendar_event.end_date = parse_google_event_datetime(event["end"]["dateTime"])
    else:
        calendar_event.end_date = None
    calendar_event.location = event.setdefault("location", None)
    if "reminders" in event:
        for reminder in event["reminders"].setdefault("overrides", []):
            calendar_event.reminders.append(reminder["minutes"])
    return calendar_event


def setup_calendar_from_config(config):
    api_key = config.get("credentials", "api_key")
    cal_id = config.get("credentials", "cal_id")
    calendar = GoogleCalendar(api_key, cal_id)
    return calendar


def parse_google_event_datetime(event_datetime):
    return datetime.fromisoformat(event_datetime).strftime("%H:%M")
