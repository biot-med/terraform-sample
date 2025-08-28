resource "biot_template" "DeviceType1" {
  analytics_db_configuration = {
    name = "DeviceType1"
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
        name = "_id"
      }
      base_path = null
      category = "REGULAR"
      display_name = "Unique ID"
      link_configuration = null
      name = "_id"
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
        referenced_side_attribute_display_name = "Devices"
        referenced_side_attribute_name = "Devices"
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
        referenced_side_attribute_display_name = "Device"
        referenced_side_attribute_name = "Device"
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
        name = "_registrationCode"
      }
      base_path = null
      category = "REGULAR"
      display_name = "Registration Code"
      link_configuration = null
      name = "_registrationCode"
      numeric_meta_data = null
      phi = false
      reference_configuration = {
        entity_type = "registration-code"
        referenced_side_attribute_display_name = "Registration Code Devices"
        referenced_side_attribute_name = "Registration Code Devices"
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
        name = "_status._bootTime"
      }
      base_path = "_status"
      category = "STATUS"
      display_name = "Boot Time"
      link_configuration = null
      name = "_bootTime"
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
        name = "_status._certificateStatus"
      }
      base_path = "_status"
      category = "STATUS"
      display_name = "Certificate Status"
      link_configuration = null
      name = "_certificateStatus"
      numeric_meta_data = null
      phi = false
      reference_configuration = null
      selectable_values = [
        {
          display_name = "Bootstrap"
          name = "BOOTSTRAP"
        },
        {
          display_name = "Not installed"
          name = "NOT_INSTALLED"
        },
        {
          display_name = "Permanent"
          name = "PERMANENT"
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
        name = "_status._connection._connected"
      }
      base_path = "_status._connection"
      category = "STATUS"
      display_name = "Connected"
      link_configuration = null
      name = "_connected"
      numeric_meta_data = null
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
    },
    {
      analytics_db_configuration = {
        name = "_status._connection._ipAddress"
      }
      base_path = "_status._connection"
      category = "STATUS"
      display_name = "IP Address"
      link_configuration = null
      name = "_ipAddress"
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
        name = "_status._connection._lastConnectedTime"
      }
      base_path = "_status._connection"
      category = "STATUS"
      display_name = "Last Connected Time"
      link_configuration = null
      name = "_lastConnectedTime"
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
        name = "_status._fwVersion"
      }
      base_path = "_status"
      category = "STATUS"
      display_name = "FW Version"
      link_configuration = null
      name = "_fwVersion"
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
        name = "_status._hwVersion"
      }
      base_path = "_status"
      category = "STATUS"
      display_name = "HW Version"
      link_configuration = null
      name = "_hwVersion"
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
        name = "_status._operational._message"
      }
      base_path = "_status._operational"
      category = "STATUS"
      display_name = "Operational Message"
      link_configuration = null
      name = "_message"
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
        name = "_status._operational._status"
      }
      base_path = "_status._operational"
      category = "STATUS"
      display_name = "Operational Status"
      link_configuration = null
      name = "_status"
      numeric_meta_data = null
      phi = false
      reference_configuration = null
      selectable_values = [
        {
          display_name = "Critical"
          name = "CRITICAL"
        },
        {
          display_name = "Major"
          name = "MAJOR"
        },
        {
          display_name = "Minor"
          name = "MINOR"
        },
        {
          display_name = "OK"
          name = "OK"
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
        name = "_timezone"
      }
      base_path = null
      category = "REGULAR"
      display_name = "Time Zone"
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
  description = "Default Device Template 1"
  display_name = "DeviceType1"
  entity_type = "device"
  name = "DeviceType1"
  owner_organization_id = null
  parent_template_id = null
  template_attributes = [
  ]
}

