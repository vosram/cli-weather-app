from typing import Annotated
import typer
from rich import print
from rich.table import Table
from rich.console import Console
import os
from dotenv import load_dotenv
import requests
from lib.formatters import (
    kelvin_to_formatted,
    timestamp_to_fmt_text,
    format_humidity,
    format_wind_speed,
    format_weather_desc,
    format_percipitation,
)
from lib.weatherrecord import WeatherRecord

load_dotenv()
OW_API_KEY = os.environ.get("OPEN_WEATHER_MAP_API_KEY", "")
OW_API_URL = os.environ.get("WEATHER_API_URL", "")
app = typer.Typer()
console = Console()


@app.command()
def main(name: str):
    """
    Say hello to NAME
    """
    print(f"Hello {name}")


@app.command()
def SearchCity(
    name: Annotated[
        str, typer.Argument(help="<city name>,<country code> ie: 'San Antonio,US'")
    ],
):
    """
    Gets the latitude and longitude needed for the other commands.

    Copy the values in blue and paste into other commands.
    """
    print(f"You are searching for [bold green]{name}[/bold green]")
    param_payload = {"q": name, "limit": "5", "appid": OW_API_KEY}
    full_url = f"{OW_API_URL}/geo/1.0/direct"

    res = requests.get(full_url, params=param_payload)

    if res.status_code != 200:
        print(f"[red]request errored with code {res.status_code}[/red]")
        raise typer.Exit(1)
    data = res.json()

    for item in data:
        print(
            f"[bold yellow]{item["name"]}, {item["state"]}, {item["country"]}[/bold yellow]"
        )
        print(f"\tCopy the following code: {item["lat"]},{item["lon"]}")


@app.command()
def current(
    coords: Annotated[
        str,
        typer.Argument(help="<lat>,<lon>"),
    ],
    t_metric: Annotated[
        str,
        typer.Option(
            "--t-metric",
            "-t",
            help="'c' for Celcius 'f' for Fahrenheit.",
            show_default="Fahrenheit",
        ),
    ] = "f",
    w_metric: Annotated[
        str,
        typer.Option(
            "--w-metric",
            "-w",
            help="'m' for mph. 'k' for kmph.",
            show_default="mph",
        ),
    ] = "m",
):
    """
    Gets current weather data for COORDS.

    COORDS should be formatted as '<lat>,<lon>'.
    Latitude and Longitude can be fetched from searchcity command.
    """
    # Interpret CLI options for query params
    if t_metric != "c" and t_metric != "f":
        print(
            "[bold red]Error:[/bold red] --t-metric should be either 'f' or 'c'. Exiting..."
        )
        raise typer.Exit(1)

    if w_metric != "m" and w_metric != "k":
        print(
            "[bold red]Error:[/bold red] --w-metric should be either 'm' or 'k'. Exiting..."
        )
        raise typer.Exit(1)

    parsed_coords = coords.split(",")
    weather_call_params = {
        "appid": OW_API_KEY,
        "exclude": "minutely,hourly,daily,alerts",
        "lat": parsed_coords[0],
        "lon": parsed_coords[1],
    }
    geo_call_params = {
        "appid": OW_API_KEY,
        "limit": 3,
        "lat": parsed_coords[0],
        "lon": parsed_coords[1],
    }
    full_weather_url = f"{OW_API_URL}/data/3.0/onecall"
    full_geoloc_url = f"{OW_API_URL}/geo/1.0/reverse"

    # Call weather API for current weather & Geolocation API
    weather_res = requests.get(full_weather_url, params=weather_call_params)
    if weather_res.status_code != 200:
        print(
            f"[bold red]Error:[/bold red] [red]request errored with code {res.status_code}[/red]"
        )
        raise typer.Exit(1)

    geoloc_res = requests.get(full_geoloc_url, params=geo_call_params)
    if geoloc_res.status_code != 200:
        print(
            f"[bold red]Error:[/bold red] [red]request errored with code {geloc_res.status_code}[/red]"
        )
        raise typer.Exit(1)

    # Prepare Data for Console output
    weather_data = weather_res.json()
    geoloc_data = geoloc_res.json()

    wind_gust = None
    rain = None
    snow = None
    pop = None

    if "rain" in weather_data["current"]:
        rain = weather_data["current"]["rain"]["1h"]

    if "snow" in weather_data["current"]:
        snow = weather_data["current"]["snow"]["1h"]

    if "wind_gust" in weather_data["current"]:
        wind_gust = weather_data["current"]["wind_gust"], w_metric

    w_record = WeatherRecord(
        weather_data["current"]["dt"],
        weather_data["current"]["temp"],
        weather_data["current"]["feels_like"],
        weather_data["current"]["humidity"],
        weather_data["current"]["wind_speed"],
        weather_data["current"]["weather"][0],
        wind_gust=wind_gust,
        rain=rain,
        snow=snow,
        pop=pop,
        temp_units=t_metric,
        wind_units=w_metric,
    )

    # Output of data
    print(
        f"Current weather in [green]{geoloc_data[0]["name"]}, {geoloc_data[0]["state"]}, {geoloc_data[0]["country"]}[/green]"
    )
    print(f"\n{w_record.get_datetime("current")}")
    print(w_record.get_weather_condition())
    table = Table("Measurement", "Value")
    table.add_row("Temp", w_record.get_temp())
    table.add_row("Feels like", w_record.get_feels_like())
    table.add_row("Humidity", w_record.get_humidity())
    table.add_row("Wind Speed", w_record.get_wind_speed())
    if w_record.has_wind_gust():
        table.add_row("Wind Gust", w_record.get_wind_gust())
    if w_record.has_rain():
        table.add_row("Rain", w_record.get_rain())
    if w_record.has_snow():
        table.add_row("Snow", w_record.get_snow())
    console.print(table)


