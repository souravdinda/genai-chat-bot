# Document Pipeline - Security Stack (`pipeline-security.yaml`)

## Why this YAML is created
This stack is dedicated to centralized security and compliance. By isolating security resources, we ensure that:
1.  **Encryption is Universal**: A Customer Managed Key (CMK) is created once and reused across S3, SNS, and Secrets Manager to ensure meaningful encryption at rest.
2.  **Secret Management**: Sensitive credentials (like API passwords) are never hardcoded in Lambda environment variables but stored securely in AWS Secrets Manager.
3.  **Strict Scoping**: Key Policies can be tightly controlled independent of the compute logic.

## Parameter Details
This stack receives these parameters from the Root Stack.

| Parameter | Type | Description |
| :--- | :--- | :--- |
| **`Environment`** | String | The deployment environment (e.g., `dev`). |
| **`ProjectId`** | String | Project identifier prefix. |
| **`PortfolioId`** | String | Portfolio identifier prefix. |
| **`StackName`** | String | The name of the Root Stack. used to creating consistent, easy-to-identify resource names (e.g., aliasing the key). |

## Resource Details

| Logical ID | Type | Description |
| :--- | :--- | :--- |
| **`PipelineKey`** | `AWS::KMS::Key` | A symmetric encryption key used to encrypt the SNS topic, S3 bucket, and SQS Queues. It has a key policy allowing access to specific services (SNS, S3, Lambda, Textract). |
| **`PipelineKeyAlias`** | `AWS::KMS::Alias` | A friendly name for the key: `alias/{ProjectId}-{PortfolioId}-{StackName}-{Env}-key`. |

## Output Details
These values are exported to be used by `MessagingStack` (for encryption) and `ComputeStack` (for decryption).

| Output Key | Export Name | Description |
| :--- | :--- | :--- |
| **`PipelineKeyArn`** | `{StackName}-PipelineKeyArn` | The Amazon Resource Name (ARN) of the KMS Key. |
| **`PipelineKeyId`** | `{StackName}-PipelineKeyId` | The ID of the KMS Key. |
