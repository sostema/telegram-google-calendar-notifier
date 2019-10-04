from datetime import datetime


def parse_google_event_datetime(event_datetime):
    return datetime.fromisoformat(event_datetime).strftime('%H:%M')
