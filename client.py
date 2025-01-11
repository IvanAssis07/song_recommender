import requests
import json
import sys

API_URL = "http://localhost:52033/api/recommend"

def recommend_playlist(songs):
    payload = {"songs": songs}

    try:
        response = requests.post(
            API_URL,
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload)
        )

        response.raise_for_status()

        response_json = response.json()

        print(f"Recommended Songs: {response_json['songs']}")
        print(f"Model Version: {response_json['version']}")
        print(f"Model Date: {response_json['model_date']}")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP Error: {http_err}")
        print(f"Response: {response.text}")

    except Exception as err:
        print(f"An error occurred: {err}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("To generate a program you have to initiate the client this way:\npython client.py \"<song1>\" \"<song2>\" ... \"<songN>\"")
        sys.exit(1)

    songs = sys.argv[1:]
    
    recommend_playlist(songs)