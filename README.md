# **Genai-Chat-Bot**

## ✅ Overview
The **genai-chat-bot** project provisions a **secure, scalable architecture** using **AWS CloudFormation** to deploy:
- A **VPC** with public and private subnets
- An **Internet Gateway** and **NAT Gateway** for outbound internet access
- A **Lambda function** running inside a private subnet
- A **public API Gateway** endpoint integrated with Lambda
- An **S3 bucket** for storing audit logs with versioning enabled
- **IAM roles and policies** for Lambda and S3 access

This setup ensures that your Lambda function is in a **private network** for security, while still allowing controlled public access through **API Gateway**.

---

## ✅ Architecture Explanation
The **genai-chat-bot** architecture is designed for security, scalability, and compliance:

1. **VPC (10.0.0.0/16)**  
   - Provides network isolation for all resources.
   - Ensures Lambda runs in a private subnet for security.

2. **Public Subnet (10.0.1.0/24)**  
   - Hosts the **NAT Gateway** and **Internet Gateway** for outbound internet connectivity.
   - Allows Lambda in the private subnet to access AWS services or the internet without being directly exposed.

3. **Private Subnet (10.0.2.0/24)**  
   - Hosts the **Lambda function** to keep it inaccessible from the public internet.
   - Lambda communicates with S3 and API Gateway.

4. **Internet Gateway**  
   - Enables public internet connectivity for the public subnet and API Gateway.

5. **NAT Gateway**  
   - Provides outbound internet access for Lambda in the private subnet.
   - Ensures security by not exposing Lambda to incoming public traffic.

6. **API Gateway (Regional)**  
   - Serves as the **public entry point** for external clients.
   - Receives HTTP requests and forwards them to Lambda via **AWS_PROXY** integration.

7. **Lambda Function**  
   - Processes incoming API requests and stores audit logs in S3.
   - Runs Python code (Hello World logic by default).

8. **S3 Audit Log Bucket**  
   - Stores logs for compliance and monitoring.
   - Versioning is enabled to retain historical data.

9. **IAM Roles & Policies**  
   - Lambda execution role allows logging to CloudWatch and writing objects to S3.
   - Principle of least privilege applied.

---

## ✅ AWS Services Used
- **Amazon VPC**
- **Amazon EC2 (Elastic IP, NAT Gateway)**
- **Amazon API Gateway**
- **AWS Lambda**
- **Amazon S3**
- **AWS IAM**
- **Amazon CloudWatch Logs**

---

## ✅ Networking Details
| Component             | CIDR / Description              |
|----------------------|---------------------------------|
| VPC                 | `10.0.0.0/16`                  |
| Public Subnet       | `10.0.1.0/24` (NAT Gateway)    |
| Private Subnet      | `10.0.2.0/24` (Lambda)         |
| Internet Gateway    | Provides public internet access |
| NAT Gateway         | Allows private Lambda to access internet securely |

> Lambda runs **inside the private subnet** for security and uses **NAT Gateway** for outbound traffic.

---

## ✅ Parameters
| Parameter Name       | Default Value       | Description                                   |
|----------------------|---------------------|-----------------------------------------------|
| `LambdaFunctionName` | `genai-chat-lambda`| Name of the Lambda function                 |
| `LambdaRuntime`      | `python3.11`       | Lambda runtime (Python 3.9/3.10/3.11, NodeJS)|
| `ApiName`            | `genai-chat-api`   | API Gateway name                            |
| `ApiStageName`       | `dev`             | API Gateway deployment stage               |
| `AuditBucketName`    | `audit-logs-bucket`| Base name for S3 bucket (final name is `<AuditBucketName>-<AccountId>-<Region>`) |
| `VpcCidr`            | `10.0.0.0/16`     | CIDR for the VPC                            |
| `PublicSubnetCidr`   | `10.0.1.0/24`     | CIDR for the public subnet                 |
| `PrivateSubnetCidr`  | `10.0.2.0/24`     | CIDR for the private subnet                |

---

## ✅ Resources Created
- **Networking**
  - VPC
  - Internet Gateway
  - Public Subnet
  - Private Subnet
  - NAT Gateway + Elastic IP
  - Route Tables (public + private)
- **Security**
  - Security Group for Lambda
- **Compute**
  - Lambda function with VPC config
- **Storage**
  - S3 bucket for audit logs (versioning enabled)
- **API**
  - API Gateway (Regional)
  - POST `/chat` resource and method
- **IAM**
  - Lambda execution role with permissions to S3 and CloudWatch Logs

---

## ✅ Outputs
| Output Key           | Description                                     |
|----------------------|-----------------------------------------------|
| `ApiInvokeURL`       | Public URL to call the API Gateway endpoint |
| `VpcId`             | ID of the created VPC                        |
| `PublicSubnetId`    | ID of the public subnet                      |
| `PrivateSubnetId`   | ID of the private subnet                     |
| `NatGatewayId`      | ID of the NAT Gateway                        |
| `NatEIP`            | Elastic IP of the NAT Gateway                |
| `AuditBucketArn`    | ARN of the S3 audit bucket                   |
| `AuditBucketNameOut`| Name of the S3 audit bucket                  |
| `LambdaFunctionArn` | ARN of the Lambda function                   |
| `LambdaRoleArn`     | ARN of the Lambda execution role             |
| `ApiGatewayArn`     | ARN of the API Gateway REST API              |

---