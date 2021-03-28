import time
import random
import requests # pip install requests

from threading import Thread
from module import Slaves # module.py
from config import settings # config.py

token = settings['info']['TOKEN']
local_id = settings['info']['ID']
debug = settings['info']['DEBUG']

client = Slaves(token)

from api import * # api.py

balance = 0

# //////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////
# processing slaves functions //////////////////////////////////////////////////

def get_slaves_to_steal(slaves_list):
    slaves = []

    min_price = settings['steal_top']['MIN_PRICE']
    max_price = settings['steal_top']['MAX_PRICE']

    current_time = int(time.time()) # текущее unix-время
    for slave in slaves_list['slaves']: # Получаем каждого раба в словаре
        if slave['fetter_to'] < current_time: # проверяем время цепей раба
            if slave['price'] <= max_price and slave['price'] >= min_price: # если цена подходит под условие
                slaves.append(slave['id']) # добавляем раба в наш список

    return slaves


def get_slaves_to_steal_target(slaves_list):
    slaves = []

    min_price = settings['steal_target']['MIN_PRICE']
    max_price = settings['steal_target']['MAX_PRICE']

    current_time = int(time.time()) # текущее unix-время

    for slave in slaves_list['slaves']: # Получаем каждого раба в словаре
        if slave['fetter_to'] < current_time: # проверяем время цепей раба
            if slave['price'] <= max_price and slave['price'] >= min_price: # если цена подходит под условие
                slaves.append(slave['id']) # добавляем раба в наш список

    return slaves

    
def get_slaves_to_job(slaves_list):
    job_slaves = []

    for slave in slaves_list['slaves']: # Получаем каждого раба в словаре
        if slave['job']['name'] == '': # если безработен
            job_slaves.append(slave['id']) # добавляем раба в безработных

    return job_slaves

def get_slaves_to_abuse(slaves_list):
    abuse_slaves = []

    for slave in slaves_list['slaves']: # Получаем каждого раба в словаре
        if (slave['sale_price'] < 19500):
            abuse_slaves.append(slave['id']) # добавляем раба в безработных

    return abuse_slaves

def get_slaves_to_fetter(slaves_list):
    slaves = {}
    current_time = int(time.time()) # текущее unix-время

    for slave in slaves_list['slaves']: # Получаем каждого раба в словаре
        if (slave['profit_per_min'] * 120) >= slave['fetter_price']: # мы не уйдём в минус
            if slave['fetter_to'] < current_time: # проверяем время цепей раба
                if (slave['profit_per_min'] >= 1000 or (not settings['fet_slaves']['MAX_PROFIT'])):
                    slaves[slave['id']] = 1 - slave['profit_per_min'] / (slave['fetter_price'] + 1) # добавляем раба в наш словарь (по формуле выгодности)

    # сортируем рабов по цене
    {k: v for k, v in sorted(slaves.items(), key=lambda item: item[1])}
    
    # возвращаем айди рабов
    return list(slaves.keys())


# //////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////




# //////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////
# main functions to be used ////////////////////////////////////////////////////



# //////////////////////////////////////////////////////////////////////////////

# Обновление баланса для проверки
# Вывод основной информации
# Автоматическое включение

def update_me():
    global balance
    i = 0

    while True: 
        me = get_user(local_id)

        balance = me['balance']
        slaves = me['slaves_count']
        rating = me['rating_position']
        profit = me['slaves_profit_per_min']

        if (i == 3):
            print(f'[INFO] > {balance}р | {profit}р/мин | {slaves} рабов | {rating} место')
            i = 0

        time.sleep(3.5)

        i += 1

# //////////////////////////////////////////////////////////////////////////////


# //////////////////////////////////////////////////////////////////////////////

# Автоматическая выдача работы рабам
# config.py - job_slaves
# список работы настраивается там же

