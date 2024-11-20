import subprocess
import requests

def generate_oidc_token():
    try:
        # Step 1: Generate the client assertion ($TOKEN)
        helper_script = "/ms/dist/sec/PROJ/OAuthClientManager-api/2023.06.21-1/common/bin/oacmhelper.py"
        registration_id = "uid:zdcuisvc:73564.dev.WMREGID11975-cpschatuisvc"
        environment = "ops-dev"
        token_type = "jwt-bearer"

        # Run the helper script to generate the client assertion
        token_command = [
            helper_script,
            environment,
            registration_id,
            token_type
        ]
        print(f"Running command: {' '.join(token_command)}")
        client_assertion = subprocess.check_output(token_command, universal_newlines=True).strip()

        # Step 2: Token endpoint and payload for the curl request
        token_url = "https://auth-oidc-dev.ms.com/as/token.oauth2"  # Replace with actual URL
        payload = {
            "scope": "urn:api:ops-dev.42e54bc1-2ced-4578-b7f7-3737d61fca2/.app",
            "grant_type": "client_credentials",
            "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
            "client_assertion": client_assertion
        }

        # Step 3: Make the POST request to the token endpoint
        print("Making POST request to token endpoint...")
        response = requests.post(token_url, data=payload)

        # Check response status
        if response.status_code == 200:
            token_data = response.json()
            print("Token generated successfully:")
            print(token_data)

            # Optionally, parse the access token
            access_token = token_data.get("access_token")
            if access_token:
                print("\nAccess Token:")
                print(access_token)
            return token_data
        else:
            print(f"Failed to retrieve token: {response.status_code}")
            print(response.text)
            return None

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running a command: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Example usage
if __name__ == "__main__":
    generate_oidc_token()
