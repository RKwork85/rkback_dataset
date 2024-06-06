# 这个是注册用户

import requests  
import json  
  
url = 'http://localhost:5000/v1/work/datasets/create'  # 替换为你的服务器地址和端口  
data = {  
    'instruction':'添加数据',  
    'output': '添加数据',
    'uuid': 'c888fb67-dbc1-401a-a3be-ab8bbc348b38'
}  
headers = {'Content-Type': 'application/json', 'Authorization':'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxNzY1OTQ5MiwianRpIjoiNzc0MThlNWMtNDgxNC00YzRmLWE1MWEtZmZjNDU3MzZlMzQ1IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImM4ODhmYjY3LWRiYzEtNDAxYS1hM2JlLWFiOGJiYzM0OGIzOCIsIm5iZiI6MTcxNzY1OTQ5MiwiY3NyZiI6IjdmODM4ZDRhLTQ0MGEtNGM4NC05ZjE1LTliMzYzNzQyMWUwMyIsImV4cCI6MTcxNzY2MDM5Mn0.xTZ1GGjAVh0wby4921HHbkU43PMbGqgyN-qmXUYh4Is'}  
  
resp = requests.post(url=url,data=json.dumps(data), headers=headers)
print(resp.json())

