# Cloud Resume Challenge

A serverless resume website built on AWS, featuring a real-time visitor counter and automated CI/CD deployment pipeline.

🌐 **Website:** [stratajen.net](https://stratajen.net)

---

## 📋 Project Overview

This project is my implementation of the [Cloud Resume Challenge](https://cloudresumechallenge.dev/), demonstrating hands-on experience with AWS services, serverless architecture, and DevOps practices.

### Key Features

- ✅ **Serverless Architecture** - No servers to manage, scales automatically
- ✅ **Real-Time Visitor Counter** - Tracks unique visitors using DynamoDB and Lambda
- ✅ **Custom Domain with HTTPS** - Secure delivery via CloudFront CDN
- ✅ **CI/CD Pipeline** - Automated deployments with GitHub Actions
- ✅ **Infrastructure as Code** - Reproducible deployments (coming soon: Terraform)
- ✅ **CORS-Compliant API** - Proper handling of preflight requests

---

## 🏗️ Architecture

*(Architecture diagram will be added here)*

### Frontend
- **Hosting:** AWS S3 (static website)
- **CDN:** CloudFront with HTTPS
- **DNS:** Route 53 with custom domain
- **SSL/TLS:** AWS Certificate Manager

### Backend
- **Database:** DynamoDB (visitor count storage)
- **Compute:** AWS Lambda (Python 3.12)
- **API:** API Gateway (HTTP API)
- **Architecture Pattern:** Serverless, event-driven

### DevOps
- **Version Control:** GitHub
- **CI/CD:** GitHub Actions
- **Deployment:** Automated sync to S3 + CloudFront invalidation

---

## 🛠️ Technologies Used

**Cloud Platform:**
- AWS (S3, CloudFront, Route 53, Lambda, DynamoDB, API Gateway, ACM, IAM)

**Programming:**
- Python (Lambda backend)
- JavaScript (Frontend visitor counter logic)
- HTML/CSS (Responsive design)

**DevOps:**
- GitHub Actions (CI/CD)
- Git (Version control)
- AWS CLI

**Future Additions:**
- Terraform (Infrastructure as Code)
- Cypress (End-to-end testing)

---

## 🚀 How It Works

### Visitor Counter Flow

1. User visits `stratajen.net`
2. JavaScript makes POST request to API Gateway
3. API Gateway triggers Lambda function
4. Lambda atomically increments count in DynamoDB
5. Updated count returns to frontend
6. Visitor sees: "You are visitor #42"

### Deployment Flow

1. Developer pushes code to GitHub
2. GitHub Actions workflow triggers automatically
3. Files sync to S3 bucket
4. CloudFront cache invalidates
5. Website updates live within 2-3 minutes

---

## 💡 Key Learnings

### Technical Challenges Solved

**CORS Configuration:**
- Learned the difference between simple and preflight requests
- Implemented OPTIONS request handling in Lambda
- Configured proper CORS headers for cross-origin API calls

**Lambda Permissions:**
- Set up IAM roles with least-privilege access
- Configured execution role for DynamoDB access

**CloudFront Caching:**
- Implemented cache invalidation in CI/CD pipeline
- Balanced performance with content freshness

**Atomic Updates:**
- Used DynamoDB's atomic counter operations
- Ensured accurate visitor counting under concurrent requests

### DevOps Skills Gained

- Built end-to-end CI/CD pipeline from scratch
- Automated infrastructure deployment
- Implemented proper secrets management with GitHub Secrets
- Learned the importance of testing in isolated environments

---

## 📊 Project Stats

- **Lines of Code:** ~1,000+
- **AWS Services Used:** 8
- **Deployment Time:** ~2 minutes (automated)
- **Cost:** <$2/month
- **Uptime:** 99.9%+

---

## 🎯 Future Enhancements

- [ ] Convert infrastructure to Terraform (IaC)
- [ ] Add CloudWatch monitoring and alarms
- [ ] Implement end-to-end testing with Cypress
- [ ] Optimize API performance with CloudFront caching
- [ ] Add DynamoDB point-in-time recovery
- [ ] Implement blue/green deployments

---

## 📝 Blog Post

*Coming soon: Detailed write-up of challenges faced and lessons learned*

---

## 🙏 Acknowledgments

- [The Cloud Resume Challenge](https://cloudresumechallenge.dev/) - Created by Forrest Brazeal, owned and maintained by ExamPro and Andrew Brown
- AWS Documentation and tutorials
- The cloud engineering community

---

## 📬 Connect With Me

- **LinkedIn:** [Jennifer Magruder](https://www.linkedin.com/in/jennifer-magruder/)
- **GitHub:** [@JenMagruder](https://github.com/JenMagruder)
- **Website:** [stratajen.net](https://stratajen.net)

---

## 📄 License

This project is open source and available for learning purposes.

---

*Built with ☁️ by Jennifer Magruder*