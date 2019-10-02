from googleapiclient.discovery import build
from Code.utils import *


def init_calendar():
    _api_key = config.get("credentials", "api_key")
    _cal_id = config.get("credentials", "cal_id")
    return _api_key, _cal_id


def get_service(api_key):
    service = build('calendar', 'v3', developerKey=api_key)
    return service


def get_calendar_timezone():
    cal_tz = service.events().list(calendarId=cal_id, maxResults=1).execute()['timeZone']
    return str(cal_tz)


def get_events(cal_id, time_begin, time_end, max_results=1):
    time_begin = time_begin.isoformat()
    time_end = time_end.isoformat()
    events_result = service.events().list(calendarId=cal_id,
                                          timeMin=time_begin, timeMax=time_end,
                                          maxResults=max_results,
                                          singleEvents=True,
                                          orderBy='startTime').execute()
    return events_result


def get_today_events():
    time_begin, time_end = get_today()
    events_result = get_events(cal_id, time_begin, time_end, MAX_RESULTS)
    return events_result['items']


def get_now_events():
    pass


def get_tomorrow_events():
    pass


def get_today_parsed_events():
    events = get_today_events()
    parsed_events = "\n\n".join(map(get_parsed_event, events))
    return parsed_events


def get_parsed_event(event_item):
    parsed_event = event_item['summary'] + " " + datetime.datetime.fromisoformat(
        event_item['start']['dateTime']).strftime('%H:%M') + "-" + datetime.datetime.fromisoformat(
        event_item['end']['dateTime']).strftime('%H:%M')
    if 'description' in event_item:
        parsed_event += "\n" + event_item.setdefault('description', '')
    return parsed_event


MAX_RESULTS = 1000
config = get_config()
api_key, cal_id = init_calendar()
service = get_service(api_key)
