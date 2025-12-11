# Route 53 Hosted Zone for Domain
# Manages DNS records for stratajen.net

data "aws_route53_zone" "main" {
  name = var.domain_name
}

# A Record - Root Domain to CloudFront
resource "aws_route53_record" "root" {
  zone_id = data.aws_route53_zone.main.zone_id
  name    = var.domain_name
  type    = "A"

  alias {
    name                   = aws_cloudfront_distribution.website.domain_name
    zone_id                = aws_cloudfront_distribution.website.hosted_zone_id
    evaluate_target_health = false
  }
}

# A Record - WWW Subdomain to CloudFront
resource "aws_route53_record" "www" {
  zone_id = data.aws_route53_zone.main.zone_id
  name    = "www.${var.domain_name}"
  type    = "A"

  alias {
    name                   = aws_cloudfront_distribution.website.domain_name
    zone_id                = aws_cloudfront_distribution.website.hosted_zone_id
    evaluate_target_health = false
  }
}

# ACM Certificate Validation Record
resource "aws_route53_record" "cert_validation" {
  zone_id = data.aws_route53_zone.main.zone_id
  name    = "_b787500195ae5af936bd9e2d3158d50d.stratajen.net."
  type    = "CNAME"
  ttl     = 300
  records = ["_3f64fe2dfe15b7a4c769d43811cd54aa.jkddzztszm.acm-validations.aws."]
}