import requests

url = "http://20.244.56.144/evaluation-service/auth"

data = {'email': 'devanshsharma9314@gmail.com',
        'name': 'devansh sharma',
          'rollNo': '9922103087', 
          'accessCode': 'SrMQqR', 
          'clientID': '72bef2b8-515d-4e5a-a3bf-13b3a609582f', 
          'clientSecret': 'tNsDEJajJnheZnJH'}

response = requests.post(url, json=data)

if response.status_code == 200:
    print("Authentication Successful:")
    print(response.json())
else:
    print("Authentication Failed:", response.status_code)
    print(response.text)

    