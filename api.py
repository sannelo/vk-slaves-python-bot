import time
import random
import requests # pip install requests

from run import client
from config import settings

# //////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////
# Default Calls using API //////////////////////////////////////////////////////


def do_start():
    try:
        start = client.start()
        return start
    except Exception as e:
        print(str(e))
        time.sleep(15)
        return do_start()

def get_user(id):
    try:
        user = client.user(id=id)
        return user
    except Exception as e:
        print(str(e))
        time.sleep(15)
        return get_user(id)

def get_slaves(id):
    try:
        slaves = client.slave_list(id=id)
        return slaves
    except Exception as e:
        print(str(e))
        time.sleep(15)
        return get_slaves(id)

def buy(id):
    try:
        a_buy = client.buy_slave(slave_id=id)
        return a_buy
    except Exception as e:
        print(str(e))
        time.sleep(15)
        return buy(id)

def make_job(id):
    try:
        job = client.job_slave(slave_id=id, job_name=settings['job_slaves']['JOBS'][random.randrange(0, len(settings['job_slaves']['JOBS']))])
        return job
    except Exception as e:
        print(str(e))
        time.sleep(15)
        return make_job(id)

def fetter(id):
    try:
        a_fetter = client.buy_fetter(slave_id=id)
        return a_fetter
    except Exception as e:
        print(str(e))
        time.sleep(15)
        return fetter(id)

def sale(id):
    try:
        a_sale = client.sale_slave(slave_id=id)
        return a_sale
    except Exception as e:
        print(str(e))
        time.sleep(15)
        return sale(id)

def get_top():
    try:
        top = client.top_users()
        return top
    except Exception as e:
        print(str(e))
        time.sleep(15)
        return get_top()


# //////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////
# //////////////////////////////////////////////////////////////////////////////