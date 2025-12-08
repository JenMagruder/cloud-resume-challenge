# DynamoDB Table for Visitor Counter
# Stores the visitor count for the cloud website

resource "aws_dynamodb_table" "visitor_counter" {
  name           = var.dynamodb_table_name
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "id"

  attribute {
    name = "id"
    type = "S"
  }

  tags = {
    Name        = "Cloud Resume Visitor Counter"
    Environment = "Production"
    ManagedBy   = "Terraform"
  }
}