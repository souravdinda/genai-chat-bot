# Compute Stack (`compute.yaml`)

## Overview
This stack contains the serverless compute resources (**AWS Lambda**) that run the application logic.

## Parameters
*   `ConfigTableName`: Name of the DynamoDB Config table.
*   `ChatHistoryTableName`: Name of the DynamoDB History table.
*   `OpenSearchEndpoint`: Endpoint of the OpenSearch domain.

## Resources Created

### 1. Lambda Execution Role (`LambdaExecutionRole`)
*   **Purpose**: Grants permissions to the Lambda functions.
*   **Permissions**:
    *   **DynamoDB**: Read/Write access to Config and History tables.
    *   **OpenSearch**: HTTP POST/PUT/GET access to the domain (`es:*`).
    *   **CloudWatch**: Basic execution (logs).

### 2. Content Designer Function (`ContentDesignerFunction`)
*   **Purpose**: Backend for the Content Designer UI.
*   **Runtime**: Python 3.11.
*   **Env Variables**: `CONFIG_TABLE`.

### 3. Bot Fulfillment Function (`BotFulfillmentFunction`)
*   **Purpose**: Handles chat interactions and fulfills user requests.
*   **Runtime**: Python 3.11.
*   **Env Variables**:
    *   `HISTORY_TABLE`: For storing chat logs.
    *   `OPENSEARCH_ENDPOINT`: For vector search (RAG).

## Outputs
*   `ContentDesignerFunctionArn`: ARN of the designer function.
*   `BotFulfillmentFunctionArn`: ARN of the fulfillment function.
