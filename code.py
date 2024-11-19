import requests

# Define the URL and Bearer token
url = 'https://api.example.com/your-endpoint'
token = 'YOUR_BEARER_TOKEN'

# Set up headers with the Bearer token
headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'  # Optional, depending on the API
}

# Make the GET request
response = requests.get(url, headers=headers)

# Check the response
if response.status_code == 200:
    print("Request was successful.")
    print("Response data:", response.json())  # Assuming the response is in JSON format
else:
    print(f"Request failed with status code {response.status_code}")
    print("Error response:", response.text)
