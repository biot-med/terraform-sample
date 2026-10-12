import argparse
import os
import shlex
import sys

from template_utils import (
    fetch_biot_templates, get_template_tf_path, import_templates, read_managed_templates, refresh_templates,
    run_generate_tfvars,
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

    # Templates already in the state count as processed, so their children can be generated
    processed_ids = set(managed)
    to_generate = []  # (entity_type, template_name), parents before their children
    to_refresh = []  # (entity_type, template_name, terraform_address)
    skipped = []
    already_managed = 0
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
                    to_refresh.append((template_entity_type, template_name, managed[template_id]))
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

            # Parent is processed (or no parent), so this template can be generated
            to_generate.append((template_entity_type, template_name))
            processed_ids.add(template_id)
            progress_made = True

        if not progress_made:
            print("No progress made ! printing next_round:")
            print(next_round)
            raise RuntimeError("Could not resolve dependencies — circular or missing parent IDs? "
                               "When using --name, generate the parent template first.")

        remaining_templates = next_round

    # Each runs Terraform once for all its templates, so BioT sees a few logins rather than one per template
    generated = []
    refreshed = []
    failed_templates = []
    missing = []
    try:
        import_templates(to_generate)
        generated = [f"{entity_type}:{name}" for entity_type, name in to_generate]
    except Exception as e:
        print(f"Failed to generate templates: {e}")
        failed_templates += [f"{entity_type}:{name}" for entity_type, name in to_generate]
    try:
        missing = refresh_templates(to_refresh)
        refreshed = [f"{entity_type}:{name}" for entity_type, name, _ in to_refresh if f"{entity_type}:{name}" not in missing]
    except Exception as e:
        print(f"Failed to refresh templates: {e}")
        failed_templates += [f"{entity_type}:{name}" for entity_type, name, _ in to_refresh]

    print(f"\nGenerated {len(generated)} template(s), refreshed {len(refreshed)}.")
    if skipped:
        print(f"\nSkipped {len(skipped)} template(s):")
        for line in skipped:
            print(f"   - {line}")
    if already_managed:
        filters = "".join(f"--{name}={shlex.quote(value)} " for name, value in [("type", args.type), ("name", args.name)] if value)
        print(f"\nHint: to update templates that are already managed with their current state in BioT, add --refresh:\n"
              f"   python3 ../../scripts/templates/init_templates.py {filters}--refresh")
    if missing:
        print(f"\n{len(missing)} template(s) no longer exist in BioT - delete their .tf files:")
        for line in missing:
            print(f"   - {line}")
    if failed_templates:
        print(f"\nSummary: {len(failed_templates)} template(s) failed:")
        for failed in failed_templates:
            print(f"   - {failed}")
        print("\nRe-run the script to retry - templates already generated are skipped.")
        sys.exit(1)

if __name__ == "__main__":
    main()
