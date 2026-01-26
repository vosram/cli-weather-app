# CLI Weather App

This project is a personal project created as a part of the [Boot.dev](https://www.boot.dev) course.

This app gets weather data from [openweathermap.org One Call API 3.0](https://openweathermap.org/api/one-call-3). To get this setup please go to their [pricing page](https://openweathermap.org/price) where you can subscribe to the One Call API 3.0 plan. It is free for up to 1,000 calls per day but does require a credit/debit card on file. Once you are subscribed, get an API key and add the key to a `.env` file in the root of this project.

## Set Up

This project uses [uv](https://docs.astral.sh/uv/getting-started/installation/) as the python package and project manager. Install it first then continue with this setup. All dependencies and virtual env will be setup when you first run `uv run main.py`. If you wish to do this manually, then run `uv sync` first and that will do the same thing before running any python script. The next few sections will help you prepare the project locally to use it as intended.

### Env File

This project requires a `.env` file in the root of the project. The file should look like this:

```text
OPEN_WEATHER_MAP_API_KEY=<API key>
WEATHER_API_URL=<API url>
```

The API url as of creating this project is `https://api.openweathermap.org`. The API calls made by `requests` utilize these env variables. The resource path of the url and query params are setup in the commands. Enviroment variables are loaded with `load_dotenv()` and if they're not set, it will cause an error and exit any command that calls the weather api. Which is literally every command available which we will detail further down in this document.

### Image Export for Current Command

There is a feature in the `current` command that allows you to export some of the basic data to an image you can share anywhere like chat messengers, social media, etc... To set this up, check out the [docs for this feature](/docs/Commands.md#image-creation). Essentially you need 7 images that are at least 800px by 800px and named like the following (they should be in an `images` folder in the root directory of the project):

- `images/atmosphere.jpg`
- `images/clear.jpg`
- `images/clouds.jpg`
- `images/drizzle.jpg`
- `images/rain.jpg`
- `images/snow.jpg`
- `images/thunderstorm.jpg`


## How to use

There are 5 commands available once the project is fully setup.

- searchcity
- current
- 12hours
- 24hours
- 8days

If you wish to see full documentation on each command, you can either see the [docs here](/docs/Commands.md) or use the CLI app like the following:

```bash
uv run main.py command --help
```

## Example Of A Workflow

```bash
uv run main.py searchcity 'Austin,TX,US'
```

```text
---Response---
Austin, Texas, US
        Copy the following code: 30.2711286,-97.7436995
```

```bash
uv run main.py current -t c -i 30.2711286,-97.7436995
```

```text
---Response---
Current weather in Austin, Texas, US

Sun Jan 25, 2026 11:42 AM
Clouds: overcast clouds
┏━━━━━━━━━━━━━┳━━━━━━━━━━━━┓
┃ Measurement ┃ Value      ┃
┡━━━━━━━━━━━━━╇━━━━━━━━━━━━┩
│ Temp        │ -4.15 C    │
│ Feels like  │ -11.09 C   │
│ Humidity    │ 85%        │
│ Wind Speed  │ 14.97 mi/h │
│ Wind Gust   │ 21.85 mi/h │
└─────────────┴────────────┘
File saved to /Users/<username>/Downloads/Austin-2026-01-25-11-42-56.jpg
```

The image exported to your Downloads folder would look like this:

![exported image from current command](/docs/assets/Austin-2026-01-25-11-42-56.jpg)


# Roadmap

- [x] Implement searchcity command
- [x] Implement current command 
- [x] Implement WeatherRecord class
- [x] Implement 12hour command
- [x] Implement 24hour command
- [x] Implement 8days command
- [x] Implement Image Creation
- [x] Add alerts to commands