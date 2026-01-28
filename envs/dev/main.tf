terraform {
  required_providers {
    biot = {
      source  = "registry.terraform.io/biot-med/biot-gen2"
      version = "1.0.3"
    }
  }
}

provider "biot" {
  base_url           = var.biot_base_url
  service_id         = var.biot_service_id
  service_secret_key = var.biot_service_secret_key
}