import requests
payload = {
    "token":"XWRl4WvwFeF2ZRV7",
}
res = requests.request('POST', url='http://192.168.1.84:5553/get_user/', json = payload)
print(res.text)
print(res.status_code)