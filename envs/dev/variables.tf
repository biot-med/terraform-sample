
variable "biot_service_id" {
  type        = string
  description = "Service ID"
}

variable "biot_service_secret_key" {
  type        = string
  description = "Service Secret Key"
  sensitive   = true
}

variable "biot_templates_map" {
  type        = map(any)
  description = "Map of template ids"
}