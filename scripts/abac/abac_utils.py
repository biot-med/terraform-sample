import json
import os
import re
import sys

SCRIPTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.insert(0, SCRIPTS_DIR)
import terraform_utils
from terraform_utils import check_env_folder, find_closing, format_dir, read_resource_blocks, read_string_attribute

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

OWNER = "scripts/abac"
# Written for each run and deleted right after, so they never need to be kept or edited
QUERY_FILE = "abac_scripts_query.tfquery.hcl"
IMPORTS_FILE = "abac_scripts_imports.tf"
PLAN_FILE = "abac_scripts_imports.tfplan"


def ensure_module():
    """Creates modules/abac and adds it to the env's main.tf if missing. Runs terraform init when anything changed."""
    terraform_utils.ensure_module(MODULE_NAME, MODULE_DIR, MODULE_SOURCE)


def query(abac_type):
    """
    Runs terraform query for one ABAC type and returns what it found as a list of
    {"id": ..., "config": ...}, where config is the generated resource block.
    """
    found = terraform_utils.query(RESOURCE_TYPES[abac_type], QUERY_FILE, f"{abac_type}s", OWNER)
    return [{"id": obj["identity"]["id"], "config": obj["config"]} for obj in found]


def to_resource_name(object_id, taken_names):
    """Turns an ABAC id into a Terraform resource name, e.g. "Filter reference test" -> filter_reference_test"""
    return terraform_utils.to_resource_name(object_id, taken_names)


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
    return terraform_utils.clean_config(config, resource_name, ATTRIBUTE_ORDER[abac_type])


def format_module_files():
    """Re-aligns the module files the way `terraform fmt` does, since reordering attributes breaks the `=` alignment"""
    format_dir(MODULE_DIR)


def _find_list(config, attribute):
    """Returns (start, end) of the [...] value of a top-level list attribute, or None"""
    match = re.search(rf"^  {attribute}\s*=\s*\[", config, re.MULTILINE)
    if not match:
        return None
    start = match.end() - 1
    end = find_closing(config, start, "[", "]")
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


def read_module_resources():
    """
    Reads the ABAC resources already defined in modules/abac.
    Returns {abac_type: {object_id: resource_name}}.
    """
    resources = {abac_type: {} for abac_type in ABAC_TYPES}

    for abac_type in ABAC_TYPES:
        path = os.path.join(MODULE_DIR, MODULE_FILES[abac_type])
        for resource_name, block in read_resource_blocks(path, RESOURCE_TYPES[abac_type]):
            object_id = read_string_attribute(block, "id")
            if object_id is not None:
                resources[abac_type][object_id] = resource_name

    return resources


def write_resource_block(abac_type, resource_name, config):
    """Adds the resource block to its module file, replacing the existing block with the same name"""
    path = os.path.join(MODULE_DIR, MODULE_FILES[abac_type])
    terraform_utils.write_resource_block(path, RESOURCE_TYPES[abac_type], resource_name, config)


def read_state_addresses():
    """
    Reads the ABAC objects in the env's terraform.tfstate.
    Returns {abac_type: {object_id: terraform_address}}.
    """
    addresses = {abac_type: {} for abac_type in ABAC_TYPES}
    abac_types_by_resource = {resource_type: abac_type for abac_type, resource_type in RESOURCE_TYPES.items()}

    for resource_type, address, attributes in terraform_utils.read_state_resources(abac_types_by_resource):
        object_id = attributes.get("id")
        if object_id is not None:
            addresses[abac_types_by_resource[resource_type]][object_id] = address

    return addresses


def module_address(abac_type, resource_name):
    return f"module.{MODULE_NAME}.{RESOURCE_TYPES[abac_type]}.{resource_name}"


def import_to_state(objects):
    """
    Imports objects into the env's state in a single Terraform run, applying the plan only if it contains nothing but
    these imports. objects is a list of (abac_type, resource_name, object_id).
    Returns None on success, or the error to show.
    """
    imports = [(module_address(abac_type, resource_name), object_id) for abac_type, resource_name, object_id in objects]
    return terraform_utils.import_to_state(imports, IMPORTS_FILE, PLAN_FILE, OWNER)
