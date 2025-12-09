# AI Services Stack (`ai-services.yaml`)

## Overview
This stack provisions the AI and Search capabilities using **Amazon OpenSearch Service** and **Amazon Lex**.

## Resources Created

### 1. OpenSearch Domain (`OpenSearchDomain`)
*   **Purpose**: Vector database for storing embeddings and performing semantic search (RAG).
*   **Configuration**:
    *   **Instance Type**: `t3.small.search` (Cost-effective for dev).
    *   **Storage**: 10GB EBS (gp3).
    *   **Encryption**: Encryption at rest and node-to-node encryption enabled.
    *   **Access Policy**: Restricted to the AWS Account Root user.

### 2. Lex Bot (`GenAIBot`)
*   **Purpose**: Conversational interface for the bot.
*   **Status**: *Currently commented out in the template due to import complexity.*
*   **Intended Configuration**:
    *   Locale: `en_US`.
    *   Voice: `Joanna`.
    *   Idle Session TTL: 5 minutes.

## Outputs
*   `OpenSearchDomainEndpoint`: The HTTPS endpoint for the OpenSearch cluster.
