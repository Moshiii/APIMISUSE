import requests
import time

# # Replace ACCESS_TOKEN with your actual access token
headers = {'Authorization': 'token  <API_TOKEN>'}

url = "https://api.github.com/rate_limit"
response = requests.get(url, headers=headers)

if response.status_code == 200:
    response_json = response.json()
    limit = response_json["rate"]["limit"]
    remaining = response_json["rate"]["remaining"]
    reset_time = response_json["rate"]["reset"]
    print(f"API usage: {remaining}/{limit} requests remaining until {reset_time}")
else:
    print(f"Error: {response.status_code}")
