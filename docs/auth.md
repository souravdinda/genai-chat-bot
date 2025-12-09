# Authentication Stack (`auth.yaml`)

## Overview
This stack handles all user authentication and identity management using **Amazon Cognito**. It secures the API and manages user sign-ups/sign-ins.

## Resources Created

### 1. Cognito User Pool (`UserPool`)
*   **Purpose**: A user directory for the application.
*   **Configuration**:
    *   Auto-verifies email addresses.
    *   Enforces a strong password policy (8 chars, numbers, symbols, mixed case).

### 2. User Pool Client (`UserPoolClient`)
*   **Purpose**: An interface for the application (frontend) to interact with the User Pool.
*   **Configuration**:
    *   Enables `ALLOW_USER_PASSWORD_AUTH` and `ALLOW_REFRESH_TOKEN_AUTH`.
    *   Does **not** generate a client secret (required for web apps).

### 3. Identity Pool (`IdentityPool`)
*   **Purpose**: Exchanges Cognito User Pool tokens for temporary AWS credentials (if needed for direct AWS access from client).
*   **Configuration**:
    *   Linked to the User Pool Client.
    *   Does not allow unauthenticated identities.

### 4. Authenticated Role (`AuthenticatedRole`)
*   **Purpose**: IAM Role assumed by authenticated users.
*   **Permissions**:
    *   Basic Cognito identity permissions.
    *   Mobile analytics permissions.

## Outputs
*   `UserPoolId`: The ID of the User Pool.
*   `UserPoolArn`: The ARN of the User Pool (used by API Gateway Authorizer).
*   `UserPoolClientId`: The Client ID for the frontend.
*   `IdentityPoolId`: The ID of the Identity Pool.
