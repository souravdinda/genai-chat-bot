# Genai Chat Bot 

## ✅ Overview
The **genai-chat-bot** project provisions an **Amazon API Gateway**, **AWS Lambda function**, and an **S3 audit log bucket** using AWS CloudFormation.  
The API receives requests via API Gateway, processes them through Lambda, and stores audit logs in S3 for compliance and monitoring purposes.

---

## ✅ Services Created
1. **Amazon API Gateway**
   - REST API with `POST /chat` method
   - Proxy integration with Lambda
2. **AWS Lambda**
   - Handles API requests and writes logs to S3
   - Uses Python code (Hello World by default)
3. **Amazon S3**
   - Audit log bucket for storing API request data
   - Versioning enabled for compliance
4. **IAM Role**
   - Grants Lambda permissions to write to S3 and log to CloudWatch

---

## ✅ Resources Created by CloudFormation
| Resource Logical ID     | AWS Service      | Description                                         |
|-------------------------|-----------------|---------------------------------------------------|
| `AuditLogBucket`       | Amazon S3       | Stores API request payloads as audit logs         |
| `LambdaExecutionRole`  | IAM Role        | Grants Lambda permissions to S3 & CloudWatch      |
| `ChatLambdaFunction`   | AWS Lambda      | Processes API requests and logs data to S3        |
| `ApiGatewayRestApi`    | API Gateway     | Creates REST API with `/chat` endpoint            |
| `ApiGatewayResource`   | API Gateway     | Resource path `/chat` under the API               |
| `ApiGatewayMethod`     | API Gateway     | POST method integrated with Lambda                |
| `ApiGatewayDeployment` | API Gateway     | Deployment for the API stage                      |
| `ApiGatewayStage`      | API Gateway     | Defines stage (e.g., `dev`) for the API           |
| `LambdaInvokePermission`| Lambda Permission | Allows API Gateway to invoke the Lambda function |

---

## ✅ Parameters
| Parameter             | Description                                      | Default               |
|----------------------|--------------------------------------------------|----------------------|
| `LambdaFunctionName` | Name of the Lambda function                     | `api-lambda`         |
| `LambdaRuntime`      | Lambda runtime (e.g., python3.11, nodejs18.x)  | `python3.11`         |
| `ApiName`            | Name of the API Gateway                        | `chat-api`           |
| `ApiStageName`       | Deployment stage name for API Gateway          | `dev`                |
| `AuditBucketName`    | Base name for S3 bucket (suffix will be added) | `audit-logs-bucket`  |

---

## ✅ Outputs
| Output Name           | Description                                    |
|----------------------|-----------------------------------------------|
| `ApiInvokeURL`       | Invoke URL of the API Gateway                |
| `ApiGatewayArn`      | ARN of the API Gateway REST API              |
| `LambdaFunctionArn`  | ARN of the Lambda function                   |
| `LambdaRoleArn`      | ARN of the IAM Role for Lambda execution     |
| `AuditBucketArn`     | ARN of the S3 audit log bucket               |

---

## ✅ Notes
- The S3 bucket name is generated dynamically as:  
\${AuditBucketName}-\${AWS::AccountId}-\${AWS::Region}

- S3 bucket deletion requires manual cleanup due to versioning.

---
