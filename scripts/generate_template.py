#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
import os
import re

RESOURCE_TYPE = "biot_template"
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.abspath(os.path.join(CURRENT_PATH, os.pardir))
TEMPLATES_MAP_VAR_NAME = "biot_templates_map"
INDENT = "  "

class RawHCL: #Used for when formating values using terraform functions like 'lookup' to not have unwanted ""
    def __init__(self, expr):
        self.expr = expr

    def __str__(self):
        return self.expr

def prompt_if_missing(value, prompt_message):
    return value or input(f"{prompt_message}: ").strip()

def get_full_template_name(entity_type, template_name):
    return f"module.templates.module.{entity_type}.{RESOURCE_TYPE}.{template_name}"

def import_template_to_tfstate(project_dir, entity_type, template_name):
    # temp_file_path = f"./temp.tf"
    temp_file_path = f"{project_dir}/modules/templates/{entity_type}/temp.tf"
    
    # Ensure the directory exists
    temp_dir = os.path.dirname(temp_file_path)
    os.makedirs(temp_dir, exist_ok=True)

    # Creates temporary block
    with open(temp_file_path, "a") as f:
        f.write(f'resource "{RESOURCE_TYPE}" "{template_name}" {{}}\n\n')

    try:
        run_terraform_init()

        # Import template to terraform.tfstate local file
        cmd = [
            "terraform", "import",
            get_full_template_name(entity_type, template_name),
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

def get_template_resource_by_id(template_id):
    with open("./terraform.tfstate", 'r') as f:
        state = json.load(f)
    
    all_resources = state.get("resources", [])

    for resource in all_resources:
        if resource.get("type") != RESOURCE_TYPE:
            continue

        for instance in resource.get("instances", []):
            attributes = instance.get("attributes", {})
            if attributes.get("id") == template_id:
                return resource  # return the whole matching resource
    
    return None

def get_template_resource(entity_type, template_name):
    with open("./terraform.tfstate", 'r') as f:
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

def convert_valid_templates_to_reference(value):
    """Convert a list of template IDs to lookup function expressions."""
    if not isinstance(value, list) or not value:
        return value
    
    lookup_expressions = []
    for template_id in value:
        if isinstance(template_id, str):
            template_resource = get_template_resource_by_id(template_id)
            if template_resource:
                template_name = extract_template_value_from_resource(template_resource, "name")
                lookup_expressions.append(f'lookup(var.biot_templates_map["{template_name}"], "id", null)')
            else:
                # Fallback to original ID if template not found in state
                lookup_expressions.append(f'"{template_id}"')
        else:
            lookup_expressions.append(str(template_id))
    
    return RawHCL("[ " + ", ".join(lookup_expressions) + " ]")

def process_valid_templates_recursively(data):
    """Recursively process data structure to convert valid_templates_to_reference values."""
    if isinstance(data, dict):
        processed = {}
        for key, value in data.items():
            if key == "valid_templates_to_reference":
                processed[key] = convert_valid_templates_to_reference(value)
            elif isinstance(value, (dict, list)):
                processed[key] = process_valid_templates_recursively(value)
            else:
                processed[key] = value
        return processed
    elif isinstance(data, list):
        return [process_valid_templates_recursively(item) for item in data]
    else:
        return data

def generate_resource_block(resource, level=0):
    resource_type = resource["type"]
    resource_name = resource["name"]
    attributes = resource.get("attributes", {})
    last_keys_to_render = ["custom_attributes", "builtin_attributes", "template_attributes"]

    # Process attributes recursively to convert valid_templates_to_reference at all nesting levels
    attributes = process_valid_templates_recursively(attributes)

    indent = INDENT * level
    lines = [f'{indent}resource "{resource_type}" "{resource_name}" {{']

    for key, value in attributes.items():
        if key == "id" or key in last_keys_to_render:
            continue  # Skip top-level "id"
        
        if key == "parent_template_id" and value is not None:
            parent_template_resource = get_template_resource_by_id(value)
            parent_template_name = extract_template_value_from_resource(parent_template_resource, "name")
            value = RawHCL(f'lookup(var.biot_templates_map["{parent_template_name}"], "id", null)')

        lines.append(render_block(key, value, level + 1))

    # Handling custom, builtin and template attributes last for readability of the .tf file.
    for key in last_keys_to_render:
        value = attributes.get(key)
        if value is not None:
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
        # Fallback: just render as a quoted string (escape backslashes and quotes)
        escaped = str(value).replace('\\', '\\\\').replace('"', '\\"')
        return f"\"{escaped}\""

def format_value(value, level=1):
    indent = INDENT * level
    next_indent = INDENT * (level + 1)

    if isinstance(value, RawHCL):
        return str(value)
    if isinstance(value, bool):
        return "true" if value else "false"
    elif isinstance(value, str):
        if '\n' in value:
            heredoc_tag = "EOT"
            return f"<<-{heredoc_tag}\n{value.strip()}\n{heredoc_tag}"
        else:
            # Escape backslashes first, then double quotes
            escaped = value.replace('\\', '\\\\').replace('"', '\\"')
            return f"\"{escaped}\""
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

def extract_template_value_from_resource(template_resource, key):
    instances = template_resource.get("instances", [])
    if not instances:
        print("No instances found in template resource.")
        return

    instance = instances[0]
    return instance.get("attributes", {})[key]

def write_tf_file(project_dir, template_resource, entity_type, template_name):
    filepath = os.path.join(f"{project_dir}/modules/templates/{entity_type}", f"{template_name}.tf")

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

    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        f.write(generate_resource_block(resource_block).strip() + "\n")

def get_module_name(entity_type):
    return f"{entity_type}_templates"

def add_tf_module_to_main():
    # main_tf_path = os.path.join(CURRENT_PATH, "main.tf")
    module_block = f"""module templates {{
    source = "../../modules/templates"
}}"""

    with open("./main.tf", "a") as f:
        f.write("\n" + module_block)
        print(f"✅ Added module block for [templates] to main.tf")

def create_providers_tf(dir_path):
    providers_tf_path = os.path.join(dir_path, "providers.tf")
    
    content = '''
terraform {
  required_providers {
    biot = {
      source  = "registry.terraform.io/biot-med/biot-gen2"
      version = "1.0.0"
    }
  }
}
'''.lstrip()

    with open(providers_tf_path, "w") as f:
        f.write(content)

    print(f"✅ Created providers.tf in {dir_path}")

def create_main_tf(project_dir):
    main_tf_path = os.path.join(project_dir, "main.tf")

    with open(main_tf_path, "w") as f:
        f.write("\n")

    print(f"✅ Created empty main.tf for [{project_dir}]")

# Returns true if created, false if not.
def create_module_if_not_exist(dir_path, include_main=True):
    if not os.path.exists(dir_path):
        os.makedirs(f"{dir_path}", exist_ok=True)
        create_providers_tf(dir_path)
        create_template_ids_variable_file(dir_path)
        if include_main:
            create_main_tf(dir_path)
        return True
    
    return False
    
def add_module_to_main(main_dir_path, module_name, module_source):
    module_block = f"""module {module_name} {{
    source = "{module_source}"
"""
    module_block += "    biot_templates_map = var.biot_templates_map\n"

    module_block += "}"

    with open(f"{main_dir_path}/main.tf", "a") as f:
        f.write("\n" + module_block)
        print(f"✅ Added module block for [{module_name}] to [{main_dir_path}/main.tf]")

def remove_module_from_main(main_dir_path, module_name):
    main_tf_path = f"{main_dir_path}/main.tf"

    try:
        with open(main_tf_path, "r") as f:
            content = f.read()

        # Regex pattern to match the entire module block
        pattern = rf'\n?module\s+"?{re.escape(module_name)}"?\s*{{.*?^\}}'  # non-greedy match up to closing }
        updated_content = re.sub(pattern, '', content, flags=re.DOTALL | re.MULTILINE)

        with open(main_tf_path, "w") as f:
            f.write(updated_content)

        print(f"🧹 Removed module block for [{module_name}] from [{main_tf_path}]")

    except FileNotFoundError:
        print(f"⚠️ File not found: {main_tf_path} while trying to rollback template")
    except Exception as e:
        print(f"❌ Error removing module block: {e}")

def run_terraform_init(working_dir="./"):
    """
    Runs `terraform init` in the specified working directory.
    Defaults to the current directory.
    """
    print(f"📦 Running `terraform init` in [{working_dir}]")
    result = subprocess.run(["terraform", "init"], cwd=working_dir, capture_output=True, text=True)

    if result.returncode == 0:
        print("✅ Terraform initialized successfully.")
    else:
        print("❌ Terraform init failed.")
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
        raise RuntimeError("Terraform initialization failed.")

def generate_output_tf_if_needed(project_dir, entity_type, template_name, template_id):
    if entity_type not in {"patient", "device"}:
        return  # Do nothing
    
    dir_path = os.path.join(project_dir, "modules", "templates", entity_type)

    output_tf_path = os.path.join(dir_path, "output.tf")

    output_block = f'''
output "{template_name}_id" {{
  value = "{template_id}"
}}
'''.lstrip()

    with open(output_tf_path, "a") as f:
        f.write(output_block)

    print(f"'output.tf' generated at: {output_tf_path}")

def create_template_ids_variable_file(module_path):
    variable_tf_content = f'''variable {TEMPLATES_MAP_VAR_NAME} {{
  type        = map(any)
  default     = {{}}
  description = "Map of all template IDs passed to this module"
}}
'''
    # Ensure the directory exists
    os.makedirs(module_path, exist_ok=True)

    # Write the file
    file_path = os.path.join(module_path, "variables.tf")
    with open(file_path, "w") as f:
        f.write(variable_tf_content)

    print(f"✅ Created 'variables.tf' in: {file_path}")

def update_template_ids_tf_file(file_path, template_id, entity_type, template_name):
    template_block_header = TEMPLATES_MAP_VAR_NAME
    new_entry = f'    "{template_id}" = {{ name = "{template_name}" }}'

    if not os.path.exists(file_path):
        print(f"📄 File not found. Creating new: {file_path}")
        content = f'''output "{template_block_header}" {{
  value = {{
{new_entry}
  }}
}}
'''
        with open(file_path, 'w') as f:
            f.write(content)
        print(f"✅ Created {file_path} with initial {TEMPLATES_MAP_VAR_NAME}.")
        return

    with open(file_path, 'r') as f:
        content = f.read()

    # Match existing template_ids block
    pattern = rf'(output\s+"{template_block_header}"\s*\{{[^}}]*value\s*=\s*\{{)([^}}]*)(\}}\s*\}})'
    match = re.search(pattern, content, re.DOTALL)

    if not match:
        # If not found, append the whole block
        updated_content = content + f'''\n\noutput "{template_block_header}" {{
  value = {{
{new_entry}
  }}
}}'''
        with open(file_path, 'w') as f:
            f.write(updated_content)
        print(f"✅ Appended new output block to {file_path}.")
        return

    # Extract existing entries
    header, body, footer = match.groups()

    # Check if entry already exists
    entry_pattern = rf'"{re.escape(template_name)}"\s*='
    if re.search(entry_pattern, body):
        # Update existing entry
        body_lines = body.splitlines()
        updated_lines = []
        for line in body_lines:
            if re.search(entry_pattern, line):
                updated_lines.append(new_entry)
            else:
                updated_lines.append(line)
        new_body = '\n'.join(updated_lines)
        updated_block = f'{header}{new_body}{footer}'
        updated_content = re.sub(pattern, updated_block, content, flags=re.DOTALL)
        print(f"♻️ Updated existing entry '{template_name}' in {file_path}")
    else:
        # Append new entry
        new_body = body + '\n' + new_entry
        updated_block = f'{header}{new_body}{footer}'
        updated_content = re.sub(pattern, updated_block, content, flags=re.DOTALL)
        print(f"➕ Added new entry '{template_name}' to {file_path}")

    # Write back to file
    with open(file_path, 'w') as f:
        f.write(updated_content)
    print(f"✅ Saved changes to {file_path}")

def validate_template_creation(project_dir, template_resource, entity_type, template_name):
    instances = template_resource.get("instances", [])
    attributes = instances[0].get("attributes", {})
    parent_template_id = attributes["parent_template_id"]
    if not parent_template_id:
        return
    
    # if parent_template_id exists:
    parent_template_resource = get_template_resource_by_id(parent_template_id)
    if parent_template_resource is None:
        # Removing template resource from state before raising error.
        command = ["terraform", "state", "rm", get_full_template_name(entity_type, template_name)]
        subprocess.run(command, check=True)

        remove_module_from_main(f"{project_dir}/modules/templates", entity_type)

        raise ValueError(
            f"Failed to generate template '{template_name}': missing parent with ID {parent_template_id}. "
            f"Parent templates must be generated before their children."
        )

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
    parser.add_argument(
        "--skip_tfvars",
        help="Flag indicating need to run tfvars update or not"
    )

    args = parser.parse_args()

    entity_type = prompt_if_missing(args.type, "Enter the entity type")
    template_name = prompt_if_missing(args.name, "Enter the template name")

    if not args.skip_tfvars:
        subprocess.run(["python3", "../../scripts/generate_biot_templates_tfvars.py"], check=True)

    project_dir = f"../.."

    templates_dir = f"{project_dir}/modules/templates"
    # Creating templates module if not exist
    is_templates_module_created = create_module_if_not_exist(templates_dir)
    # Adding the templates module to the current dir main.tf
    if is_templates_module_created:
        add_module_to_main("./", "templates", "../../modules/templates")
    
    # Creating the entity-type module if not exist
    is_entity_type_module_created = create_module_if_not_exist(f"{templates_dir}/{entity_type}", include_main=False)
    # Adding the entity-type module to the templates module's main.tf
    if is_entity_type_module_created:
        add_module_to_main(f"{project_dir}/modules/templates", entity_type, f"./{entity_type}")

    # Generating .tf config:
    import_template_to_tfstate(project_dir, entity_type, template_name)
    template_resource = get_template_resource(entity_type, template_name)
    validate_template_creation(project_dir, template_resource, entity_type, template_name)
    write_tf_file(project_dir, template_resource, entity_type, template_name)

    # Required to load modules
    run_terraform_init()

    sys.exit()

if __name__ == "__main__":
    main()
