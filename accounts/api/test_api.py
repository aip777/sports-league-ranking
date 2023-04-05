import json
import requests

login_endpoint = "http://127.0.0.1:8000/account/login-api/"
register_endpoint = "http://127.0.0.1:8000/account/register/"

headers = {
    "Content-Type":"application/json"
}
# data = {
#     "email":"admin@admin.com",
#     "password":"admin"
# }
# response = requests.post(login_endpoint, data=json.dumps(data), headers=headers)
# print(response)

### Register

data = {
    "username":"emarn",
    "email":"emarn@admin.com",
    "password":"admin123"
}
response = requests.post(register_endpoint, data=json.dumps(data), headers=headers)
# result = response.json()
print(response)