from lib.converters import (
    kelvin_to_c,
    kelvin_to_f,
    wind_speed_to_kmph,
    wind_speed_to_mph,
)
from datetime import datetime


def timestamp_to_fmt_text(timestamp: int, t_format: str) -> str:
    match t_format:
        case "hourly":
            return datetime.fromtimestamp(timestamp).strftime("%m/%d/%y %I:%M %p")
        case "filename":
            return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d-%H-%M-%S")
        case "daily":
            return datetime.fromtimestamp(timestamp).strftime("%a %b %d %Y")
        case _:
            return datetime.fromtimestamp(timestamp).strftime("%a %b %d, %Y %I:%M %p")
