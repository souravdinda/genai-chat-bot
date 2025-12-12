# Document Pipeline - Database Stack (`pipeline-database.yaml`)

## Why this YAML is created
This stack provides the state storage layer for the pipeline. Separation of the database layer allows for:
1.  **Lifecycle Management**: The database table can be protected from accidental deletion (via DeletionPolicy) or backed up independently of the compute logic.
2.  **State Tracking**: It provides a persistent record of every document processed, its status (`STARTED`, `COMPLETED`, `FAILED`), and associated metadata, which is critical for async workflows like Textract.

## Parameter Details
This stack receives these parameters from the Root Stack.

| Parameter | Type | Description |
| :--- | :--- | :--- |
| **`Environment`** | String | The deployment environment (e.g., `dev`). |
| **`ProjectId`** | String | Project identifier prefix. |
| **`PortfolioId`** | String | Portfolio identifier prefix. |
| **`StackName`** | String | The name of the Root Stack, included in the DynamoDB Table name for uniqueness. |

## Resource Details

| Logical ID | Type | Description |
| :--- | :--- | :--- |
| **`JobStatusTable`** | `AWS::DynamoDB::Table` | The main NoSQL table for tracking jobs. <br>• **Name**: `{ProjectId}-{PortfolioId}-{StackName}-{Env}-jobs`<br>• **Partition Key**: `JobId` (String)<br>• **Billing**: `PAY_PER_REQUEST` (Serverless, scales to zero)<br>• **Encryption**: Default AWS Owned Key<br>• **Recovery**: Point-in-Time Recovery (PITR) enabled. |

## Output Details
These values are exported to be used by `ComputeStack` (so Lambdas know which table to read/write).

| Output Key | Export Name | Description |
| :--- | :--- | :--- |
| **`JobStatusTableName`** | `{StackName}-JobStatusTableName` | The actual name of the DynamoDB table. |
| **`JobStatusTableArn`** | `{StackName}-JobStatusTableArn` | The ARN of the table, used for IAM permissions. |
