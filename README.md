# BioT Terraform Sample Project

This is a sample Terraform project for managing BioT resources using the `BioT` Terraform provider.

This repository is intended to manage BioT's resources for your own environments, such as `dev`, `staging`, or `prod`.
Currently supported resources: Templates.

---

## Prerequisites

Before using this project, make sure you have the following:

- **Terraform** version **1.14+** installed (required for `terraform query`)  
  [Terraform Installation Guide](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli)

- **Python** version **3.x+** installed  
  [Python Download and Installation](https://www.python.org/downloads/)

- **Python dependencies** installed  
  Install required Python packages from the project root directory:
  ```bash
  pip3 install -r scripts/requirements.txt
  ```
  
  **Note:** Make sure you're in the project root directory when running this command. If `pip3` is not available, try `pip` instead.

- **BIOT Service ID and Secret Key**  
  You will need valid credentials (service ID and secret key) for the Terraform to authenticate with the BioT APIs.  
  See the [BioT Service Credentials documentation](https://docs.biot-med.com/docs/technical-information) (under the "Terraform Service User" section) for details on how to obtain these.

---

## Main Flows

## First Time Initialization

After forking this project to initialize the terraform project and sync it with your current environment's state:

1. Remove 'example' extension from the envs/dev/secret.auto.tfvars.example file (the new name should be secret.auto.tfvars)
2. Make sure the values in both secret.auto.tfvars and public.auto.tfvars are updated and correct for your environment (more explanations in the below sections about how to get the values)
3. Navigate in the terminal to the envs/dev environment - `cd envs/dev`
4. Run init script - `python3 ../../scripts/templates/init_templates.py`

After running the above steps you will have 'modules/templates' folder containing all of your template resources from your state ready to be managed in terraform.

**Important:** Run the initialization script on DEV only, not on other environments (for creating a new environment in terraform find the instructions below). Re-running it on DEV is safe - templates already managed are skipped.

## Updating a Template via Terraform

To update a specific template from terraform all you have to do is find the template you wish to update in the modules/templates folder, modify any attribute you wish move to the environment's folder (`cd envs/dev`) and run `terraform apply`

- Incase you want terraform to apply changes only for a specific module or a specific .tf file - 

* terraform apply -target=module.templates                                    (applies for all templates)
* terraform apply -target=module.templates.module.caregiver                    (applies for all caregiver templates)
* terraform apply -target=module.templates.module.caregiver.biot_template.nurse(applies only for the nurse.tf)

## Creating a New Template
It is possible to create new .tf file config with a new template but this may be very hard due to many attributes.
A simple solution for that is creating the template via the BioT Console portal and then generate it in terraform using the following python script:

1. Navigate to your dev env - `cd envs/dev`
2. Run in terminal - `python3 ../../scripts/templates/init_templates.py --type=<entity-type> --name=<template-name>`

Supported entity-types:

- patient
- caregiver
- organization-user
- organization
- device
- generic-entity
- command
- device-alert
- patient-alert
- usage-session
- registration-code

You can find now the template under the modules/template/<entity-type> folder.

**Important:** The method to create via console and auto-generate in terraform should only be used in DEV environment. Terraform resources should only be managed in terraform and you should never update a resource manually. (except for testing in your develop environment)

## Updating a Template via BioT Console and Sync Terraform with the Change

In some cases we want to update our template resource but not sure exactly how to do if from terraform. 
In this case you can change the template via the BioT Console portal and regenerate its .tf file from it:

1. Update the template via the console portal, e.g. add a new attribute.
2. In your terminal - `cd envs/dev`
3. In your terminal - `python3 ../../scripts/templates/init_templates.py --type=<entity-type> --name=<template-name> --refresh`

This method should only be used for development environments.

## Managing ABAC Actions, Conditions and Rules

ABAC objects are managed in the shared `modules/abac` module (`actions.tf`, `conditions.tf`, `rules.tf`) and imported with
the [ABAC scripts](#abac-scripts-scriptsabac). Run them from your dev env - `cd envs/dev`.

- **Import all existing ABAC objects** - `python3 ../../scripts/abac/init_abac.py`
- **Import one created via the BioT Console** - `python3 ../../scripts/abac/init_abac.py --type=<action|condition|rule> --id=<id>`
- **Update one changed via the BioT Console** - `python3 ../../scripts/abac/init_abac.py --type=<action|condition|rule> --id=<id> --refresh`

Run `terraform plan` afterwards - it should show no changes.

**Good to know:**
- Changing `id` destroys and recreates the object, so check the plan before applying.
- An action's or condition's `value` can't be changed once it exists - to switch it, give the object a new `id` as well.
- Built-in objects can be imported and updated, but not destroyed. To stop managing one, use a `removed` block with
  `lifecycle { destroy = false }` instead of just deleting its resource block.

This method should only be used for development environments.

---

## 📁 Project Structure

```
envs/
├── dev/                 # Development environment configuration
│   ├── main.tf          # Terraform entrypoint configuring the provider and resources
│   ├── public.auto.tfvars  # Public environment-specific variables (e.g., URLs)
│   ├── secret.auto.tfvars.example  # Example secrets file (should be renamed and gitignored - remove the .example from the file's name)
│   └── variables.tf     # Variable definitions used in this environment
├── staging/             # Optional: Staging environment configuration (similar structure to dev)
│   ├── main.tf
│   ├── public.auto.tfvars
│   ├── secret.auto.tfvars.example
│   └── variables.tf
└── prod/                # Optional: Production environment configuration (similar structure)
    ├── main.tf
    ├── public.auto.tfvars
    ├── secret.auto.tfvars.example
    └── variables.tf

modules/
└── templates/           # Terraform modules for different BioT template types
    ├── caregiver/       # Caregiver template module variations
    │   ├── caregiver-type1.tf
    │   ├── caregiver-type2.tf
    │   └── variables.tf
    ├── patient/         # Patient template module variations
    │   ├── patient-type1.tf
    │   └── variables.tf
    └── device/          # Device template module variations
        ├── device-type1.tf
        ├── device-type2.tf
        └── variables.tf
```

### `envs/dev/main.tf`

This `main.tf` acts as the entry point for managing BioT templates in the `dev` environment.

### `public.auto.tfvars`

This file contains **non-sensitive, environment-specific variables** that are safe to commit to your version control system.

- **Purpose:**  
  Store values that differ between environments (e.g., URLs or feature flags) but are **not secrets**.

- **Important:**  
  You **must update** the `biot_base_url` value to match the URL of your BioT environment, for example:

  ```hcl
  biot_base_url = "https://api.dev.yourproject.biot-med.com"

  You can get this information via console portal -> Technical Information (top right settings icon)

### `secret.auto.tfvars.example`

This is an **example file** showing how to provide your sensitive environment variables, such as service IDs and secret keys.

- **Important:**  
  Before using it, **remove the `.example` extension** to create `secret.auto.tfvars`.  
  This is the file Terraform will actually load to get your secrets.

- **Secrets:**  
  This file should contain sensitive information like:

  ```hcl
  biot_service_id         = "<your-service-id>"
  biot_service_secret_key = "<your-service-secret-key>"

Security:
The file without the .example suffix (secret.auto.tfvars) is already included in the project’s .gitignore file by default.

This means it will not be committed to version control, protecting your secrets.

It’s very important not to remove this entry from .gitignore.

If you decide to use a different filename for your secrets, make sure to add that filename to .gitignore as well, to keep your sensitive information safe.

---

# Modules

Modules form the core infrastructure of the project and are **shared across all environments**. This means the module code is the same whether you are working with `dev`, `staging`, or `prod`.

BioT's terraform provider currently supported modules: Templates.

## Template Module

Template module contains a `main.tf` file that includes several **child modules** such as:

- `caregiver/`
- `patient/`
- `device/`
- ...and others

These child modules represent different types of BioT templates.

Each child module contains multiple `.tf` files like `doctor.tf`, `nurse.tf`, etc. These files are where the actual template configurations are managed and defined.

Note that each module also has its own `provider.tf` and `variables.tf` files, which we will explain in detail later.

This modular design helps keep your template infrastructure organized, reusable, and consistent across all environments.

### Module: `provider.tf`

Each module contains its own `provider.tf` file where the **BioT provider** is defined.  

This ensures that the module is properly connected to the BioT API using the provider configuration passed from the environment’s main Terraform configuration.  

By defining the provider inside each module, we keep modules self-contained and able to interact with the BioT service independently.

---

### Module: `variables.tf`

The `variables.tf` file in each module declares the variables the module expects to receive.  

A key variable across all child template modules is a **map of BioT templates**. This map contains template IDs and related data that modules use dynamically instead of hardcoding values.  

Using this map allows the modules to work across different environments seamlessly, as each environment’s `main.tf` provides its own environment-specific map.  

In practice, the environment’s `main.tf` defines this templates map and passes it down to the template modules, which then pass it to specific child modules as needed.

This structure helps maintain flexibility and avoids environment-specific hardcoding, enabling smoother multi-environment support.

*Note: This map is generated automatically within the project — more details below.*

---

## Scripts

To simplify working with the BioT Terraform provider, this project includes several helper Python scripts.  
Each script should be run from within a specific environment folder (e.g., `envs/dev`, `envs/staging`, etc.) unless specified differently.

---

### Template scripts (`scripts/templates/`)

#### `init_templates.py`
Generates the `.tf` config for the templates in the current environment and imports them into its terraform state.

**Important:** use only on DEV. It creates infrastructure which is common for all envs - other environments should be managed by terraform only.

- **Usage:**
  ```bash
  cd envs/dev
  python3 ../../scripts/templates/init_templates.py                                    # every template not yet managed
  python3 ../../scripts/templates/init_templates.py --type=caregiver                   # only caregiver templates
  python3 ../../scripts/templates/init_templates.py --type=caregiver --name=nurse      # one template, e.g. created in the console
  python3 ../../scripts/templates/init_templates.py --type=caregiver --name=nurse --refresh   # changed in the console - regenerate its .tf file
  ```
- **Supported entity types:** patient, caregiver, organization-user, organization, device, generic-entity, command,
  device-alert, patient-alert, usage-session, registration-code
- **What it does:**
  - Fetches the templates from the BioT API (using the credentials and `biot_base_url` of the current environment).
  - Writes each one to `modules/templates/<type>/<template-name>.tf`, parents before their children.
  - Imports each template into the env's state.
  - Creates the `modules/templates/<type>` folders with their `providers.tf` and `variables.tf`, and adds the modules to
    `main.tf`, if missing.
  - Runs `generate_biot_templates_tfvars.py` to update `biot_templates_map`.
- Templates already in the state are skipped, so the script can be re-run at any time. A `.tf` file that exists without
  its template in the state is never overwritten - the script reports it instead. `--refresh` overwrites the `.tf` files of
  templates already managed with their current state in BioT.

#### `generate_template.py` (deprecated)
Use `init_templates.py --type=<type> --name=<template-name>` instead. Still works - it forwards to `init_templates.py` -
but will be removed in a future release.

#### `generate_biot_templates_tfvars.py`
Generates the `biot_templates_map` variable for the current environment.

- **Usage:**
  ```bash
  cd envs/dev
  python3 ../../scripts/templates/generate_biot_templates_tfvars.py
  ```
- **What it does:** reads your BioT credentials (from `secret.auto.tfvars`) and base URL (from `public.auto.tfvars`), fetches
  all existing templates for the current environment, and writes a `biot_templates_map` variable from them, so your
  configuration never hardcodes template IDs. The map is written to `biot_templates.auto.tfvars`; every env's `variables.tf`
  declares `biot_templates_map` with an empty default, so environments that don't manage templates (e.g. ABAC only) work without it.
- `init_templates.py` runs it automatically, so you only need it to refresh the map by hand.

#### `populate_tfstate.py`
Imports the templates defined in `modules/templates` into a new environment's state. `create_env.py` runs it automatically.

---

### ABAC scripts (`scripts/abac/`)

Manage ABAC actions, conditions and rules in terraform. Their `.tf` files are generated into a shared module, `modules/abac`
(`actions.tf`, `conditions.tf`, `rules.tf`), which every environment uses. Requires Terraform **1.14+** (`terraform query`).

#### `init_abac.py`
Generates the `.tf` config for the ABAC objects in the current environment and imports them into its terraform state.

**Important:** use only on DEV. Other environments should get their ABAC config through terraform.

- **Usage:**
  ```bash
  cd envs/dev
  python3 ../../scripts/abac/init_abac.py                                    # everything not yet managed
  python3 ../../scripts/abac/init_abac.py --type rule                        # only rules
  python3 ../../scripts/abac/init_abac.py --type rule --id <rule-id>         # one object, e.g. created in the console
  python3 ../../scripts/abac/init_abac.py --type rule --id <rule-id> --refresh   # changed in the console - regenerate its config
  ```
- **What it does:**
  - Finds the objects with `terraform query`, using a temporary `.tfquery.hcl` file it writes and deletes itself. Other
    `.tfquery.hcl` files in the env folder would change the results, so the script stops if it finds one.
  - Writes each one to `modules/abac/<type>s.tf`, named after its id (e.g. `ADD_SELF_ID_FILTER_ACTION` -> `add_self_id_filter_action`).
  - In rules, references the actions and conditions managed in the module instead of their id strings, so terraform creates them first.
  - Imports each object into the env's state.
  - Creates `modules/abac` and adds `module "abac"` to the env's `main.tf` if missing.
- Objects already in the state are skipped, so the script can be re-run at any time. `--refresh` overwrites the config of
  objects already managed with their current state in BioT.

#### `populate_abac_state.py`
Prepares an environment for its first `terraform apply` of `modules/abac`.

- **Usage:**
  ```bash
  cd envs/staging
  python3 ../../scripts/abac/populate_abac_state.py
  terraform apply
  ```
- **What it does:** imports the objects defined in `modules/abac` that already exist in this environment (e.g. the ones
  BioT ships), so `terraform apply` only creates what's missing instead of failing with "already exists".
- `create_env.py` runs it automatically when `modules/abac` exists.

---

### `create_env.py`

- Should be run from project's root folder.
- Creates new foldering structure with all required files for a new environment.

- **Usage:**
```bash
python3 scripts/create_env.py
```

---

### ⚠️ Destructive Changes Warning

The BioT Terraform provider includes built-in protection against **destructive changes** — changes that would result in data loss (e.g., deleting measurements)

#### 🛑 What happens:

When Terraform detects a destructive change during `terraform apply`, it will:

- **Block the operation**
- Show a clear **error message** explaining the issue
- Suggest how to continue if you're sure about the change

#### ✅ If you're sure you want to proceed:

You can **force the apply** by adding the `TF_FORCE_UPDATE=true` flag:

```bash
TF_FORCE_UPDATE=true terraform apply
```
⚠️ Use with caution!
This will apply changes that may lead to data loss. Always double-check before forcing.

## ➕ Creating a New Environment

To create a new environment (e.g., `staging`, `prod`, or any other), follow these steps:

In the project root folder:

```bash
python3 scripts/create_env.py
```

Insert env name / base_url / service id + secret (prompt in the CLI)

Your new environment is now set up and ready to use!

- **important**:
  - If any imports fail, a message listing all templates that failed to import will be displayed.
  - In case you change template name in previous environment the script will not be able to import that template to your new environment (since it's name does not match the previous name). In that case you will have to import the template manually as it is in the new environment:
  ```bash
  terraform import module.templates.module.<template-type>.biot_template.<template-name> <template-type>:<template-name>"
  ```

----------------------------------------------------------