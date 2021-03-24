import time
import requests
import random

from vk_slaves import Slaves # pip install vk-slaves
from config import settings

token = settings['TOKEN']
local_id = settings['ID']
min_profit = settings['MIN_PROFIT']
steal = settings['STEAL']
targets = settings['TARGETS']
price = settings['MAX_PRICE']

client = Slaves(token)

jobs = ['Сварщик', 'Шахтёр', 'Бармен', 'Наркоторговец', 'Дилер', 'Брокер', 'Трейдер', 'Инвестор', 'Врач', 'Технарь', 'IT', 'Хирург', 'Бомж', 'Инженер', 'Бригадир']

def _start():
    try:
        return client.start()
    except Exception as e:
        print(str(e))
        time.sleep(15)
        return _start()

def get_user(id):
    try:
        return client.user(id=id)
    except Exception as e:
        print(str(e))
        time.sleep(15)
        return get_user(id)

def get_slaves(id):
    try:
        return client.slave_list(id=id)
    except Exception as e:
        print(str(e))
        time.sleep(15)
        return get_slaves(id)

def buy(id):
    try:
        return client.buy_slave(slave_id=id)
    except Exception as e:
        print(str(e))
        time.sleep(15)
        return buy(id)

def make_job(id, name):
    try:
        return client.job_slave(slave_id=id, job_name=name)
    except Exception as e:
        print(str(e))
        time.sleep(15)
        return make_job(id, name)

def fetter(id):
    try:
        return client.buy_fetter(slave_id=id)
    except Exception as e:
        print(str(e))
        time.sleep(15)
        return fetter(id)

def get_slaves_to_steal(slaves_list):
    slaves = {}

    current_time = int(time.time()) # текущее unix-время
    for slave in slaves_list['slaves']: # Получаем каждого раба в словаре
        if min_profit <= slave['profit_per_min']: # минимальный профит в конфиге удовлетворяет рабу
            if slave['fetter_to'] < current_time: # проверяем время цепей раба
                if slave['price'] <= price: # если цена подходит под условие
                    slaves[slave['id']] = slave['price'] # добавляем раба в наш словарь

    return slaves

def get_slaves_to_fetter(slaves_list):
    slaves = {}
    job_slaves = []

    current_time = int(time.time()) # текущее unix-время
    for slave in slaves_list['slaves']: # Получаем каждого раба в словаре
        if slave['job']['name'] == '': # если безработен
            job_slaves.append(slave['id']) # добавляем раба в безработных
        if min_profit <= slave['profit_per_min']: # минимальный профит в конфиге удовлетворяет рабу
            if slave['fetter_to'] < current_time: # проверяем время цепей раба
                slaves[slave['id']] = slave['fetter_price'] # добавляем раба в наш словарь

    # сортируем рабов по цене
    {k: v for k, v in sorted(slaves.items(), key=lambda item: item[1])}
    
    # возвращаем айди рабов
    return list(slaves.keys()), job_slaves



if __name__ == '__main__':
    # start
    _start()

    while True:
        # получение данных о себе
        #me = get_user(local_id)

        # получение баланса
        #balance = me['balance']

        # получение списка ваших рабов
        slaves_list = get_slaves(local_id)

        # получаем список рабов подлежащих оцепенению и работе
        slaves_to_fetter, slaves_to_job = get_slaves_to_fetter(slaves_list)
        
        print(f'{len(slaves_to_fetter)} раба(ов) подлежат оцепенению')
        print(f'{len(slaves_to_job)} раба(ов) подлежат работе')

        # кидаем цепи на рабов
        for slave in slaves_to_fetter:
            fetter(slave)

        # даём работу рабам
        for slave in slaves_to_job:
            make_job(slave, jobs[random.randrange(0, len(jobs))])

        # покупаем рабов без цепей у целей
        if steal:
            for target in targets:
                targets_slaves = get_slaves(target)
                slaves_to_steal = get_slaves_to_steal(targets_slaves)

                if len(slaves_to_steal) > 0:
                    print(f'Найдено {len(slaves_to_steal)} раба(ов) для кражи')

                for slave in slaves_to_steal:
                    buy(slave)
                    fetter(slave)
                    make_job(slave, jobs[random.randrange(0, len(jobs))])

        # \n
        print('')

        # тихий час
        time.sleep(15)
