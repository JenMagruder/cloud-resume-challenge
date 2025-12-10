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
# S3 Bucket for CloudFront Logs
resource "aws_s3_bucket" "cloudfront_logs" {
  bucket = var.cloudfront_logs_bucket

  tags = {
    Name        = "CloudFront Access Logs"
    Environment = "Production"
    ManagedBy   = "Terraform"
  }
}

# Enable ACLs for CloudFront logging
resource "aws_s3_bucket_ownership_controls" "cloudfront_logs" {
  bucket = aws_s3_bucket.cloudfront_logs.id

  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_acl" "cloudfront_logs" {
  depends_on = [aws_s3_bucket_ownership_controls.cloudfront_logs]
  
  bucket = aws_s3_bucket.cloudfront_logs.id
  acl    = "log-delivery-write"
}