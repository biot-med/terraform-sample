terraform {
  required_version = ">= 1.14"

  required_providers {
    biot = {
      source  = "biot-med/biot-gen2"
      version = "1.1.0"
    }
  }
}

provider "biot" {
  base_url           = var.biot_base_url
  service_id         = var.biot_service_id
  service_secret_key = var.biot_service_secret_key
}
