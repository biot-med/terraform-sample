import json
import sys

INDENT = "  "

def render_value_json(value, indent_level):
    indent = INDENT * indent_level
    try:
        # If value is a JSON string, parse it to pretty JSON for jsonencode
        parsed = json.loads(value) if isinstance(value, str) else value
        pretty_json = json.dumps(parsed, indent=2)
        # Format with indentation
        json_lines = pretty_json.splitlines()
        formatted_json = "\n".join(indent + "  " + line for line in json_lines)
        return f"jsonencode(\n{formatted_json}\n{indent})"
    except Exception:
        # Fallback: just render as a quoted string
        return f"\"{value}\""


def format_value(value, level=1):
    indent = INDENT * level
    next_indent = INDENT * (level + 1)

    if isinstance(value, bool):
        return "true" if value else "false"
    elif isinstance(value, str):
        return f"\"{value}\""
    elif value is None:
        return "null"
    elif isinstance(value, (int, float)):
        return str(value)
    elif isinstance(value, list):
        if all(isinstance(item, (str, int, float, bool)) for item in value):
            return "[ " + ", ".join(format_value(item, level) for item in value) + " ]"
        elif all(isinstance(item, dict) for item in value):
            # Render list of dicts
            lines = ["["]
            for item in value:
                lines.append(f"{next_indent}{{")
                for key, val in item.items():
                    if key == "id":
                        continue  # Skip "id" in nested dict
                    lines.append(f"{next_indent}{INDENT}{key} = {format_value(val, level + 2)}")
                lines.append(f"{next_indent}}},")
            lines.append(f"{indent}]")
            return "\n".join(lines)
        else:
            return "[ " + ", ".join(format_value(item, level) for item in value) + " ]"
    elif isinstance(value, dict):
        lines = ["{"]
        for key, val in value.items():
            if key == "id":
                continue  # Skip "id" in object
            lines.append(f"{next_indent}{key} = {format_value(val, level + 1)}")
        lines.append(f"{indent}}}")
        return "\n".join(lines)

    return f"\"{value}\""



def render_block(name, content, level):
    indent = INDENT * level

    # Special case for template_attributes list
    if name == "template_attributes" and isinstance(content, list):
        lines = [f"{indent}{name} = ["]
        for item in content:
            lines.append(f"{indent}{INDENT}{{")
            for k, v in item.items():
                if k == "id":
                    continue  # skip id field inside template_attributes
                if k == "value_json":
                    # Render value with jsonencode if possible
                    rendered_value = render_value_json(v, level + 2)
                    lines.append(f"{indent}{INDENT*2}{k} = {rendered_value}")
                else:
                    # normal rendering for other fields
                    rendered_val = format_value(v, level + 2)
                    lines.append(f"{indent}{INDENT*2}{k} = {rendered_val}")
            lines.append(f"{indent}{INDENT}}},")
        lines.append(f"{indent}]")
        return "\n".join(lines)

    # default rendering
    return f"{indent}{name} = {format_value(content, level)}"
    

def generate_resource_block(resource, level=0):
    resource_type = resource["type"]
    resource_name = resource["name"]
    attributes = resource.get("values", {})

    indent = INDENT * level
    lines = [f'{indent}resource "{resource_type}" "{resource_name}" {{']

    for key, value in attributes.items():
        if key == "id":
            continue  # Skip top-level "id"
        lines.append(render_block(key, value, level + 1))

    lines.append(f"{indent}}}")
    return "\n".join(lines)

def main():
    data = json.load(sys.stdin)
    resources = data.get("values", {}).get("root_module", {}).get("resources", [])

    if not resources:
        print("No resources found.")
        return

    with open("generated.tf", "w") as f:
        for resource in resources:
            f.write(generate_resource_block(resource))
            f.write("\n\n")

    print("✅ HCL written to generated.tf using only list/map-style syntax — no repeated blocks.")

if __name__ == "__main__":
    main()
