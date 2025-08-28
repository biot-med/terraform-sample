#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
import os

RESOURCE_TYPE = "biot_template"
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.abspath(os.path.join(CURRENT_PATH, os.pardir))
# TEMP_FILE_PATH = os.path.join(PARENT_DIR, "temp.tf")
INDENT = "  "

def prompt_if_missing(value, prompt_message):
    return value or input(f"{prompt_message}: ").strip()

def import_template_to_tfstate(dir_path, entity_type, template_name):
    temp_file_path = f"{dir_path}/temp.tf"

    # Creates temporary block
    with open(temp_file_path, "a") as f:
        f.write(f'resource "{RESOURCE_TYPE}" "{template_name}" {{}}\n\n')

    try:
        # Import template to terraform.tfstate local file
        cmd = [
            "terraform", "import",
            f"module.{get_module_name(entity_type)}.{RESOURCE_TYPE}.{template_name}",
            f"{entity_type}:{template_name}"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            print(f"✅ Imported {template_name}")
        else:
            raise RuntimeError(f"❌ Failed to import {template_name}: {result.stderr}")

    finally:
        # Delete temporary file regardless of success or failure
        try:
            os.remove(temp_file_path)
            print(f"🧹 Deleted temp file: '{temp_file_path}'")
        except FileNotFoundError:
            print(f"⚠️ File '{temp_file_path}' not found.")
        except PermissionError:
            print(f"🚫 Permission denied deleting '{temp_file_path}'.")
        except Exception as e:
            print(f"❌ Unexpected error deleting '{temp_file_path}': {e}")

def get_template_resource(entity_type, template_name):
    with open(f'{PARENT_DIR}/terraform.tfstate', 'r') as f:
        state = json.load(f)
    
    all_resources = state.get("resources", [])

    for resource in all_resources:
        if resource.get("type") != RESOURCE_TYPE:
            continue

        for instance in resource.get("instances", []):
            attributes = instance.get("attributes", {})
            if attributes.get("name") == template_name and attributes.get("entity_type") == entity_type:
                return resource  # return the whole matching resource
    
    return None

def generate_resource_block(resource, level=0):
    resource_type = resource["type"]
    resource_name = resource["name"]
    attributes = resource.get("attributes", {})

    indent = INDENT * level
    lines = [f'{indent}resource "{resource_type}" "{resource_name}" {{']

    for key, value in attributes.items():
        if key == "id":
            continue  # Skip top-level "id"
        lines.append(render_block(key, value, level + 1))

    lines.append(f"{indent}}}")
    return "\n".join(lines)

def render_block(name, content, level):
    indent = INDENT * level

    # Special case for template_attributes list
    if name == "template_attributes" and isinstance(content, list):
        lines = [f"{indent}{name} = ["]
        for item in content:
            lines.append(f"{indent}{INDENT}{{")
            for k, v in item.items():
                if k == "id":
                    continue  # skip id field inside template_attributes
                if k == "value_json":
                    # Render value with jsonencode if possible
                    rendered_value = render_value_json(v, level + 2)
                    lines.append(f"{indent}{INDENT*2}{k} = {rendered_value}")
                else:
                    # normal rendering for other fields
                    rendered_val = format_value(v, level + 2)
                    lines.append(f"{indent}{INDENT*2}{k} = {rendered_val}")
            lines.append(f"{indent}{INDENT}}},")
        lines.append(f"{indent}]")
        return "\n".join(lines)

    # default rendering
    return f"{indent}{name} = {format_value(content, level)}"

def render_value_json(value, indent_level):
    indent = INDENT * indent_level
    try:
        # If value is a JSON string, parse it to pretty JSON for jsonencode
        parsed = json.loads(value) if isinstance(value, str) else value
        pretty_json = json.dumps(parsed, indent=2)
        # Format with indentation
        json_lines = pretty_json.splitlines()
        formatted_json = "\n".join(indent + "  " + line for line in json_lines)
        return f"jsonencode(\n{formatted_json}\n{indent})"
    except Exception:
        # Fallback: just render as a quoted string
        return f"\"{value}\""

def format_value(value, level=1):
    indent = INDENT * level
    next_indent = INDENT * (level + 1)

    if isinstance(value, bool):
        return "true" if value else "false"
    elif isinstance(value, str):
        return f"\"{value}\""
    elif value is None:
        return "null"
    elif isinstance(value, (int, float)):
        return str(value)
    elif isinstance(value, list):
        if all(isinstance(item, (str, int, float, bool)) for item in value):
            return "[ " + ", ".join(format_value(item, level) for item in value) + " ]"
        elif all(isinstance(item, dict) for item in value):
            # Render list of dicts
            lines = ["["]
            for item in value:
                lines.append(f"{next_indent}{{")
                for key, val in item.items():
                    if key == "id":
                        continue  # Skip "id" in nested dict
                    lines.append(f"{next_indent}{INDENT}{key} = {format_value(val, level + 2)}")
                lines.append(f"{next_indent}}},")
            lines.append(f"{indent}]")
            return "\n".join(lines)
        else:
            return "[ " + ", ".join(format_value(item, level) for item in value) + " ]"
    elif isinstance(value, dict):
        lines = ["{"]
        for key, val in value.items():
            if key == "id":
                continue  # Skip "id" in object
            lines.append(f"{next_indent}{key} = {format_value(val, level + 1)}")
        lines.append(f"{indent}}}")
        return "\n".join(lines)

    return f"\"{value}\""

def write_tf_file(dir_path, template_resource, entity_type, template_name):
    filepath = os.path.join(dir_path, f"{template_name}.tf")

    instances = template_resource.get("instances", [])
    if not instances:
        print("No instances found in template resource.")
        return

    instance = instances[0]
    resource_block = {
        "type": template_resource["type"],
        "name": template_resource["name"],
        "attributes": instance.get("attributes", {})
    }

    with open(filepath, "w") as f:
        f.write(generate_resource_block(resource_block))
        f.write("\n\n")

def get_module_name(entity_type):
    return f"{entity_type}_templates"

def add_tf_module_to_main(entity_type):
    main_tf_path = os.path.join(PARENT_DIR, "main.tf")
    module_block = f"""module "{get_module_name(entity_type)}" {{
    source = "./modules/templates/{entity_type}"
}}"""

    with open(main_tf_path, "a") as f:
        f.write("\n" + module_block)
        print(f"✅ Added module block for {entity_type} to main.tf")

def create_providers_tf(dir_path):
    providers_tf_path = os.path.join(dir_path, "providers.tf")
    
    content = '''
terraform {
  required_providers {
    biot = {
      source  = "example.com/biot/biot"
      version = "1.0.0"
    }
  }
}
'''.lstrip()

    with open(providers_tf_path, "w") as f:
        f.write(content)

    print(f"✅ Created providers.tf in {dir_path}")

def create_module_if_not_exist(dir_path, entity_type):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=True)  # Creates directory if missing
        create_providers_tf(dir_path)
        add_tf_module_to_main(entity_type)
        run_terraform_init()

