
variable "biot_base_url" {
  type        = string
  description = "Your BIOT Base URL for the current environment"
}

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
  default     = {}
  description = "Map of template ids - filled in biot_templates.auto.tfvars by generate_biot_templates_tfvars.py"
}
