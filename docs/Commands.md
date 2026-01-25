# Commands Available

Since this project uses Typer to create a nice CLI, we are using functions to serve as CLI "commands".

A general use flow would be to use:

```Bash
uv run main.py CitySearch 'My City, State'

<return will contain a list of ids>

uv run main.py 12hour -tm celcius --to-image 12345
```

Here is a complete list of commands available

- searchcity
- current
- 12hours
- 24hours
- 8days

## SearchCity

This command helps to find the latitude and longitude needed to get the exact location to get the weather. The [OpenWeather geocoding API](https://openweathermap.org/api/geocoding-api) will return a list of potential locations so our CLI will provide a list of details for each location along with a clearly visible `lat` and `lon` that a user can copy and paste for the next command they want to execute.

### SearchCity Arguments

`cityname` is the **required** argument that is the name of the city the user is searching for. The CLI can deliver a list of cities with their `lats` and `lons`. The correct way to format the search is `<city name>,<state code>,<country code>` where country code is in [ISO 3166](https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes). The state code and even country code can be omitted, but this will usually cause a longer list to be displayed. For a more precise and smaller list, use both the state code and country code.

For example

```bash
uv run main.py searchcity 'Los Angeles,CA,US'

uv run main.py searchcity 'Los Angeles,US'
```

## Current Command

This command will get the [current weather information](https://openweathermap.org/api/one-call-3#how). It should have some of the following options and arguments.

### Current Arguments

The current command really only needs 1 argument, that being `coords`. This `coords`, formatted like `lat,lon`, can be fetched from the `searchcity` command to search for the `lat` and `lon`.

### Current Options

`-t`,`--t-metric` is "f" for Fahrenheit by default, but can be set to "c" for Celcius. Any other value will cause an error and exit.

`-w`, `--w-metric` is "m" for miles per hour by default but can be set to "k" for kilometers per hour. Any other value will cause an error and exit.

`-i`, `--to-image` is a boolean that will cause the data to be exported to a sharable image file.

### Image Creation

The function to create an image of the current weather data uses background images in a `images` folder within the root folder of this project. These images are not added in the repo to keep the repo light and to allow customization of the images one would like to use. To use this functionality, create the following files:

- `images/atmosphere.jpg`
- `images/clear.jpg`
- `images/clouds.jpg`
- `images/drizzle.jpg`
- `images/rain.jpg`
- `images/snow.jpg`
- `images/thunderstorm.jpg`

The images must be at least 800px by 800px. The images don't need to be 1:1 ratio, if the image is landscape or portrait, the image will be centered to fill 800px x 800px. I used images from unsplash. You can find the exact ones I used here:

- [atmosphere](https://unsplash.com/photos/silhouette-of-pine-trees-photo-BS-Uxe8wU5Y)
- [clear sky](https://unsplash.com/photos/white-clouds--qGKIX1Vxtk)
- [clouds](https://unsplash.com/photos/white-clouds-under-blue-sky-during-daytime-gJILnne_HFg)
- [drizzle](https://unsplash.com/photos/macro-photography-of-water-droplets-on-clear-glass-MU93ZoQPNB8)
- [rain](https://unsplash.com/photos/rain-drops-on-window-glass-HCDugQDdtfc)
- [snow](https://unsplash.com/photos/focused-photo-of-a-snow-flake-5AiWn2U10cw)
- [thunderstorm](https://unsplash.com/photos/lightning-strike-on-cloudy-sky-during-night-time-ESL1rIs9j48)

If these images are not available, then the function will return early. Make sure all the image files are both jpg files and named exactly as listed above.

## 12hours Command

This gets the Weather details for [12 hours](https://openweathermap.org/api/one-call-3#current) at the given location. The API actually returns 48 hours of data but we only return 12 hours of data.

### 12hours Arguments

Like the other commands it only requires a `coords` argument. The format is the same as the current command.

### 12hours Options

`-t`,`--t-metric` is "f" for Fahrenheit by default, but can be set to "c" for Celcius. Any other value will cause an error and exit.

`-w`, `--w-metric` is "m" for miles per hour by default but can be set to "k" for kilometers per hour. Any other value will cause an error and exit.

## 24hours Command

This command will get weather information for [24 hours](https://openweathermap.org/api/one-call-3#current) as a list of data for each hour. The API actually returns 48 hours of data but we only return 24 hours of data.

### 24hours Arguments

Like the other commands it only requires a `coords` argument. The format is the same as the current command.

### 24hours Options

`-t`,`--t-metric` is "f" for Fahrenheit by default, but can be set to "c" for Celcius. Any other value will cause an error and exit.

`-w`, `--w-metric` is "m" for miles per hour by default but can be set to "k" for kilometers per hour. Any other value will cause an error and exit.

## 8days Command

This command will get weather data for [8 days](https://openweathermap.org/api/one-call-3#current) at a specified location `coords`.

## 8days Arguments

Like the other commands it only requires a `coords` argument. The format is the same as the current command.

### 8days Options

`-t`,`--t-metric` is "f" for Fahrenheit by default, but can be set to "c" for Celcius. Any other value will cause an error and exit.

`-w`, `--w-metric` is "m" for miles per hour by default but can be set to "k" for kilometers per hour. Any other value will cause an error and exit.

`--to-image` is a boolean that will cause the data to be exported to a sharable image file.
