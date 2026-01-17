from typing import Annotated
import typer
from rich import print
import os
from dotenv import load_dotenv
import requests

load_dotenv()
OW_API_KEY = os.environ.get("OPEN_WEATHER_MAP_API_KEY", "")
OW_API_URL = os.environ.get("WEATHER_API_URL", "")
app = typer.Typer()


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


if __name__ == "__main__":
    app()
