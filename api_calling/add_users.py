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

for i in range(10):
    for i in range(100):
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
存在问题：
    当发送请求时，没有办法确保每一个请求都可以发送成功。待改进  √
    
    wo 当状态码不为200时，我就一直发送请求，
    设置程序退出条件，
    状态码为400，是服务器那边设置的用户已存在的状态码
    200是又一次发送请求后成功状态码
'''