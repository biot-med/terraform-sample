import os
import subprocess
import re
from template_utils import fetch_biot_templates
from common_utils import get_required_variables, login

def extract_biot_template_resource(file_path):
    """
    Parses the .tf file and returns (terraform_resource_name, template_name) if found.
    Only returns `name` if it's defined at the top level of the resource block.
    """
    resource_name = None
    template_name = None
    inside_biot_template = False
    brace_depth = 0

    with open(file_path, "r") as f:
        for line in f:
            # Detect start of biot_template resource
            if not inside_biot_template:
                match_res = re.match(r'^\s*resource\s+"biot_template"\s+"([a-zA-Z0-9_]+)"\s*{', line)
                if match_res:
                    resource_name = match_res.group(1)
                    inside_biot_template = True
                    brace_depth = 1
                continue

            if inside_biot_template:
                # Track nesting depth using braces
                brace_depth += line.count("{")
                brace_depth -= line.count("}")

                # Only match name if at top level of resource block
                if brace_depth == 1:
                    match_name = re.match(r'^\s*name\s*=\s*"(.*?)"', line)
                    if match_name:
                        template_name = match_name.group(1)

                # Exit resource block
                if brace_depth == 0:
                    break

    return resource_name, template_name


def fetch_templates():
    boit_base_url, service_id, service_key = get_required_variables()

    token = login(boit_base_url, service_id, service_key)

    templates = fetch_biot_templates(boit_base_url, token)

    return templates['data']

def run_terraform_import(terraform_address, template_type, template_name):
    cmd = [
        "terraform", "import",
        terraform_address,
        f"{template_type}:{template_name}"
    ]
    print("▶️ Running:", " ".join(cmd))
    try:
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Failed to import {template_type}:{template_name}")
        return False

def main():
    modules_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../modules/templates"))
    if not os.path.isdir(modules_path):
        raise FileNotFoundError(f"Templates folder not found: {modules_path}")

    # Fetch templates from backend (API)
    backend_templates = fetch_templates()
    backend_set = set((t["entityTypeName"], t["name"]) for t in backend_templates)

    imported_templates = set()
    missing_in_backend = []

    print(f"📦 Scanning submodules in: {modules_path}\n")

    # Loop over each submodule (folder == template type)
    skip_files = ['providers.tf', 'variables.tf', 'main.tf']
    for template_type in os.listdir(modules_path):
        type_path = os.path.join(modules_path, template_type)
        if not os.path.isdir(type_path):
            continue

        for filename in os.listdir(type_path):
            if not filename.endswith(".tf"):
                continue

            if filename in skip_files:
                continue

            file_path = os.path.join(type_path, filename)
            resource_name, template_name = extract_biot_template_resource(file_path)

            if not resource_name or not template_name:
                print(f"⚠️ Skipping {file_path} — could not parse resource or template name.")
                continue

            # Validate against backend
            key = (template_type, template_name)
            terraform_address = f"module.templates.module.{template_type}.biot_template.{resource_name}"

            if key in backend_set:
                success = run_terraform_import(terraform_address, template_type, template_name)
                if success:
                    imported_templates.add(key)
            else:
                print(f"❌ Not found in backend: {template_type}:{template_name} ({terraform_address})")
                missing_in_backend.append(key)

    unmatched_backend = backend_set - imported_templates

    print("\n✅ Import Complete.\n")

    if missing_in_backend:
        print("❌ Templates defined in code but missing in backend:")
        for t_type, t_name in missing_in_backend:
            print(f"  - {t_type}:{t_name}")
        print("❌ The above templates could not match any template from the BE, this can happen if the template name was changed before started managing it in terraform. in this case you will have to import it manually.")

    if unmatched_backend:
        print("📌 Templates in backend but not imported (not found in code):")
        for t_type, t_name in unmatched_backend:
            print(f"  - {t_type}:{t_name}")
        print("📌 In your next terraform plan / apply terraform will attempt to delete the above templates.")


if __name__ == "__main__":
    main()
