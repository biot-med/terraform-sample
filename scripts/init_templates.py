import subprocess
import os
import sys
from template_utils import fetch_biot_templates
from common_utils import get_required_variables, login

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.abspath(os.path.join(CURRENT_PATH, os.pardir))
TEMP_FILE_PATH = os.path.join(PARENT_DIR, "temp.tf")

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

def generate_template(template_entity_type, template_name):
    script_path = os.path.join(CURRENT_PATH, "generate_template.py")
    cmd = f"python3 {script_path} --type={template_entity_type} --name={template_name} --skip_tfvars={True}"

    print(f"Going to generate template -  Name: {template_name}, Type: {template_entity_type}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    if result.returncode == 0: 
        print(f"✅ Generated [{template_name}.tf] file")
        return True
    else: 
        print(f"❌ Failed to generate [{template_name}.tf] files") 
        print("stderr:", result.stderr)
        return False

def check_tfstate_in_current_dir():
    tfstate_files = ["terraform.tfstate", "terraform.tfstate.backup"]
    found = [f for f in tfstate_files if os.path.exists(f)]

    if found:
        print(f"❌ Terraform state file(s) already exist for current env, It is not allowed to run initialization agian. If you wish to run initialization you have to clean this terraform environment first.")
        sys.exit(1)

def main():
    check_tfstate_in_current_dir()
    boit_base_url, service_id, service_key = get_required_variables()

    token = login(boit_base_url, service_id, service_key)

    templates = fetch_biot_templates(boit_base_url, token)

    subprocess.run(["python3", "../../scripts/generate_biot_templates_tfvars.py"], check=True)

    templates_to_process = templates['data']
    processed_ids = set()
    failed_templates = []
    remaining_templates = templates_to_process.copy()
    
    while remaining_templates:
        progress_made = False
        next_round = []

        for template in remaining_templates:
            template_id = template.get('id')
            parent_id = template.get('parentTemplateId')
            template_name = template.get('name')
            template_entity_type = template.get('entityTypeName')

            # Skip templates missing required fields
            if not template_id or not template_name or not template_entity_type:
                print(f"Skipping invalid template: {template}")
                continue

            # Check if parent is processed (if there is a parent)
            if parent_id and parent_id not in processed_ids:
                # Parent not ready yet
                next_round.append(template)
                continue

            # Parent is processed (or no parent), so process this template
            success = generate_template(template_entity_type, template_name)
            if success:
                processed_ids.add(template_id)
                progress_made = True
            else:
                # Track failed templates but don't mark as processed
                failed_templates.append(f"{template_entity_type}:{template_name}")
                # Still mark progress to avoid infinite loop, but don't add to processed_ids
                progress_made = True

        if not progress_made:
            print("No progress made ! printing next_round:")
            print(next_round)
            if failed_templates:
                print(f"\n⚠️  Previously failed templates: {failed_templates}")
            raise RuntimeError("Could not resolve dependencies — circular or missing parent IDs?")
        
        remaining_templates = next_round
    
    # Report failed templates at the end
    if failed_templates:
        print(f"\n⚠️  Summary: {len(failed_templates)} template(s) failed to generate:")
        for failed in failed_templates:
            print(f"   - {failed}")
        print("\n💡 You can try generating these templates individually using:")
        print("   python3 ../../scripts/generate_template.py --type=<entity-type> --name=<template-name>")
    else:
        print("\n✅ All templates generated successfully!")
    
if __name__ == "__main__":
    main()