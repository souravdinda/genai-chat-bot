# API Stack (`api.yaml`)

## Overview
This stack sets up **Amazon API Gateway** to expose the Lambda functions as a RESTful API. It handles routing and authentication.

## Parameters
*   `ContentDesignerFunctionArn`: ARN of the backend Lambda.
*   `BotFulfillmentFunctionArn`: ARN of the chat Lambda.
*   `UserPoolArn`: ARN of the Cognito User Pool for authentication.

## Resources Created

### 1. REST API (`ApiGateway`)
*   **Name**: `genai-bot-api-{env}`.

### 2. Cognito Authorizer (`ApiAuthorizer`)
*   **Type**: `COGNITO_USER_POOLS`.
*   **Purpose**: Validates JWT tokens from Cognito in the `Authorization` header.

### 3. Resources & Methods
*   **/config (GET)**:
    *   Integrates with `ContentDesignerFunction`.
    *   Secured by `CognitoAuthorizer`.
*   **/chat (POST)**:
    *   Integrates with `BotFulfillmentFunction`.
    *   Secured by `CognitoAuthorizer`.

### 4. Lambda Permissions
*   Grants API Gateway permission to invoke the specific Lambda functions.

## Outputs
*   `ApiEndpoint`: The base URL of the API (e.g., `https://xyz.execute-api.us-east-1.amazonaws.com/dev`).