def run_terraform_init(working_dir=PARENT_DIR):
    """
    Runs `terraform init` in the specified working directory.
    Defaults to the current directory.
    """
    print(f"📦 Running `terraform init` in {working_dir}...")
    result = subprocess.run(["terraform", "init"], cwd=working_dir, capture_output=True, text=True)

    if result.returncode == 0:
        print("✅ Terraform initialized successfully.")
    else:
        print("❌ Terraform init failed.")
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
        raise RuntimeError("Terraform initialization failed.")

def main():
    parser = argparse.ArgumentParser(description="Template Import CLI")
    parser.add_argument(
        "--name",
        help="Template json-name (e.g., clinician)"
    )
    parser.add_argument(
        "--type",
        help="Entity type to import (e.g., caregiver)"
    )

    args = parser.parse_args()

    entity_type = prompt_if_missing(args.type, "Enter the entity type")
    template_name = prompt_if_missing(args.name, "Enter the template name")

    dir_path = f"{PARENT_DIR}/modules/templates/{entity_type}"
    create_module_if_not_exist(dir_path, entity_type)
    import_template_to_tfstate(dir_path, entity_type, template_name)
    template_resource = get_template_resource(entity_type, template_name)
    write_tf_file(dir_path, template_resource, entity_type, template_name)

    sys.exit()

if __name__ == "__main__":
    main()
