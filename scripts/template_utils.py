import os
import requests

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

def fetch_biot_templates(base_url, token):
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(f"{base_url}/settings/v1/templates/minimized", headers=headers)
    response.raise_for_status()
    data = response.json()

    return data
