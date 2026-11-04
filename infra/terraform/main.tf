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
