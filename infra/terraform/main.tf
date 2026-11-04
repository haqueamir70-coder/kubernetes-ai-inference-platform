resource "azurerm_resource_group" "platform" {
  name     = var.resource_group_name
  location = var.location
  tags = {
    project     = "kubernetes-ai-inference-platform"
    environment = var.environment
    managed_by  = "terraform"
  }
}

resource "azurerm_virtual_network" "platform" {
  name                = var.vnet_name
  location            = azurerm_resource_group.platform.location
  resource_group_name = azurerm_resource_group.platform.name
  address_space       = var.address_space
  tags = {
    project     = "kubernetes-ai-inference-platform"
    environment = var.environment
  }
}

resource "azurerm_subnet" "aks" {
  name                 = "snet-aks-nodes"
  resource_group_name  = azurerm_resource_group.platform.name
  virtual_network_name = azurerm_virtual_network.platform.name
  address_prefixes     = var.aks_subnet_prefixes
}

resource "azurerm_kubernetes_cluster" "platform" {
  count               = var.enable_aks ? 1 : 0
  name                = "aks-ai-inference-${var.environment}"
  location            = azurerm_resource_group.platform.location
  resource_group_name = azurerm_resource_group.platform.name
  dns_prefix          = var.aks_dns_prefix
  kubernetes_version  = null

  default_node_pool {
    name           = "system"
    node_count     = var.aks_node_count
    vm_size        = var.aks_vm_size
    vnet_subnet_id = azurerm_subnet.aks.id
    type           = "VirtualMachineScaleSets"
  }

  identity {
    type = "SystemAssigned"
  }

  network_profile {
    network_plugin    = "azure"
    network_policy    = "azure"
    load_balancer_sku = "standard"
  }

  tags = {
    project     = "kubernetes-ai-inference-platform"
    environment = var.environment
    managed_by  = "terraform"
  }
}
