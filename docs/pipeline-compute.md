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
| **`KmsKeyArn`** | String | KMS Key ARN (from Security Stack) to decrypt SNS messages and SQS messages. |
| **`DocumentUploadQueueArn`** | String | SQS Queue ARN (from Messaging Stack) used as the event source for the StartTextract Lambda. |

## Resource Details

### IAM Roles
- **`PipelineLambdaRole`**: One unified role for the functions. It allows:
  - `s3:GetObject/PutObject` on the input bucket.
  - `dynamodb:PutItem/UpdateItem` on the status table.
  - `textract:Start/GetDocumentAnalysis`.
  - `kms:Decrypt` using the pipeline key.
  - `sqs:ReceiveMessage/DeleteMessage` from the upload queue.
- **`TextractPublishRole`**: A role assumed by the Textract service itself to publish "Job Complete" notifications to our SNS topic.

### Lambda Functions
1. **`StartTextractFunction`**:
   - **Trigger**: SQS Queue (`DocumentUploadQueue`) Event Source Mapping. The Queue receives native S3 Event Notifications.
   - **Logic**: Parses SQS body to find S3 event, calls Textract `StartDocumentAnalysis`, saves `JobId` to DynamoDB.
2. **`UpdateSalesForceFunction`**:
   - **Trigger**: SNS Subscription to the `TextractJobCompleteTopic`.
   - **Logic**: Receives `JobId`, checks status, fetches results from Textract, and sends data to Salesforce.
3. **`ManualLambdaFunction`**:
   - **Trigger**: EventBridge Schedule (`rate(1 day)`).
   - **Logic**: Intended for manual or scheduled ingestion of documents.
4. **`ClearinghouseFunction`**:
   - **Trigger**: EventBridge Schedule (`rate(1 day)`).
   - **Logic**: Fetches documents from the Clearinghouse/external sources and uploads to S3.

## Output Details
These values are available for reference.

| Output Key | Description |
| :--- | :--- |
| **`StartTextractFunctionArn`** | The ARN of the function that starts processing. |
| **`ProcessTextractFunctionArn`** | The ARN of the Salesforce update function. |
| **`ManualLambdaFunctionArn`** | The ARN of the manual ingestion function. |
| **`ClearinghouseFunctionArn`** | The ARN of the Clearinghouse ingestion function. |
