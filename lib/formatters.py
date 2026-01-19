from lib.converters import (
    kelvin_to_c,
    kelvin_to_f,
    wind_speed_to_kmph,
    wind_speed_to_mph,
)
from datetime import datetime


def kelvin_to_formatted(k_temp: float, unit: "f" | "c") -> str:
    if unit == "f":
        return kelvin_to_f(k_temp)
    else:
        return kelvin_to_c(k_temp)


def format_wind_speed(speed: float, unit: "m" | "k") -> str:
    if unit == "k":
        return wind_speed_to_kmph(speed)
    else:
        return wind_speed_to_mph(speed)


def timestamp_to_fmt_text(timestamp: int) -> str:
    return datetime.fromtimestamp(timestamp).strftime("%a %b %d, %Y %I:%M %p")


def format_humidity(val: int) -> str:
    return f"{val}%"


def format_weather_desc(weather):
    return f"{weather["main"]}: {weather["description"]}"


def format_percipitation(val: float) -> str:
    return "{:.2f}mm/h".format(val)
