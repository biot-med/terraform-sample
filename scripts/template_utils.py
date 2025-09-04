import os
import requests

BASE_URL = 'http://localhost:9999' # TODO - change base-url to be taken like service id / secret key.
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

def fetch_biot_templates(token):
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(f"{BASE_URL}/settings/v1/templates/minimized", headers=headers)
    response.raise_for_status()
    data = response.json()

    return data
