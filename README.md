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

## Main Flows

## First time initialize

After forking this project to initialize the terraform project and sync it with your current environment's state:

1. Remove 'example' from the secret.auto.tfvars.example file (the new name should be secret.auto.tfvars)
2. Make sure the values in both secret.auto.tfvars and public.auto.tfvars are updated and correct for your environment (more explanations in the below sections about how to get the values)
3. Navigate in the terminal to the envs/dev environment - `cd envs/dev`
4. Run init script - `python3 ../../scripts/init_templates.py`

After running the above steps you will have 'modules/templates' folder containing all of your template resources from your state ready to be managed in terraform.

**Important:** Initialization script can run only once per project and should not be run again even on different environment. (for creating new environment in terraform find the instructions below)

## Updating template via terraform

To update a specific template from terraform all you have to do is find the template you wish to update in the modules/templates folder, modify any attribute you wish and run `terraform apply`

## Creating new template

It is possible to create new .tf file config with a new template but this may be very hard due to many attributes. A simple solution for that is creating the template via the console portal and then generate it in terraform using the following python script:

1. Navigate to your dev env - `cd envs/dev`
2. Run in terminal - `python3 ../../scripts/generate_template.py`
3. The scripts will require you to type entity-type and template-name.

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

## Updating template via console and sync terraform with the change

In some cases we want to update our template resource but not sure exactly how to do from terraform. In this case you can change the template via the console portal and remove the resource management from terraform and auto-generating it again. Here are the steps how to do that:

1. Update the template via the console portal.
2. Remove the resource management from terraform:
   - Delete the relevant template's .tf file from the module/templates
   - In your terminal - `cd envs/dev`
   - In your terminal - `terraform state list`
   - Copy the template full path you wish from the state list (From above step) and run - `terraform state rm <paste-template-full-path>`
   - In your terminal - `python3 ../../scripts/generate_template.py` (more details in the previous title)

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
└── templates/           # Terraform modules for different BIOT template types
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

This `main.tf` acts as the entry point for managing BIOT templates in the `dev` environment.

### `public.auto.tfvars`

This file contains **non-sensitive, environment-specific variables** that are safe to commit to your version control system.

- **Purpose:**  
  Store values that differ between environments (e.g., URLs or feature flags) but are **not secrets**.

- **Important:**  
  You **must update** the `biot_base_url` value to match the URL of your BIOT environment, for example:

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

Biot's terraform provider currently supported modules: Templates.

## Template Module

Template module contains a `main.tf` file that includes several **child modules** such as:

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
Each script should be run from within a specific environment folder (e.g., `envs/dev`, `envs/staging`, etc.) unless specified differently.

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

- **Supported Template Types**:
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

- **Usage:**

  ```bash
  cd envs/dev
  python3 ../../scripts/generate_template.py --name=<template-name> --type=<template-type>
  ```

  example - python3 ../../scripts/generate_template.py --name=nurse --type=caregiver

- **Supported Template Types:**


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

### `create_env.py`

- Should be run from project's root folder.
- Creates new foldering structure with all required files for a new environment.

- **Usage:**
```bash
python3 scripts/create_env.py
```

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
terraform apply -target=module.templates                                      # applies for all templates.
terraform apply -target=module.templates.module.caregiver                     # applies for all caregiver templates
terraform apply -target=module.templates.module.caregiver.biot_template.nurse # applies only for the nurse.tf

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

    ```bash
    terraform state list
    ```

4. Remove the old template from state:

  ```bash
  terraform state rm biot_template.<template-name> # name from the above list
  ```

5. Delete the corresponding .tf file for the template:
  For example: rm modules/templates/caregiver/nurse.tf

Re-generate the template using the script:
```bash
python3 ../../scripts/generate_template.py --name=nurse --type=caregiver
```

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