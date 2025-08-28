import requests
import subprocess
import os
import getpass
import re

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.abspath(os.path.join(CURRENT_PATH, os.pardir))
TEMP_FILE_PATH = os.path.join(PARENT_DIR, "temp.tf")
BASE_URL = 'http://localhost:9999'

def login(service_id, secret_key):
    payload = {
        "id": service_id,
        "secretKey": secret_key
    }

    try:
        response = requests.post(f"{BASE_URL}/ums/v2/services/accessToken", json=payload)
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

def fetch_biot_templates(token):
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(f"{BASE_URL}/settings/v1/templates/minimized", headers=headers)
    response.raise_for_status()
    data = response.json()

    return data

def write_resource_block(template_name):
    with open(TEMP_FILE_PATH, "a") as f:
        f.write(f'resource "biot_template" "{template_name}" {{}}\n\n')

def import_template(template_name, template_entity_type):
    cmd = ["terraform", "import", f"biot_template.{template_name}", f"{template_entity_type}:{template_name}"]
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        print(f"✅ Imported {template_name}")
    else:
        print(f"❌ Failed to import {template_name}: {result.stderr}")

def delete_temp_tf_files():
    try:
        os.remove(TEMP_FILE_PATH)
        print(f"File '{TEMP_FILE_PATH}' deleted successfully.")
    except FileNotFoundError:
        print(f"File '{TEMP_FILE_PATH}' not found.")
    except PermissionError:
        print(f"Permission denied: '{TEMP_FILE_PATH}' is in use or locked.")
    except Exception as e:
        print(f"Error deleting file '{TEMP_FILE_PATH}': {e}")

def generate_tf_files(): 
    cmd = [
        "terraform", "show", "-json",
        "|", "python3", os.path.join(CURRENT_PATH, "generate_tf_files.py")
    ]
    # cmd = f"terraform show -json | python3 {os.path.join(CURRENT_PATH, "generate_tf_files.py")}" 
    # result = subprocess.run(cmd, shell=True, capture_output=True, text=True) 
    # Execute the command
    result = subprocess.run(" ".join(cmd), shell=True, capture_output=True, text=True)

    if result.returncode == 0: 
        print("✅ Generated .tf files") 
    else: 
        print("❌ Failed to generate .tf files") 
        print("stderr:", result.stderr)

def generate_template(template_entity_type, template_name):
    script_path = os.path.join(CURRENT_PATH, "generate_template.py")
    cmd = f"python3 {script_path} --type={template_entity_type} --name={template_name}"

    print("----")
    print(cmd)
    print("----")
    print(f"Going to generate template -  Name: {template_name}, Type: {template_entity_type}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    if result.returncode == 0: 
        print(f"✅ Generated [{template_name}.tf] file") 
    else: 
        print(f"❌ Failed to generate [{template_name}.tf] files") 
        print("stderr:", result.stderr)

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

    # Prompt for missing values
    if 'biot_service_id' not in variables:
        variables['biot_service_id'] = input("Enter your BIOT Service ID: ").strip()

    if 'biot_service_secret_key' not in variables:
        variables['biot_service_secret_key'] = getpass.getpass("Enter your BIOT Secret Key: ")

    return variables

def main():
    tf_file_path = os.path.abspath(os.path.join(CURRENT_PATH, '../secret.auto.tfvars'))
    variables = read_tf_variables(tf_file_path)
    service_id = variables['biot_service_id']
    service_key = variables['biot_service_secret_key']

    token = login(service_id, service_key)

    templates = fetch_biot_templates(token)
    for template in templates['data']:
            # Ensure 'name' and 'id' keys exist in each template
            template_name = template.get('name')
            template_entity_type = template.get('entityTypeName')
            if template_name and template_entity_type:
                generate_template(template_entity_type, template_name)
                # print(f"Name: {template_name}, template_entity_type: {template_entity_type}")
                # write_resource_block(template_name)
                # import_template( template_name, template_entity_type)
            else:
                print("Missing 'name' or 'entity type' in template:", template)
    
    generate_tf_files()
    delete_temp_tf_files()

if __name__ == "__main__":
    main()