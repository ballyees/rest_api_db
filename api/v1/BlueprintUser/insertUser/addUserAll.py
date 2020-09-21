import sqlite3
import requests
from os.path import join, dirname, abspath
import random
import threading

def rand_pass(t=0, minl=10, maxl=14):
    l = random.randint(minl, maxl+1)
    passw = ''
    for i in range(l):
        toggle = random.randint(0, 3)
        if toggle:
            if toggle == 1:
                passw += chr(random.randint(ord('a'), ord('z')+1))
            else:
                passw += chr(random.randint(ord('A'), ord('Z')+1))
        else:
            passw += str(random.randint(0, 10))
    if t:
        print(f'password lenght: {l}')
        print(f'password random: {passw}')
    return passw
def thread_function(name):
    for i in range(100):
        data = rand_pass()
        params = {'username': data, 'password': data}
        # print(params)
        r = requests.post('http://127.0.0.1:8000/v1/api/user/fakeUser', json=params)
        print(r.json())

for i in range(100):
    print(f'Thread {i} : start')
    x = threading.Thread(target=thread_function, args=(i,))
    x.start()