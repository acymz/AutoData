import base64
import requests
import os

# Download list.txt from GitHub
list_url = "https://raw.githubusercontent.com/peasoft/NoMoreWalls/master/list.txt"
response = requests.get(list_url)
with open("list.txt", "wb") as file:
    file.write(response.content)

# Read and decode list.txt
with open("list.txt", "r") as file:
    content = file.read()
decoded_content = base64.b64decode(content).decode('utf-8')

# Filter out lines starting with "http"
filtered_lines = [line for line in decoded_content.split('\n') if not line.startswith("http")]
encoded_content = base64.b64encode('\n'.join(filtered_lines).encode('utf-8')).decode('utf-8')

# Create data directory if it doesn't exist
if not os.path.exists("data"):
    os.makedirs("data")

# Save the encoded content to V2 files
with open("data/V2.txt", "w") as file:
    file.write(encoded_content)
