# CloudFront Distribution for Website
# Provides global CDN, HTTPS, and custom domain

resource "aws_cloudfront_distribution" "website" {
  enabled             = true
  is_ipv6_enabled     = true
  http_version        = "http2"
  price_class         = "PriceClass_All"
  aliases             = [var.domain_name]
  
  origin {
    domain_name = "${var.bucket_name}.s3-website-${var.aws_region}.amazonaws.com"
    origin_id   = "${var.bucket_name}.s3.${var.aws_region}.amazonaws.com-mharunabktt"

    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "http-only"
      origin_ssl_protocols   = ["TLSv1.2", "TLSv1.1", "TLSv1", "SSLv3"]
    }
  }

  default_cache_behavior {
    allowed_methods        = ["GET", "HEAD"]
    cached_methods         = ["GET", "HEAD"]
    target_origin_id       = "${var.bucket_name}.s3.${var.aws_region}.amazonaws.com-mharunabktt"
    viewer_protocol_policy = "redirect-to-https"
    compress               = true
    
    cache_policy_id = "658327ea-f89d-4fab-a63d-7e88639e58f6"
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    acm_certificate_arn      = var.acm_certificate_arn
    ssl_support_method       = "sni-only"
    minimum_protocol_version = "TLSv1.2_2021"
  }

  logging_config {
    bucket = "${var.cloudfront_logs_bucket}.s3.amazonaws.com"
    prefix = ""
  }

  tags = {
    Name        = "Website Distribution"
    Environment = "Production"
    ManagedBy   = "Terraform"
  }
}