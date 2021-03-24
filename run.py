import time

from vk_slaves import Slaves # pip install vk-slaves
from config import settings

token = settings['TOKEN']
local_id = settings['ID']
min_profit = settings['MIN_PROFIT']

client = Slaves(token)

def get_slaves(id):
    return client.slave_list(id=id)

def fetter(id):
    return client.buy_fetter(slave_id=id)

def get_slaves_to_fetter(slaves_list):
    slaves = {}

    current_time = int(time.time()) # текущее unix-время
    for slave in slaves_list['slaves']: # Получаем каждого раба в словаре
        if min_profit <= slave['profit_per_min']: # минимальный профит в конфиге удовлетворяет рабу
            if slave['fetter_to'] < current_time: # проверяем время цепей раба
                slaves[slave['id']] = slave['fetter_price'] # добавляем раба в наш словарь

    # сортируем рабов по цене
    {k: v for k, v in sorted(slaves.items(), key=lambda item: item[1])}
    
    # возвращаем айди рабов
    return list(slaves.keys())



if __name__ == '__main__':
    # start
    client.start()

    while True:
        # получение данных о себе
        me = client.user(local_id)

        # получение баланса
        balance = me['balance']

        # получение списка ваших рабов
        slaves_list = get_slaves(local_id)

        # получаем список рабов подлежащих оцепенению
        slaves_to_fetter = get_slaves_to_fetter(slaves_list)

        # кидаем цепи на рабов
        for slave in slaves_to_fetter:
            fetter(slave)

        # тихий час
        time.sleep(20)
