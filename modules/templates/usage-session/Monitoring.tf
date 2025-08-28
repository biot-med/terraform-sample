resource "biot_template" "Monitoring" {
  analytics_db_configuration = {
    name = "Monitoring"
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
        referenced_side_attribute_display_name = "Usage Sessions to Device"
        referenced_side_attribute_name = "Usage Sessions to Device"
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
        name = "_initiator"
      }
      base_path = null
      category = "REGULAR"
      display_name = "Session Initiator"
      link_configuration = null
      name = "_initiator"
      numeric_meta_data = null
      phi = false
      reference_configuration = null
      selectable_values = [
        {
          display_name = "External"
          name = "EXTERNAL"
        },
        {
          display_name = "Remote Control"
          name = "REMOTE_CONTROL"
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
        referenced_side_attribute_display_name = "Usage Sessions to Organization"
        referenced_side_attribute_name = "Usage Sessions to Organization"
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
        name = "_patient"
      }
      base_path = null
      category = "REGULAR"
      display_name = "Patient"
      link_configuration = null
      name = "_patient"
      numeric_meta_data = null
      phi = false
      reference_configuration = {
        entity_type = "patient"
        referenced_side_attribute_display_name = "Usage Sessions to Patient"
        referenced_side_attribute_name = "Usage Sessions to Patient"
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
          display_name = "Activating"
          name = "ACTIVATING"
        },
        {
          display_name = "Active"
          name = "ACTIVE"
        },
        {
          display_name = "Done"
          name = "DONE"
        },
        {
          display_name = "Paused"
          name = "PAUSED"
        },
        {
          display_name = "Pausing"
          name = "PAUSING"
        },
        {
          display_name = "Resuming"
          name = "RESUMING"
        },
        {
          display_name = "Stopping"
          name = "STOPPING"
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
    {
      analytics_db_configuration = {
        name = "_summary._stopReason"
      }
      base_path = "_summary"
      category = "SUMMARY"
      display_name = "Stop Reason"
      link_configuration = null
      name = "_stopReason"
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
        name = "_summary._stopReasonCode"
      }
      base_path = "_summary"
      category = "SUMMARY"
      display_name = "Stop Reason Code"
      link_configuration = null
      name = "_stopReasonCode"
      numeric_meta_data = null
      phi = false
      reference_configuration = null
      selectable_values = [
        {
          display_name = "Completion"
          name = "COMPLETION"
        },
        {
          display_name = "General Device Error"
          name = "GENERAL_DEVICE_ERROR"
        },
        {
          display_name = "Timeout"
          name = "TIMEOUT"
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
  description = "Monitoring"
  display_name = "Monitoring"
  entity_type = "usage-session"
  name = "Monitoring"
  owner_organization_id = "00000000-0000-0000-0000-000000000000"
  parent_template_id = "95fe5241-cb15-4db5-b000-d7d7e02fff0d"
  template_attributes = [
    {
      base_path = null
      category = "REGULAR"
      display_name = "Required Measurement Interval"
      link_configuration = null
      name = "_requiredMeasurementIntervalMilliseconds"
      numeric_meta_data = {
        lower_range = null
        sub_type = null
        units = "Milliseconds"
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
          "value": 1000
        }
      )
    },
  ]
}

