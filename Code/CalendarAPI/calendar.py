from googleapiclient.discovery import build

import Code.CalendarAPI.helpers as helpers
import Code.time_helpers


class GoogleCalendar:
    def __init__(self, api_key, cal_id):
        self.api_key = api_key
        self.cal_id = cal_id
        self.service = build('calendar', 'v3', developerKey=self.api_key)

        self.cal_timezone = self.get_calendar_timezone()

    def get_calendar_timezone(self):
        return self.service.events().list(calendarId=self.cal_id, maxResults=1).execute()['timeZone']

    def get_events(self, time_begin, time_end, max_results=250):
        time_begin = time_begin.isoformat()
        time_end = time_end.isoformat()
        result = self.service.events().list(calendarId=self.cal_id,
                                            timeMin=time_begin, timeMax=time_end,
                                            maxResults=max_results,
                                            singleEvents=True,
                                            orderBy='startTime').execute()
        events = map(CalendarEvent().parse_google_event, result['items'])
        return events

    def get_date_events(self, dt):
        date = Code.time_helpers.Date(dt)
        return self.get_events(date.datetime_begin, date.datetime_end)


class CalendarEvent:
    def __init__(self, name=None, description=None, begin_date=None, end_date=None, location=None, teacher=None,
                 reminders=None):
        if reminders is None:
            reminders = []
        self.name = name
        self.description = description
        self.begin_date = begin_date
        self.end_date = end_date
        self.location = location
        self.teacher = teacher
        self.reminders = reminders

    def parse_google_event(self, event: dict):
        self.name = event['summary']
        self.description = event.setdefault('description', None)
        if 'start' in event:
            self.begin_date = helpers.parse_google_event_datetime(event['start']['dateTime'])
        else:
            self.begin_date = None
        if 'end' in event:
            self.end_date = helpers.parse_google_event_datetime(event['end']['dateTime'])
        else:
            self.end_date = None
        self.location = event.setdefault('location', None)
        if 'reminders' in event:
            for reminder in event['reminders'].setdefault('overrides', []):
                self.reminders.append(reminder['minutes'])
        return self

    def __str__(self):
        string = ""
        if self.name:
            string = self.name + '\n'
        if self.begin_date and self.end_date:
            string += self.begin_date + "-" + self.end_date + "\n"
        if self.location:
            string += "Кабинет: " + self.location + '\n'
        if self.teacher:
            string += "Преподаватель: " + self.teacher + '\n'
        if self.description:
            string += self.description + '\n'
        return string
