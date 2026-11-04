variable "location" {
  description = "Azure region for the example foundation."
  type        = string
  default     = "eastus"
}
variable "resource_group_name" {
  description = "Resource group name."
  type        = string
  default     = "rg-ai-inference-platform"
}
variable "vnet_name" {
  description = "Virtual network name."
  type        = string
  default     = "vnet-ai-inference"
}
variable "address_space" {
  description = "Virtual network address space."
  type        = list(string)
  default     = ["10.40.0.0/16"]
}
variable "aks_subnet_prefixes" {
  description = "Subnet prefixes reserved for an AKS node pool."
  type        = list(string)
  default     = ["10.40.1.0/24"]
}
variable "environment" {
  description = "Environment label."
  type        = string
  default     = "dev"
}
