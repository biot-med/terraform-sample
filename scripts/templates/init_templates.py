import argparse
import os
import shlex
import sys

from template_utils import (
    fetch_biot_templates, generate_template, get_template_tf_path, prepare_template_modules, read_managed_templates,
    refresh_template, run_generate_tfvars,
)
from common_utils import get_required_variables, login

def parse_args():
    parser = argparse.ArgumentParser(
        description="Generates modules/templates .tf files for the templates in the current environment, and imports "
                    "them into its terraform state. Templates already in the state are skipped."
    )
    parser.add_argument("--type", help="Only templates of this entity type (e.g. caregiver)")
    parser.add_argument("--name", help="Only the template with this name - requires --type (e.g. --type=caregiver --name=nurse)")
    parser.add_argument(
        "--refresh", action="store_true",
        help="Regenerate the .tf files of templates already managed, from their current state in BioT"
    )
    args = parser.parse_args()

    if args.name and not args.type:
        parser.error("--name requires --type, since template names are unique per entity type")

    return args

def main():
    args = parse_args()
    boit_base_url, service_id, service_key = get_required_variables()

    token = login(boit_base_url, service_id, service_key)

    templates = fetch_biot_templates(boit_base_url, token)['data']
    if args.type:
        templates = [t for t in templates if t.get('entityTypeName') == args.type]
    if args.name:
        templates = [t for t in templates if t.get('name') == args.name]
    if not templates:
        print(f"No templates found in this environment for type [{args.type}]" + (f" and name [{args.name}]" if args.name else ""))
        sys.exit(1)

    run_generate_tfvars()

    managed = read_managed_templates()

    # Set up the modules of every entity type that has templates to generate, so terraform init runs once, not per type
    entity_types_to_generate = sorted({
        t['entityTypeName'] for t in templates
        if t.get('id') and t.get('name') and t.get('entityTypeName') and t['id'] not in managed
        and not os.path.exists(get_template_tf_path(t['entityTypeName'], t['name']))
    })
    if entity_types_to_generate:
        prepare_template_modules(entity_types_to_generate)

    # Templates already in the state count as processed, so their children can be generated
    processed_ids = set(managed)
    generated = []
    refreshed = []
    skipped = []
    already_managed = 0
    failed_templates = []
    remaining_templates = templates.copy()

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

            label = f"{template_entity_type}:{template_name}"

            if template_id in managed:
                if args.refresh:
                    try:
                        print(f"Going to refresh template -  Name: {template_name}, Type: {template_entity_type}")
                        refresh_template(template_entity_type, template_name, managed[template_id])
                        refreshed.append(label)
                    except Exception as e:
                        print(f"Failed to refresh [{template_name}.tf]: {e}")
                        failed_templates.append(label)
                else:
                    skipped.append(f"{label} - already managed")
                    already_managed += 1
                progress_made = True
                continue

            # A .tf file without state, e.g. an import that failed half way or a file written by hand - never overwritten
            if os.path.exists(get_template_tf_path(template_entity_type, template_name)):
                skipped.append(f"{label} - {template_name}.tf exists but the template is not in the state, check it and import it manually")
                progress_made = True
                continue

            # Check if parent is processed (if there is a parent)
            if parent_id and parent_id not in processed_ids:
                # Parent not ready yet
                next_round.append(template)
                continue

            # Parent is processed (or no parent), so process this template
            try:
                print(f"Going to generate template -  Name: {template_name}, Type: {template_entity_type}")
                generate_template(template_entity_type, template_name)
                processed_ids.add(template_id)
                generated.append(label)
            except Exception as e:
                # Track failed templates but don't mark as processed
                print(f"Failed to generate [{template_name}.tf] files: {e}")
                failed_templates.append(label)
            # Still mark progress to avoid infinite loop
            progress_made = True

        if not progress_made:
            print("No progress made ! printing next_round:")
            print(next_round)
            if failed_templates:
                print(f"\nPreviously failed templates: {failed_templates}")
            raise RuntimeError("Could not resolve dependencies — circular or missing parent IDs? "
                               "When using --name, generate the parent template first.")

        remaining_templates = next_round

    print(f"\nGenerated {len(generated)} template(s), refreshed {len(refreshed)}.")
    if skipped:
        print(f"\nSkipped {len(skipped)} template(s):")
        for line in skipped:
            print(f"   - {line}")
    if already_managed:
        filters = "".join(f"--{name}={shlex.quote(value)} " for name, value in [("type", args.type), ("name", args.name)] if value)
        print(f"\nHint: to update templates that are already managed with their current state in BioT, add --refresh:\n"
              f"   python3 ../../scripts/templates/init_templates.py {filters}--refresh")
    if failed_templates:
        print(f"\nSummary: {len(failed_templates)} template(s) failed:")
        for failed in failed_templates:
            print(f"   - {failed}")
        print("\nRe-run the script to retry - templates already generated are skipped.")
        sys.exit(1)

if __name__ == "__main__":
    main()
