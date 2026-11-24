import argparse
import shlex
import sys

from portal_view_utils import (
    MODULE_DIR, MODULE_NAME, PORTALS, VIEW_TYPES, check_env_folder, clean_config, describe, ensure_module,
    format_module_files, import_to_state, module_file, query, read_module_resources, read_state_addresses,
    to_resource_name, write_resource_block,
)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generates modules/portal_views .tf files for the portal builder views in the current environment, "
                    "and imports them into its terraform state. Views already in the state are skipped."
    )
    parser.add_argument("--portal", choices=list(PORTALS), help="Only the views of this portal")
    parser.add_argument("--view-type", choices=VIEW_TYPES, help="Only views of this type")
    parser.add_argument("--template", help="Only the views of the template with this name (e.g. Clinician)")
    parser.add_argument("--entity", help="Only the views of this entity (e.g. patient) - its template views included")
    parser.add_argument(
        "--refresh", action="store_true",
        help="Regenerate the .tf config of views already managed, from their current layout in BioT"
    )
    return parser.parse_args()


def main():
    args = parse_args()
    check_env_folder()
    ensure_module()

    views = query(PORTALS.get(args.portal), args.view_type)
    if args.template:
        views = [view for view in views if view["attributes"]["template_name"] == args.template]
    if args.entity:
        views = [view for view in views if view["attributes"]["entity_type_name"] == args.entity]
    if not views:
        print("No portal views found in this environment for these filters.")
        sys.exit(1)
    # New blocks are appended in this order, so each template's or entity's views end up next to each other
    views.sort(key=lambda view: (view["key"][0], view["key"][2].lower(), VIEW_TYPES.index(view["key"][1])
                                 if view["key"][1] in VIEW_TYPES else len(VIEW_TYPES)))

    state = read_state_addresses()
    # {view_key: resource_name} - what modules/portal_views defines, plus what this run adds to it
    names = read_module_resources()

    to_write = []
    to_import = []
    skipped = []
    already_managed = 0

    for view in views:
        key = view["key"]
        address = state.get(key)

        if address and key not in names:
            if not address.startswith(f"module.{MODULE_NAME}."):
                skipped.append(f"{describe(key)} - already managed outside {MODULE_DIR} at {address}")
                continue
            # In the module's state, but its block was removed from the module files - write it back
            names[key] = address.split(".")[-1]
            to_write.append(view)
            continue
        if address and not args.refresh:
            skipped.append(f"{describe(key)} - already managed")
            already_managed += 1
            continue

        if key not in names:
            names[key] = to_resource_name(key, set(names.values()))
            to_write.append(view)
        elif args.refresh:
            to_write.append(view)

        if not address:
            to_import.append((names[key], view["import_id"]))

    for view in to_write:
        portal_type = view["key"][0]
        write_resource_block(portal_type, names[view["key"]], clean_config(view["config"], names[view["key"]]))
        print(f"Wrote {describe(view['key'])} to {module_file(portal_type)}")
    if to_write:
        format_module_files()

    error = import_to_state(to_import)
    imported = 0 if error else len(to_import)

    print(f"\nWrote {len(to_write)} block(s), imported {imported} view(s).")
    if skipped:
        print(f"\nSkipped {len(skipped)} view(s):")
        for line in skipped:
            print(f"   - {line}")
    if already_managed:
        filters = "".join(
            f" --{name} {shlex.quote(value)}"
            for name, value in [("portal", args.portal), ("view-type", args.view_type),
                                ("template", args.template), ("entity", args.entity)]
            if value
        )
        print(f"\nHint: to update views that are already managed with their current layout in BioT, add --refresh:\n"
              f"   python3 ../../scripts/portal_views/init_portal_views.py{filters} --refresh")
    if error:
        print(f"\nImport failed - the .tf blocks were kept, fix the error and re-run the script to retry:\n{error}")
        sys.exit(1)

    print("\nRun `terraform plan` to check - it should show no changes.")


if __name__ == "__main__":
    main()
