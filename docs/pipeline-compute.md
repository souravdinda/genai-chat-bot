# Document Pipeline - Compute Stack (`pipeline-compute.yaml`)

## Why this YAML is created
This is the "Brain" of the pipeline. It is created to:
1.  **Execute Business Logic**: Contains the Python code that actually coordinates the AWS services (Textract, DynamoDB, Systems).
2.  **Manage Permissions**: Defines IAM roles that strictly adhere to the Principle of Least Privilege, binding the physical resources (S3, Table, Key) to the logic.
3.  **Integrate Triggers**: Sets up the glue between events (S3 Upload, SNS Notification, Schedule) and the code execution.

## Parameter Details
This stack consumes the outputs from ALL other stacks to wire everything together.

| Parameter | Type | Description |
| :--- | :--- | :--- |
| **`Environment`, `ProjectId`...** | String | Standard naming parameters. |
| **`StackName`** | String | Used for consistent function naming. |
| **`InputDocumentBucketName`** | String | S3 Bucket name (from Storage Stack) to allow read/write access. |
| **`JobStatusTableName`** | String | DynamoDB Table name (from Database Stack) to update job status. |
| **`TextractJobCompleteTopicArn`** | String | SNS Topic ARN (from Messaging Stack) to subscribe to or publish to. |
| **`KmsKeyArn`** | String | KMS Key ARN (from Security Stack) to decrypt SNS messages and Secrets. |
| **`IngestionSecretArn`** | String | Secret ARN (from Security Stack) to retrieve API credentials. |

## Resource Details

### IAM Roles
- **`PipelineLambdaRole`**: One unified role for the functions. It allows:
  - `s3:GetObject/PutObject` on the input bucket.
  - `dynamodb:PutItem/UpdateItem` on the status table.
  - `textract:Start/GetDocumentAnalysis`.
  - `kms:Decrypt` using the pipeline key.
  - `secretsmanager:GetSecretValue` for the ingestion credentials.
- **`TextractPublishRole`**: A role assumed by the Textract service itself to publish "Job Complete" notifications to our SNS topic.

### Lambda Functions
1. **`StartTextractFunction`**:
   - **Trigger**: EventBridge Rule matching `Object Created` in the Input Bucket.
   - **Logic**: Calls Textract `StartDocumentAnalysis`, saves `JobId` to DynamoDB.
2. **`ProcessTextractFunction`**:
   - **Trigger**: SNS Subscription to the `TextractJobCompleteTopic`.
   - **Logic**: Receives `JobId`, checks status, fetching results from Textract, and (placeholder) sends data to Salesforce.
3. **`IngestionFunction`**:
   - **Trigger**: EventBridge Schedule (`rate(1 day)`).
   - **Logic**: Pulls data from external sources (Parchment/NSC) using credentials from Secrets Manager.

## Output Details
These values are available for reference.

| Output Key | Description |
| :--- | :--- |
| **`StartTextractFunctionArn`** | The ARN of the function that starts processing. |
| **`ProcessTextractFunctionArn`** | The ARN of the function that handles results. |
| **`IngestionFunctionArn`** | The ARN of the scheduled ingestion function. |
