import requests
import json

# Configuration
server_url = 'https://media.tits-guru.net/images/'
json_file_name = 'images.json'

# Get list of files from the server
response = requests.get(server_url)
files = response.json()  # Assuming the server returns a JSON list of files

# Find the JSON file
json_file_url = None
for file in files:
    if file.endswith('.json'):
        json_file_url = server_url + file
        break

if not json_file_url:
    print("No JSON file found on the server.")
else:
    # Download the JSON file
    response = requests.get(json_file_url)
    data = response.json()

    # Filter links to JPEG images larger than 130KB
    large_jpeg_links = []
    for item in data:
        if item.get('url', '').endswith('.jpg'):
            image_url = item['url']
            image_response = requests.head(image_url)
            file_size = int(image_response.headers.get('Content-Length', 0))  # Size in bytes
            if file_size > 130 * 1024:
                large_jpeg_links.append(image_url)

    # Output the results
    print("Links to JPEG images larger than 130KB:")
    for link in large_jpeg_links:
        print(link)
