

Prequisitions:
- Terraform version 1.5+
- Python 3.x+
- Service id + secret key. - <doc link>

TODO:

- parentTemplateId - should use resource. and not hard coded ids
- Make sure when we delete .tf file (meaning we want to delete the template) - if the template is already in use we display proper message and suggest how to continue...
- List of available entity-types should be on our DOC
- Make attributes be on the bottom of the resource. (in generate)
- When trying to generate template with not exist type - need to delete the folder module.
- Make endpoint URL a variable and use it in the python scripts.t


terraform apply -target=module.templates

terraform apply -target=module.templates.module.device-alert

terraform apply -target=module.templates.module.device-alert.biot_template.ben_test_1
