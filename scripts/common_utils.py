import getpass
import os
import re
import requests

def login(base_url, service_id, secret_key):
    payload = {
        "id": service_id,
        "secretKey": secret_key
    }

    try:
        response = requests.post(f"{base_url}/ums/v2/services/accessToken", json=payload)
        response.raise_for_status()  # Raises HTTPError for 4xx/5xx responses

        data = response.json()

        access_token = data.get("accessToken")
        if not access_token:
            raise ValueError("Login response does not contain accessToken.")

        return access_token

    except requests.exceptions.RequestException as e:
        print(f"Login request failed: {e}")
        return None
    except ValueError as ve:
        print(f"Login error: {ve}")
        return None

def read_tf_variables(tf_file_path):
    variables = {}

    # Read from file if it exists
    if os.path.exists(tf_file_path):
        with open(tf_file_path, 'r') as file:
            for line in file:
                match = re.match(r'(\w+)\s*=\s*"([^"]+)"', line.strip())
                if match:
                    key, value = match.groups()
                    variables[key] = value

    return variables

def get_required_variables():
    secret_variables = read_tf_variables('./secret.auto.tfvars')
    # Prompt for missing values
    if 'biot_service_id' not in secret_variables:
        secret_variables['biot_service_id'] = input("Enter your BIOT Service ID: ").strip()

    if 'biot_service_secret_key' not in secret_variables:
        secret_variables['biot_service_secret_key'] = getpass.getpass("Enter your BIOT Secret Key: ")

    public_variables = read_tf_variables('./public.auto.tfvars')
    if 'biot_base_url' not in public_variables:
        public_variables['biot_base_url'] = input("Enter your BIOT Base URL: ").strip()
    
    service_id = secret_variables['biot_service_id']
    service_key = secret_variables['biot_service_secret_key']
    biot_base_url = public_variables['biot_base_url']

    return biot_base_url, service_id, service_key