def job_niggers():
    while True:
        slaves_list = do_start()
        slaves_to_job = get_slaves_to_job(slaves_list)
        print(f'[JOB] > Найдно {len(slaves_to_job)} безработных рабов')
        
        random.shuffle(slaves_to_job)

        for slave in slaves_to_job:
            make_job(slave)

            if (debug):
                print(f'[DEBUG] >>> выдал работу {slave}')

            time.sleep(random.randrange(0, 3) + random.random() * 2.5)
        else:         
            time.sleep(random.randrange(12, 23))

# //////////////////////////////////////////////////////////////////////////////


# //////////////////////////////////////////////////////////////////////////////

# Автоматическая выдача цепей
# config.py - fet_slaves

def fet_niggers():
    while True:
        slaves_list = do_start()
        slaves_to_fetter = get_slaves_to_fetter(slaves_list)
        print(f'[FET] > Найдено {len(slaves_to_fetter)} рабов без цепей')

        random.shuffle(slaves_to_fetter)
        
        # кидаем цепи на рабов
        for slave in slaves_to_fetter:
            fetter(slave)

            if (debug):
                print(f'[DEBUG] >>> кинул цепи на {slave}')

            # обход блокировки
            time.sleep((random.randrange(0, 2) + random.randrange(0, 2)) + min(0.9, 145 / len(slaves_to_fetter)))
            time.sleep(random.randrange(0, 1))
        else:
            time.sleep(random.randrange(11, 18))

# //////////////////////////////////////////////////////////////////////////////


# //////////////////////////////////////////////////////////////////////////////

# Таргетированная кража рабов
# config.py - steal_target
# возможна настройка по ID

def steal_niggers():
    while True:
        
        targets = settings['steal_target']['TARGETS']
        random.shuffle(targets)

        for target in targets:
            info = get_user(target)
            if info['balance'] >= 2147000000: continue
            
            targets_slaves = get_slaves(target)
            slaves_to_steal = get_slaves_to_steal_target(targets_slaves)
            random.shuffle(slaves_to_steal)

            if len(slaves_to_steal) > 0:
                print(f'[TS] > Найдено {len(slaves_to_steal)} раба(ов) для кражи ({target})')

            for slave in slaves_to_steal:
                buy(slave)
                time.sleep(random.randrange(2, 4))

                if (settings['steal_target']['AUTO_FET']):
                    fetter(slave)
                    time.sleep(random.randrange(2, 3))

                if (debug):
                    print(f'[DEBUG] >>> украл {slave} у {target}')

                make_job(slave)

                # обход блокировки
                time.sleep(random.randrange(1, 3) + min(0.9, 155 / len(slaves_to_steal)))
                time.sleep(random.random() * 2.5)

            time.sleep(random.randrange(3, 5))
        
        time.sleep(random.randrange(15, 20))

# //////////////////////////////////////////////////////////////////////////////


# //////////////////////////////////////////////////////////////////////////////

# Абуз рабов для получения большего профита
# Продаёт - Покупает
# Возможна настройка цепей после абуза
# config.py - abuse_slaves

def abuse_niggers():
    while True:
        global balance

        me = get_user(local_id)
        balance = me['balance']

        if (balance >= settings['abuse_slaves']['MIN_BALANCE']):

            if (balance >= 2147000000):
                print('[ABS] > Максимальный баланс!')
                time.sleep(20)
                continue

            slaves_list = do_start()
            slaves_to_abuse = get_slaves_to_abuse(slaves_list)
            random.shuffle(slaves_to_abuse)

            for slave in slaves_to_abuse:
                if (balance < settings['abuse_slaves']['MIN_BALANCE']):
                    break

                id_used = False

                s_price = (get_user(slave))['sale_price']
                while s_price < settings['abuse_slaves']['LIMIT']):
                    id_used = True

                    sale(slave) # продаём
                    time.sleep(random.random() * 2 + random.randrange(0, 2))

                    buy(slave)
                    time.sleep(random.randrange(2, 4))

                    s_price = (get_user(slave))['sale_price']

                    if (debug):
                        print(f'[DEBUG] >>> {slave} в процессе абуза [{s_price}р]')

                if (id_used):
                    print(f'[ABS] > Заабузил {slave}')

                    if (settings['abuse_slaves']['AUTO_FET']):
                        fetter(slave)  
                        time.sleep(random.random() * 2 + random.random() * 3)

                    make_job(slave)
                    time.sleep(random.randrange(1, 3) + random.random())

                    id_used = False

                # update balance
                me = get_user(local_id)
                balance = me['balance']
        
        time.sleep(random.randrange(24, 40))

