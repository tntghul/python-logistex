import requests

url = "http://127.0.0.1:5000/api/update-status"
data = {
    "order_id": 6152,
    "current_step": 1
}

response = requests.post(url, json=data)

print("Status Code:", response.status_code)
print("Response Body:", response.json())
