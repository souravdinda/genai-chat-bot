# Document Pipeline - Storage Stack (`pipeline-storage.yaml`)

## Why this YAML is created
This stack serves as the ingestion layer for the pipeline. It is created to:
1.  **Isolate Input Data**: Provides a dedicated, secure endpoint for uploading raw documents (PDFs).
2.  **Trigger Workflows**: It is configured to emit events to Amazon EventBridge whenever a file is uploaded, acting as the catalyst for the entire processing workflow.
3.  **Data Protection**: Ensures that all data at rest is encrypted.

## Inputs
| Parameter | Type | Description |
| :--- | :--- | :--- |
| **`Environment`** | String | Deployment environment (e.g., dev, prod). |
| **`ProjectId`** | String | Project identifier prefix. |
| **`PortfolioId`** | String | Portfolio identifier prefix. |
| **`StackName`** | String | Used to name the bucket consistently. |
| **`DocumentUploadQueueArn`** | String | ARN of the SQS Queue to receive object creation notifications. |

## Resource Details

| Logical ID | Type | Description |
| :--- | :--- | :--- |
| **`InputDocumentBucket`** | `AWS::S3::Bucket` | The S3 bucket for uploading documents. <br>• **Name**: `{ProjectId}-{PortfolioId}-{StackName}-{Env}-input`<br>• **Encryption**: SSE-S3 (AES256).<br>• **Notifications**: Sends `s3:ObjectCreated:*` events to `DocumentUploadQueue`. |

## Output Details
These values are exported to be used by `ComputeStack` (permissions to read/write).

| Output Key | Export Name | Description |
| :--- | :--- | :--- |
| **`InputDocumentBucketName`** | `{StackName}-InputDocumentBucketName` | The name of the S3 bucket. |
| **`InputDocumentBucketArn`** | `{StackName}-InputDocumentBucketArn` | The ARN of the S3 bucket. |
