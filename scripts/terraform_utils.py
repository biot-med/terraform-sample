"""
Terraform helpers shared by the scripts that generate a module's .tf files with `terraform query` and import what they
generate into the env's state (scripts/abac, scripts/portal_views). Run from an env folder, e.g. envs/dev.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

from common_utils import read_main_tf_required_providers


def check_env_folder():
    if not os.path.exists("main.tf"):
        print("main.tf not found. Run this script from an environment folder, e.g. envs/dev")
        sys.exit(1)


def run_terraform_init():
    print("Running `terraform init`")
    result = subprocess.run(["terraform", "init", "-input=false", "-no-color"], capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr)
        raise RuntimeError("Terraform initialization failed.")


def module_block(module_name, module_source, depends_on_modules=()):
    depends_on = ""
    if depends_on_modules:
        depends_on = f"\n  depends_on = [{', '.join(f'module.{name}' for name in depends_on_modules)}]\n"
    return f'module "{module_name}" {{\n  source = "{module_source}"\n{depends_on}}}\n'


def has_module(main_tf, module_name):
    return re.search(rf'^module\s+"?{module_name}"?\s*{{', main_tf, re.MULTILINE) is not None


def ensure_module(module_name, module_dir, module_source, depends_on_modules=()):
    """
    Creates the module folder and adds the module to the env's main.tf if missing. Runs terraform init when anything
    changed. depends_on_modules are added to the module's depends_on if main.tf has them.
    """
    changed = False

    if not os.path.isdir(module_dir):
        os.makedirs(module_dir)
        print(f"Created module folder: {module_dir}")

    providers_tf_path = os.path.join(module_dir, "providers.tf")
    if not os.path.exists(providers_tf_path):
        with open(providers_tf_path, "w") as f:
            f.write(f"terraform {{\n{read_main_tf_required_providers()}\n}}\n")
        print(f"Created {providers_tf_path}")

    with open("main.tf", "r") as f:
        main_tf = f.read()

    if not has_module(main_tf, module_name):
        depends_on = [name for name in depends_on_modules if has_module(main_tf, name)]
        with open("main.tf", "a") as f:
            f.write("\n" + module_block(module_name, module_source, depends_on))
        print(f"Added module block for [{module_name}] to main.tf")
        changed = True

    if changed or not os.path.isdir(".terraform"):
        run_terraform_init()


def hcl_string(value):
    """Quotes a value as an HCL string - JSON escaping, plus escaping HCL's ${ and %{ template sequences"""
    return json.dumps(value).replace("${", "$${").replace("%{", "%%{")


def query(resource_type, query_file, label, owner, filters=None):
    """
    Runs terraform query for one list resource type and returns what it found as a list of
    {"identity": ..., "config": ...}, where config is the generated resource block.

    query_file is written for the run and deleted right after. filters are the list block's config attributes.
    label names what's queried in messages (e.g. "rules"), owner names the scripts folder (e.g. "scripts/abac").
    """
    # terraform query reads every .tfquery.hcl in the folder, so another one would change the results
    other_query_files = [f for f in os.listdir(".") if f.endswith(".tfquery.hcl") and f != query_file]
    if other_query_files:
        print(f"Found {', '.join(other_query_files)} in this folder. The {owner} scripts run their own query - "
              f"remove or rename these files (e.g. to .hcl.bak) and run the script again.")
        sys.exit(1)

    config = ""
    if filters:
        config = "\n  config {\n" + "".join(f"    {name} = {hcl_string(value)}\n" for name, value in filters.items()) + "  }\n"

    print(f"Querying {label}...")
    with open(query_file, "w") as f:
        f.write(f"""# Temporary file written by {owner} - safe to delete.
list "{resource_type}" "query" {{
  provider = biot

  # Terraform returns at most 100 results per list block unless told otherwise.
  limit = 1000
{config}}}
""")

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
        os.remove(query_file)

    found = []
    errors = []
    for line in result.stdout.splitlines():
        try:
            message = json.loads(line)
        except json.JSONDecodeError:
            continue
        if message.get("type") == "list_resource_found":
            resource = message["list_resource_found"]
            found.append({"identity": resource["identity"], "config": resource["config"]})
        elif message.get("@level") == "error":
            errors.append(message.get("@message", line))

    if result.returncode != 0 or errors:
        print("\n".join(errors) or result.stderr or result.stdout)
        raise RuntimeError(f"terraform query failed for {label}.")

    return found


def to_resource_name(value, taken_names, fallback="object"):
    """Turns a value into a unique Terraform resource name, e.g. "Filter reference test" -> filter_reference_test"""
    name = re.sub(r"[^a-z0-9_]+", "_", value.lower()).strip("_") or fallback
    if name[0].isdigit():
        name = f"id_{name}"

    unique_name = name
    suffix = 2
    while unique_name in taken_names:
        unique_name = f"{name}_{suffix}"
        suffix += 1
    return unique_name


def clean_config(config, resource_name, order):
    """
    Renames the generated resource (e.g. query_3 -> resource_name), drops the `provider = biot-gen2` line and
    puts the attributes in order - a list of attribute names, where "*" marks where attributes not listed go
    """
    config = re.sub(r'^(resource\s+"[^"]+"\s+)"[^"]+"', rf'\1"{resource_name}"', config, count=1)
    config = re.sub(r"^\s*provider\s*=\s*biot-gen2\s*\n", "", config, flags=re.MULTILINE)
    return order_attributes(config, order)


