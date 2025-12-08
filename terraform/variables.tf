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

variable "dynamodb_table_name" {
  description = "DynamoDB table name for visitor counter"
  type        = string
}
variable "lambda_function_name" {
  description = "Lambda function name for visitor counter"
  type        = string
}

variable "lambda_zip_path" {
  description = "Path to Lambda deployment package (zip file)"
  type        = string
}