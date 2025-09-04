#!/usr/bin/env python3

import os
import sys

from common_utils import get_service_id_and_key, login
from template_utils import fetch_biot_templates

def generate_map_value(templates):
    entries = []
    for template in templates['data']:
        name = template.get('name')
        tid = template.get('id')
        entries.append(f'  "{name}" = {{ id = "{tid}" }}')
    return "{\n" + "\n".join(entries) + "\n}"

def replace_or_append_variable_block(content, var_name, new_block):
    lines = content.splitlines()
    start, end = None, None

    for i, line in enumerate(lines):
        if line.strip().startswith(f"{var_name} = {{"):
            start = i
            for j in range(i + 1, len(lines)):
                if lines[j].strip() == "}":
                    end = j
                    break
            break

    if start is not None and end is not None:
        updated_lines = lines[:start] + new_block.strip().splitlines() + lines[end + 1:]
    else:
        updated_lines = lines + ["", new_block.strip()]

    return "\n".join(updated_lines) + "\n"

def write_or_update_tfvars(tfvars_path):
    service_id, service_key = get_service_id_and_key()
    token = login(service_id, service_key)
    templates = fetch_biot_templates(token)

    new_var_block = f'biot_templates_map = {generate_map_value(templates)}'

    if not os.path.exists(tfvars_path):
        with open(tfvars_path, 'w') as f:
            f.write(new_var_block + "\n")
        print(f"✅ Created {tfvars_path} with biot_templates_map")
        return

    with open(tfvars_path, 'r') as f:
        content = f.read()

    updated_content = replace_or_append_variable_block(content, "biot_templates_map", new_var_block)

    with open(tfvars_path, 'w') as f:
        f.write(updated_content)

    print(f"✅ Updated {tfvars_path} with biot_templates_map")

# --------------------------
# Main entry point
# --------------------------
if __name__ == "__main__":
    # Default file path if not provided
    default_path = "biot_templates.auto.tfvars"

    # Use CLI arg if given, else default
    tfvars_path = sys.argv[1] if len(sys.argv) > 1 else default_path

    try:
        write_or_update_tfvars(tfvars_path)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