def order_attributes(config, order):
    body_start = config.index("{") + 1
    body_end = config.rindex("}")
    attributes = split_attributes(config[body_start:body_end])

    def position(attribute):
        name = attribute.split("=", 1)[0].strip()
        return order.index(name) if name in order else order.index("*")

    # sorted() is stable, so attributes in the same position keep Terraform's order
    attributes = sorted(attributes, key=position)
    return config[:body_start] + "\n" + "\n".join(attributes) + "\n" + config[body_end:]


def split_attributes(body):
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


def format_dir(path):
    """Re-aligns the .tf files the way `terraform fmt` does, since reordering attributes breaks the `=` alignment"""
    subprocess.run(["terraform", "fmt", path], capture_output=True, text=True)


def find_closing(text, start, opening, closing):
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


def find_resource_block(content, resource_type, resource_name):
    """Returns (start, end) of a resource block in a file's content, or None"""
    match = re.search(rf'^resource\s+"{resource_type}"\s+"{re.escape(resource_name)}"\s*{{', content, re.MULTILINE)
    if not match:
        return None
    end = find_closing(content, match.end() - 1, "{", "}")
    return (match.start(), end + 1) if end is not None else None


def read_resource_blocks(path, resource_type):
    """Yields (resource_name, block_text) for each block of resource_type in a .tf file"""
    if not os.path.exists(path):
        return
    with open(path, "r") as f:
        content = f.read()

    for match in re.finditer(rf'^resource\s+"{resource_type}"\s+"([^"]+)"', content, re.MULTILINE):
        block = find_resource_block(content, resource_type, match.group(1))
        if block is not None:
            yield match.group(1), content[block[0]:block[1]]


def read_string_attribute(block, attribute):
    """The value of a top-level string attribute in a resource block, or None"""
    match = re.search(rf'^  {attribute}\s*=\s*("(?:[^"\\]|\\.)*")', block, re.MULTILINE)
    return json.loads(match.group(1)) if match else None


def write_resource_block(path, resource_type, resource_name, config):
    """Adds the resource block to a .tf file, replacing the existing block with the same name"""
    content = ""
    if os.path.exists(path):
        with open(path, "r") as f:
            content = f.read()

    block = find_resource_block(content, resource_type, resource_name)
    if block:
        content = content[:block[0]] + config + content[block[1]:]
    else:
        content = (content.rstrip("\n") + "\n\n" if content.strip() else "") + config + "\n"

    with open(path, "w") as f:
        f.write(content)


def read_state_resources(resource_types):
    """
    Reads the managed resources of the given types in the env's terraform.tfstate.
    Yields (resource_type, terraform_address, attributes) for each instance.
    """
    if not os.path.exists("terraform.tfstate"):
        return

    with open("terraform.tfstate", "r") as f:
        state = json.load(f)

    for resource in state.get("resources", []):
        if resource.get("mode") != "managed" or resource.get("type") not in resource_types:
            continue
        prefix = f"{resource['module']}." if resource.get("module") else ""
        for instance in resource.get("instances", []):
            yield resource["type"], f"{prefix}{resource['type']}.{resource['name']}", instance.get("attributes", {})


def import_to_state(imports, imports_file, plan_file, owner):
    """
    Imports resources into the env's state in a single Terraform run: writes an import block for each one, plans,
    and applies the saved plan only if it contains nothing but these imports - so other pending changes in the env
    are never applied by accident. imports is a list of (terraform_address, import_id).
    Returns None on success, or the error to show.
    """
    if not imports:
        return None

    blocks = [f"import {{\n  to = {address}\n  id = {hcl_string(import_id)}\n}}\n" for address, import_id in imports]
    with open(imports_file, "w") as f:
        f.write(f"# Temporary file written by {owner} - safe to delete.\n\n" + "\n".join(blocks))

    try:
        print(f"Planning the import of {len(imports)} object(s)...")
        result = subprocess.run(
            ["terraform", "plan", "-input=false", "-no-color", "-refresh=false", f"-out={plan_file}"],
            capture_output=True, text=True,
        )
        if result.returncode != 0:
            return (result.stderr or result.stdout).strip()

        result = subprocess.run(["terraform", "show", "-json", plan_file], capture_output=True, text=True)
        if result.returncode != 0:
            return (result.stderr or result.stdout).strip()

        other_changes = []
        imported = 0
        for change in json.loads(result.stdout).get("resource_changes", []):
            actions = change["change"]["actions"]
            if "importing" in change["change"] and actions == ["no-op"]:
                imported += 1
            elif actions != ["no-op"]:
                other_changes.append(f"{change['address']} ({', '.join(actions)})")

        if other_changes:
            return ("Nothing was imported - the plan has changes other than these imports. Apply or revert them first, "
                    "or check the generated config of the objects listed:\n" + "\n".join(f"   - {c}" for c in other_changes))
        if imported != len(imports):
            return f"Nothing was imported - expected {len(imports)} import(s) in the plan but found {imported}."

        print(f"Importing {imported} object(s)...")
        result = subprocess.run(["terraform", "apply", "-input=false", "-no-color", plan_file], capture_output=True, text=True)
        if result.returncode != 0:
            return (result.stderr or result.stdout).strip()
        return None
    finally:
        for path in (imports_file, plan_file):
            if os.path.exists(path):
                os.remove(path)
