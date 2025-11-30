# S3 Bucket for Static Website
# This bucket hosts the frontend HTML/CSS/JS files

resource "aws_s3_bucket" "website" {
  bucket = var.bucket_name
  
  tags = {
    Name        = "Cloud Resume Website"
    Environment = "Production"
    ManagedBy   = "Terraform"
  }
}

# S3 Bucket Website Configuration
resource "aws_s3_bucket_website_configuration" "website" {
  bucket = aws_s3_bucket.website.id

  index_document {
    suffix = "index.html"
  }

  error_document {
    key = "error.html"
  }
}