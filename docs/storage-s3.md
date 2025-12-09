# Storage S3 Stack (`storage-s3.yaml`)

## Overview
This stack creates **Amazon S3 Buckets** for storing static assets and data.

## Resources Created

### 1. Client UI Bucket (`ClientUIBucket`)
*   **Purpose**: Hosts the frontend web application.
*   **Configuration**:
    *   Static Website Hosting enabled (`index.html`).
    *   **Public Access**: Policy allows `s3:GetObject` for everyone (standard for public static sites).

### 2. Knowledge Base Source Bucket (`KnowledgeBaseSourceBucket`)
*   **Purpose**: Stores source documents (PDFs, txt) for the RAG (Retrieval Augmented Generation) knowledge base.
*   **Configuration**:
    *   Versioning enabled.
    *   Server-side encryption (AES256) enabled.

## Outputs
*   `ClientUIBucketWebsiteURL`: The URL to access the hosted website.
*   `KnowledgeBaseSourceBucketName`: The name of the KB source bucket.
