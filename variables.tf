
variable "biot_service_id" {
  type        = string
  description = "Service ID"
}

variable "biot_service_secret_key" {
  type        = string
  description = "Service Secret Key"
  sensitive   = true
}