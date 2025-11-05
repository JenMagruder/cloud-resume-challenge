# Cloud Resume Challenge

A serverless resume website built on AWS, featuring a real-time visitor counter, automated CI/CD deployment pipeline, and comprehensive analytics system.

🌐 **Live Website:** [stratajen.net](https://stratajen.net)
📝 **Blog Post:** [Read about my experience on Medium](https://medium.com/@stratajen)

---

## 📋 Project Overview

This project is my implementation of the [Cloud Resume Challenge](https://cloudresumechallenge.dev/), demonstrating hands-on experience with AWS services, serverless architecture, DevOps practices, and data analytics.

---

## 🏗️ Architecture

### Frontend
- **S3** - Static website hosting
- **CloudFront** - CDN with HTTPS
- **Route 53** - Custom domain management
- **ACM** - SSL/TLS certificate

### Backend (Visitor Counter)
- **API Gateway** - RESTful API endpoint
- **Lambda** - Python function with atomic counter logic
- **DynamoDB** - Visitor count storage
- **CORS** - Cross-origin resource sharing configuration

### Analytics System
- **CloudFront Access Logs** - Real-time request logging
- **S3** - Log file storage
- **Athena** - SQL queries on log data
- **Lambda** - Daily analytics processing
- **SNS** - Email notification delivery
- **EventBridge** - Scheduled daily triggers (8am EST)

### CI/CD Pipeline
- **GitHub Actions** - Automated deployment workflow
- **AWS CLI** - S3 sync and CloudFront invalidation
- **GitHub Secrets** - Secure credential management

---

## 📊 Analytics Features

The automated analytics system provides daily insights:

- **Traffic Overview**: Total visits, unique visitors, days tracked
- **Daily Reports**: Yesterday's traffic breakdown
- **Page Analytics**: Most visited pages
- **Geographic Distribution**: Visitor locations via CloudFront edge locations
- **Visitor Tracking**: Top IP addresses (with personal IPs filtered)

**Email Reports Delivered Daily at 8:00 AM EST**

### Analytics Architecture Flow
```
CloudFront Access Logs → S3 Bucket → Athena SQL Queries → Lambda Function → SNS Email → Daily Report
                                            ↑
                                      EventBridge Scheduler
                                      (Triggers at 8am EST)
```

---

## 🛠️ Technologies Used

**Frontend:**
- HTML5, CSS3, JavaScript
- Responsive design

**Backend:**
- Python 3.13
- Boto3 (AWS SDK)
- JSON data handling

**AWS Services:**
- S3, CloudFront, Route 53, ACM
- Lambda, API Gateway, DynamoDB
- Athena, SNS, EventBridge
- IAM (Identity and Access Management)

**DevOps:**
- GitHub Actions
- Infrastructure as Code principles
- Automated testing and deployment

---

## 📁 Project Structure

```
cloud-resume-challenge/
├── frontend/
│   ├── index.html          # Resume website
│   ├── styles.css          # Styling
│   └── script.js           # Visitor counter JavaScript
├── backend/
│   └── lambda_function.py  # Visitor counter Lambda
├── analytics/
│   └── analytics_lambda.py # Analytics Lambda function
├── .github/
│   └── workflows/
│       └── deploy.yml      # CI/CD pipeline
└── README.md
```

---

## 🚀 Deployment

### Prerequisites
- AWS Account
- GitHub Account
- Custom domain (optional)

### Setup Steps

1. **Frontend Deployment**
   - Create S3 bucket with static website hosting
   - Upload HTML/CSS/JS files
   - Configure CloudFront distribution
   - Set up Route 53 and ACM certificate

2. **Backend Setup**
   - Create DynamoDB table
   - Deploy Lambda function
   - Configure API Gateway
   - Set up CORS

3. **Analytics Configuration**
   - Enable CloudFront access logging
   - Create Athena database and table
   - Deploy analytics Lambda function
   - Configure SNS topic and subscription
   - Set up EventBridge schedule

4. **CI/CD Pipeline**
   - Configure GitHub Actions workflow
   - Add AWS credentials to GitHub Secrets
   - Test automated deployment

---

## 🔐 IAM Permissions

### CI/CD User Permissions:
- S3 read/write access
- CloudFront cache invalidation

### Analytics Lambda Permissions:
- Athena query execution
- S3 read access (CloudFront logs)
- SNS publish

---

## 📈 Key Learnings

- **Serverless Architecture**: Designing scalable, cost-effective solutions
- **API Integration**: Building and securing RESTful APIs
- **Data Analytics**: SQL queries on CloudFront access logs using Athena
- **Automation**: Event-driven architecture with EventBridge
- **DevOps**: CI/CD pipelines with GitHub Actions
- **AWS Services**: Hands-on experience with 10+ AWS services
- **Problem Solving**: Debugging CORS, CloudFront caching, IAM permissions

---

## 💰 Cost Optimization

- Serverless architecture: Pay only for usage
- CloudFront caching: Reduced origin requests
- S3 lifecycle policies: Automatic log cleanup
- DynamoDB on-demand: No unused capacity charges

**Estimated monthly cost: < $2**

---

## 🔮 Future Enhancements

- [ ] Infrastructure as Code with Terraform
- [ ] Enhanced monitoring with CloudWatch dashboards
- [ ] A/B testing for resume layout
- [ ] Multi-region deployment
- [ ] Advanced analytics (conversion tracking, heatmaps)

---

## 📝 Blog Post

Read about my experience building this project: [Medium Blog Post](https://medium.com/@stratajen)

---

## 📧 Contact

Jennifer Magruder
- **Email**: strataspherejen@gmail.com
- **LinkedIn**: [jennifer-magruder](https://www.linkedin.com/in/jennifer-magruder)
- **Website**: [stratajen.net](https://stratajen.net)

---

## 🙏 Acknowledgments

- [Forrest Brazeal](https://forrestbrazeal.com/) for creating the Cloud Resume Challenge
- AWS documentation and community
- Fellow cloud engineers for inspiration and support

---

**⭐ If you found this project helpful, please consider giving it a star!**