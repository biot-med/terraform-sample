#!/usr/bin/env python3
# Deprecated - use init_templates.py --type=<entity-type> --name=<template-name> instead.
import argparse
import os
import subprocess
import sys

from template_utils import CURRENT_PATH, prompt_if_missing

def main():
    parser = argparse.ArgumentParser(description="Deprecated - use init_templates.py --type --name instead")
    parser.add_argument("--name", help="Template json-name (e.g., clinician)")
    parser.add_argument("--type", help="Entity type to import (e.g., caregiver)")
    parser.add_argument("--skip_tfvars", help="Ignored")
    args = parser.parse_args()

    entity_type = prompt_if_missing(args.type, "Enter the entity type")
    template_name = prompt_if_missing(args.name, "Enter the template name")

    print("generate_template.py is deprecated and will be removed in a future release. Use:\n"
          f"   python3 ../../scripts/templates/init_templates.py --type={entity_type} --name={template_name}\n", flush=True)

    result = subprocess.run([
        "python3", os.path.join(CURRENT_PATH, "init_templates.py"), f"--type={entity_type}", f"--name={template_name}",
    ])
    sys.exit(result.returncode)

if __name__ == "__main__":
    main()
