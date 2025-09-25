terraform {
  required_providers {
    biot = {
      // TODO: change to the real source.
      source  = "example.com/biot/biot"
      version = "1.0.0"
    }
  }
}

provider "biot" {
  base_url           = var.biot_base_url
  service_id         = var.biot_service_id
  service_secret_key = var.biot_service_secret_key
}