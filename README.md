# Text Summarization with AWS Step Functions

A serverless text summarization service using AWS Step Functions, Bedrock (Claude), Polly, and WebSocket real-time notifications.

## Architecture

- **API Gateway**: REST endpoint for text submission
- **Step Functions**: Orchestrates the summarization workflow
- **Bedrock (Claude)**: AI text summarization
- **Polly**: Text-to-speech audio generation
- **WebSocket API**: Real-time progress notifications
- **DynamoDB**: Stores results and WebSocket connections
- **S3**: Audio file storage

## Features

- Real-time WebSocket notifications
- Audio summary generation
- Serverless architecture
- Automatic scaling
- Cost-effective pay-per-use

## Prerequisites

- AWS CLI configured
- AWS SAM CLI installed
- Python 3.11+
- Node.js (for WebSocket testing)

## Environment Setup

### 1. AWS Configuration

```bash
# Configure AWS credentials
aws configure
# Set your AWS Access Key ID, Secret Access Key, and region 
```

### 2. Required Environment Files

Create a `.env` file in the project root:

```bash
# API endpoints (will be populated after deployment)
WEBSOCKET_URI="wss://your-websocket-id.execute-api..."
API_URL="https://your-api-id.execute-api..."
```

### 3. SAM Configuration

Create `samconfig.toml` for deployment settings:

```toml
version = 0.1

[default.deploy.parameters]
stack_name = "your-stack-name"
s3_prefix = "your-stack-name"
resolve_s3 = true
capabilities = "CAPABILITY_IAM"
confirm_changeset = true
disable_rollback = false
region = "your-region"
```

### 4. Bedrock Model Access

Ensure Claude 3 Haiku model access in your AWS account:

```bash
# Check available models
aws bedrock list-foundation-models --region your-region
```

**Note**: Request access to Anthropic Claude models in AWS Bedrock console if needed.

## Quick Start

### 1. Deploy Infrastructure

```bash
sam build
sam deploy --guided
```

### 2. Test with Python

```python
workflow notebook


### 3. Environment Variables

Create `.env` file:
```
WEBSOCKET_URI=wss://your-websocket-url/
API_URL=https://your-api-gateway-url
```

## Project Structure

```
├── LICENSE                 # MIT License
├── README.md              # Project documentation
├── api.yaml               # API Gateway specification
├── template.yaml          # SAM CloudFormation template
├── summarization.asl.json # Step Functions state machine definition
├── workflow.ipynb         # Testing and demo notebook
└── src/                   # Lambda function source code
    ├── websocket-handler/ # WebSocket message sender
    │   └── index.py
    ├── on_connect/        # WebSocket connection handler
    │   └── index.py
    ├── on_disconnect/     # WebSocket disconnection handler
    │   └── index.py
    └── audio_link/        # S3 presigned URL generator
        └── index.py
```

## API Endpoints

- **POST** `/` - Submit text for summarization
- **WebSocket** `/` - Real-time notifications

## Configuration

- **Max tokens**: 500 (configurable in Step Functions)
- **Audio expiry**: 15 minutes
- **Supported models**: Claude 3 Haiku

## Cost Optimization

- Pay-per-request pricing
- Automatic resource cleanup
- S3 lifecycle policies (30-day deletion)

## Security

- IAM role-based access
- VPC endpoints supported
- No hardcoded credentials
- Presigned URLs for secure S3 access

## Monitoring

- CloudWatch logs for all components
- Step Functions execution history
- DynamoDB metrics
- API Gateway access logs

## License

MIT License