# Root Stack (`root.yaml`)

## Overview
The **Root Stack** is the orchestrator for the entire GenAI Bot infrastructure. It does not create any physical resources (like EC2 or S3) directly, but instead uses the `AWS::CloudFormation::Stack` resource to create **Nested Stacks**. This ensures that all components are deployed in the correct order and dependencies are managed automatically.

## Parameters
| Parameter | Description | Default |
|-----------|-------------|---------|
| `Environment` | The deployment environment (e.g., `dev`, `prod`). | `dev` |
| `S3TemplateBucket` | The S3 bucket name where the nested templates (`auth.yaml`, `api.yaml`, etc.) are stored. | *Required* |

## Resources Created
The root stack creates the following nested stacks:

1.  **AuthStack** (`auth.yaml`): Sets up Cognito.
2.  **DatabaseStack** (`database.yaml`): Sets up DynamoDB tables.
3.  **StorageS3Stack** (`storage-s3.yaml`): Sets up S3 buckets.
4.  **AIServicesStack** (`ai-services.yaml`): Sets up OpenSearch and Lex.
5.  **ComputeStack** (`compute.yaml`): Sets up Lambda functions.
    *   *Depends On*: `DatabaseStack`, `AIServicesStack` (needs tables and OpenSearch endpoint).
6.  **ApiStack** (`api.yaml`): Sets up API Gateway.
    *   *Depends On*: `ComputeStack`, `AuthStack` (needs Lambda ARNs and User Pool ARN).

## Outputs
| Output | Description |
|--------|-------------|
| `ApiEndpoint` | The URL of the deployed API Gateway. |
| `CognitoUserPoolId` | The ID of the created Cognito User Pool. |
