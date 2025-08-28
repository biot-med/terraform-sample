resource "biot_template" "ben_test_1" {
  analytics_db_configuration = {
    name = "ben_test_1"
  }
  builtin_attributes = [
    {
      analytics_db_configuration = {
        name = "_clearDateTime"
      }
      base_path = null
      category = "REGULAR"
      display_name = "Clear Date Time"
      link_configuration = null
      name = "_clearDateTime"
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
        name = "_clearNotes"
      }
      base_path = null
      category = "REGULAR"
      display_name = "Clear Notes"
      link_configuration = null
      name = "_clearNotes"
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
        name = "_clearTrigger"
      }
      base_path = null
      category = "REGULAR"
      display_name = "Clear Trigger"
      link_configuration = null
      name = "_clearTrigger"
      numeric_meta_data = null
      phi = false
      reference_configuration = null
      selectable_values = [
        {
          display_name = "Automatic"
          name = "AUTOMATIC"
        },
        {
          display_name = "Manual"
          name = "MANUAL"
        },
      ]
      type = "SINGLE_SELECT"
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
        name = "_clearedBy"
      }
      base_path = null
      category = "REGULAR"
      display_name = "Cleared By"
      link_configuration = null
      name = "_clearedBy"
      numeric_meta_data = null
      phi = false
      reference_configuration = {
        entity_type = "organization-user"
        referenced_side_attribute_display_name = "ben-test-1 Cleared By To Alert"
        referenced_side_attribute_name = "ben-test-1 Cleared By To Alert"
        uniquely = false
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
        referenced_side_attribute_display_name = "ben-test-1 Device to Alert"
        referenced_side_attribute_name = "ben-test-1 Device to Alert"
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
        referenced_side_attribute_display_name = "ben-test-1 Device Alert to Organization"
        referenced_side_attribute_name = "ben-test-1 Device Alert to Organization"
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
        name = "_setDateTime"
      }
      base_path = null
      category = "REGULAR"
      display_name = "Set Date Time"
      link_configuration = null
      name = "_setDateTime"
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
        name = "_severity"
      }
      base_path = null
      category = "REGULAR"
      display_name = "Severity"
      link_configuration = null
      name = "_severity"
      numeric_meta_data = null
      phi = false
      reference_configuration = null
      selectable_values = [
        {
          display_name = "Critical"
          name = "CRITICAL"
        },
        {
          display_name = "Info"
          name = "INFO"
        },
        {
          display_name = "Major"
          name = "MAJOR"
        },
        {
          display_name = "Minor"
          name = "MINOR"
        },
      ]
      type = "SINGLE_SELECT"
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
          display_name = "Active"
          name = "ACTIVE"
        },
        {
          display_name = "Cleared"
          name = "CLEARED"
        },
        {
          display_name = "Suspended"
          name = "SUSPENDED"
        },
      ]
      type = "SINGLE_SELECT"
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
  description = "12"
  display_name = "ben-test-1"
  entity_type = "device-alert"
  name = "ben_test_1"
  owner_organization_id = "00000000-0000-0000-0000-000000000000"
  parent_template_id = "95fe5241-cb15-4db5-b000-d7d7e02fff0d"
  template_attributes = [
    {
      base_path = null
      category = "REGULAR"
      display_name = "Allow Multiple Open Alerts"
      link_configuration = null
      name = "_allowMultipleOpenAlerts"
      numeric_meta_data = null
      organization_selection = null
      phi = false
      reference_configuration = null
      selectable_values = [  ]
      type = "BOOLEAN"
      validation = {
        default_value = null
        mandatory = false
        max = null
        min = null
        regex = null
      }
      value_json = jsonencode(
        {
          "value": false
        }
      )
    },
  ]
}

