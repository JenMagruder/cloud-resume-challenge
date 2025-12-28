# Cloud Resume Challenge

A serverless resume website built on AWS with complete Infrastructure as Code using Terraform, featuring remote state management, OIDC authentication, real-time visitor counter, automated CI/CD pipeline, and analytics system.

🌐 **Live Website:** [stratajen.net](https://stratajen.net)  
⚙️ **Infrastructure:** 100% managed with Terraform  
🔐 **Security:** OIDC authentication for GitHub Actions (no stored credentials)

---

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Architecture](#-architecture)
- [Infrastructure as Code (Terraform)](#️-infrastructure-as-code-terraform)
- [Technologies Used](#️-technologies-used)
- [Project Structure](#-project-structure)
- [Troubleshooting](#-troubleshooting)
- [Key Learnings](#-key-learnings)
- [Future Enhancements](#-future-enhancements)
- [Contact](#-contact)

---

## 📋 Project Overview

This project is my implementation of the [Cloud Resume Challenge](https://cloudresumechallenge.dev/), demonstrating hands-on experience with AWS services, Infrastructure as Code with Terraform, and DevOps practices.

**Built for:** [Cloud Resume Challenge Cohort](https://cloudresumechallenge.dev/) by Andrew Brown (December 2025)

**Infrastructure migration:** Console-built resources imported into Terraform with zero downtime, then enhanced with remote state management and OIDC authentication for secure CI/CD automation.

---

## 🏗️ Architecture

![Cloud Resume Architecture](images/cloud-resume-architecture.png)

### Frontend
- **S3** - Static website hosting
- **CloudFront** - CDN with HTTPS
- **Route 53** - Custom domain management
- **ACM** - SSL/TLS certificate
- **Blog** - Technical blog with Terraform migration post

### Backend (Visitor Counter)
- **API Gateway (HTTP API)** - RESTful endpoint
- **Lambda** - Python 3.13 function with atomic counter
- **DynamoDB** - Visitor count storage
- **IAM** - Least-privilege permissions

### Analytics System
- **CloudFront Access Logs** - Request logging
- **S3** - Log file storage
- **Athena** - SQL queries on log data
- **Lambda** - Daily analytics processing
- **SNS** - Email notification delivery
- **EventBridge** - Scheduled daily triggers (8am EST)

### CI/CD Pipeline
- **GitHub Actions** - Automated deployment workflow
- **OIDC Authentication** - Temporary credentials (no stored keys)
- **AWS CLI** - S3 sync and CloudFront invalidation
- **Terraform** - Infrastructure deployment automation

---

## ⚙️ Infrastructure as Code (Terraform)

All infrastructure is managed with Terraform v1.13.5, including remote state storage and OIDC authentication for GitHub Actions.

**📚 For comprehensive Terraform documentation, see [terraform/README.md](terraform/README.md)**

### Remote State Management

**S3 Backend:**
- State stored in `stratajen-terraform-state` bucket
- Encrypted with AES-256
- Versioning enabled for rollback capability
- Accessible by both local development and GitHub Actions

**DynamoDB State Locking:**
- Table: `terraform-state-lock`
- Prevents concurrent Terraform runs from corrupting state
- Pay-per-request billing (~$0.00/month)

### OIDC Authentication

**Secure GitHub Actions deployment:**
- No AWS access keys stored in GitHub Secrets
- Temporary credentials issued per workflow run (1-hour expiration)
- Least-privilege IAM role scoped to project resources only
- Repository-restricted authentication

**Components:**
- IAM OIDC identity provider (trusts GitHub)
- IAM role with assume role policy
- Scoped permissions (S3, Lambda, DynamoDB, CloudFront, Route53, API Gateway)

### Terraform Resources

#### **Remote State Infrastructure**
- `aws_s3_bucket.terraform_state` - Remote state storage
- `aws_s3_bucket_versioning.terraform_state` - State versioning
- `aws_s3_bucket_server_side_encryption_configuration.terraform_state` - AES-256 encryption
- `aws_s3_bucket_public_access_block.terraform_state` - Block all public access
- `aws_dynamodb_table.terraform_locks` - State locking table

#### **OIDC Authentication**
- `aws_iam_openid_connect_provider.github_actions` - GitHub OIDC provider
- `aws_iam_role.github_actions` - GitHub Actions role
- `aws_iam_role_policy.github_actions_terraform` - Least-privilege permissions

#### **Storage & Content Delivery**
- `aws_s3_bucket.website` - Static website bucket
- `aws_s3_bucket_website_configuration.website` - Website hosting config
- `aws_s3_bucket.cloudfront_logs` - CloudFront access logs bucket
- `aws_s3_bucket_ownership_controls.cloudfront_logs` - ACL configuration
- `aws_s3_bucket_acl.cloudfront_logs` - Log delivery permissions
- `aws_cloudfront_distribution.website` - CDN distribution

#### **DNS**
- `data.aws_route53_zone.main` - Hosted zone lookup
- `aws_route53_record.root` - A record for apex domain
- `aws_route53_record.www` - A record for www subdomain
- `aws_route53_record.cert_validation` - ACM certificate validation

#### **Backend**
- `aws_dynamodb_table.visitor_counter` - Visitor counter table
- `aws_lambda_function.visitor_counter` - Counter Lambda
- `aws_iam_role.lambda_role` - Lambda execution role
- `aws_iam_role_policy.lambda_dynamodb_policy` - Restricted DynamoDB access
- `aws_iam_role_policy_attachment.lambda_basic_execution` - CloudWatch logs

#### **API**
- `aws_apigatewayv2_api.visitor_counter` - HTTP API
- `aws_apigatewayv2_integration.lambda` - Lambda integration
- `aws_apigatewayv2_route.post` - POST /count route
- `aws_apigatewayv2_stage.default` - API stage
- `aws_lambda_permission.api_gateway` - API Gateway invoke permission

### Project Structure
```
terraform/
├── README.md                # Detailed Terraform documentation
├── backend.tf               # S3 backend configuration
├── remote-state-setup.tf    # S3 bucket + DynamoDB for state
├── oidc.tf                  # OIDC provider + IAM role
├── provider.tf              # AWS provider configuration
├── variables.tf             # Variable definitions
├── terraform.tfvars         # Variable values (gitignored)
├── s3.tf                    # S3 resources
├── dynamodb.tf              # DynamoDB table
├── lambda.tf                # Lambda function and IAM
├── apigateway.tf            # API Gateway resources
├── cloudfront.tf            # CloudFront distribution
├── route53.tf               # DNS records
└── .terraform.lock.hcl      # Provider version lock file
```

### Security Practices

**Secrets Protection:**
- Sensitive values in `terraform.tfvars` (gitignored)
- No hardcoded credentials or account IDs
- State file stored remotely in encrypted S3 bucket
- OIDC replaces long-lived access keys

**Least-Privilege IAM:**
- Lambda has ONLY UpdateItem + GetItem permissions
- Specific DynamoDB table access only
- GitHub Actions role scoped to project resources only
- Removed `AmazonDynamoDBFullAccess` managed policy

**Resource Tagging:**
- All resources tagged: Name, Environment, ManagedBy
- Enables cost tracking and management

---

## 🛠️ Technologies Used

**Frontend:**
- HTML5, CSS3, JavaScript
- Responsive design

**Backend:**
- Python 3.13
- Boto3 (AWS SDK)

**Infrastructure as Code:**
- Terraform v1.13.5
- AWS Provider v5.100.0
- S3 remote backend
- DynamoDB state locking

**AWS Services:**
- S3, CloudFront, Route 53, ACM
- Lambda, API Gateway, DynamoDB
- Athena, SNS, EventBridge
- IAM (including OIDC identity provider)

**DevOps:**
- GitHub Actions with OIDC authentication
- Git version control
- AWS CLI
- CI/CD automation

---

## 📁 Project Structure
```
cloud-resume-challenge/
├── frontend/
│   ├── index.html              # Resume website
│   ├── styles.css              # Styling
│   ├── script.js               # Visitor counter
│   └── blog/
│       └── terraform.html      # Terraform migration blog post
├── backend/
│   ├── lambda_function.py      # Visitor counter Lambda
│   └── lambda_function.zip     # Deployment package
├── analytics/
│   └── analytics_lambda.py     # Analytics Lambda
├── terraform/
│   ├── README.md               # Detailed Terraform docs
│   ├── backend.tf              # S3 backend config
│   ├── remote-state-setup.tf   # Remote state infrastructure
│   ├── oidc.tf                 # OIDC authentication
│   ├── provider.tf             # Provider config
│   ├── variables.tf            # Variables
│   ├── terraform.tfvars        # Values (gitignored)
│   ├── s3.tf                   # S3 resources
│   ├── dynamodb.tf             # DynamoDB
│   ├── lambda.tf               # Lambda + IAM
│   ├── apigateway.tf           # API Gateway
│   ├── cloudfront.tf           # CloudFront
│   └── route53.tf              # DNS
├── images/
│   └── Cloud-Resume-Architecture.png  # Architecture diagram
├── .github/
│   └── workflows/
│       └── deploy.yml          # CI/CD pipeline (OIDC)
└── README.md
```

---

## 🔧 Troubleshooting

### Error 1: CloudFront Logging ACL Configuration

**Error:**
```
Error: updating CloudFront Distribution (ELGFDIW5LH2XK): 
InvalidArgument: The S3 bucket that you specified for CloudFront logs 
does not enable ACL access: stratajen-cloudfront-logs.s3.amazonaws.com
```

**Cause:**  
S3 Public Access Block setting `IgnorePublicAcls = true` prevented CloudFront log delivery ACL from working.

**Solution:**
```bash
aws s3api put-public-access-block \
  --bucket stratajen-cloudfront-logs \
  --public-access-block-configuration \
  "BlockPublicAcls=true,IgnorePublicAcls=false,BlockPublicPolicy=true,RestrictPublicBuckets=true"
```

Then configured bucket ownership controls in Terraform.

---

### Error 2: IAM Role Import Path Mismatch

**Error:**
```
Error: reading IAM Role (service-role/visitor-counter-role-t3za3qyi): 
ValidationError: The specified value for roleName is invalid. 
It must contain only alphanumeric characters and/or the following: +=,.@_-
```

**Cause:**  
The `/` in `service-role/visitor-counter-role-t3za3qyi` is part of the ARN path, not the role name.

**Solution:**
1. Found actual role name:
```bash
aws lambda get-function --function-name visitor-counter --query 'Configuration.Role'
```

2. Imported with just the role name:
```bash
terraform import aws_iam_role.lambda_role visitor-counter-role-t3za3qyi
```

3. Added `path = "/service-role/"` to Terraform code

---

### Error 3: S3 ACL Not Supported

**Error:**
```
An error occurred (AccessControlListNotSupported) when calling the 
PutBucketAcl operation: The bucket does not allow ACLs
```

**Cause:**  
Default S3 bucket configuration blocked ACLs.

**Solution:**  
Configured ownership controls in Terraform:
```hcl
resource "aws_s3_bucket_ownership_controls" "cloudfront_logs" {
  bucket = aws_s3_bucket.cloudfront_logs.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}
```

---

## 📈 Key Learnings

- **Infrastructure as Code**: Migrated console-built AWS resources to Terraform with zero downtime
- **Remote State Management**: Implemented S3 backend with DynamoDB locking for team collaboration
- **OIDC Authentication**: Eliminated stored AWS credentials with temporary token-based authentication
- **Import Strategies**: Successfully imported existing AWS resources into Terraform state
- **Serverless Architecture**: Built scalable backend with Lambda and API Gateway
- **Security Best Practices**: Applied least-privilege IAM policies throughout infrastructure
- **CI/CD Automation**: Automated deployments with GitHub Actions and OIDC
- **Troubleshooting**: Debugged CloudFront ACL configuration and IAM role import issues
- **Community Learning**: Leveraged ExamPro Discord community for remote state and OIDC implementation guidance

---

## 🔮 Future Enhancements

- [ ] AWS Secrets Manager integration for analytics Lambda email credentials

---

## 📧 Contact

**Jennifer Magruder**

- 📧 Email: [strataspherejen@gmail.com](mailto:strataspherejen@gmail.com)
- 💼 LinkedIn: [jennifer-magruder](https://www.linkedin.com/in/jennifer-magruder)
- 💻 GitHub: [JenMagruder](https://github.com/JenMagruder)
- 🌐 Website: [stratajen.net](https://stratajen.net)

---

## 🙏 Acknowledgments

- [Forrest Brazeal](https://forrestbrazeal.com/) for creating the Cloud Resume Challenge
- [Andrew Brown](https://www.exampro.co/) for Cloud Resume Challenge cohort guidance and community support
- Cloud Resume Challenge Discord community for remote state and OIDC implementation tips
- AWS documentation and community

---

**⭐ If you found this project helpful, please consider giving it a star!**