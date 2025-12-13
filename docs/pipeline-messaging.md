# Document Pipeline - Messaging Stack (`pipeline-messaging.yaml`)

## Why this YAML is created
This stack implements the "Event-Driven" architecture pattern. It is created to:
1.  **Decouple Services**: The process that starts document analysis (`StartTextractFunction`) does not need to wait for it to finish. It fires a job and forgets.
2.  **Asynchronous Integration**: Amazon Textract is an async service. It sends a notification to an SNS topic when done. This stack provides that topic.
3.  **Scalability**: Multiple subscribers could strictly be added to this topic in the future (e.g., one for processing, one for audit logging) without changing the upstream code.

## Parameter Details
This stack receives these parameters from the Root Stack.

| Parameter | Type | Description |
| :--- | :--- | :--- |
| **`Environment`** | String | The deployment environment. |
| **`ProjectId`** | String | Project identifier prefix. |
| **`PortfolioId`** | String | Portfolio identifier prefix. |
| **`StackName`** | String | Used to name the topic consistently. |
| **`KmsKeyArn`** | String | The ARN of the KMS Key from the Security Stack. Required because the SNS Topic and SQS Queues are encrypted at rest. |

## Resource Details

| Logical ID | Type | Description |
| :--- | :--- | :--- |
| **`TextractJobCompleteTopic`** | `AWS::SNS::Topic` | The communication channel for Textract completion events. <br>• **Name**: `{ProjectId}-{PortfolioId}-{StackName}-{Env}-textract-complete`<br>• **Encryption**: Encrypted using `KmsKeyArn`. |
| **`DocumentUploadQueue`** | `AWS::SQS::Queue` | Buffers S3 upload events before they trigger the Lambda. <br>• **Name**: `{ProjectId}-{PortfolioId}-{StackName}-{Env}-doc-upload-queue`<br>• **VisibilityTimeout**: 300s<br>• **RedrivePolicy**: Sends to DLQ after 3 failed attempts. |
| **`DocumentUploadDLQ`** | `AWS::SQS::Queue` | Dead Letter Queue for failed messages. <br>• **Name**: `{ProjectId}-{PortfolioId}-{StackName}-{Env}-doc-upload-dlq`<br>• **Retention**: 14 days. |

## Output Details
These values are exported to be used by `ComputeStack`.

| Output Key | Export Name | Description |
| :--- | :--- | :--- |
| **`TextractJobCompleteTopicArn`** | `{StackName}-TextractJobCompleteTopicArn` | The ARN of the SNS topic. |
| **`DocumentUploadQueueArn`** | `{StackName}-DocumentUploadQueueArn` | The ARN of the SQS queue. |
