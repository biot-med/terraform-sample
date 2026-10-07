import sys

from abac_utils import (
    ABAC_TYPES, MODULE_DIR, check_env_folder, ensure_module, import_to_state,
    module_address, query, read_module_resources, read_state_addresses,
)


def main():
    """
    Prepares an environment for its first `terraform apply` of modules/abac: imports the ABAC objects
    that are defined in the module and already exist in this environment (e.g. ones BioT ships), so
    apply only creates what's missing instead of failing with "already exists".
    """
    check_env_folder()
    ensure_module()

    module_resources = read_module_resources()
    if not any(module_resources.values()):
        print(f"No ABAC resources defined in {MODULE_DIR} - nothing to import.")
        return

    state = read_state_addresses()
    to_import = []
    to_create = []

    for abac_type in ABAC_TYPES:
        existing_ids = {obj["id"] for obj in query(abac_type)}
        for object_id, resource_name in module_resources[abac_type].items():
            if object_id in state[abac_type]:
                continue
            if object_id in existing_ids:
                to_import.append((abac_type, resource_name, object_id))
            else:
                to_create.append(f"{abac_type} [{object_id}]")

    failed = []
    for index, (abac_type, resource_name, object_id) in enumerate(to_import, start=1):
        print(f"Importing ({index}/{len(to_import)}) {module_address(abac_type, resource_name)}")
        error = import_to_state(abac_type, resource_name, object_id)
        if error:
            failed.append(f"{abac_type} [{object_id}]: {error}")

    print(f"\nImported {len(to_import) - len(failed)} existing object(s).")
    if to_create:
        print(f"{len(to_create)} object(s) don't exist in this environment yet and will be created by `terraform apply`:")
        for line in to_create:
            print(f"   - {line}")
    if failed:
        print(f"\n{len(failed)} import(s) failed - re-run the script to retry:")
        for line in failed:
            print(f"   - {line}")
        sys.exit(1)


if __name__ == "__main__":
    main()
