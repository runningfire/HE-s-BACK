# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 19:02:26 2023

@author: home
"""

import asyncio, time, sys
from aiohttp import ClientSession



quality_calman = lambda quality_prev, disp: (quality_prev*disp**2)/(quality_prev + disp**2)
Own_eth = lambda own_ethprev, disp, quality, eth: own_ethprev + (quality/disp**2)*(eth - own_ethprev) #Первые два выражения это Фильтр Калмана
percentage = lambda prev_value, current_value: (abs(current_value - prev_value))/current_value #Вычисление процентов для проверки условия


async def get_price(base, path):
    async with ClientSession() as session:
        url = base + path
        params = {'symbol': 'ETHUSDT', 'limit':1, 'interval': '0m'}
        async with session.get(url=url, params=params) as response:
            resp = await response.json()
            try:
                return resp['price']
            except KeyError:
                return None
        

def checker_60(prev, current):  #Проверяет не изменилась ли валюта
    change = percentage(prev, current)
    #if change >= 0.01:
    change = round(change, 4)
    print(f'Значение изменилось на {change*100}%, Текущее значение валюты: {current}$')


def cleaner_calman(disp, qual_prev, value_prev, value): #Здесь лучше через web aiohttp, но я пока это изучаю.
    qual =  quality_calman(qual_prev, disp)
    new_value = Own_eth(value_prev, disp, qual, value)
    return qual, new_value                              #Фильтр Калмана для дискретного времени через лямбда выражения


async def main(base, path, disp, qual, value):
    '''
    

    Parameters 
    ----------
    base : string
        Главная часть гиперссылки при запросе.
    path : string
        Вспомогательная часть гиперссылки, её можно менять, 
        если нужно получить другие данные.
    disp : float
        Дисперсия значений валюты, полученная из предыдущего задания. Принята постоянной, 
        так как одно значение мало изменяет дисперсию при выборке в 180 значений.
    qual : float
        Критерий качества фильтра Калмана для дискретного времени. Используется при подсчёте собственного значения валюты
    value :float
        Последнее собственное значение валюты из выборки в первом задании, используется для подсчёта первого значения в этой программе.

    -------
    Основная функция для исполнения всего кода.


    '''
    t0 = time.perf_counter()
    Itter = 0
    while True:
        task_get = asyncio.create_task(get_price(base, path))
        price = await asyncio.gather(task_get)
        while price[0] is None:
            print('Произошла ошибка при получении данных.\nПовторная попытка.')
            task_get = asyncio.create_task(get_price(base, path))
            price = await asyncio.gather(task_get)
            pass
        price = float(price[0])       
        if Itter == 0:
            price0 = price
        if ((time.perf_counter() - t0) >= 24*60*60) or (Itter == 0):
            t0 = time.perf_counter()
            tuple_value = cleaner_calman(disp, qual, value, price)
            qual = tuple_value[0]
            value = round(tuple_value[1], 2)
            print(f'Cобственное значение валюты:{value}$. \nМетод используется раз в сутки, так как исходные наблюдения происходили раз в сутки')
        if (time.perf_counter() - t0) >= 60*60:
            t0 = time.perf_counter()
            checker_60(price0, price)
            price0 = price
        Itter += 1 
        await asyncio.sleep(3)





if __name__ == '__main__':
    b =  'https://fapi.binance.com' 
    p =  '/fapi/v1/ticker/price'
    disp = 11467.80    #Это начальные параметры, взяты значения из анализа валюты за полгода каждый день(скрипт p1)
    qual = 722584.22   #Проверено, что за большое количество итераций через метод, разница между значениями уменьшается вместе с критерием качества
    value = 1422.04
    if (sys.platform).find('win') != -1:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main(b, p, disp, qual, value))        

                                      
                         