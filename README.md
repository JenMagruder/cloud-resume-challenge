# Cloud Resume Challenge

A serverless resume website built on AWS with Infrastructure as Code using Terraform. Features remote state management, OIDC authentication, real-time visitor counter, automated CI/CD pipeline, and analytics system.

**Live Website:** [stratajen.net](https://stratajen.net)

**Built for:** Cloud Resume Challenge Cohort by Andrew Brown (December 2025)

---

## Table of Contents

- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Infrastructure as Code](#infrastructure-as-code)
- [Technologies](#technologies)
- [Project Structure](#project-structure)
- [Key Troubleshooting Scenarios](#key-troubleshooting-scenarios)
- [Lessons Learned](#lessons-learned)
- [Future Enhancements](#future-enhancements)
- [Contact](#contact)
- [Acknowledgments](#acknowledgments)

---

## Project Overview

This project demonstrates hands-on AWS experience through a production resume website. The infrastructure was originally built via AWS Console, then imported into Terraform with zero downtime to enable Infrastructure as Code management.

### What This Project Demonstrates

- Serverless architecture on AWS
- Infrastructure as Code with Terraform
- Zero-downtime migration strategy
- Secure CI/CD with OIDC authentication
- Remote state management
- Production troubleshooting and debugging

---

## Architecture

![Cloud Resume Architecture](images/cloud-resume-architecture.png)

The architecture consists of three main systems:

**Website Delivery:**
Static files hosted in S3, distributed via CloudFront CDN with custom domain (Route53) and SSL certificate (ACM).

**Visitor Counter:**
HTTP API (API Gateway) triggering Lambda function to atomically increment visitor count in DynamoDB.

**Analytics:**
EventBridge scheduler triggers Lambda function daily to query CloudFront logs via Athena, sending email reports via SNS.

**Deployment:**
GitHub Actions workflow uses OIDC authentication to run Terraform, managing all infrastructure with remote state stored in S3 and DynamoDB state locking.

---

## Infrastructure as Code

All infrastructure is managed with Terraform. See [terraform/README.md](terraform/README.md) for comprehensive documentation including:

- Remote state configuration
- OIDC authentication setup
- Resource definitions
- Deployment procedures

**Key Implementation Details:**

**Remote State Management:**
State stored in S3 bucket with versioning and encryption. DynamoDB table provides state locking to prevent concurrent modifications.

**OIDC Authentication:**
GitHub Actions authenticates via OIDC provider instead of long-lived access keys. Temporary credentials issued per workflow run with repository-restricted IAM role.

**Import Strategy:**
Existing Console-built resources imported into Terraform state to enable IaC management without recreation. Zero downtime maintained throughout migration.

---

## Technologies

**Infrastructure:**
- Terraform v1.13.5
- AWS Provider v5.100.0
- CloudFormation (for analytics Lambda)

**Languages:**
- Python 3.13 (Lambda functions)
- HTML/CSS/JavaScript (frontend)

**AWS Services:**
- Compute: Lambda
- Storage: S3, DynamoDB
- Networking: CloudFront, Route 53, API Gateway
- Security: ACM, IAM
- Analytics: Athena, SNS, EventBridge

**DevOps:**
- GitHub Actions
- OIDC authentication
- S3 remote backend
- DynamoDB state locking

---

## Project Structure

```
cloud-resume-challenge/
├── frontend/
│   ├── index.html
│   ├── styles.css
│   ├── script.js
│   └── blog/
│       ├── terraform.html
│       ├── journey.html
│       └── job-searcher.html
├── backend/
│   ├── lambda_function.py
│   └── lambda_function.zip
├── analytics/
│   └── analytics_lambda.py
├── terraform/
│   └── [See terraform/README.md for structure]
├── images/
│   └── Cloud-Resume-Architecture.png
├── .github/
│   └── workflows/
│       └── deploy.yml
└── README.md
```

---

## Key Troubleshooting Scenarios

### CloudFront Logging ACL Configuration

**Problem:** CloudFront logging failed due to S3 Public Access Block setting `IgnorePublicAcls = true` preventing ACL configuration.

**Solution:** Updated S3 Public Access Block to `IgnorePublicAcls = false` and configured bucket ownership controls in Terraform to enable CloudFront log delivery.

### IAM Role Import Path Mismatch

**Problem:** Terraform import command failed when attempting to import Lambda execution role using full ARN path.

**Solution:** Used only the role name for import command, then added `path = "/service-role/"` to Terraform resource definition to match existing configuration.

### S3 ACL Not Supported

**Problem:** S3 bucket ACL configuration failed because ACLs were disabled by default on the bucket.

**Solution:** Added `aws_s3_bucket_ownership_controls` resource with explicit dependency ordering using `depends_on` to ensure ownership controls were applied before ACL configuration.

---

## Lessons Learned

Importing existing resources into Terraform allowed zero-downtime migration, which was critical since my site was live and linked in active job applications. Most OIDC and remote state implementation details came from Discord community discussions rather than official documentation. IAM permissions took extra time to scope properly, but limiting each role to specific resources reduced security risk.

---

## Future Enhancements

- AWS Secrets Manager integration for analytics Lambda email credentials

---

## Contact

**Jennifer Magruder**

- Email: [strataspherejen@gmail.com](mailto:strataspherejen@gmail.com)
- LinkedIn: [jennifer-magruder](https://www.linkedin.com/in/jennifer-magruder)
- GitHub: [JenMagruder](https://github.com/JenMagruder)
- Website: [stratajen.net](https://stratajen.net)

---

## Acknowledgments

- [Forrest Brazeal](https://forrestbrazeal.com/) for creating the Cloud Resume Challenge
- [Andrew Brown](https://www.exampro.co/) for Cloud Resume Challenge cohort guidance and community support
- Cloud Resume Challenge Discord community for remote state and OIDC implementation tips
- AWS documentation and community