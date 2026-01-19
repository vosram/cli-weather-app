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

    final_data = {
        "loc_name": geoloc_data[0]["name"],
        "loc_state": geoloc_data[0]["state"],
        "loc_country": geoloc_data[0]["country"],
        "currenttime": timestamp_to_fmt_text(weather_data["current"]["dt"]),
        "temp": kelvin_to_formatted(weather_data["current"]["temp"], t_metric),
        "feels_like": kelvin_to_formatted(
            weather_data["current"]["feels_like"], t_metric
        ),
        "humidity": format_humidity(weather_data["current"]["humidity"]),
        "windspeed": format_wind_speed(weather_data["current"]["wind_speed"], w_metric),
        "wind_gust": None,
        "weather": format_weather_desc(weather_data["current"]["weather"][0]),
        "rain": None,
        "snow": None,
    }

    if "rain" in weather_data["current"]:
        final_data["rain"] = format_percipitation(weather_data["current"]["rain"]["1h"])

    if "snow" in weather_data["current"]:
        final_data["snow"] = format_percipitation(weather_data["current"]["snow"]["1h"])

    if "wind_gust" in weather_data["current"]:
        final_data["wind_gust"] = format_wind_speed(
            weather_data["current"]["wind_gust"], w_metric
        )
    # Output of data
    print(
        f"current weather in [green]{final_data["loc_name"]}, {final_data["loc_state"]}, {final_data["loc_country"]}[/green]"
    )
    print(f"\n{final_data["currenttime"]}")
    print(final_data["weather"])
    table = Table("Measurement", "Value")
    table.add_row("Temp", final_data["temp"])
    table.add_row("Feels like", final_data["feels_like"])
    table.add_row("Humidity", final_data["humidity"])
    table.add_row("Wind Speed", final_data["windspeed"])
    if final_data["wind_gust"] is not None:
        table.add_row("Wind Gust", final_data["wind_gust"])
    if final_data["rain"] is not None:
        table.add_row("Rain", final_data["rain"])
    if final_data["snow"] is not None:
        table.add_row("Snow", final_data["snow"])
    console.print(table)


if __name__ == "__main__":
    app()
