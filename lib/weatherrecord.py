from datetime import datetime
from lib.converters import (
    kelvin_to_c,
    kelvin_to_f,
    wind_speed_to_kmph,
    wind_speed_to_mph,
)
from lib.formatters import format_percipitation


class WeatherRecord:
    def __init__(
        self,
        timestamp: int,
        temp: float,
        feels_like: float,
        humidity: int,
        wind_speed: float,
        weather,
        wind_gust: float | None = None,
        rain: float | None = None,
        snow: float | None = None,
        pop: float | None = None,
        temp_units: "f" | "c" = "f",
        wind_units: "m" | "k" = "m",
    ):
        self.timestamp = timestamp
        self.temp = temp
        self.feels_like = feels_like
        self.humidity = humidity
        self.wind_speed = wind_speed
        self.wind_gust = wind_gust
        self.weather = weather
        self.rain = rain
        self.snow = snow
        self.pop = pop
        self.temp_units = temp_units
        self.wind_units = wind_units

    def get_datetime(self, t_format: "hourly" | "daily" | "current"):
        match t_format:
            case "hourly":
                return datetime.fromtimestamp(self.timestamp).strftime(
                    "%m/%d/%y %I:%M %p"
                )
            case "daily":
                pass
            case _:
                return datetime.fromtimestamp(self.timestamp).strftime(
                    "%a %b %d, %Y %I:%M %p"
                )

    def get_temp(self):
        if self.temp_units == "c":
            return kelvin_to_c(self.temp)
        else:
            return kelvin_to_f(self.temp)

    def get_feels_like(self):
        if self.temp_units == "c":
            return kelvin_to_c(self.temp)
        else:
            return kelvin_to_f(self.temp)

    def get_humidity(self):
        return f"{self.humidity}%"

    def get_wind_speed(self):
        if self.wind_units == "k":
            return wind_speed_to_kmph(self.wind_speed)
        else:
            return wind_speed_to_mph(self.wind_speed)

    def has_wind_gust(self):
        if self.wind_gust:
            return True
        else:
            return False

    def get_wind_gust(self):
        if self.wind_gust is None:
            return "N/A"

        if self.wind_units == "k":
            return wind_speed_to_kmph(self.wind_gust)
        else:
            return wind_speed_to_mph(self.wind_gust)

    def get_weather_condition(self):
        return f"{self.weather["main"]}: {self.weather["description"]}"

    def has_rain(self):
        if self.rain:
            return True
        else:
            return False

    def get_rain(self):
        if self.rain:
            return format_percipitation(self.rain)
        else:
            return "N/A"

    def has_snow(self):
        if self.snow:
            return True
        else:
            return False

    def get_snow(self):
        if self.snow:
            return format_percipitation(self.snow)
        else:
            return "N/A"

    def has_pop(self):
        if self.pop:
            return True
        else:
            return False

    def get_pop(self):
        # probability of percipitation frm 0 to 1
        if self.pop:
            result = self.pop * 100
            return "{:.2f}%".format(result)
        else:
            return "N/A"
