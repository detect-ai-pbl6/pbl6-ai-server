#!/bin/bash

# Exit on any error
set -e

# Output file
OUTPUT_FILE=".env"

# Define the prefix to remove
PREFIX_TO_REMOVE="pbl6-dev-secrets"

# Function to sanitize the secret key
sanitize_key() {
    KEY=$1
    # Remove the prefix if it exists
    if [[ $KEY == ${PREFIX_TO_REMOVE}* ]]; then
        KEY=${KEY#"$PREFIX_TO_REMOVE"}
    fi
    # Convert to uppercase and replace '-' with '_'
    SANITIZED_KEY="${KEY^^}"              # Convert to uppercase
    SANITIZED_KEY="${SANITIZED_KEY//-/_}" # Replace '-' with '_'
    echo "$SANITIZED_KEY"
}
# Clear or create the output file
: >"$OUTPUT_FILE"

# Get a list of all secret names
SECRET_NAMES=$(gcloud secrets list --format="value(name)")

if [ -z "$SECRET_NAMES" ]; then
    echo "No secrets found in the current project."
    exit 0
fi

# Loop through each secret name and fetch its latest value
for SECRET_NAME in $SECRET_NAMES; do
    echo "Fetching secret: $SECRET_NAME"

    # Get the latest value of the secret
    LATEST_SECRET_VALUE=$(gcloud secrets versions access latest --secret="$SECRET_NAME" 2>/dev/null)

    if [ $? -ne 0 ]; then
        echo "Error: Failed to retrieve the value for $SECRET_NAME"
        LATEST_SECRET_VALUE=""
    fi

    # Sanitize the key
    SANITIZED_KEY=$(sanitize_key "$SECRET_NAME")

    # Append to .env file
    echo "${SANITIZED_KEY}=\"${LATEST_SECRET_VALUE}\"" >>"$OUTPUT_FILE"
done

echo ".env file created successfully: $OUTPUT_FILE"
