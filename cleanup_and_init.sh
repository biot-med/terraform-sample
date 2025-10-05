#!/bin/bash

# Remove the .terraform directory, .terraform.lock.hcl, and terraform.tfstate file
echo "Cleaning up Terraform files..."
rm -rf .terraform .terraform.lock.hcl terraform.tfstate templates

# Run terraform init to reinitialize the working directory
echo "Running terraform init..."
terraform init
