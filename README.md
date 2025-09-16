# **Genai-Chat-Bot**

## ✅ Overview
The **genai-chat-bot** project provisions a **secure, scalable serverless architecture** using **AWS SAM (Serverless Application Model)** and **CloudFormation** to deploy:

- A **VPC** with public and private subnets  
- An **Internet Gateway** and **NAT Gateway** for outbound internet access  
- A **Lambda function** (deployed with `AWS::Serverless::Function`) running inside a private subnet  
- A **public API Gateway** endpoint integrated with Lambda  
- An **S3 bucket** for storing **audit logs** (versioned)  
- An **S3 bucket** for **input documents** (to feed into Kendra/Textract)  
- **IAM roles and policies** for Lambda, Bedrock, and Kendra  
- A **Kendra GenAI Enterprise Edition index** (must be created as `GEN_AI_ENTERPRISE_EDITION`)  
- An **Amazon Bedrock Knowledge Base** backed by the Kendra GenAI index  
- An **Amazon Lex Bot** integrated with Lambda  

This setup ensures your Lambda function runs securely in a **private subnet**, while **API Gateway** and **Lex** provide controlled external access.

---

## ✅ Architecture
The architecture follows security-first and event-driven design principles:

1. **VPC (10.0.0.0/16)** → Provides isolation for all workloads.
2. **Public Subnet (10.0.1.0/24)** → Hosts NAT Gateway + IGW for outbound traffic.
3. **Private Subnet (10.0.2.0/24)** → Runs Lambda without direct public exposure.
4. **Internet Gateway + NAT Gateway** → Allow private workloads to access AWS APIs and internet securely.
5. **API Gateway** → Public entry point (HTTP POST `/chat`) integrated with Lambda.
6. **Lambda** → Processes requests, logs audits, queries Kendra GenAI, or calls Bedrock models.
7. **S3 Buckets** →
   - Audit bucket (immutable logs).
   - Input bucket (feeds into Kendra/Textract).
8. **IAM Roles** → Granular roles for Lambda, Kendra, and Bedrock.
9. **Kendra GenAI Index** → Enterprise GenAI edition index, required for Bedrock KB.
10. **Bedrock Knowledge Base** → RAG (retrieval-augmented generation) layer on top of Kendra.
11. **Lex Bot** → Conversational interface tied to Lambda.

---

## ✅ AWS Services Used
- **Amazon VPC** (network isolation)
- **Amazon EC2 (NAT Gateway, Elastic IP)**
- **Amazon API Gateway** (public REST API)
- **AWS Lambda** (serverless compute)
- **Amazon S3** (Audit + Input)
- **Amazon Kendra (GenAI Enterprise Edition)**
- **Amazon Bedrock (Knowledge Base + model inference)**
- **Amazon Lex (chatbot)**
- **Amazon Textract (OCR/analysis)**
- **AWS IAM** (roles & policies)
- **Amazon CloudWatch Logs** (logging)

---

## ✅ Networking
| Component          | CIDR / Description              |
|-------------------|---------------------------------|
| VPC               | `10.0.0.0/16`                  |
| Public Subnet     | `10.0.1.0/24` (NAT Gateway)    |
| Private Subnet    | `10.0.2.0/24` (Lambda)         |
| Internet Gateway  | Provides outbound access       |
| NAT Gateway       | Private → Internet access      |

> Lambda runs **only in the private subnet**, accessing AWS services via NAT.

---

## ✅ Parameters
| Parameter Name          | Default Value                                     | Description |
|-------------------------|---------------------------------------------------|-------------|
| `LambdaFunctionName`    | `genai-chat-lambda`                               | Lambda function name |
| `LambdaRuntime`         | `python3.11`                                      | Runtime (Python 3.9–3.11, NodeJS) |
| `ApiName`               | `genai-chat-api`                                  | API Gateway name |
| `ApiStageName`          | `dev`                                             | API stage |
| `AuditBucketName`       | `audit-logs-bucket`                               | S3 audit logs bucket base name |
| `InputContentBucketBase`| `input-content-bucket`                            | S3 input bucket base name |
| `VpcCidr`               | `10.0.0.0/16`                                     | VPC CIDR |
| `PublicSubnetCidr`      | `10.0.1.0/24`                                     | Public subnet CIDR |
| `PrivateSubnetCidr`     | `10.0.2.0/24`                                     | Private subnet CIDR |
| `BotName`               | `GenAIChatBot`                                    | Lex bot name |

---

## ✅ Resources Provisioned
- **Networking:** VPC, Subnets, NAT, IGW, Route Tables
- **Security:** Lambda Security Group
- **Compute:** Lambda (serverless, private subnet)
- **Storage:** S3 audit bucket + input bucket
- **API Layer:** API Gateway (Regional) + POST `/chat`
- **IAM:** Roles for Lambda, Kendra, Bedrock (with GenAI permissions: `Query`, `Retrieve`, `DescribeIndex`, etc.)
- **AI Services:**
  - Lex Bot (utterances → Lambda)
  - Kendra Data Source (from InputContentBucket)
  - Kendra GenAI Index (must be Enterprise GenAI)
  - Bedrock Knowledge Base (uses Kendra index)

---

## ✅ Outputs
| Output Key               | Description                                |
|---------------------------|--------------------------------------------|
| `ApiInvokeURL`            | Invoke URL for API Gateway (`/chat`)       |
| `VpcId`                   | VPC ID                                     |
| `PublicSubnetId`          | Public Subnet ID                           |
| `PrivateSubnetId`         | Private Subnet ID                          |
| `AuditBucketArn`          | ARN of audit S3 bucket                     |
| `InputContentBucketName`  | Input S3 bucket name                       |
| `KendraIndexId`           | Kendra GenAI index ID                      |
| `LambdaFunctionArn`       | Lambda ARN                                 |
| `LambdaRoleArn`           | Lambda execution role ARN                  |
| `ApiGatewayArn`           | API Gateway ARN                            |
