import requests
import os

# URL of the FastAPI server
url = 'http://127.0.0.1:8000/calculate/'

# Path to the image file
image_file_path = os.getenv("IMAGE_FILE_PATH", 'C:/Users/applesde/Downloads/your_image.jpg')  # Replace with your actual image file path

# User input prompt
user_prompt = os.getenv("USER_PROMPT", 'Input prompt text here')  # Replace with your input prompt

# Prepare the request payload
payload = {'input': user_prompt}
files = {'file': open(image_file_path, 'rb')}  # Assuming you want to send an image file

# Send the POST request
try:
    response = requests.post(url, files=files, data=payload)
    response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
    print(response.json())  # Print the JSON response from the FastAPI server
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")  # Print any network or HTTP error that occurs
