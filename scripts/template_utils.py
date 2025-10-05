import os
import requests
import json

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

def fetch_biot_templates(base_url, token):
    params = {
        "searchRequest": json.dumps({
            "limit": 10000
        })
    }
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(f"{base_url}/settings/v1/templates/minimized", headers=headers, params=params)
    response.raise_for_status()
    data = response.json()

    return data
