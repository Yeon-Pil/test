import requests

URL = "http://127.0.0.1:8000/analyze"

payload = {
    "text": "월급을 받으면 계획 없이 소비해서 저축을 거의 못 하고 있어요."
}

response = requests.post(URL, json=payload, timeout=90)

print("상태 코드:", response.status_code)
print("응답:")
print(response.json())
