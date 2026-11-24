import os
import sys

SCRIPTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.insert(0, SCRIPTS_DIR)
import terraform_utils
from terraform_utils import check_env_folder, format_dir, read_resource_blocks, read_string_attribute  # noqa: F401

# Scripts run from an env folder (e.g. envs/dev), two levels below the project root
MODULE_NAME = "portal_views"
MODULE_SOURCE = "../../modules/portal_views"
MODULE_DIR = os.path.join(os.pardir, os.pardir, "modules", "portal_views")

RESOURCE_TYPE = "biot_portal_view"

# Each portal's views go to their own file, and their resource names start with the portal's short name
PORTALS = {
    "organization": "ORGANIZATION_PORTAL",
    "manufacturer": "MANUFACTURER_PORTAL",
}
PORTAL_SHORT_NAMES = {portal_type: short_name for short_name, portal_type in PORTALS.items()}

VIEW_TYPES = [
    "ENTITY_LIST",
    "TEMPLATE_EXPAND",
    "TEMPLATE_PREVIEW",
    "TEMPLATE_LIST",
    "MAIN",
    "OPERATIONAL_ENTITY_LIST",
    "OPERATIONAL_TEMPLATE_PREVIEW",
]

# Terraform generates the attributes alphabetically, which puts the long config_json first
ATTRIBUTE_ORDER = ["portal_type", "view_type", "template_name", "entity_type_name", "*", "config_json"]

OWNER = "scripts/portal_views"
# Written for each run and deleted right after, so they never need to be kept or edited
QUERY_FILE = "portal_views_scripts_query.tfquery.hcl"
IMPORTS_FILE = "portal_views_scripts_imports.tf"
PLAN_FILE = "portal_views_scripts_imports.tfplan"


def module_file(portal_type):
    return f"{PORTAL_SHORT_NAMES[portal_type]}_portal.tf"


def view_key(attributes):
    """
    Identifies a view the same way in every environment - view ids differ between environments, but a portal has one
    view per view type and template (or entity, for entity views, or nothing, for MAIN).
    """
    return (
        attributes.get("portal_type"),
        attributes.get("view_type"),
        attributes.get("template_name") or attributes.get("entity_type_name") or "",
    )


def describe(key):
    portal_type, view_type, subject = key
    return f"{PORTAL_SHORT_NAMES.get(portal_type, portal_type)} {view_type}" + (f" [{subject}]" if subject else "")


def to_resource_name(key, taken_names):
    """e.g. ("ORGANIZATION_PORTAL", "TEMPLATE_EXPAND", "Clinician") -> organization_clinician_template_expand"""
    portal_type, view_type, subject = key
    parts = [PORTAL_SHORT_NAMES.get(portal_type, portal_type), subject, view_type]
    return terraform_utils.to_resource_name("_".join(part for part in parts if part), taken_names, fallback="view")


def ensure_module():
    """Creates modules/portal_views and adds it to the env's main.tf if missing. Runs terraform init when anything changed."""
    # Views find their template by name, so in a new environment the templates must be created first
    terraform_utils.ensure_module(MODULE_NAME, MODULE_DIR, MODULE_SOURCE, depends_on_modules=["templates"])


def _read_config_attributes(config):
    return {
        name: read_string_attribute(config, name)
        for name in ("portal_type", "view_type", "template_name", "entity_type_name")
    }


def query(portal_type=None, view_type=None):
    """
    Runs terraform query for the portal views and returns what it found as a list of
    {"key": ..., "attributes": ..., "import_id": ..., "config": ...}, where config is the generated resource block.
    """
    filters = {name: value for name, value in [("portal_type", portal_type), ("view_type", view_type)] if value}
    found = terraform_utils.query(RESOURCE_TYPE, QUERY_FILE, "portal views", OWNER, filters)
    views = []
    for view in found:
        attributes = _read_config_attributes(view["config"])
        views.append({
            "key": view_key(attributes),
            "attributes": attributes,
            # The provider imports a view by <portal_type>/<view_id>
            "import_id": f"{view['identity']['portal_type']}/{view['identity']['id']}",
            "config": view["config"],
        })
    return views


def clean_config(config, resource_name):
    """Renames the generated resource (query_3 -> resource_name), drops the `provider = biot-gen2` line and orders the attributes"""
    return terraform_utils.clean_config(config, resource_name, ATTRIBUTE_ORDER)


def read_module_resources():
    """
    Reads the portal views already defined in modules/portal_views.
    Returns {view_key: resource_name}.
    """
    resources = {}
    for portal_type in PORTALS.values():
        path = os.path.join(MODULE_DIR, module_file(portal_type))
        for resource_name, block in read_resource_blocks(path, RESOURCE_TYPE):
            resources[view_key(_read_config_attributes(block))] = resource_name
    return resources


def write_resource_block(portal_type, resource_name, config):
    """Adds the resource block to its portal's module file, replacing the existing block with the same name"""
    path = os.path.join(MODULE_DIR, module_file(portal_type))
    terraform_utils.write_resource_block(path, RESOURCE_TYPE, resource_name, config)


def format_module_files():
    format_dir(MODULE_DIR)


def read_state_addresses():
    """
    Reads the portal views in the env's terraform.tfstate.
    Returns {view_key: terraform_address}.
    """
    return {
        view_key(attributes): address
        for _, address, attributes in terraform_utils.read_state_resources({RESOURCE_TYPE})
    }


def module_address(resource_name):
    return f"module.{MODULE_NAME}.{RESOURCE_TYPE}.{resource_name}"


def import_to_state(views):
    """
    Imports views into the env's state in a single Terraform run, applying the plan only if it contains nothing but
    these imports. views is a list of (resource_name, import_id).
    Returns None on success, or the error to show.
    """
    imports = [(module_address(resource_name), import_id) for resource_name, import_id in views]
    return terraform_utils.import_to_state(imports, IMPORTS_FILE, PLAN_FILE, OWNER)
