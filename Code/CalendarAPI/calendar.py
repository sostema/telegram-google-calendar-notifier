class CalendarEvent:
    def __init__(self):
        self.name = None
        self.description = None
        self.begin_date = None
        self.end_date = None
        self.location = None
        self.teacher = None
        self.notification_delay = None

    def parse_google_event(self, event):
        self.name = event['summary']
        self.description = event['description']
        self.begin_date = event['']
