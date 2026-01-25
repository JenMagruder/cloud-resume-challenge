# Terraform Infrastructure

This directory contains Terraform configuration managing the Cloud Resume Challenge AWS infrastructure.

## What's Managed

**Website Delivery:**
- S3 buckets (website hosting, CloudFront logs)
- CloudFront distribution
- Route53 DNS records
- ACM SSL certificate

**Visitor Counter:**
- API Gateway HTTP API
- Lambda function (Python 3.13)
- DynamoDB table
- IAM execution role

**Deployment Infrastructure:**
- S3 remote state bucket
- DynamoDB state lock table
- IAM OIDC provider for GitHub Actions
- IAM role for GitHub Actions with scoped permissions

**Current State:**
- 3 S3 buckets
- 1 CloudFront distribution
- 1 Lambda function
- 2 DynamoDB tables
- 1 API Gateway
- Route53 records
- IAM roles and policies

---

## Project Structure

```
terraform/
├── README.md                    # This file
├── screenshots/                 # Documentation images
│   ├── terraforminit.png
│   ├── counterimportedterraform.png
│   ├── counterapplyterraform.png
│   ├── terraformoidcapply.png
│   ├── dynamdbterraform.png
│   └── terraformcommits3.png
├── backend.tf                   # S3 backend configuration
├── remote-state-setup.tf        # S3 bucket + DynamoDB for state
├── oidc.tf                      # OIDC provider + IAM role
├── provider.tf                  # AWS provider configuration
├── variables.tf                 # Variable definitions
├── terraform.tfvars             # Variable values (gitignored)
├── s3.tf                        # S3 resources
├── dynamodb.tf                  # DynamoDB table
├── lambda.tf                    # Lambda function and IAM
├── apigateway.tf                # API Gateway resources
├── cloudfront.tf                # CloudFront distribution
├── route53.tf                   # DNS records
└── .terraform.lock.hcl          # Provider version lock file
```

---

## Remote State Configuration

### S3 Backend

State stored in `stratajen-terraform-state` bucket with AES-256 encryption and versioning enabled. Separate bucket used for security isolation from website content bucket.

Configuration in `backend.tf`:
```hcl
terraform {
  backend "s3" {
    bucket         = "stratajen-terraform-state"
    key            = "cloud-resume/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
  }
}
```

### State Locking

DynamoDB table `terraform-state-lock` provides state locking to prevent concurrent Terraform operations from corrupting state. Table uses pay-per-request billing mode.

### Bootstrap Process

Remote state infrastructure requires two-step setup:

**Step 1:** Create S3 bucket and DynamoDB table using local state (backend configuration commented out)
```bash
terraform init
terraform apply
```

**Step 2:** Migrate local state to S3
```bash
# Uncomment backend configuration in backend.tf
terraform init -migrate-state
```

---

## OIDC Authentication

GitHub Actions authenticates via OIDC provider instead of long-lived access keys. Configuration creates IAM OIDC identity provider trusting GitHub's token service and IAM role with assume role policy restricted to specific repository.

### Trust Policy

Role can only be assumed by workflows running in `JenMagruder/cloud-resume-challenge` repository:

```hcl
Condition = {
  StringEquals = {
    "token.actions.githubusercontent.com:aud" = "sts.amazonaws.com"
  }
  StringLike = {
    "token.actions.githubusercontent.com:sub" = "repo:JenMagruder/cloud-resume-challenge:*"
  }
}
```

### Permissions

IAM policy scoped to project resources only:

- S3 buckets: `stratajen.net*`, `stratajen-cloudfront-logs`, `stratajen-terraform-state`
- Lambda: `visitor-counter*`
- DynamoDB: `cloud-resume-visitor-counter`, `terraform-state-lock`
- CloudFront, Route53, API Gateway, ACM: necessary permissions for infrastructure management

### GitHub Actions Integration

Workflow uses `aws-actions/configure-aws-credentials@v4` action with `role-to-assume` parameter. Temporary credentials issued per workflow run, expiring after 1 hour.

---

## Import Strategy

Existing Console-built resources imported into Terraform state rather than recreated. Zero downtime maintained throughout migration process.

Import process for each resource:
1. Write Terraform configuration matching existing resource
2. Run `terraform import` command with resource ID
3. Verify with `terraform plan` showing no changes

Critical for live production infrastructure where recreation would cause service interruption.

---

## Common Issues and Solutions

### CloudFront Logging ACL Configuration

**Problem:** CloudFront logging requires ACL permissions but S3 Public Access Block setting `IgnorePublicAcls = true` prevented ACL configuration.

**Solution:** Updated Public Access Block to `IgnorePublicAcls = false` and configured bucket ownership controls before setting ACL.

### IAM Role Import Path

**Problem:** IAM role ARN includes path (`/service-role/`) but import command expects role name only.

**Solution:** Import with role name, add `path` attribute to Terraform resource to match existing configuration.

### S3 ACL Not Supported

**Problem:** S3 bucket ACL configuration failed because ACLs disabled by default.

**Solution:** Added `aws_s3_bucket_ownership_controls` resource with `depends_on` to ensure ordering.

---

## Deployment Workflow

**Local development:**
```bash
terraform init
terraform plan
terraform apply
```

**Automated deployment:**
GitHub Actions workflow triggered on push to main branch. Workflow:
1. Authenticates via OIDC
2. Initializes Terraform with S3 backend
3. Plans infrastructure changes
4. Applies changes if approved
5. Syncs frontend files to S3
6. Invalidates CloudFront cache

---

## Variables

Configuration uses variables for environment-specific values. Variable definitions in `variables.tf`, values in `terraform.tfvars` (gitignored).

Required variables:
- `domain_name` - Custom domain for website
- `route53_zone_id` - Hosted zone ID for DNS records
- `aws_region` - AWS region for resources

---

## Security Practices

**Secrets Management:**
Sensitive values in `terraform.tfvars` (gitignored). No hardcoded credentials in configuration files.

**Least Privilege:**
IAM roles scoped to minimum necessary permissions. Lambda execution role has only DynamoDB UpdateItem and GetItem permissions for specific table.

**State Encryption:**
State file encrypted at rest in S3. Contains resource IDs and configuration but no sensitive credentials.

**Resource Tagging:**
All resources tagged with Name, Environment, and ManagedBy for cost tracking and management.

---

## References

- **Terraform: Up and Running** by Yevgeniy Brikman - Comprehensive guide to Terraform best practices, remote state, and production workflows
- [Terraform S3 Backend Documentation](https://developer.hashicorp.com/terraform/language/settings/backends/s3)
- [GitHub Actions OIDC with AWS](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services)
- [AWS IAM OIDC Identity Providers](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc.html)
- [Terraform Import Documentation](https://developer.hashicorp.com/terraform/cli/import)