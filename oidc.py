import requests
import json

# API endpoint URL (replace with the one shown in Postman)
url = "https://confluence.corp.etradegrp.com/rest/api/content/453863638?expand=body.view"

# Credentials (replace with your username and password)
username = "your_username"  # Replace with your Confluence username
password = "your_password"  # Replace with your Confluence password

# Make the GET request with Basic Authentication
response = requests.get(url, auth=(username, password))

# Check the response status
if response.status_code == 200:
    # Parse the JSON response
    content = response.json()
    
    # Print the response nicely
    print(json.dumps(content, indent=4))
    
    # Optionally save the JSON response to a file
    with open("response.json", "w", encoding="utf-8") as f:
        json.dump(content, f, ensure_ascii=False, indent=4)
        print("Response saved to 'response.json'")
else:
    print(f"Request failed with status code {response.status_code}")
    print("Error response:", response.text)
