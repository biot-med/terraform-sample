

Prequisitions:
- Terraform version 1.5+
- Python 3.x+
- Service id + secret key. - <doc link>


** Mention all flows.
- Initialize
- Re-initialize - When you want to align your project with the cloud mostly after making manual changes
- Import specific tempalte
- Re-import specific template

- List of available entity-types





TODO:

- Read about modules
- Moduling best practices
- Multi environment best practices
- Do we want to encourge terraform to apply to all the resources ? or have main per module ? or ?????
- Make sure when we delete .tf file (meaning we want to delete the template) - if the template is already in use we display proper message and suggest how to continue...

- Moduling best practices
** Resuse
** maintain
** Clean
**** DO NOT - when you have only a few resources.


Multi environment:
- Have "env" folder and inside: dev / staging / prod folders
** Each folder contains terraform.vars
** Option1 - each folder contains it's own main.tf (HashiCorp Developer Docs recommend) - looks like for better isolation.
** Option2 - Have 1 main for all envs.


tf/
├── versions.tf
├── variables.tf
├── provider.tf
├── droplets.tf
├── dns.tf
└── external/
    └── name-generator.py

tf/
├── modules/
│   ├── network/
│   └── spaces/
└── applications/
    ├── backend-app/
    │   ├── env/
    │   │   ├── dev.tfvars
    │   │   └── production.tfvars
    │   └── main.tf
    └── frontend-app/
        └── ...

├── modules/
└── dev/
    ├── main.tf
    └── terraform.tfvars

infrastructure/
├── environments/
│   ├── com/
│   ├── pre/
│   ├── pro/
│   └── rev/
└── modules/
    ├── app/
    ├── db/
    └── queue/

terraform-project/
├── environments/
│   ├── dev/
│   ├── staging/
│   └── prod/
└── modules/
    ├── vpc/
    ├── ec2/
    └── rds/

