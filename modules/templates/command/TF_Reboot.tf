resource "biot_template" "TF_Reboot" {
  analytics_db_configuration = {
    name = "TF_Reboot"
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
        name = "_device"
      }
      base_path = null
      category = "REGULAR"
      display_name = "Device"
      link_configuration = null
      name = "_device"
      numeric_meta_data = null
      phi = false
      reference_configuration = {
        entity_type = "device"
        referenced_side_attribute_display_name = "TF commands to Device"
        referenced_side_attribute_name = "TF commands to Device"
        uniquely = false
        valid_templates_to_reference = [ "95fe5241-cb15-4db5-b000-d7d7e02fff0d" ]
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
    {
      analytics_db_configuration = {
        name = "_endTime"
      }
      base_path = null
      category = "REGULAR"
      display_name = "End Time"
      link_configuration = null
      name = "_endTime"
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
        name = "_errorMessage"
      }
      base_path = null
      category = "REGULAR"
      display_name = "Error Message"
      link_configuration = null
      name = "_errorMessage"
      numeric_meta_data = null
      phi = false
      reference_configuration = null
      selectable_values = [  ]
      type = "LABEL"
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
        mandatory = false
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
        referenced_side_attribute_display_name = "TF Commands to Organization"
        referenced_side_attribute_name = "TF Commands to Organization"
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
    {
      analytics_db_configuration = {
        name = "_startTime"
      }
      base_path = null
      category = "REGULAR"
      display_name = "Start Time"
      link_configuration = null
      name = "_startTime"
      numeric_meta_data = null
      phi = false
      reference_configuration = null
      selectable_values = [  ]
      type = "DATE_TIME"
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
        name = "_state"
      }
      base_path = null
      category = "REGULAR"
      display_name = "State"
      link_configuration = null
      name = "_state"
      numeric_meta_data = null
      phi = false
      reference_configuration = null
      selectable_values = [
        {
          display_name = "Aborted"
          name = "ABORTED"
        },
        {
          display_name = "Completed"
          name = "COMPLETED"
        },
        {
          display_name = "Failed"
          name = "FAILED"
        },
        {
          display_name = "In Progress"
          name = "IN_PROGRESS"
        },
        {
          display_name = "Starting"
          name = "STARTING"
        },
        {
          display_name = "Stopping"
          name = "STOPPING"
        },
        {
          display_name = "Timeout"
          name = "TIMEOUT"
        },
      ]
      type = "SINGLE_SELECT"
      validation = {
        default_value = null
        mandatory = true
        max = null
        min = null
        regex = null
      }
    },
  ]
  custom_attributes = [  ]
  description = "TF Reboot"
  display_name = "TF Reboot"
  entity_type = "command"
  name = "TF_Reboot"
  owner_organization_id = "00000000-0000-0000-0000-000000000000"
  parent_template_id = "95fe5241-cb15-4db5-b000-d7d7e02fff0d"
  template_attributes = [
    {
      base_path = null
      category = "REGULAR"
      display_name = "Support Stop"
      link_configuration = null
      name = "_supportStop"
      numeric_meta_data = {
        lower_range = null
        sub_type = null
        units = "Seconds"
        upper_range = null
      }
      organization_selection = null
      phi = false
      reference_configuration = null
      selectable_values = [  ]
      type = "BOOLEAN"
      validation = {
        default_value = null
        mandatory = true
        max = null
        min = null
        regex = null
      }
      value_json = jsonencode(
        {
          "value": true
        }
      )
    },
    {
      base_path = null
      category = "REGULAR"
      display_name = "Timeout In Seconds"
      link_configuration = null
      name = "_timeoutInSeconds"
      numeric_meta_data = {
        lower_range = null
        sub_type = null
        units = "Seconds"
        upper_range = null
      }
      organization_selection = null
      phi = false
      reference_configuration = null
      selectable_values = [  ]
      type = "INTEGER"
      validation = {
        default_value = null
        mandatory = true
        max = null
        min = 1
        regex = null
      }
      value_json = jsonencode(
        {
          "value": 10
        }
      )
    },
  ]
}

