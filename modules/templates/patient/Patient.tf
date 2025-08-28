resource "biot_template" "Patient" {
  analytics_db_configuration = {
    name = "Patient"
  }
  builtin_attributes = [
    {
      analytics_db_configuration = {
        name = "_additionalPhone"
      }
      base_path = null
      category = "REGULAR"
      display_name = "Additional Phone"
      link_configuration = null
      name = "_additionalPhone"
      numeric_meta_data = null
      phi = true
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
        name = "_address"
      }
      base_path = null
      category = "REGULAR"
      display_name = "Address"
      link_configuration = null
      name = "_address"
      numeric_meta_data = null
      phi = true
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
        name = "_canLogin"
      }
      base_path = null
      category = "LOGIN"
      display_name = "Can Login"
      link_configuration = null
      name = "_canLogin"
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
        name = "_caregiver"
      }
      base_path = null
      category = "REGULAR"
      display_name = "Caregiver"
      link_configuration = null
      name = "_caregiver"
      numeric_meta_data = null
      phi = false
      reference_configuration = {
        entity_type = "caregiver"
        referenced_side_attribute_display_name = "Patients"
        referenced_side_attribute_name = "Patients"
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
        name = "_dateOfBirth"
      }
      base_path = null
      category = "REGULAR"
      display_name = "Date of Birth"
      link_configuration = null
      name = "_dateOfBirth"
      numeric_meta_data = null
      phi = true
      reference_configuration = null
      selectable_values = [  ]
      type = "DATE"
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
        name = "_description"
      }
      base_path = null
      category = "REGULAR"
      display_name = "Description"
      link_configuration = null
      name = "_description"
      numeric_meta_data = null
      phi = true
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
        name = "_email"
      }
      base_path = null
      category = "REGULAR"
      display_name = "Email"
      link_configuration = null
      name = "_email"
      numeric_meta_data = null
      phi = true
      reference_configuration = null
      selectable_values = [  ]
      type = "EMAIL"
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
        name = "_enabled"
      }
      base_path = null
      category = "REGULAR"
      display_name = "Enabled"
      link_configuration = null
      name = "_enabled"
      numeric_meta_data = null
      phi = false
      reference_configuration = null
      selectable_values = [
        {
          display_name = "Disabled"
          name = "DISABLED"
        },
        {
          display_name = "Enabled"
          name = "ENABLED"
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
        name = "_gender"
      }
      base_path = null
      category = "REGULAR"
      display_name = "Gender"
      link_configuration = null
      name = "_gender"
      numeric_meta_data = null
      phi = false
      reference_configuration = null
      selectable_values = [
        {
          display_name = "Female"
          name = "FEMALE"
        },
        {
          display_name = "Male"
          name = "MALE"
        },
        {
          display_name = "Undisclosed"
          name = "UNDISCLOSED"
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
        name = "_mfa.enabled"
      }
      base_path = "_mfa"
      category = "LOGIN"
      display_name = "Login Using MFA"
      link_configuration = null
      name = "enabled"
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
        name = "_mfa.expirationInMinutes"
      }
      base_path = "_mfa"
      category = "LOGIN"
      display_name = "MFA Expiration Period"
      link_configuration = null
      name = "expirationInMinutes"
      numeric_meta_data = null
      phi = false
      reference_configuration = null
      selectable_values = [  ]
      type = "INTEGER"
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
      phi = true
      reference_configuration = null
      selectable_values = [  ]
      type = "NAME"
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
        name = "_nationalId"
      }
      base_path = null
      category = "REGULAR"
      display_name = "National ID"
      link_configuration = null
      name = "_nationalId"
      numeric_meta_data = null
      phi = true
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
        referenced_side_attribute_display_name = "Patients"
        referenced_side_attribute_name = "Patients"
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
        name = "_phone"
      }
      base_path = null
      category = "REGULAR"
      display_name = "Phone"
      link_configuration = null
      name = "_phone"
      numeric_meta_data = null
      phi = true
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
        name = "_registrationSource"
      }
      base_path = null
      category = "LOGIN"
      display_name = "Registration Source"
      link_configuration = null
      name = "_registrationSource"
      numeric_meta_data = null
      phi = false
      reference_configuration = null
      selectable_values = [
        {
          display_name = "Anonymous"
          name = "ANONYMOUS"
        },
        {
          display_name = "Invitation"
          name = "INVITATION"
        },
        {
          display_name = "Self"
          name = "SELF"
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
        name = "_username"
      }
      base_path = null
      category = "LOGIN"
      display_name = "Username"
      link_configuration = null
      name = "_username"
      numeric_meta_data = null
      phi = true
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
  ]
  custom_attributes = [  ]
  description = "Patient 12345"
  display_name = "Patient"
  entity_type = "patient"
  name = "Patient"
  owner_organization_id = null
  parent_template_id = null
  template_attributes = [
    {
      base_path = null
      category = "LOGIN"
      display_name = "Self Sign Up Methods"
      link_configuration = null
      name = "_signUpMethods"
      numeric_meta_data = null
      organization_selection = {
        all = false
        selected = null
      }
      phi = false
      reference_configuration = null
      selectable_values = [
        {
          display_name = "Anonymous"
          name = "ANONYMOUS"
        },
        {
          display_name = "Identified"
          name = "SELF"
        },
      ]
      type = "MULTI_SELECT"
      validation = {
        default_value = null
        mandatory = false
        max = null
        min = null
        regex = null
      }
      value_json = jsonencode(
        {
          "value": []
        }
      )
    },
  ]
}