# //////////////////////////////////////////////////////////////////////////////


# //////////////////////////////////////////////////////////////////////////////

# Кража рабов у топа игроков
# config.py - steal_top

def steal_top():
    top = (get_top())['list']
    users = []
    [users.append(x['id']) for x in top]

    random.shuffle(users)

    while True:
        for target in users:
            info = get_user(target)
            if info['balance'] >= 2147000000: continue

            targets_slaves = get_slaves(target)
            slaves_to_steal = get_slaves_to_steal(targets_slaves)
            random.shuffle(slaves_to_steal)

            if len(slaves_to_steal) > 0:
                print(f'[TOP] > Найдено {len(slaves_to_steal)} раба(ов) для кражи ({target})')

            for slave in slaves_to_steal:
                buy(slave)
                time.sleep(random.randrange(2, 4))

                if (settings['steal_top']['AUTO_FET']):
                    fetter(slave)
                    time.sleep(random.random() + random.randrange(0, 2))

                make_job(slave)

                if (debug):
                    print(f'[DEBUG] >>> украл {slave} у {target}')

                time.sleep((random.randrange(1, 3) + random.randrange(0, 2)) + min(0.9, 155 / len(slaves_to_steal)))
                time.sleep(random.random())

            time.sleep(random.randrange(2, 4))

        time.sleep(random.randrange(8, 15))

# //////////////////////////////////////////////////////////////////////////////


# //////////////////////////////////////////////////////////////////////////////

# Покупка несуществующий id
# config.py - abuse_unknowns

def abuse_unknowns():
    min_id = -325325252
    max_id = -32352522

    while True:
        targets = []
        [targets.append(random.randrange(min_id, max_id)) for _ in range(1000)]
        targets = set(targets)

        print(f'[UNK] > Сгенерировал список из {len(targets)} id')

        for target in targets:
            info = get_user(target)

            if ((info['price'] >= settings['abuse_unknowns']['MIN_PRICE']) and (info['price'] <= settings['abuse_unknowns']['MAX_PRICE'])):

                buy(target)
                time.sleep(random.randrange(1, 3))
                
                if (settings['abuse_unknowns']['AUTO_FET']):
                    fetter(target)

                if (debug):
                    print(f'[DEBUG] >>> (UNK) Купил {target}')

            time.sleep(random.randrange(0, 2) + random.random())

# //////////////////////////////////////////////////////////////////////////////

# //////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////



# just start

if __name__ == '__main__':
    do_start()

    Thread(target=update_me).start()

    if (settings['job_slaves']['ENABLED']):
        Thread(target=job_niggers).start()

        if (settings['job_slaves']['MULTI-THREAD']):
            Thread(target=job_niggers).start()


    if (settings['fet_slaves']['ENABLED']):
        Thread(target=fet_niggers).start()

        if (settings['fet_slaves']['MULTI-THREAD']):
            Thread(target=fet_niggers).start()


    if (len(settings['steal_target']['TARGETS'])):
        Thread(target=steal_niggers).start()

        if (settings['steal_target']['MULTI-THREAD']):
            Thread(target=steal_niggers).start()


    if (settings['abuse_slaves']['ENABLED']):
        Thread(target=abuse_niggers).start()

        if (settings['abuse_slaves']['MULTI-THREAD']):
            Thread(target=abuse_niggers).start()


    if (settings['steal_top']['ENABLED']):
        Thread(target=steal_top).start()

        if (settings['steal_top']['MULTI-THREAD']):
            Thread(target=steal_top).start()


    if (settings['abuse_unknowns']['ENABLED']):
        Thread(target=abuse_unknowns).start()

        if (settings['abuse_unknowns']['MULTI-THREAD']):
            Thread(target=abuse_unknowns).start()
