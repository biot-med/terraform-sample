resource "biot_template" "Organization" {
  analytics_db_configuration = {
    name = "Organization"
  }
  builtin_attributes = [
    {
      analytics_db_configuration = {
        name = "_creationTime"
      }
      base_path = null
      category = "REGULAR"
      display_name = "Creation Time"
      link_configuration = null
      name = "_creationTime"
      numeric_meta_data = null
      phi = false
      reference_configuration = null
      selectable_values = [  ]
      type = "DATE_TIME"
      validation = {
        default_value = null
        mandatory = false
        max = null
        min = null
        regex = null
      }
    },
    {
      analytics_db_configuration = {
        name = "_description"
      }
      base_path = null
      category = "REGULAR"
      display_name = "Description"
      link_configuration = null
      name = "_description"
      numeric_meta_data = null
      phi = false
      reference_configuration = null
      selectable_values = [  ]
      type = "PARAGRAPH"
      validation = {
        default_value = null
        mandatory = false
        max = null
        min = null
        regex = null
      }
    },
    {
      analytics_db_configuration = {
        name = "_headquarters"
      }
      base_path = null
      category = "REGULAR"
      display_name = "Headquarters"
      link_configuration = null
      name = "_headquarters"
      numeric_meta_data = null
      phi = false
      reference_configuration = null
      selectable_values = [  ]
      type = "ADDRESS"
      validation = {
        default_value = null
        mandatory = false
        max = null
        min = null
        regex = null
      }
    },
    {
      analytics_db_configuration = {
        name = "_lastModifiedTime"
      }
      base_path = null
      category = "REGULAR"
      display_name = "Last Modified Time"
      link_configuration = null
      name = "_lastModifiedTime"
      numeric_meta_data = null
      phi = false
      reference_configuration = null
      selectable_values = [  ]
      type = "DATE_TIME"
      validation = {
        default_value = null
        mandatory = false
        max = null
        min = null
        regex = null
      }
    },
    {
      analytics_db_configuration = {
        name = "_locale"
      }
      base_path = null
      category = "REGULAR"
      display_name = "Locale"
      link_configuration = null
      name = "_locale"
      numeric_meta_data = null
      phi = false
      reference_configuration = null
      selectable_values = [  ]
      type = "LOCALE"
      validation = {
        default_value = null
        mandatory = false
        max = null
        min = null
        regex = null
      }
    },
    {
      analytics_db_configuration = {
        name = "_name"
      }
      base_path = null
      category = "REGULAR"
      display_name = "Name"
      link_configuration = null
      name = "_name"
      numeric_meta_data = null
      phi = false
      reference_configuration = null
      selectable_values = [  ]
      type = "LABEL"
      validation = {
        default_value = null
        mandatory = true
        max = null
        min = null
        regex = null
      }
    },
    {
      analytics_db_configuration = {
        name = "_phone"
      }
      base_path = null
      category = "REGULAR"
      display_name = "Phone"
      link_configuration = null
      name = "_phone"
      numeric_meta_data = null
      phi = false
      reference_configuration = null
      selectable_values = [  ]
      type = "PHONE"
      validation = {
        default_value = null
        mandatory = false
        max = null
        min = null
        regex = null
      }
    },
    {
      analytics_db_configuration = {
        name = "_primaryAdministrator"
      }
      base_path = null
      category = "REGULAR"
      display_name = "Primary Administrator"
      link_configuration = null
      name = "_primaryAdministrator"
      numeric_meta_data = null
      phi = false
      reference_configuration = {
        entity_type = "organization-user"
        referenced_side_attribute_display_name = "Administered Organization"
        referenced_side_attribute_name = "Administered Organization"
        uniquely = true
        valid_templates_to_reference = [  ]
      }
      selectable_values = [  ]
      type = "REFERENCE"
      validation = {
        default_value = null
        mandatory = false
        max = null
        min = null
        regex = null
      }
    },
    {
      analytics_db_configuration = {
        name = "_timezone"
      }
      base_path = null
      category = "REGULAR"
      display_name = "Timezone"
      link_configuration = null
      name = "_timezone"
      numeric_meta_data = null
      phi = false
      reference_configuration = null
      selectable_values = [  ]
      type = "TIMEZONE"
      validation = {
        default_value = null
        mandatory = false
        max = null
        min = null
        regex = null
      }
    },
  ]
  custom_attributes = [  ]
  description = "Organization"
  display_name = "Organization"
  entity_type = "organization"
  name = "Organization"
  owner_organization_id = null
  parent_template_id = null
  template_attributes = [
  ]
}

