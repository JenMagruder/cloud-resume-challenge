# Variables for Cloud Resume Challenge Infrastructure
# Actual values are stored in terraform.tfvars (not committed to GitHub)

variable "bucket_name" {
  description = "S3 bucket name for static website"
  type        = string
}

variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-east-1"
}