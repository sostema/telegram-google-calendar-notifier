import Code.CalendarAPI.helpers as helpers


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
        return self.get_event_string()

    def get_event_string(self):
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
