import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

SCRIPTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.insert(0, SCRIPTS_DIR)
from common_utils import read_main_tf_required_providers

# Scripts run from an env folder (e.g. envs/dev), two levels below the project root
MODULE_NAME = "abac"
MODULE_SOURCE = "../../modules/abac"
MODULE_DIR = os.path.join(os.pardir, os.pardir, "modules", "abac")

# Processed in this order so rules can reference the actions and conditions they use
ABAC_TYPES = ["action", "condition", "rule"]
RESOURCE_TYPES = {
    "action": "biot_abac_action",
    "condition": "biot_abac_condition",
    "rule": "biot_abac_rule",
}
MODULE_FILES = {
    "action": "actions.tf",
    "condition": "conditions.tf",
    "rule": "rules.tf",
}

# Written by query() for each run and deleted right after, so it never needs to be kept or edited
QUERY_FILE = "abac_scripts_query.tfquery.hcl"


def get_query_file_content(abac_type):
    return f"""# Temporary file written by scripts/abac - safe to delete.
list "{RESOURCE_TYPES[abac_type]}" "{abac_type}" {{
  provider = biot

  # Terraform returns at most 100 results per list block unless told otherwise.
  limit = 1000
}}
"""


def check_env_folder():
    if not os.path.exists("main.tf"):
        print("main.tf not found. Run this script from an environment folder, e.g. envs/dev")
        sys.exit(1)


def ensure_module():
    """Creates modules/abac and adds it to the env's main.tf if missing. Runs terraform init when anything changed."""
    changed = False

    if not os.path.isdir(MODULE_DIR):
        os.makedirs(MODULE_DIR)
        print(f"Created module folder: {MODULE_DIR}")

    providers_tf_path = os.path.join(MODULE_DIR, "providers.tf")
    if not os.path.exists(providers_tf_path):
        with open(providers_tf_path, "w") as f:
            f.write(f"terraform {{\n{read_main_tf_required_providers()}\n}}\n")
        print(f"Created {providers_tf_path}")

    with open("main.tf", "r") as f:
        main_tf = f.read()

    if not re.search(rf'^module\s+"?{MODULE_NAME}"?\s*{{', main_tf, re.MULTILINE):
        with open("main.tf", "a") as f:
            f.write(f'\nmodule "{MODULE_NAME}" {{\n  source = "{MODULE_SOURCE}"\n}}\n')
        print(f"Added module block for [{MODULE_NAME}] to main.tf")
        changed = True

    if changed or not os.path.isdir(".terraform"):
        run_terraform_init()


def run_terraform_init():
    print("Running `terraform init`")
    result = subprocess.run(["terraform", "init", "-input=false", "-no-color"], capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr)
        raise RuntimeError("Terraform initialization failed.")


def query(abac_type):
    """
    Runs terraform query for one ABAC type and returns what it found as a list of
    {"id": ..., "config": ...}, where config is the generated resource block.
    """
    # terraform query reads every .tfquery.hcl in the folder, so another one would change the results
    other_query_files = [f for f in os.listdir(".") if f.endswith(".tfquery.hcl") and f != QUERY_FILE]
    if other_query_files:
        print(f"Found {', '.join(other_query_files)} in this folder. The ABAC scripts run their own query - "
              f"remove or rename these files (e.g. to .hcl.bak) and run the script again.")
        sys.exit(1)

    print(f"Querying {abac_type}s...")
    with open(QUERY_FILE, "w") as f:
        f.write(get_query_file_content(abac_type))

    # The generated config is read from the JSON output. The file Terraform also writes goes
    # to a temp folder, so it never lands in the env folder.
    temp_dir = tempfile.mkdtemp()
    try:
        result = subprocess.run(
            [
                "terraform", "query", "-json", "-no-color",
                f"-generate-config-out={os.path.join(temp_dir, 'generated.tf')}",
            ],
            capture_output=True, text=True,
        )
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)
        os.remove(QUERY_FILE)

    found = []
    errors = []
    for line in result.stdout.splitlines():
        try:
            message = json.loads(line)
        except json.JSONDecodeError:
            continue
        if message.get("type") == "list_resource_found":
            resource = message["list_resource_found"]
            found.append({"id": resource["identity"]["id"], "config": resource["config"]})
        elif message.get("@level") == "error":
            errors.append(message.get("@message", line))

    if result.returncode != 0 or errors:
        print("\n".join(errors) or result.stderr or result.stdout)
        raise RuntimeError(f"terraform query failed for {abac_type}s.")

    return found


