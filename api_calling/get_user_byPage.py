import requests 

with requests.get('http://127.0.0.1:5000//user?page=2&per_page=100') as res:
    print(res.json())


'''
page: 第几页
per_page: 每页多少条数据

'''

