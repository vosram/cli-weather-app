from lib.weatherrecord import WeatherRecord, WeatherType
from pathlib import Path
import os
from PIL import Image, ImageOps, ImageDraw, ImageFont
from rich import print


def current_to_image(record: WeatherRecord, city: str, state: str, country: str):
    bg_path = None
    match (record.get_weather_category()):
        case WeatherType.THUNDERSTORM:
            bg_path = Path(os.path.join("images", "thunderstorm.jpg"))
        case WeatherType.DRIZZLE:
            bg_path = Path(os.path.join("images", "drizzle.jpg"))
        case WeatherType.RAIN:
            bg_path = Path(os.path.join("images", "rain.jpg"))
        case WeatherType.SNOW:
            bg_path = Path(os.path.join("images", "snow.jpg"))
        case WeatherType.ATMOSPHERE:
            bg_path = Path(os.path.join("images", "atmosphere.jpg"))
        case WeatherType.CLEAR:
            bg_path = Path(os.path.join("images", "clear.jpg"))
        case WeatherType.CLOUDS:
            bg_path = Path(os.path.join("images", "clouds.jpg"))
        case _:
            bg_path = Path(os.path.join("images", "clear"))

    try:
        with Image.open(bg_path) as im:
            new_size = (800, 800)
            new_im = ImageOps.fit(im, new_size)
            draw = ImageDraw.Draw(new_im)
            draw.text(
                (new_size[0] * 0.5, new_size[1] * 0.15875),
                record.get_datetime("current"),
                anchor="ms",
                font_size=32,
            )
            draw.text(
                (new_size[0] * 0.5, new_size[1] * 0.235),
                f"{city}, {state}, {country}",
                anchor="ms",
                font_size=43,
            )
            draw.text(
                (new_size[0] * 0.5, new_size[1] * 0.2925),
                record.get_weather_condition(),
                anchor="ms",
                font_size=24,
            )
            draw.text(
                (new_size[0] * 0.5, new_size[1] * 0.5),
                record.get_temp(),
                anchor="ms",
                font_size=135,
            )

            # Humidity
            draw.text(
                (new_size[0] * 0.22375, new_size[1] * 0.7),
                "Humidity",
                anchor="ms",
                font_size=24,
            )
            draw.text(
                (new_size[0] * 0.22375, new_size[1] * 0.755),
                record.get_humidity(),
                anchor="ms",
                font_size=43,
            )
            # Feels Like
            draw.text(
                (new_size[0] * 0.4425, new_size[1] * 0.7),
                "Feels Like",
                anchor="ms",
                font_size=24,
            )
            draw.text(
                (new_size[0] * 0.4425, new_size[1] * 0.755),
                record.get_feels_like(),
                anchor="ms",
                font_size=43,
            )
            # Wind Speed
            draw.text(
                (new_size[0] * 0.71875, new_size[1] * 0.7),
                "Wind Speed",
                anchor="ms",
                font_size=24,
            )
            draw.text(
                (new_size[0] * 0.71875, new_size[1] * 0.755),
                record.get_wind_speed(),
                anchor="ms",
                font_size=43,
            )

            # Rain and snow display

            if record.has_rain() and record.has_snow():
                draw.text(
                    (new_size[0] * 0.39125, new_size[1] * 0.84125),
                    "Rain",
                    anchor="ms",
                    font_size=24,
                )
                draw.text(
                    (new_size[0] * 0.39125, new_size[1] * 0.8975),
                    record.get_rain(),
                    anchor="ms",
                    font_size=43,
                )
                draw.text(
                    (new_size[0] * 0.6125, new_size[1] * 0.84125),
                    "Snow",
                    anchor="ms",
                    font_size=24,
                )
                draw.text(
                    (new_size[0] * 0.6125, new_size[1] * 0.8975),
                    record.get_snow(),
                    anchor="ms",
                    font_size=43,
                )
            elif record.has_rain():
                draw.text(
                    (new_size[0] * 0.5, new_size[1] * 0.84125),
                    "Rain",
                    anchor="ms",
                    font_size=24,
                )
                draw.text(
                    (new_size[0] * 0.5, new_size[1] * 0.8975),
                    record.get_rain(),
                    anchor="ms",
                    font_size=43,
                )
            elif record.has_snow():
                draw.text(
                    (new_size[0] * 0.5, new_size[1] * 0.84125),
                    "Snow",
                    anchor="ms",
                    font_size=24,
                )
                draw.text(
                    (new_size[0] * 0.5, new_size[1] * 0.8975),
                    record.get_snow(),
                    anchor="ms",
                    font_size=43,
                )

            # Credit text
            draw.text(
                (new_size[0] * 0.5, new_size[1] * 0.95),
                "Weather data provided from openweathermap.org",
                anchor="ms",
                font_size=12,
            )
            download_path = os.path.expanduser(
                os.path.join(
                    "~", "Downloads", f"{city}-{record.get_datetime("filename")}.jpg"
                )
            )
            new_im.save(download_path)
            new_im.close()
            print(f"File saved to [bold green]{download_path}[/bold green]")

    except Exception as err:
        print(f"[bold red]Error: [/bold red]", err)