def to_resource_name(object_id, taken_names):
    """Turns an ABAC id into a Terraform resource name, e.g. "Filter reference test" -> filter_reference_test"""
    name = re.sub(r"[^a-z0-9_]+", "_", object_id.lower()).strip("_") or "object"
    if name[0].isdigit():
        name = f"id_{name}"

    unique_name = name
    suffix = 2
    while unique_name in taken_names:
        unique_name = f"{name}_{suffix}"
        suffix += 1
    return unique_name


# Order of the attributes in the generated blocks - Terraform generates them alphabetically, which puts a rule's long
# api_execution_points list before its id, description and conditions. "*" marks where attributes not listed here go.
ATTRIBUTE_ORDER = {
    "action": ["id", "description", "value", "params", "tags", "*"],
    "condition": ["id", "description", "value", "params", "tags", "*"],
    "rule": ["id", "description", "conditions", "action_ids", "tags", "*", "api_execution_points"],
}


def clean_config(config, resource_name, abac_type):
    """
    Renames the generated resource (action_0_3 -> resource_name), drops the `provider = biot-gen2` line and
    puts the attributes in ATTRIBUTE_ORDER
    """
    config = re.sub(r'^(resource\s+"[^"]+"\s+)"[^"]+"', rf'\1"{resource_name}"', config, count=1)
    config = re.sub(r"^\s*provider\s*=\s*biot-gen2\s*\n", "", config, flags=re.MULTILINE)
    return _order_attributes(config, ATTRIBUTE_ORDER[abac_type])


def _order_attributes(config, order):
    body_start = config.index("{") + 1
    body_end = config.rindex("}")
    attributes = _split_attributes(config[body_start:body_end])

    def position(attribute):
        name = attribute.split("=", 1)[0].strip()
        return order.index(name) if name in order else order.index("*")

    # sorted() is stable, so attributes in the same position keep Terraform's order
    attributes = sorted(attributes, key=position)
    return config[:body_start] + "\n" + "\n".join(attributes) + "\n" + config[body_end:]


def _split_attributes(body):
    """Splits a block's body into its top-level attributes, keeping multi-line values whole"""
    attributes = []
    current = ""
    depth = 0
    in_string = False
    i = 0
    while i < len(body):
        char = body[i]
        current += char
        if in_string:
            if char == "\\":
                i += 1
                current += body[i] if i < len(body) else ""
            elif char == '"':
                in_string = False
        elif char == '"':
            in_string = True
        elif char in "([{":
            depth += 1
        elif char in ")]}":
            depth -= 1
        elif char == "\n" and depth == 0:
            if current.strip():
                attributes.append(current.rstrip("\n"))
            current = ""
        i += 1
    if current.strip():
        attributes.append(current.rstrip("\n"))
    return attributes


def format_module_files():
    """Re-aligns the module files the way `terraform fmt` does, since reordering attributes breaks the `=` alignment"""
    subprocess.run(["terraform", "fmt", MODULE_DIR], capture_output=True, text=True)


def _find_list(config, attribute):
    """Returns (start, end) of the [...] value of a top-level list attribute, or None"""
    match = re.search(rf"^  {attribute}\s*=\s*\[", config, re.MULTILINE)
    if not match:
        return None
    start = match.end() - 1
    end = _find_closing(config, start, "[", "]")
    return (start, end + 1) if end is not None else None


def reference_rule_dependencies(config, managed_names):
    """
    In a rule's generated config, replaces the ids of actions and conditions that are managed in
    the module with references (e.g. biot_abac_action.my_action.id), so Terraform creates them
    before the rule. Ids of objects that aren't in the module (e.g. CLASS actions) stay as strings.
    """
    def replace_ids(span, abac_type, pattern):
        nonlocal config
        if span is None:
            return
        start, end = span
        names = managed_names[abac_type]

        def to_reference(match):
            object_id = json.loads(match.group("id"))
            if object_id not in names:
                return match.group(0)
            reference = f"{RESOURCE_TYPES[abac_type]}.{names[object_id]}.id"
            return match.group(0).replace(match.group("id"), reference)

        config = config[:start] + re.sub(pattern, to_reference, config[start:end]) + config[end:]

    replace_ids(_find_list(config, "conditions"), "condition", r'\bid\s*=\s*(?P<id>"(?:[^"\\]|\\.)*")')
    replace_ids(_find_list(config, "action_ids"), "action", r'(?P<id>"(?:[^"\\]|\\.)*")')
    return config


