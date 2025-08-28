
terraform {
  required_providers {
    biot = {
      // TODO: change to the real source.
      source  = "example.com/biot/biot"
      version = "1.0.0"
    }
  }
}

// TF_VAR_service_id=<your-service-id> TF_VAR_service_biot_service_secret_key=<your-service-secret-key> terraform <terraform-command>
provider "biot" {
  # base_url            = "https://api.dev.biot-gen2.biot-med.com"
  base_url            = "http://localhost:9999"
  service_id         = var.biot_service_id
  service_secret_key = var.biot_service_secret_key
}
module "command_templates" {
    source = "./modules/templates/command"
}
module "device-alert_templates" {
    source = "./modules/templates/device-alert"
}
module "patient_templates" {
    source = "./modules/templates/patient"
}
module "organization-user_templates" {
    source = "./modules/templates/organization-user"
}
module "usage-session_templates" {
    source = "./modules/templates/usage-session"
}
module "caregiver_templates" {
    source = "./modules/templates/caregiver"
}
module "registration-code_templates" {
    source = "./modules/templates/registration-code"
}
module "organization_templates" {
    source = "./modules/templates/organization"
}
module "device_templates" {
    source = "./modules/templates/device"
}
module "generic-entity_templates" {
    source = "./modules/templates/generic-entity"
}