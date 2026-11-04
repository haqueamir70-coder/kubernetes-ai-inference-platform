output "resource_group_name" {
  description = "Created resource group."
  value       = azurerm_resource_group.platform.name
}

output "virtual_network_id" {
  description = "Virtual network resource ID."
  value       = azurerm_virtual_network.platform.id
}

output "aks_subnet_id" {
  description = "Subnet ID reserved for AKS nodes."
  value       = azurerm_subnet.aks.id
}

output "aks_cluster_name" {
  description = "Name of the optional AKS cluster, null when enable_aks is false."
  value       = try(azurerm_kubernetes_cluster.platform[0].name, null)
}

output "aks_cluster_fqdn" {
  description = "FQDN of the optional AKS cluster, null when enable_aks is false."
  value       = try(azurerm_kubernetes_cluster.platform[0].fqdn, null)
}
