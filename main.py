"""
https://github.com/public-apis/public-apis#weather
"""
import requests, datetime

from pprint import pprint


class MyCity:
    name = 'Lille'
    lon = 3.14
    lat = 50.67


def get_forecast_7timer():
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

    result = requests.get(url=url, params=query_params)

    if result.status_code == 200:
        data = result.json()

        temp_values_for_next_24 = []
        # Сервис дает прогноз на 8 дней с шагом 3 часа, то есть 8 измерений в сутки.
        # Поэтому для прогноза на ближайшие 7 дней, берем первые 56 значений
        for record in data.get('dataseries')[:56]:
            temp_values_for_next_24.append(record.get('temp2m'))

        min_temp = min(temp_values_for_next_24)
        max_temp = max(temp_values_for_next_24)
        avg_temp = sum(temp_values_for_next_24)/len(temp_values_for_next_24)
        print(temp_values_for_next_24, min_temp, max_temp, avg_temp, sep='\n')

def get_forecast_open_meteo():
    """
    https://open-meteo.com/
    :return:
    """
    url = 'https://api.open-meteo.com/v1/forecast'
    query_params = {
        'latitude': MyCity.lat,
        'longitude': MyCity.lon,
        'hourly': 'temperature_2m',
        'forecast_days': 7,
    }

    result = requests.get(url=url, params=query_params)
    if result.status_code == 200:
        data = result.json()
        temp_values_for_next_24 = data.get('hourly').get('temperature_2m')

        min_temp = min(temp_values_for_next_24)
        max_temp = max(temp_values_for_next_24)
        avg_temp = sum(temp_values_for_next_24) / len(temp_values_for_next_24)
        print(temp_values_for_next_24, min_temp, max_temp, avg_temp, sep='\n')


def main():
    get_forecast_7timer()
    get_forecast_open_meteo()


if __name__ == '__main__':
    main()
