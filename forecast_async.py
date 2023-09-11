import aiohttp
import asyncio
import time
import json


class MyCity:
    lon = 3.14
    lat = 50.67


async def get_forecast_7timer() -> list:
    """
    Get temperature values for next 5 days from 7timer.info
    http://www.7timer.info/doc.php?lang=en

    :return: list of values: temperature forecast for the next 5 days at 3 hour intervals
    """
    # return [20]
    url = 'http://www.7timer.info/bin/api.pl'
    query_params = {
        "lon": MyCity.lon,
        "lat": MyCity.lat,
        "product": 'civil',
        "output": 'json',
        "tzshift": 0,
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, params=query_params) as response:
            if response.status == 200:
                # JSON-энкодер библиотеки aiohttp не справляется с JSON-ответом, который генерирует этот сайт.
                # Поэтому получаем ответ в виде текста и преобразовываем его через энкодер библиотеки json.
                # Но вообще это странно, т.к. экодер библиотеки requests прекрасно читает этот JSON-ответ.
                forecast_as_text = await response.text()
                forecast = json.loads(forecast_as_text)
                temp_values_for_next_5_days = []
                # Сервис дает прогноз на 8 дней с шагом 3 часа, то есть 8 измерений в сутки.
                # Поэтому для прогноза на ближайшие 5 дней, берем первые 40 значений
                for record in forecast.get('dataseries')[:40]:
                    temp_values_for_next_5_days.append(record.get('temp2m'))
                return temp_values_for_next_5_days
            else:
                return []


async def get_forecast_open_meteo() -> list:
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
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, params=query_params) as response:
            if response.status == 200:
                forecast = await response.json()
                temp_values_for_next_5_days = forecast.get('hourly').get('temperature_2m')
                return temp_values_for_next_5_days
            else:
                return []


async def get_forecast_accu_weather() -> list:
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
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, params=query_params) as response:
            if response.status == 200:
                location_key_json = await response.json()
                location_key = location_key_json.get('Key')
            else:
                return []

    # Получить прогноз погоды
    url = f'http://dataservice.accuweather.com/forecasts/v1/daily/5day/{location_key}'
    query_params = {
        'apikey': api_key,
        'metric': 'true'
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, params=query_params) as response:
            if response.status == 200:
                forecast = await response.json()
                temp_values_for_next_5_days = []
                for _ in forecast.get('DailyForecasts'):
                    temp_values_for_next_5_days.append(_.get('Temperature').get('Maximum').get('Value'))
                    temp_values_for_next_5_days.append(_.get('Temperature').get('Minimum').get('Value'))
                return temp_values_for_next_5_days
            else:
                return []


async def main():

    fc1, fc2, fc3 = await asyncio.gather(get_forecast_7timer(), get_forecast_open_meteo(), get_forecast_accu_weather())

    print('Temperature forecast from 7timer.info:', fc1, sep='\n', end='\n')
    print('Temperature forecast from OpenMeteo:', fc2, sep='\n', end='\n')
    print('Temperature forecast from AccuWeather:', fc3, sep='\n', end='\n')

    temp_values = fc1 + fc2 + fc3

    average_temp_value = sum(temp_values) / len(temp_values)
    print(f'Average temperature:\n{average_temp_value:.2f} C')


if __name__ == '__main__':
    t = time.perf_counter()
    asyncio.run(main())
    time_spent = time.perf_counter() - t
    print(f'\nTime spent: {time_spent:.4f} sec')
