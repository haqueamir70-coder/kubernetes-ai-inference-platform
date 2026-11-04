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

variable "enable_aks" {
  description = "Whether to create an AKS cluster. Disabled by default to prevent unexpected Azure spend."
  type        = bool
  default     = false
}

variable "aks_dns_prefix" {
  description = "DNS prefix for the optional AKS cluster."
  type        = string
  default     = "ai-inference-dev"
}

variable "aks_node_count" {
  description = "Initial node count for the optional AKS cluster."
  type        = number
  default     = 2
}

variable "aks_vm_size" {
  description = "VM size for the optional AKS system node pool."
  type        = string
  default     = "Standard_D2s_v5"
}
