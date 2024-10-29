import requests
import hashlib
import base64
import random
import string
from urllib.parse import urlencode

# Configuration
config = {
    "issuer": "https://your-identity-provider.com",
    "authorize_endpoint": "/authorize",
    "token_endpoint": "/oauth/token",
    "api_endpoint": "https://api.example.com",
    "client_id": "your-client-id",
    "client_secret": "your-client-secret",
    "redirect_uri": "https://localhost:5443/callback",
    "scope": "openid profile email",
}

# Generate PKCE code verifier and challenge
def generate_code_verifier():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=128))

def generate_code_challenge(verifier):
    challenge = hashlib.sha256(verifier.encode('utf-8')).digest()
    return base64.urlsafe_b64encode(challenge).rstrip(b'=').decode('utf-8')

code_verifier = generate_code_verifier()
code_challenge = generate_code_challenge(code_verifier)

# Step 1: Redirect to Authorization Endpoint
auth_url = f"{config['issuer']}{config['authorize_endpoint']}?" + urlencode({
    "response_type": "code",
    "client_id": config["client_id"],
    "redirect_uri": config["redirect_uri"],
    "scope": config["scope"],
    "code_challenge": code_challenge,
    "code_challenge_method": "S256",
    "state": "random_state"
})
print("Go to the following URL to authorize:")
print(auth_url)

# After user authorizes, they are redirected to `redirect_uri` with a code in the URL
# Example: https://localhost:5443/callback?code=AUTH_CODE_FROM_PROVIDER
# For demonstration, enter the code manually
auth_code = input("Enter the authorization code from the callback URL: ")

# Step 2: Exchange Authorization Code for Tokens
token_response = requests.post(
    f"{config['issuer']}{config['token_endpoint']}",
    data={
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": config["redirect_uri"],
        "client_id": config["client_id"],
        "client_secret": config["client_secret"],
        "code_verifier": code_verifier
    },
    headers={"Content-Type": "application/x-www-form-urlencoded"}
)

# Check token response
if token_response.status_code == 200:
    tokens = token_response.json()
    access_token = tokens["access_token"]
    id_token = tokens["id_token"]
    print("Access Token:", access_token)
    print("ID Token:", id_token)
else:
    print("Failed to get tokens:", token_response.status_code, token_response.text)

# Step 3: Use Access Token to Call API
api_response = requests.get(
    config["api_endpoint"],
    headers={"Authorization": f"Bearer {access_token}"}
)

# Print API response
if api_response.status_code == 200:
    print("API Response:", api_response.json())
else:
    print("Failed to call API:", api_response.status_code, api_response.text)
