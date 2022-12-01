import requests

request_data = { "user_id": 7, "bank":"BBVA", "clabe":"123416789123456788"}
API_URL = "https://hnk1omclb5.execute-api.us-east-1.amazonaws.com/Development/createdatabank"
try:
    response = requests.post(API_URL, json=request_data)
    res = response.json()
    print(res)
except:
    print("except")