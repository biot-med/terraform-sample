import argparse
import sys

from abac_utils import (
    ABAC_TYPES, MODULE_DIR, MODULE_FILES, MODULE_NAME, check_env_folder, clean_config, ensure_module, format_module_files,
    import_to_state, module_address, query, read_module_resources, read_state_addresses,
    reference_rule_dependencies, to_resource_name, write_resource_block,
)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generates modules/abac .tf files for the ABAC actions, conditions and rules in the current "
                    "environment, and imports them into its terraform state. Objects already in the state are skipped."
    )
    parser.add_argument("--type", choices=ABAC_TYPES, help="Only this ABAC type")
    parser.add_argument("--id", help="Only the object with this id")
    parser.add_argument(
        "--refresh", action="store_true",
        help="Regenerate the .tf config of objects already managed, from their current state in BioT"
    )
    return parser.parse_args()


def main():
    args = parse_args()
    check_env_folder()
    ensure_module()

    abac_types = [args.type] if args.type else ABAC_TYPES
    found = {abac_type: query(abac_type) for abac_type in abac_types}

    if args.id:
        found = {abac_type: [obj for obj in objects if obj["id"] == args.id] for abac_type, objects in found.items()}
        if not any(found.values()):
            print(f"No {args.type or 'ABAC object'} with id [{args.id}] found in this environment.")
            sys.exit(1)

    state = read_state_addresses()
    # {abac_type: {object_id: resource_name}} - what modules/abac defines, plus what this run adds to it
    managed_names = read_module_resources()

    to_write = []
    to_import = []
    skipped = []
    already_managed = 0

    for abac_type in abac_types:
        names = managed_names[abac_type]
        for obj in found[abac_type]:
            object_id = obj["id"]
            address = state[abac_type].get(object_id)

            if address and object_id not in names:
                if not address.startswith(f"module.{MODULE_NAME}."):
                    skipped.append(f"{abac_type} [{object_id}] - already managed outside {MODULE_DIR} at {address}")
                    continue
                # In the module's state, but its block was removed from the module files - write it back
                names[object_id] = address.split(".")[-1]
                to_write.append((abac_type, obj))
                continue
            if address and not args.refresh:
                skipped.append(f"{abac_type} [{object_id}] - already managed")
                already_managed += 1
                continue

            if object_id not in names:
                names[object_id] = to_resource_name(object_id, set(names.values()))
                to_write.append((abac_type, obj))
            elif args.refresh:
                to_write.append((abac_type, obj))

            if not address:
                to_import.append((abac_type, object_id))

    for abac_type, obj in to_write:
        resource_name = managed_names[abac_type][obj["id"]]
        config = clean_config(obj["config"], resource_name, abac_type)
        if abac_type == "rule":
            config = reference_rule_dependencies(config, managed_names)
        write_resource_block(abac_type, resource_name, config)
        print(f"Wrote {abac_type} [{obj['id']}] to {MODULE_FILES[abac_type]}")
    if to_write:
        format_module_files()

    failed = []
    for index, (abac_type, object_id) in enumerate(to_import, start=1):
        resource_name = managed_names[abac_type][object_id]
        print(f"Importing ({index}/{len(to_import)}) {module_address(abac_type, resource_name)}")
        error = import_to_state(abac_type, resource_name, object_id)
        if error:
            failed.append(f"{abac_type} [{object_id}]: {error}")

    print(f"\nWrote {len(to_write)} block(s), imported {len(to_import) - len(failed)} object(s).")
    if skipped:
        print(f"\nSkipped {len(skipped)} object(s):")
        for line in skipped:
            print(f"   - {line}")
    if already_managed:
        filters = "".join(f' --{name} "{value}"' for name, value in [("type", args.type), ("id", args.id)] if value)
        print(f"\nHint: to update objects that are already managed with their current state in BioT, add --refresh:\n"
              f"   python3 ../../scripts/abac/init_abac.py{filters} --refresh")
    if failed:
        print(f"\n{len(failed)} import(s) failed - their .tf blocks were kept, re-run the script to retry:")
        for line in failed:
            print(f"   - {line}")
        sys.exit(1)

    print("\nRun `terraform plan` to check - it should show no changes.")


if __name__ == "__main__":
    main()
