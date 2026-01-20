def kelvin_to_f(k_temp: float) -> str:
    result = (k_temp * 1.8) - 459.67
    return "{:.2f} F".format(result)


def kelvin_to_c(k_temp: float) -> str:
    result = k_temp - 273.15
    return "{:.2f} C".format(result)


def wind_speed_to_kmph(speed: float) -> str:
    result = speed * 3.6
    return "{:.2f} km/h".format(result)


def wind_speed_to_mph(speed: float) -> str:
    result = speed * 2.2369362921
    return "{:.2f} mi/h".format(result)


def mm_to_in(mm_val: float) -> str:
    result = mm_val * 0.0393700787
    return "{:.2f} in".format(result)
