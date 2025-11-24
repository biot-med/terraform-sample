import os
import shutil
import subprocess
from common_utils import read_main_tf_required_providers

def get_main_tf_content():
    """Generate main.tf content using required_providers from envs/dev/main.tf"""
    # Read required_providers from envs/dev/main.tf as template
    dev_main_tf_path = os.path.join(os.getcwd(), "envs", "dev", "main.tf")
    required_providers = read_main_tf_required_providers(dev_main_tf_path)
    
    return f"""terraform {{
{required_providers}
}}

provider "biot" {{
  base_url           = var.biot_base_url
  service_id         = var.biot_service_id
  service_secret_key = var.biot_service_secret_key
}}

module templates {{
    source = "../../modules/templates"
    biot_templates_map = var.biot_templates_map
}}
"""

VARIABLES_TF_CONTENT = """variable "biot_base_url" {
  type        = string
  description = "Your BIOT Base URL for the current environment"
}

variable "biot_service_id" {
  type        = string
  description = "Service ID"
}

variable "biot_service_secret_key" {
  type        = string
  description = "Service Secret Key"
  sensitive   = true
}

variable "biot_templates_map" {
  type        = map(any)
  description = "Map of template ids"
}
"""

def create_public_auto_tfvars(base_url):
    return f"""biot_base_url = "{base_url}"
"""

def create_secret_auto_tfvars(service_id, secret_key):
    return f"""biot_service_id         = "{service_id}"
biot_service_secret_key = "{secret_key}"
"""

def write_file(folder, filename, content):
    path = os.path.join(folder, filename)
    with open(path, "w") as f:
        f.write(content)
    print(f"Created file: {path}")

def delete_folder(path):
    if os.path.exists(path):
        shutil.rmtree(path)
        print(f"Deleted folder due to failure: {path}")

def create_new_env_folder():
    base_env_path = os.path.join(os.getcwd(), "envs")

    if not os.path.isdir(base_env_path):
        raise FileNotFoundError(f"The required 'envs' folder does not exist at {base_env_path}. Make sure you run the script from the project's root folder.")

    # Get inputs
    env_name = input("Enter the environment name (e.g. qa): ").strip()
    base_url = input("Enter the full base URL (e.g. https://api.staging.mycompany.biot-med.com): ").strip()
    service_id = input("Enter the service ID: ").strip()
    secret_key = input("Enter the service secret key: ").strip()

    new_env_path = os.path.join(base_env_path, env_name)

    if os.path.exists(new_env_path):
        print(f"Environment '{env_name}' already exists at {new_env_path}")
        return

    os.makedirs(new_env_path)
    print(f"Created new environment folder: {new_env_path}")

    try:
        # Create files
        write_file(new_env_path, "main.tf", get_main_tf_content())
        write_file(new_env_path, "variables.tf", VARIABLES_TF_CONTENT)
        write_file(new_env_path, "public.auto.tfvars", create_public_auto_tfvars(base_url))
        write_file(new_env_path, "secret.auto.tfvars", create_secret_auto_tfvars(service_id, secret_key))

        env_dir = os.path.join("envs", env_name)
        os.chdir(env_dir)
        # Run external scripts
        scripts_dir = os.path.join(os.pardir, os.pardir, "scripts")
        subprocess.run(["python3", os.path.join(scripts_dir, "generate_biot_templates_tfvars.py")], check=True)
        subprocess.run(["terraform", "init"], cwd='.', check=True)
        subprocess.run(["python3", os.path.join(scripts_dir, "populate_tfstate.py")], check=True)

    except Exception as e:
        print(f"\nError occurred: {e}")
        delete_folder(new_env_path)
        raise  # Re-raise the error after cleanup

if __name__ == "__main__":
    create_new_env_folder()
