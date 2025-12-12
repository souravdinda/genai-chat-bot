# Document Pipeline - Storage Stack (`pipeline-storage.yaml`)

## Why this YAML is created
This stack serves as the ingestion layer for the pipeline. It is created to:
1.  **Isolate Input Data**: Provides a dedicated, secure endpoint for uploading raw documents (PDFs).
2.  **Trigger Workflows**: It is configured to emit events to Amazon EventBridge whenever a file is uploaded, acting as the catalyst for the entire processing workflow.
3.  **Data Protection**: Ensures that all data at rest is encrypted.

## Parameter Details
This stack receives these parameters from the Root Stack.

| Parameter | Type | Description |
| :--- | :--- | :--- |
| **`Environment`** | String | The deployment environment. |
| **`ProjectId`** | String | Project identifier prefix. |
| **`PortfolioId`** | String | Portfolio identifier prefix. |
| **`StackName`** | String | Used to name the bucket. |

## Resource Details

| Logical ID | Type | Description |
| :--- | :--- | :--- |
| **`InputDocumentBucket`** | `AWS::S3::Bucket` | The S3 bucket for file uploads. <br>• **Name**: `{ProjectId}-{PortfolioId}-{StackName}-{Env}-input`<br>• **EventBridge**: `EventBridgeEnabled: true` allowing standard S3 events to be routed to EventBridge rules in the Compute stack.<br>• **Encryption**: Server-Side Encryption (AES256) enabled by default. |

## Output Details
These values are exported to be used by `ComputeStack` (permissions to read/write).

| Output Key | Export Name | Description |
| :--- | :--- | :--- |
| **`InputDocumentBucketName`** | `{StackName}-InputDocumentBucketName` | The name of the S3 bucket. |
| **`InputDocumentBucketArn`** | `{StackName}-InputDocumentBucketArn` | The ARN of the S3 bucket. |
