"""
Python API Connector Demo
=========================
This script demonstrates how to send a Request to an API and handle the Response.

Key Concepts:
1. GET Request: Asking the API for data.
2. Status Codes: Checking if the request was successful (200 OK).
3. JSON: The format data usually comes back in.
4. Error Handling: Managing connection issues.
"""

import requests
import json

# Define the endpoint URL (Where we are sending the request)
# This is a free testing API that returns fake user data.
API_URL = "https://jsonplaceholder.typicode.com/users/1"


def get_api_data():
    print(f"--- Connecting to: {API_URL} ---")

    try:
        # 1. Send the GET request
        # This is like typing a URL into your browser.
        response = requests.get(API_URL)

        # 2. Check the Status Code
        # 200 means Success. 404 means Not Found. 500 means Server Error.
        if response.status_code == 200:
            print("✅ Success! Connection established.\n")

            # 3. Parse the JSON data
            # The API returns raw text. We convert it to a Python Dictionary.
            data = response.json()

            # Let's print the raw data nicely
            print("--- Raw Data Received ---")
            print(json.dumps(data, indent=4))

            # 4. Access specific pieces of data
            print("\n--- Extracted Information ---")
            name = data['name']
            email = data['email']
            city = data['address']['city']

            print(f"👤 Name:  {name}")
            print(f"📧 Email: {email}")
            print(f"🏙️ City:  {city}")

        else:
            print(f"❌ Failed. Status Code: {response.status_code}")
            print("Reason:", response.reason)

    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the internet or the API server.")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")


def post_api_data():
    """
    Bonus: How to SEND data to an API (POST Request)
    """
    print("\n\n--- Sending Data (POST Request) ---")
    url = "https://jsonplaceholder.typicode.com/posts"

    # The data we want to send
    new_post = {
        "title": "My Python Script",
        "body": "This data was sent via Python code!",
        "userId": 1
    }

    # Sending the POST request
    response = requests.post(url, json=new_post)

    if response.status_code == 201:  # 201 means 'Created'
        print("✅ Data sent successfully!")
        print("Server Response:", response.json())
    else:
        print("❌ Failed to send data.")


if __name__ == "__main__":
    # 1. Get data from the internet
    get_api_data()

    # 2. Send data to the internet
    post_api_data()