from enum import Enum
from datetime import datetime
from lib.converters import (
    kelvin_to_c,
    kelvin_to_f,
    wind_speed_to_kmph,
    wind_speed_to_mph,
    mm_to_in,
)
from lib.formatters import format_percipitation, timestamp_to_fmt_text


class WeatherType(Enum):
    THUNDERSTORM = "thunderstorm"
    DRIZZLE = "drizzle"
    RAIN = "rain"
    SNOW = "snow"
    ATMOSPHERE = "atmosphere"
    CLEAR = "clear"
    CLOUDS = "clouds"


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

    def get_datetime(self, t_format: "hourly" | "daily" | "current" | "filename"):
        match t_format:
            case "hourly":
                return timestamp_to_fmt_text(self.timestamp, "hourly")
            case "filename":
                return timestamp_to_fmt_text(self.timestamp, "filename")
            case "daily":
                return timestamp_to_fmt_text(self.timestamp, "daily")
            case "generic" | "current" | _:
                return timestamp_to_fmt_text(self.timestamp, "generic")

    def get_temp(self):
        if self.temp_units == "c":
            return kelvin_to_c(self.temp)
        else:
            return kelvin_to_f(self.temp)

    def get_feels_like(self):
        if self.temp_units == "c":
            return kelvin_to_c(self.feels_like)
        else:
            return kelvin_to_f(self.feels_like)

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

    def get_weather_category(self) -> WeatherType:
        weather_code = self.weather["id"]
        if weather_code >= 200 and weather_code < 300:
            return WeatherType.THUNDERSTORM
        elif weather_code >= 300 and weather_code < 400:
            return WeatherType.DRIZZLE
        elif weather_code >= 500 and weather_code < 600:
            return WeatherType.RAIN
        elif weather_code >= 600 and weather_code < 700:
            return WeatherType.SNOW
        elif weather_code >= 700 and weather_code < 800:
            return WeatherType.ATMOSPHERE
        elif weather_code == 800:
            return WeatherType.CLEAR
        elif weather_code >= 801 and weather_code < 805:
            return WeatherType.CLOUDS
        else:
            return WeatherType.CLEAR

    def has_rain(self):
        if self.rain:
            return True
        else:
            return False

    def get_rain(self):
        if self.rain:
            if self.wind_units == "k":
                return f"{self.rain} mm"
            return mm_to_in(self.rain)
        else:
            return "N/A"

    def has_snow(self):
        if self.snow:
            return True
        else:
            return False

    def get_snow(self):
        if self.snow:
            if self.wind_units == "k":
                return f"{self.snow} mm"
            return mm_to_in(self.snow)
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


class DailyWeatherRecord(WeatherRecord):
    def __init__(
        self,
        timestamp: int,
        summary: str,
        min_temp: float,
        max_temp: float,
        feels_like,
        humidity: int,
        wind_speed: float,
        pop: float,
        weather,
        wind_gust: float | None = None,
        rain: float | None = None,
        snow: float | None = None,
        temp_units: str = "f",
        wind_units: str = "m",
    ):
        avg_temp = (max_temp + min_temp) / 2
        avg_feels_like = (
            feels_like["day"]
            + feels_like["night"]
            + feels_like["eve"]
            + feels_like["morn"]
        ) / 4

        super().__init__(
            timestamp,
            avg_temp,
            avg_feels_like,
            humidity,
            wind_speed,
            weather,
            wind_gust=wind_gust,
            rain=rain,
            snow=snow,
            pop=pop,
            temp_units=temp_units,
            wind_units=wind_units,
        )
        self.summary = summary
        self.min_temp = min_temp
        self.max_temp = max_temp

    def get_min_temp(self):
        if self.temp_units == "c":
            return kelvin_to_c(self.min_temp)
        else:
            return kelvin_to_f(self.min_temp)

    def get_max_temp(self):
        if self.temp_units == "c":
            return kelvin_to_c(self.max_temp)
        else:
            return kelvin_to_f(self.max_temp)

    def get_summary(self):
        return self.summary