@app.command("12hours")
def _12hours(
    coords: Annotated[
        str,
        typer.Argument(help="<lat>,<lon>"),
    ],
    t_metric: Annotated[
        str,
        typer.Option(
            "--t-metric",
            "-t",
            help="'c' for Celcius 'f' for Fahrenheit.",
            show_default="Fahrenheit",
        ),
    ] = "f",
    w_metric: Annotated[
        str,
        typer.Option(
            "--w-metric",
            "-w",
            help="'m' for mph. 'k' for kmph.",
            show_default="mph",
        ),
    ] = "m",
):
    # Interpret CLI options for query params
    if t_metric != "c" and t_metric != "f":
        print(
            "[bold red]Error:[/bold red] --t-metric should be either 'f' or 'c'. Exiting..."
        )
        raise typer.Exit(1)

    if w_metric != "m" and w_metric != "k":
        print(
            "[bold red]Error:[/bold red] --w-metric should be either 'm' or 'k'. Exiting..."
        )
        raise typer.Exit(1)

    parsed_coords = coords.split(",")
    weather_call_params = {
        "appid": OW_API_KEY,
        "exclude": "current,minutely,daily,alerts",
        "lat": parsed_coords[0],
        "lon": parsed_coords[1],
    }
    geo_call_params = {
        "appid": OW_API_KEY,
        "limit": 3,
        "lat": parsed_coords[0],
        "lon": parsed_coords[1],
    }
    full_weather_url = f"{OW_API_URL}/data/3.0/onecall"
    full_geoloc_url = f"{OW_API_URL}/geo/1.0/reverse"

    # Call weather API for current weather & Geolocation API
    weather_res = requests.get(full_weather_url, params=weather_call_params)
    if weather_res.status_code != 200:
        print(
            f"[bold red]Error:[/bold red] [red]request errored with code {res.status_code}[/red]"
        )
        raise typer.Exit(1)

    geoloc_res = requests.get(full_geoloc_url, params=geo_call_params)
    if geoloc_res.status_code != 200:
        print(
            f"[bold red]Error:[/bold red] [red]request errored with code {geloc_res.status_code}[/red]"
        )
        raise typer.Exit(1)

    # Prepare Data for Console output
    weather_data = weather_res.json()
    geoloc_data = geoloc_res.json()

    hourly_records = []

    for i in range(12):
        data = weather_data["hourly"][i]
        wind_gust = None
        rain = None
        snow = None
        pop = None
        if "wind_gust" in data:
            wind_gust = data["wind_gust"]
        if "rain" in data:
            rain = data["rain"]["1h"]
        if "snow" in data:
            snow = data["snow"]["1h"]
        if "pop" in data:
            pop = data["pop"]
        record = WeatherRecord(
            data["dt"],
            data["temp"],
            data["feels_like"],
            data["humidity"],
            data["wind_speed"],
            data["weather"][0],
            wind_gust=wind_gust,
            rain=rain,
            snow=snow,
            pop=pop,
            temp_units=t_metric,
            wind_units=w_metric,
        )
        hourly_records.append(record)

    print(
        f"12 hour weather for [green]{geoloc_data[0]["name"]}, {geoloc_data[0]["state"]}, {geoloc_data[0]["country"]}[/green]"
    )

    table = Table(
        "Datetime",
        "Temp",
        "Feels Like",
        "Humidity",
        "Wind Speed",
        "Wind Gust",
        "Condition",
        "rain",
        "snow",
        "pop",
    )
    for i in range(12):
        record = hourly_records[i]
        table.add_row(
            record.get_datetime("hourly"),
            record.get_temp(),
            record.get_feels_like(),
            record.get_humidity(),
            record.get_wind_speed(),
            record.get_wind_gust(),
            record.get_weather_condition(),
            record.get_rain(),
            record.get_snow(),
            record.get_pop(),
        )
    console.print(table)


if __name__ == "__main__":
    app()
