"""
https://github.com/public-apis/public-apis#weather
"""
import requests

from pprint import pprint


class MyCity:
    lon = 3.14
    lat = 50.67


def get_forecast_7timer() -> list:
    """
    http://www.7timer.info/doc.php?lang=en

    :return:
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
    https://open-meteo.com/
    :return:
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
    https://developer.accuweather.com/apis
    vwKlaeDmagfRGAycHzvxwInGupggm0tF
    :return:
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
    print(get_forecast_7timer())
    print(get_forecast_open_meteo())
    print(get_forecast_accu_weather())


if __name__ == '__main__':
    main()
