import requests
import json

url = 'http://api.msg91.com/api/v2/sendsms'

headers = {
    'authkey':'263822AtqZb3rXHfIk5c6f0be5',
    'Content-Type':'application/json'
}

data = {
    "sender": "ALERTF",
    "route": "4",
    "country": "91",
    "sms": [
        {
            "message": "Message pdhoge to pitoge",
            "to": [
                "9592400151",
                "7015557612"
            ]
        }
    ]
}

response = requests.post(url = url, data = json.dumps(data), headers = headers)
print(response)
print(response.text)
print(response.status_code)