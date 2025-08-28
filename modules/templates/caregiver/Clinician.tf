resource "biot_template" "Clinician" {
  analytics_db_configuration = {
    name = "Clinician"
  }
  builtin_attributes = [
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
      phi = false
      reference_configuration = null
      selectable_values = [  ]
      type = "DATE"
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
        name = "_degree"
      }
      base_path = null
      category = "REGULAR"
      display_name = "Degree"
      link_configuration = null
      name = "_degree"
      numeric_meta_data = null
      phi = false
      reference_configuration = null
      selectable_values = [
        {
          display_name = "Clinical Nurse Specialists (CNS)"
          name = "CLINICAL_NURSE_SPECIALISTS"
        },
        {
          display_name = "Doctor of Osteopathy (DO)"
          name = "DOCTOR_OF_OSTEOPATHY"
        },
        {
          display_name = "Licensed Practical Nurse (LPN)"
          name = "LICENSED_PRACTICAL_NURSE"
        },
        {
          display_name = "Medical Assistant (MA)"
          name = "MEDICAL_ASSISTANT"
        },
        {
          display_name = "Medical Doctor (MD)"
          name = "MEDICAL_DOCTOR"
        },
        {
          display_name = "No Degree"
          name = "NO_DEGREE"
        },
        {
          display_name = "Nurse Practitioner (NP)"
          name = "NURSE_PRACTITIONER"
        },
        {
          display_name = "Other"
          name = "OTHER"
        },
        {
          display_name = "Physician Assistant (PA)"
          name = "PHYSICIAN_ASSISTANT"
        },
        {
          display_name = "Registered Nurse (RN)"
          name = "REGISTERED_NURSE"
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
        name = "_email"
      }
      base_path = null
      category = "REGULAR"
      display_name = "Email"
      link_configuration = null
      name = "_email"
      numeric_meta_data = null
      phi = false
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
        name = "_employeeId"
      }
      base_path = null
      category = "REGULAR"
      display_name = "Employee ID"
      link_configuration = null
      name = "_employeeId"
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
        name = "_mfa.enabled"
      }
      base_path = "_mfa"
      category = "REGULAR"
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
      category = "REGULAR"
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
      phi = false
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
        referenced_side_attribute_display_name = "Caregivers"
        referenced_side_attribute_name = "Caregivers"
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
  ]
  custom_attributes = [  ]
  description = "Clinician 1"
  display_name = "Clinician"
  entity_type = "caregiver"
  name = "Clinician"
  owner_organization_id = null
  parent_template_id = null
  template_attributes = [
  ]
}


