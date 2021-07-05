#%%
import requests
data = {"a_key": "a_value"}
url = "http://127.0.0.1:4002/api/test?device_id=100"
# response = requests.post(url, data)
response = requests.get(url)
print(response.text)
