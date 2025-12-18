# Backend configuration for remote state, was initially commented out


terraform {
   backend "s3" {
     bucket         = "stratajen-terraform-state"
     key            = "cloud-resume/terraform.tfstate"
     region         = "us-east-1"
     encrypt        = true
     dynamodb_table = "terraform-state-lock"
   }
 }