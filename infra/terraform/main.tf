terraform {
  required_version = ">= 1.6.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region
}

variable "region" {
  type    = string
  default = "us-east-1"
}

variable "environment" {
  type    = string
  default = "demo"
}

locals {
  name_prefix = "enterprise-ai-${var.environment}"
}

resource "aws_s3_bucket" "raw_data" {
  bucket = "${local.name_prefix}-raw-data"
}

resource "aws_s3_bucket" "curated_data" {
  bucket = "${local.name_prefix}-curated-data"
}

resource "aws_ecr_repository" "model_images" {
  name = "${local.name_prefix}-model-images"
}

output "notes" {
  value = "Stub only: replace with your cloud, workspace, IAM, orchestration and secrets modules."
}
