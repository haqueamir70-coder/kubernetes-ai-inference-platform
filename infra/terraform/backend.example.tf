# Configure an Azure Storage backend in a separate backend.tf file.
# Create the storage account/container out-of-band or through a bootstrap stack.
# Never commit access keys or SAS tokens. Prefer workload identity / OIDC.
#
# terraform {
#   backend "azurerm" {
#     resource_group_name  = "rg-terraform-state"
#     storage_account_name = "sttfstateexample"
#     container_name       = "tfstate"
#     key                  = "ai-inference/dev.tfstate"
#     use_oidc             = true
#   }
# }
