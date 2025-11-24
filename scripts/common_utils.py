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

def _parse_required_providers_from_content(content):
    """
    Internal helper function that parses required_providers content from Terraform file content.
    
    Args:
        content: The content of a Terraform file
    
    Returns:
        str: The required_providers block content
    """
    # Find the required_providers block start
    required_providers_start = content.find('required_providers')
    if required_providers_start == -1:
        raise ValueError("required_providers block not found in main.tf")
    
    # Find the opening brace of required_providers
    brace_start = content.find('{', required_providers_start)
    if brace_start == -1:
        raise ValueError("required_providers block malformed")
    
    # Find the biot provider within required_providers
    biot_start = content.find('biot', required_providers_start)
    if biot_start == -1 or biot_start > content.find('}', brace_start):
        raise ValueError("biot provider not found in required_providers block")
    
    # Find the biot block opening brace
    biot_brace_start = content.find('{', biot_start)
    if biot_brace_start == -1:
        raise ValueError("biot provider block malformed")
    
    # Extract biot block content by matching braces
    brace_count = 0
    biot_content_start = biot_brace_start + 1
    biot_content_end = biot_content_start
    
    for i in range(biot_content_start, len(content)):
        if content[i] == '{':
            brace_count += 1
        elif content[i] == '}':
            if brace_count == 0:
                biot_content_end = i
                break
            brace_count -= 1
    
    biot_content = content[biot_content_start:biot_content_end]
    
    # Extract source (required)
    source_match = re.search(r'source\s*=\s*"([^"]+)"', biot_content)
    if not source_match:
        raise ValueError("source not found in biot provider block")
    source = source_match.group(1)
    
    # Extract version (optional)
    version_match = re.search(r'version\s*=\s*"([^"]+)"', biot_content)
    version = version_match.group(1) if version_match else None
    
    # Reconstruct the required_providers block content
    required_providers_content = "  required_providers {\n"
    required_providers_content += "    biot = {\n"
    required_providers_content += f'      source  = "{source}"\n'
    if version:
        required_providers_content += f'      version = "{version}"\n'
    required_providers_content += "    }\n"
    required_providers_content += "  }"
    
    return required_providers_content

def read_main_tf_required_providers(main_tf_path=None):
    """
    Reads the main.tf file and extracts the required_providers block content by parsing the structure.
    Looks for the biot provider within required_providers and extracts source and version.
    
    Args:
        main_tf_path: Optional path to main.tf file. If None, reads from current working directory.
    
    Returns:
        str: The required_providers block content
    """
    if main_tf_path is None:
        env_path = os.getcwd()
        main_tf_path = os.path.join(env_path, 'main.tf')
    
    if not os.path.exists(main_tf_path):
        raise FileNotFoundError(f"main.tf not found at {main_tf_path}")
    
    with open(main_tf_path, 'r') as file:
        content = file.read()
    
    return _parse_required_providers_from_content(content)