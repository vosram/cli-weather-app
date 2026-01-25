from lib.formatters import timestamp_to_fmt_text


class WeatherAlert:
    def __init__(
        self, sender_name: str, event: str, start: int, end: int, description: str
    ):
        self.sender_name = sender_name
        self.event = event
        self.start = start
        self.end = end
        self.description = description

    def get_sender(self):
        return self.sender_name

    def get_event(self):
        return self.event

    def get_start(self):
        return timestamp_to_fmt_text(self.start, "generic")

    def get_end(self):
        return timestamp_to_fmt_text(self.end, "generic")

    def get_description(self):
        return self.description
