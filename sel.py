#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Step 1: Set the REGISTRATION_ID
REGISTRATION_ID="uid:zdcuisvc:73564.dev.WMREGID11975-cpschatuisvc"

# Step 2: Define alias for jq (optional, depending on your environment)
alias jq="/ms/dist/3rd/PROJ/jq/1.5/exec/bin/jq"

# Step 3: Generate the TOKEN using the helper script
TOKEN=$(/ms/dist/sec/PROJ/OAuthClientManager-api/2023.06.21-1/common/bin/oacmhelper.py ops-dev $REGISTRATION_ID jwt-bearer)

# Step 4: Make the curl request to generate the OIDC token
curl -XPOST -vv \
    -d "scope=urn:api:ops-dev.42e54bc1-2ced-4578-b7f7-3737d61fca2/.app" \
    -d "grant_type=client_credentials" \
    -d "client_assertion_type=urn:ietf:params:oauth:client-assertion-type:jwt-bearer" \
    -d "client_assertion=$TOKEN" \
    https://auth-oidc-dev.ms.com/as/token.oauth2 | jq

# Notify the user of successful execution
echo "OIDC token request completed successfully."
