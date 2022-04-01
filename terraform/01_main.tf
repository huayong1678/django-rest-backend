terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
    # random = {
    #   source = "hashicorp/random"
    # }
    # archive = {
    #   source = "hashicorp/archive"
    # }
    # klayers = {
    #   source  = "ldcorentin/klayer"
    # }
  }
}

provider "aws" {
  region = var.aws_region
}
