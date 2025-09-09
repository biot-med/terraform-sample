# BIOT Terraform Sample Project

This is a sample Terraform project for managing BIOT resources using the `biot` Terraform provider.

This repository is intended to manage Biot's resources for your own environments, such as `dev`, `staging`, or `prod`.
Currently supported resources: Templates.

---

## Prerequisites

Before using this project, make sure you have the following:

- **Terraform** version **1.5+** installed  
  [Terraform Installation Guide](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli)

- **Python** version **3.x+** installed  
  [Python Download and Installation](https://www.python.org/downloads/)

- **BIOT Service ID and Secret Key**  
  You will need valid credentials (service ID and secret key) to authenticate with the BIOT API.  
  See the [BIOT Service Credentials documentation](<doc link>) for details on how to obtain these.

---

## 📁 Project Structure

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
└── templates/           # Terraform modules for different BIOT template types
    ├── caregiver/       # Caregiver template module variations
    │   ├── caregiver-type1.tf
    │   ├── caregiver-type2.tf
    │   └── variables.tf
    ├── patient/         # Patient template module variations
    │   ├── patient-type1.tf
    │   ├── patient-type2.tf
    │   └── variables.tf
    └── device/          # Device template module variations
        ├── device-type1.tf
        ├── device-type2.tf
        └── variables.tf

### `envs/dev/main.tf`

This file contains the Terraform configuration to set up the BIOT provider and manage BIOT templates for the `dev` environment.

- **Provider Configuration:**  
  Configures the `biot` provider with required variables such as `biot_base_url`, `biot_service_id`, and `biot_service_secret_key`. These values are supplied via environment variables or `.auto.tfvars` files to separate secrets and environment-specific data from code.

- **Required Providers:**  
  Specifies the `biot` provider source and version, ensuring Terraform installs the correct provider plugin.

This `main.tf` acts as the entry point for managing BIOT templates in the `dev` environment.

### `public.auto.tfvars`

This file contains **non-sensitive, environment-specific variables** that are safe to commit to your version control system.

- **Purpose:**  
  Store values that differ between environments (e.g., URLs or feature flags) but are **not secrets**.

- **Important:**  
  You **must update** the `biot_base_url` value to match the URL of your BIOT environment, for example:

  ```hcl
  biot_base_url = "https://api.dev.yourproject.biot-med.com"

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

### `variables.tf`

This file defines all the input variables used in your Terraform configuration for the current environment.

- **Purpose:**  
  It declares the variables that the `main.tf` and other Terraform files reference, such as:

  - `biot_base_url`: The base URL for the BIOT API in this environment.
  - `biot_service_id`: Your service ID (used to authenticate).
  - `biot_service_secret_key`: The secret key for the service (marked as sensitive).
  - Other variables relevant to your templates or provider configuration.

- **Why it matters:**  
  Defining variables here allows you to keep your configuration modular and flexible, making it easier to manage different environments by simply changing variable values without editing code.

- **Sensitive Variables:**  
  Variables like `biot_service_secret_key` are marked as sensitive, so their values won't be shown in Terraform logs or output, helping to keep secrets safe.

Make sure to provide values for these variables through `.auto.tfvars` files or environment variables before running Terraform commands.

---

### Modules

Modules form the core infrastructure of the project and are **shared across all environments**. This means the module code is the same whether you are working with `dev`, `staging`, or `prod`.

At the top level, there is a **"template" module**, which contains a `main.tf` file that includes several **child modules** such as:

- `caregiver/`
- `patient/`
- `device/`
- ...and others

These child modules represent different types of BIOT templates.

Each child module contains multiple `.tf` files like `doctor.tf`, `nurse.tf`, etc. These files are where the actual template configurations are managed and defined.

Note that each module also has its own `provider.tf` and `variables.tf` files, which we will explain in detail later.

This modular design helps keep your template infrastructure organized, reusable, and consistent across all environments.

### Module: `provider.tf`

Each module contains its own `provider.tf` file where the **BIOT provider** is defined.  

This ensures that the module is properly connected to the BIOT API using the provider configuration passed from the environment’s main Terraform configuration.  

By defining the provider inside each module, we keep modules self-contained and able to interact with the BIOT service independently.

---

### Module: `variables.tf`

The `variables.tf` file in each module declares the variables the module expects to receive.  

A key variable across all child template modules is a **map of BIOT templates**. This map contains template IDs and related data that modules use dynamically instead of hardcoding values.  

Using this map allows the modules to work across different environments seamlessly, as each environment’s `main.tf` provides its own environment-specific map.  

In practice, the environment’s `main.tf` defines this templates map and passes it down to the template modules, which then pass it to specific child modules as needed.

This structure helps maintain flexibility and avoids environment-specific hardcoding, enabling smoother multi-environment support.

*Note: This map is generated automatically within the project — more details below.*

---

## Scripts

To simplify working with the BIOT Terraform provider, this project includes several helper Python scripts.  
Each script should be run from within a specific environment folder (e.g., `envs/dev`, `envs/staging`, etc.).

---

### `generate_biot_templates_tfvars.py`

Generates the `biot_templates_map` variable for the current environment.

- **Usage:**

  ```bash
  cd envs/dev
  python3 ../../scripts/generate_biot_templates_tfvars.py
  ```

- **What it does:**
This script reads your BIOT credentials (from secret.auto.tfvars) and base URL (from public.auto.tfvars),
connects to the BIOT API, and fetches all existing templates for the current environment.

It then generates a Terraform-compatible biot_templates_map variable based on the live data,
which can be used throughout your configuration without hardcoding template IDs.

You can use this script to update your environment's map if new templates was created, Also the other scripts
that generates .tf files for you will automatically update this map.

- **Important:**
If you’re using the init_templates.py or generate_template.py scripts (explained below), this script will run automatically — so you do not need to run it manually.

### `generate_template.py`

Creates a new `.tf` file for a specific BIOT template and updates the project structure accordingly.

- **Usage:**

  ```bash
  cd envs/dev
  python3 ../../scripts/generate_template.py --name=<template-name> --type=<template-type>
  ```

  example - python3 ../../scripts/generate_template.py --name=nurse --type=caregiver

- **Important:**
  The script will create the .tf file from the template of the specific env. it is suggested to use this only for dev
  and to manage other environments by terraform only.

- **What it does:**
  Creates the .tf file for the template at:
  modules/templates/<type>/<template-name>.tf

  Automatically creates:

  The modules/templates/<type>/ directory if it doesn’t exist.

  The required provider.tf and variables.tf files in the appropriate module folders (if missing).

  Calls generate_biot_templates_tfvars.py internally to update the biot_templates_map with the latest templates from the environment.

  Adds the template-type to the templates/main.tf module if missing and adds the templates module to the current env main.tf file if not exist there.

- **Why it's useful:**
  This script gives you a fast and consistent way to create template .tf config from the current backend state instaed.
  This way, you can create a template manually through our console and then generate it's .tf config file here.
   **Important:**: USE THIS METHOD ONLY FOR DEV. OTHER ENVIRONMENTS SHOULD BE MANAGED ONLY BY TERRAFORM.

### `init_templates.py`

Initializes the full templates infrastructure for the current environment by generating `.tf` files for **all existing templates**.

 **Important:** This script should only run on the DEV environment as it creates infrastructure which is common for all envs.

- **Usage:**

  ```bash
  cd envs/dev
  python3 ../../scripts/init_templates.py
  ```

- **What it does:**

  Automatically runs generate_template.py for each existing template retrieved from the BIOT API (based on credentials and biot_base_url in the current environment).

  Creates the full folder structure under modules/templates/, including:

  Individual <template-type>/<template-name>.tf files

  Required provider.tf and variables.tf files (if missing)

  Automatically runs generate_biot_templates_tfvars.py to update the biot_templates_map for the current environment.

- **Important:**

  This script is intended to be used once, when initializing a new environment.

  It will only run if there is no existing .tfstate file in the current environment folder — to avoid overwriting or duplicating infrastructure.

  Meant for bootstrapping your template setup when starting the project.

---

## 🛠️ Managing State, Imports & Targeted Applies

---

## 🔄 Updating a Template

To update an existing BIOT template:

1. **Edit the relevant `.tf` file** inside the appropriate module.  
   For example:

   ```bash
   modules/templates/caregiver/nurse.tf
   ```

2. Apply the changes by running Terraform from the environment where you want the update to take effect.
For example, from the dev environment:

cd envs/dev
terraform apply

That’s it — Terraform will detect the changes in the configuration and apply them to your BIOT environment.

- Incase you want terraform to apply changes only for a specific module or a specific .tf file - 
terraform apply -target=module.templates                        # applies for all templates.
terraform apply -target=module.templates.module.caregiver       # applies for all caregiver templates
terraform apply -target=module.templates.module.caregiver.nurse # applies only for the nurse.tf

---

### 🧪 Syncing Changes Made in the BIOT Console

If you've made changes directly in the **BIOT Console UI** and want to reflect those changes in your Terraform code, follow this process.

> ⚠️ **Recommended:** Perform these steps only in the **`dev`** environment to safely test changes before applying them elsewhere.

#### 🔁 Steps to Re-Import an Updated Template:

1. **Make changes** to the template in the BIOT Console.

2. In your terminal, go to the environment folder:

   ```bash
   cd envs/dev
   ```

3. View the current state to find the resource name:

  terraform state list

4. Remove the old template from state:

  terraform state rm biot_template.<template-name> # from the above list

5. Delete the corresponding .tf file for the template:
  For example: rm modules/templates/caregiver/nurse.tf

Re-generate the template using the script:

python3 ../../scripts/generate_template.py --name=nurse --type=caregiver

This process ensures your Terraform configuration reflects the latest version of the template from the BIOT environment.

---

### ⚠️ Destructive Changes Warning

The BIOT Terraform provider includes built-in protection against **destructive changes** — changes that would result in data loss (e.g., deleting measurements)

#### 🛑 What happens:

When Terraform detects a destructive change during `terraform apply`, it will:

- **Block the operation**
- Show a clear **error message** explaining the issue
- Suggest how to continue if you're sure about the change

#### ✅ If you're sure you want to proceed:

You can **force the apply** by adding the `--force=true` flag:

```bash
terraform apply --force=true
```
⚠️ Use with caution!
This will apply changes that may lead to data loss. Always double-check before forcing.

## ➕ Creating a New Environment

To create a new environment (e.g., `staging`, `prod`, or any other), follow these steps:

### 🪄 1. Copy an Existing Environment

Duplicate the `dev` environment folder:

```bash
cp -r envs/dev envs/<new-env-name>
```

Replace <new-env> with your desired environment name, such as staging or prod.

🛠️ 2. Update Environment Variables

Inside your new environment folder (envs/<new-env>), update the following files:

public.auto.tfvars
Update the biot_base_url to match your new environment's URL.

secret.auto.tfvars.example (rename and update)

Rename to secret.auto.tfvars (if not already).

Update with the correct biot_service_id and biot_service_secret_key for this environment.

✅ Note:
secret.auto.tfvars is already included in .gitignore by default to protect sensitive information.

🚀 3. Initialize

From your new environment folder:
  cd envs/<new-env>
  terraform init

Your new environment is now set up and ready to use!

----------------------------------------------------------

TODO:

- Make sure when we delete .tf file (meaning we want to delete the template) - if the template is already in use we display proper message and suggest how to continue...
- List of available entity-types should be on our DOC
