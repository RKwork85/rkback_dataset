from app import User, db
from faker import Faker
import json
import requests
import time 

faker = Faker(locale='zh-CN')

def generation():
    for i in range(10):
        print(faker.name())
        print(faker.email())
        print(faker.phone_number())
        print(faker.address())

headers = {'Content-Type': 'application/json'}  


data = {
    'username' :faker.name(),
    'email' : faker.email()
}
resp = requests.post(url='http://127.0.0.1:5000/user', data=json.dumps(data), headers=headers)
print(resp.json())

while resp.status_code!=200:  
        print(data)
        time.sleep(2)
        resp = requests.post(url='http://127.0.0.1:5000/user', data=json.dumps(data), headers=headers)
        if resp.status_code==200 or resp.status_code==400:
            break
        else:
            continue

time.sleep(1)

'''
添加一条数据
headers 需要添加，不然 爆json格式错误
'''