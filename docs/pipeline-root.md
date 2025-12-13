# Document Pipeline - Root Stack (`pipeline-root.yaml`)

## Why this YAML is created
The Root Stack serves as the main entry point and orchestrator for the entire Document Processing Pipeline. It adopts a specific architectural pattern using CloudFormation Nested Stacks to:
1.  **Manage Dependencies**: Explicitly defining the creation order (e.g., Security must exist before Messaging) to prevent race conditions.
2.  **Overcome Limits**: AWS CloudFormation has a limit on the number of resources per stack (500). breaking the architecture into nested stacks serves as a future-proof strategy.
3.  **Separation of Concerns**: Logically grouping resources (Security, Storage, Compute) makes the infrastructure easier to maintain and understand.
4.  **Parameter Passing**: It acts as the single source of truth for global configuration (like `ProjectId`, `StackName`) and passes these down to all child stacks.

## Parameter Details
These parameters are inputs to the Root stack, which typically come from the `deploy.sh` script or the console.

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| **`Environment`** | String | `dev` | The target environment for deployment (e.g., `dev`, `prod`, `qa`). |
| **`ProjectId`** | String | `034` | A unique identifier for the project this pipeline belongs to. used in naming conventions. |
| **`PortfolioId`** | String | `020` | A unique identifier for the portfolio. used in naming conventions. |
| **`S3TemplateBucket`** | String | - | The S3 bucket name where the nested CloudFormation templates (`pipeline-*.yaml`) are uploaded before deployment. |

## Resource Details
This stack does not create low-level AWS resources (like functions or buckets) directly but instead creates `AWS::CloudFormation::Stack` resources.

| Logical ID | Type | Description |
| :--- | :--- | :--- |
| **`SecurityStack`** | `AWS::CloudFormation::Stack` | Deploys KMS keys. |
| **`DatabaseStack`** | `AWS::CloudFormation::Stack` | Deploys the DynamoDB table. |
| **`MessagingStack`** | `AWS::CloudFormation::Stack` | Deploys the SNS topic and SQS Queues. depends on `SecurityStack` for encryption keys. |
| **`StorageStack`** | `AWS::CloudFormation::Stack` | Deploys the S3 input bucket. |
| **`ComputeStack`** | `AWS::CloudFormation::Stack` | Deploys all Lambda functions and IAM roles. depends on all previous stacks. |

## Output Details
This stack exports key values from its child stacks to be easily accessible from the AWS Console or other parent stacks.

| Output Key | Description | Value Source |
| :--- | :--- | :--- |
| **`InputBucket`** | The name of the S3 bucket created for document ingestion. | `StorageStack.Outputs.InputDocumentBucketName` |
| **`JobStatusTable`** | The name of the DynamoDB table used for tracking jobs. | `DatabaseStack.Outputs.JobStatusTableName` |
