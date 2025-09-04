
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
