# AWS-POC

## Description
This repository contains a proof of concept (POC) for an AWS-based workflow. The workflow demonstrates how to handle document uploads, generate signed URLs, and store data in DynamoDB using various AWS services such as API Gateway, Lambda, S3, and SQS.

## Workflow Overview
1. **Frontend to API Gateway**: The frontend (Angular App) connects with API Gateway.
2. **API Gateway to Lambda**: Data is sent to AWS Lambda.
3. **Lambda to S3**: Lambda uploads the document file to S3.
4. **Generate Signed URL**: S3 generates a signed URL for the uploaded document.
5. **Return Signed URL to Lambda**: The signed URL is returned to Lambda.
6. **Send to SQS**: Lambda sends the unique ID, system prompt, and signed URL to an SQS queue.
7. **SQS to DynamoDB**: Another Lambda function (triggered by SQS) reads the message from the queue and stores the data in DynamoDB.

## Detailed Workflow
1. **Frontend (Angular App)**: Sends `companyName`, `prompt`, and `document` to API Gateway.
2. **API Gateway**: Triggers the Lambda function.
3. **Lambda Function**:
   - Generates a unique ID.
   - Uploads the document to S3.
   - Retrieves a pre-signed URL for the uploaded document.
   - Sends the unique ID, `companyName`, `prompt`, and pre-signed URL to DynamoDB via SQS.


