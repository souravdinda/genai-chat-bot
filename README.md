# GenAI Chat Bot - Serverless Architecture (AWS SAM)

## ✅ Overview

This project provisions a **serverless architecture** using **AWS SAM** and **CloudFormation**.  
It automates the ingestion of PDF documents, extraction of text via **Amazon Textract**, and metadata persistence in **DynamoDB**, with notifications via **SNS**.  

The solution includes:  
- **KMS** for encrypting data at rest  
- **S3** bucket for PDF storage  
- **EventBridge scheduled Lambdas** for ingestion tasks  
- **Textract Starter Lambda** triggered on S3 upload to start Textract jobs  
- **Textract Completion Lambda** subscribed to SNS for post-processing results  
- **DynamoDB** for storing job metadata and results  

---

## 🏗️ Architecture

1. **EventBridge → LambdaOne & LambdaTwo**  
   - Two scheduled EventBridge rules trigger ingestion Lambdas.  
   - These Lambdas fetch data (e.g., transcripts, PDFs) and upload to the S3 bucket.  

2. **S3 → TextractStarterLambda**  
   - When a PDF is uploaded, it triggers `TextractStarterLambda`.  
   - This Lambda starts a Textract job and records the `JobId` in DynamoDB.  

3. **Textract → SNS → TextractCompletionLambda**  
   - Textract publishes job completion messages to the SNS topic.  
   - `TextractCompletionLambda` is subscribed to this topic.  
   - The Lambda fetches results from Textract and updates DynamoDB.  

4. **KMS**  
   - The S3 bucket is encrypted with a Customer Managed KMS Key (`AppKmsKey`).  
   - Lambdas are granted `kms:Encrypt`, `kms:Decrypt`, and `kms:GenerateDataKey` permissions.  

---

## ⚙️ Parameters

| Parameter       | Description                                                                 |
|-----------------|-----------------------------------------------------------------------------|

---

## 📤 Outputs

| Output             | Description                                                        |
|---------------------|--------------------------------------------------------------------|
| `BucketName`        | The name of the KMS-encrypted S3 bucket for PDFs.                 |
| `KmsKeyId`          | The ARN of the KMS CMK used for encryption.                       |
| `DynamoTableName`   | The name of the DynamoDB table used for case/job metadata.        |
| `TextractSNSTopic`  | The ARN of the SNS Topic used for Textract job completion events. |

---

## 🚀 Deployment

1. Build the project:
   ```bash
   sam build
