import asyncio
import time


class MyCity:
    lon = 3.14
    lat = 50.67


async def get_forecast_7timer() -> list:
    return ['Forecast 1']


async def get_forecast_open_meteo() -> list:
    return ['Forecast 2']


async def get_forecast_accu_weather() -> list:
    return ['Forecast 3']


async def main():
    fc1, fc2, fc3 = await asyncio.gather(get_forecast_7timer(), get_forecast_open_meteo(), get_forecast_accu_weather())
    print(fc1, fc2, fc3)


if __name__ == '__main__':
    t = time.perf_counter()
    asyncio.run(main())
    time_spent = time.perf_counter() - t
    print(f'\nTime spent: {time_spent:.4f} sec')
