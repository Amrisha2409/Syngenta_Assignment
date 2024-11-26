import requests

# Test URL
url = "http://api.openweathermap.org/data/2.5/weather?q=Pune&appid=6f40f87e32a28866983fb5dea5ca0f11&units=metric"
response = requests.get(url)
print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")