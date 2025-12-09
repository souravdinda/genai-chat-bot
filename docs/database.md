# Database Stack (`database.yaml`)

## Overview
This stack provisions the NoSQL databases using **Amazon DynamoDB**. It stores configuration settings and chat history.

## Resources Created

### 1. Config Table (`ConfigTable`)
*   **Purpose**: Stores dynamic configuration for the bot.
*   **Partition Key**: `configKey` (String).
*   **Billing**: Pay-per-request (On-Demand).

### 2. Chat History Table (`ChatHistoryTable`)
*   **Purpose**: Stores the conversation history between users and the bot.
*   **Partition Key**: `userId` (String).
*   **Sort Key**: `timestamp` (Number).
*   **Billing**: Pay-per-request (On-Demand).

## Outputs
*   `ConfigTableName`: The name of the created Config table.
*   `ChatHistoryTableName`: The name of the created Chat History table.
