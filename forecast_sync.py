"""
https://github.com/public-apis/public-apis#weather
"""
import requests
import time


class MyCity:
    lon = 3.14
    lat = 50.67


def get_forecast_7timer() -> list:
    """
    Get temperature values for next 5 days from 7timer.info
    http://www.7timer.info/doc.php?lang=en

    :return: list of values: temperature forecast for the next 5 days at 3 hour intervals
    """

    url = 'http://www.7timer.info/bin/api.pl'
    query_params = {
        "lon": MyCity.lon,
        "lat": MyCity.lat,
        "product": 'civil',
        "output": 'json',
        "tzshift": 0,
    }

    response = requests.get(url=url, params=query_params)

    if response.status_code == 200:
        forecast = response.json()

        temp_values_for_next_5_days = []
        # Сервис дает прогноз на 8 дней с шагом 3 часа, то есть 8 измерений в сутки.
        # Поэтому для прогноза на ближайшие 5 дней, берем первые 40 значений
        for record in forecast.get('dataseries')[:40]:
            temp_values_for_next_5_days.append(record.get('temp2m'))
        return temp_values_for_next_5_days
    else:
        return []


def get_forecast_open_meteo() -> list:
    """
    Get temperature values for next 5 days from Open Meteo
    https://open-meteo.com/

    :return: list of values: temperature forecast for the next 5 days at 1 hour intervals
    """
    url = 'https://api.open-meteo.com/v1/forecast'
    query_params = {
        'latitude': MyCity.lat,
        'longitude': MyCity.lon,
        'hourly': 'temperature_2m',
        'forecast_days': 5,
    }

    response = requests.get(url=url, params=query_params)
    if response.status_code == 200:
        forecast = response.json()
        temp_values_for_next_5_days = forecast.get('hourly').get('temperature_2m')
        return temp_values_for_next_5_days
    else:
        return []


def get_forecast_accu_weather() -> list:
    """
    Get temperature values for next 5 days from AccuWeather
    https://developer.accuweather.com/apis
    apikey = 'vwKlaeDmagfRGAycHzvxwInGupggm0tF'

    :return: list of values: temperature forecast for the next 5 days - min & max values for each day
    """
    api_key = 'vwKlaeDmagfRGAycHzvxwInGupggm0tF'

    # Получить код местоположения
    url = 'http://dataservice.accuweather.com/locations/v1/cities/geoposition/search'
    query_params = {
        'apikey': api_key,
        'q': f'{MyCity.lat},{MyCity.lon}'
    }

    response = requests.get(url=url, params=query_params)
    if response.status_code == 200:
        location_key = response.json().get('Key')
    else:
        return []

    url = f'http://dataservice.accuweather.com/forecasts/v1/daily/5day/{location_key}'
    query_params = {
        'apikey': api_key,
        'metric': 'true'
    }
    response = requests.get(url=url, params=query_params)
    if response.status_code == 200:
        forecast = response.json()
        temp_values_for_next_5_days = []
        for _ in forecast.get('DailyForecasts'):
            temp_values_for_next_5_days.append(_.get('Temperature').get('Maximum').get('Value'))
            temp_values_for_next_5_days.append(_.get('Temperature').get('Minimum').get('Value'))
        return temp_values_for_next_5_days
    else:
        return []


def main():
    fc1 = get_forecast_7timer()
    print('Temperature forecast from 7timer.info:', fc1, sep='\n', end='\n')

    fc2 = get_forecast_open_meteo()
    print('Temperature forecast from OpenMeteo:', fc2, sep='\n', end='\n')

    fc3 = get_forecast_accu_weather()
    print('Temperature forecast from AccuWeather:', fc3, sep='\n', end='\n')

    temp_values = fc1 + fc2 + fc3

    average_temp_value = sum(temp_values) / len(temp_values)
    print(f'Average temperature:\n{average_temp_value:.2f} C')


if __name__ == '__main__':
    t = time.perf_counter()
    main()
    time_spent = time.perf_counter() - t
    print(f'\nTime spent: {time_spent:.4f} sec')

