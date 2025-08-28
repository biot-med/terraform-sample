resource "biot_template" "deviceLogFile" {
  analytics_db_configuration = {
    name = "deviceLogFile"
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
        name = "_name"
      }
      base_path = null
      category = "REGULAR"
      display_name = "File Name"
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
        name = "_ownerOrganization"
      }
      base_path = null
      category = "REGULAR"
      display_name = "Owner Organization"
      link_configuration = null
      name = "_ownerOrganization"
      numeric_meta_data = null
      phi = false
      reference_configuration = {
        entity_type = "organization"
        referenced_side_attribute_display_name = "Generic-Entities"
        referenced_side_attribute_name = "Generic-Entities"
        uniquely = false
        valid_templates_to_reference = [  ]
      }
      selectable_values = [  ]
      type = "REFERENCE"
      validation = {
        default_value = null
        mandatory = true
        max = null
        min = null
        regex = null
      }
    },
  ]
  custom_attributes = [
    {
      analytics_db_configuration = {
        name = "device"
      }
      base_path = null
      category = "REGULAR"
      display_name = "Device"
      link_configuration = null
      name = "device"
      numeric_meta_data = null
      phi = false
      reference_configuration = {
        entity_type = "device"
        referenced_side_attribute_display_name = "Log Files"
        referenced_side_attribute_name = "Log Files"
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
        name = "endTime"
      }
      base_path = null
      category = "REGULAR"
      display_name = "End time"
      link_configuration = null
      name = "endTime"
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
        name = "file"
      }
      base_path = null
      category = "REGULAR"
      display_name = "File"
      link_configuration = null
      name = "file"
      numeric_meta_data = null
      phi = false
      reference_configuration = null
      selectable_values = [  ]
      type = "FILE"
      validation = {
        default_value = null
        mandatory = false
        max = 10000000
        min = null
        regex = null
      }
    },
    {
      analytics_db_configuration = {
        name = "startTime"
      }
      base_path = null
      category = "REGULAR"
      display_name = "Start time"
      link_configuration = null
      name = "startTime"
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
  ]
  description = "Device Log File"
  display_name = "Device Log File"
  entity_type = "generic-entity"
  name = "deviceLogFile"
  owner_organization_id = null
  parent_template_id = null
  template_attributes = [
  ]
}

