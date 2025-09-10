# **Genai-Chat-Bot**

## ✅ Overview
The **genai-chat-bot** project provisions a **secure, scalable architecture** using **AWS CloudFormation** to deploy:

- A **VPC** with public and private subnets  
- An **Internet Gateway** and **NAT Gateway** for outbound internet access  
- A **Lambda function** running inside a private subnet  
- A **public API Gateway** endpoint integrated with Lambda  
- An **S3 bucket** for storing **audit logs** (versioned)  
- An **S3 bucket** for **input documents** (to feed into Kendra/Textract)  
- **IAM roles and policies** for Lambda, Bedrock, and Kendra  
- A **Kendra GenAI index** (must be created manually, referenced in the template)  
- An **Amazon Bedrock Knowledge Base** backed by Kendra  
- An **Amazon Lex Bot** integrated with Lambda  

This setup ensures that your Lambda function is in a **private network** for security, while still allowing controlled public access through **API Gateway** and conversational access via **Lex**.

---

## ✅ Architecture Explanation
The **genai-chat-bot** architecture is designed for security, scalability, and compliance:

1. **VPC (10.0.0.0/16)**  
   Provides network isolation for all resources. Ensures Lambda runs in a private subnet for security.

2. **Public Subnet (10.0.1.0/24)**  
   Hosts the **NAT Gateway** and **Internet Gateway** for outbound internet connectivity.  
   Allows Lambda in the private subnet to access AWS services or the internet without being directly exposed.

3. **Private Subnet (10.0.2.0/24)**  
   Hosts the **Lambda function**, keeping it inaccessible from the public internet.  
   Lambda communicates with S3, Kendra, Bedrock, and API Gateway.

4. **Internet Gateway**  
   Enables public internet connectivity for the public subnet and API Gateway.

5. **NAT Gateway**  
   Provides outbound internet access for Lambda in the private subnet.  
   Ensures security by not exposing Lambda to incoming public traffic.

6. **API Gateway (Regional)**  
   Serves as the **public entry point** for external clients.  
   Receives HTTP requests and forwards them to Lambda via **AWS_PROXY** integration.

7. **Lambda Function**  
   - Processes incoming API requests  
   - Logs payloads to the Audit S3 bucket  
   - Queries **Kendra** or calls **Bedrock** depending on input  
   - Integrated with **Lex bot** for conversational chat

8. **S3 Buckets**  
   - **Audit Log Bucket** → Stores audit logs for compliance and monitoring (versioned).  
   - **Input Content Bucket** → Stores documents to be indexed by Kendra/Textract.

9. **IAM Roles & Policies**  
   - **LambdaExecutionRole** → Allows Lambda to access S3, CloudWatch, Textract, Kendra, and Bedrock.  
   - **KendraServiceRole** → Allows Kendra to read from InputContentBucket and manage documents.  
   - **BedrockServiceRole** → Allows Bedrock to query Kendra and read from S3.

10. **Kendra GenAI Index**  
    - Must be created manually (Enterprise Edition + GenAI).  
    - Its ID is passed to the stack via a parameter (`ExistingKendraIndexId`).  
    - Used by Lambda and Bedrock Knowledge Base.

11. **Bedrock Knowledge Base**  
    - Tied to the Kendra GenAI Index.  
    - Provides semantic search and conversational capabilities.

12. **Lex Bot**  
    - Serves as a natural language front-end.  
    - Routes utterances → Lambda → Kendra/Bedrock.

---

## ✅ AWS Services Used
- **Amazon VPC**
- **Amazon EC2 (Elastic IP, NAT Gateway)**
- **Amazon API Gateway**
- **AWS Lambda**
- **Amazon S3 (Audit + Input Content)**
- **Amazon Kendra (GenAI Index)**
- **Amazon Bedrock (Knowledge Base)**
- **Amazon Lex**
- **Amazon Textract**
- **AWS IAM**
- **Amazon CloudWatch Logs**

---

## ✅ Networking Details
| Component          | CIDR / Description              |
|-------------------|---------------------------------|
| VPC               | `10.0.0.0/16`                  |
| Public Subnet     | `10.0.1.0/24` (NAT Gateway)    |
| Private Subnet    | `10.0.2.0/24` (Lambda)         |
| Internet Gateway  | Provides public internet access |
| NAT Gateway       | Allows private Lambda to access internet securely |

> Lambda runs **inside the private subnet** for security and uses **NAT Gateway** for outbound traffic.

---

## ✅ Parameters
| Parameter Name          | Default Value                                     | Description |
|-------------------------|---------------------------------------------------|-------------|
| `LambdaFunctionName`    | `genai-chat-lambda`                               | Name of the Lambda function |
| `LambdaRuntime`         | `python3.11`                                      | Lambda runtime (Python 3.9/3.10/3.11, NodeJS) |
| `ApiName`               | `genai-chat-api`                                  | API Gateway name |
| `ApiStageName`          | `dev`                                             | API Gateway deployment stage |
| `AuditBucketName`       | `audit-logs-bucket`                               | Base name for S3 audit bucket |
| `InputContentBucketBase`| `input-content-bucket`                            | Base name for S3 input bucket |
| `ExistingKendraIndexId` | `934c7062-60c2-4f71-a200-a0a58f804353` *(example)*| ID of your manually created Kendra GenAI index |
| `VpcCidr`               | `10.0.0.0/16`                                     | CIDR for the VPC |
| `PublicSubnetCidr`      | `10.0.1.0/24`                                     | CIDR for the public subnet |
| `PrivateSubnetCidr`     | `10.0.2.0/24`                                     | CIDR for the private subnet |
| `BotName`               | `GenAIChatBot`                                    | Name of the Lex bot |

---

## ✅ Resources Created
- **Networking**
  - VPC, Subnets, NAT + Internet Gateways, Route Tables
- **Security**
  - Lambda Security Group
- **Compute**
  - Lambda function with inline Python handler
- **Storage**
  - Audit S3 bucket (versioned)
  - Input content S3 bucket
- **API**
  - API Gateway (Regional)
  - POST `/chat` resource + method
- **IAM**
  - Lambda execution role (S3, CloudWatch, Textract, Kendra, Bedrock)
  - Kendra service role (S3 access + doc ingestion)
  - Bedrock service role (Kendra query + S3 read)
- **AI Services**
  - Lex Bot
  - Kendra Data Source (from InputContentBucket)
  - Bedrock Knowledge Base (backed by Kendra)

---

## ✅ Outputs
| Output Key               | Description                                |
|---------------------------|--------------------------------------------|
| `ApiInvokeURL`            | Public URL to call the API Gateway endpoint |
| `VpcId`                   | ID of the created VPC                       |
| `PublicSubnetId`          | ID of the public subnet                     |
| `PrivateSubnetId`         | ID of the private subnet                    |
| `AuditBucketArn`          | ARN of the S3 audit bucket                  |
| `InputContentBucketName`  | Name of the S3 input content bucket         |
| `KendraIndexId`           | ID of the manually created Kendra GenAI index |
| `BedrockKnowledgeBaseId`  | ID of the Bedrock Knowledge Base            |
| `LambdaFunctionArn`       | ARN of the Lambda function                  |
| `LambdaRoleArn`           | ARN of the Lambda execution role            |
| `ApiGatewayArn`           | ARN of the API Gateway REST API             |

---