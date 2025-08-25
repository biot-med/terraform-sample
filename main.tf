
terraform {
  required_providers {
    biot = {
      source  = "example.com/biot/biot"
      version = "1.0.0"
    }
  }
}

provider "biot" {
  # base_url            = "https://api.dev.biot-gen2.biot-med.com"
  base_url            = "http://localhost:9999"
  service_id          = "880f301d-5924-4c6d-8cf3-29f6ae6393a9"
  service_secret_key  = "H1ekUDcOcjxLh9lkxXRY9pM3ql9zi2io"
}

# resource "biot_template" "DeviceType1" {
# }