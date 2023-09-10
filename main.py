"""
https://github.com/public-apis/public-apis#weather
"""
import requests

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
        for record in data.get('dataseries')[:8]:
            temp_values_for_next_24.append(record.get('temp2m'))

        min_temp = min(temp_values_for_next_24)
        max_temp = max(temp_values_for_next_24)
        avg_temp = sum(temp_values_for_next_24)/len(temp_values_for_next_24)
        print(temp_values_for_next_24, min_temp, max_temp, avg_temp)


def main():
    get_forecast_7timer()


if __name__ == '__main__':
    main()
