#!/bin/bash

# Variables
LOCAL_DIR="test_data/"
BUCKET_NAME="liminal-s3-browser-prototype"
S3_PATH="s3://${BUCKET_NAME}/"

# Sync the directory to S3
aws s3 sync "${LOCAL_DIR}" "${S3_PATH}"

# Optional: Print a success message
if [ $? -eq 0 ]; then
    echo "Data synced successfully to ${S3_PATH}"
else
    echo "Sync failed. Please check for any errors."
fi