def _find_closing(text, start, opening, closing):
    """Index of the bracket closing the one at text[start], skipping anything inside strings"""
    depth = 0
    in_string = False
    i = start
    while i < len(text):
        char = text[i]
        if in_string:
            if char == "\\":
                i += 1
            elif char == '"':
                in_string = False
        elif char == '"':
            in_string = True
        elif char == opening:
            depth += 1
        elif char == closing:
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return None


def _find_resource_block(content, resource_type, resource_name):
    """Returns (start, end) of a resource block in a file's content, or None"""
    match = re.search(rf'^resource\s+"{resource_type}"\s+"{re.escape(resource_name)}"\s*{{', content, re.MULTILINE)
    if not match:
        return None
    end = _find_closing(content, match.end() - 1, "{", "}")
    return (match.start(), end + 1) if end is not None else None


def read_module_resources():
    """
    Reads the ABAC resources already defined in modules/abac.
    Returns {abac_type: {object_id: resource_name}}.
    """
    resources = {abac_type: {} for abac_type in ABAC_TYPES}

    for abac_type in ABAC_TYPES:
        path = os.path.join(MODULE_DIR, MODULE_FILES[abac_type])
        if not os.path.exists(path):
            continue
        with open(path, "r") as f:
            content = f.read()

        for match in re.finditer(rf'^resource\s+"{RESOURCE_TYPES[abac_type]}"\s+"([^"]+)"', content, re.MULTILINE):
            block = _find_resource_block(content, RESOURCE_TYPES[abac_type], match.group(1))
            if block is None:
                continue
            id_match = re.search(r'^  id\s*=\s*("(?:[^"\\]|\\.)*")', content[block[0]:block[1]], re.MULTILINE)
            if id_match:
                resources[abac_type][json.loads(id_match.group(1))] = match.group(1)

    return resources


def write_resource_block(abac_type, resource_name, config):
    """Adds the resource block to its module file, replacing the existing block with the same name"""
    path = os.path.join(MODULE_DIR, MODULE_FILES[abac_type])
    content = ""
    if os.path.exists(path):
        with open(path, "r") as f:
            content = f.read()

    block = _find_resource_block(content, RESOURCE_TYPES[abac_type], resource_name)
    if block:
        content = content[:block[0]] + config + content[block[1]:]
    else:
        content = (content.rstrip("\n") + "\n\n" if content.strip() else "") + config + "\n"

    with open(path, "w") as f:
        f.write(content)


def read_state_addresses():
    """
    Reads the ABAC objects in the env's terraform.tfstate.
    Returns {abac_type: {object_id: terraform_address}}.
    """
    addresses = {abac_type: {} for abac_type in ABAC_TYPES}
    if not os.path.exists("terraform.tfstate"):
        return addresses

    with open("terraform.tfstate", "r") as f:
        state = json.load(f)

    abac_types_by_resource = {resource_type: abac_type for abac_type, resource_type in RESOURCE_TYPES.items()}
    for resource in state.get("resources", []):
        abac_type = abac_types_by_resource.get(resource.get("type"))
        if resource.get("mode") != "managed" or abac_type is None:
            continue
        prefix = f"{resource['module']}." if resource.get("module") else ""
        for instance in resource.get("instances", []):
            object_id = instance.get("attributes", {}).get("id")
            if object_id is not None:
                addresses[abac_type][object_id] = f"{prefix}{resource['type']}.{resource['name']}"

    return addresses


def module_address(abac_type, resource_name):
    return f"module.{MODULE_NAME}.{RESOURCE_TYPES[abac_type]}.{resource_name}"


def import_to_state(abac_type, resource_name, object_id):
    """Imports one object into the env's state. Returns None on success, or the error output."""
    result = subprocess.run(
        ["terraform", "import", "-input=false", "-no-color", module_address(abac_type, resource_name), object_id],
        capture_output=True, text=True,
    )
    if result.returncode == 0:
        return None
    return (result.stderr or result.stdout).strip()
