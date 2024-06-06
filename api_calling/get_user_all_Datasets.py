import requests 

headers = {'Content-Type': 'application/json', 'Authorization':'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxNzY1OTQ5MiwianRpIjoiNzc0MThlNWMtNDgxNC00YzRmLWE1MWEtZmZjNDU3MzZlMzQ1IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImM4ODhmYjY3LWRiYzEtNDAxYS1hM2JlLWFiOGJiYzM0OGIzOCIsIm5iZiI6MTcxNzY1OTQ5MiwiY3NyZiI6IjdmODM4ZDRhLTQ0MGEtNGM4NC05ZjE1LTliMzYzNzQyMWUwMyIsImV4cCI6MTcxNzY2MDM5Mn0.xTZ1GGjAVh0wby4921HHbkU43PMbGqgyN-qmXUYh4Is'}  

with requests.get('http://127.0.0.1:5000/v1/work/datasets/list', headers=headers) as res:
    print(res.json())


