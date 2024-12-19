
# Aqueduct Chatbot

This project provides a simplified and refactored version of the application for interacting with AWS services (Glue, Athena) and Anthropic's Claude model using Bedrock.

## Directory Structure

```
app/
├── config.py                  # Configuration settings
├── handler.py                 # Entry point (Lambda handler)
├── prompts.py                 # Centralized prompts
├── llm_handler.py             # Handles all LLM interactions
├── utils.py                   # General-purpose utilities (Glue, Athena, and authentication)
```

### File Descriptions

1. **config.py**
   - Contains configuration settings such as AWS region and database name.

2. **handler.py**
   - The main Lambda handler that orchestrates API requests and responses.

3. **prompts.py**
   - Centralized file for managing all prompts used in the application. This ensures consistency and easier maintenance.

4. **llm_handler.py**
   - Handles all interactions with Anthropic Claude via Bedrock.
   - Functions:
     - `enrich_general_query`: Refines user queries.
     - `generate_sql_query`: Generates schema-aware SQL queries.

5. **utils.py**
   - Provides general-purpose utilities for the app.
   - Functions:
     - `fetch_metadata`: Extracts schema metadata from AWS Glue.
     - `hash_password`: Hashes passwords using Argon2.

## Features

- **Centralized Prompts**:
  - All prompts are managed in `prompts.py` to ensure consistency.

- **LLM Interactions**:
  - Generates natural language and SQL responses using Anthropic Claude.

- **Glue and Athena Integration**:
  - Fetches schema metadata from AWS Glue.
  - Uses metadata to generate Athena-compatible SQL queries.

- **Simplified Structure**:
  - Consolidated files for better maintainability and scalability.

## Prerequisites

- Python 3.9 or later
- Required Python Packages:
  ```bash
  pip install boto3 anthropic argon2-cffi
  ```
- AWS CLI configured with credentials and proper permissions.

## Environment Variables

Ensure the following environment variables are set:

- `AWS_REGION`: The AWS region where Glue and Bedrock services are deployed.
- `DATABASE_NAME`: The Glue database name.

## Usage

### Running Locally

1. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python handler.py
   ```

### Deploying to AWS Lambda

1. Package the application:
   ```bash
   zip -r app.zip .
   ```

2. Deploy using the AWS CLI:
   ```bash
   aws lambda create-function      --function-name YourFunctionName      --runtime python3.9      --role YourIAMRoleARN      --handler handler.lambda_handler      --zip-file fileb://app.zip
   ```

## Testing

### Example Queries

- **General Query Enrichment**:
  ```python
  from app.llm_handler import enrich_general_query
  query = "What is the total revenue for last month?"
  result = enrich_general_query(anthropic_client, query)
  print(result)
  ```

- **SQL Generation**:
  ```python
  from app.llm_handler import generate_sql_query
  metadata = {"sales_data": ["region", "sales", "date"]}
  query = "What is the total sales grouped by region?"
  result = generate_sql_query(anthropic_client, metadata, query)
  print(result)
  ```

## License

This project is licensed under the MIT License.
