# 这个是注册用户

import requests  
import json  
  
url = 'http://localhost:5000/register'  # 替换为你的服务器地址和端口  
data = {  
    'uuid':'rkkk'
}  
headers = {'Content-Type': 'application/json'}  
  
resp = requests.post(url=url,data=json.dumps(data), headers=headers)
print(resp.json())

