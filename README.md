# AQUEBOT

This project handles user queries through a serverless architecture using AWS services such as Lambda, Bedrock, Athena, and Glue. The workflow processes SQL-based and general queries, enriches them with metadata, executes SQL queries in Athena, and formats responses using Bedrock LLMs.

---

## **Architecture Overview**

1. **Integration Handler**:
   - Identifies query type (SQL or General).
   - Coordinates the query processing flow.

2. **SQL Generator**:
   - Generates SQL queries tailored for Athena using enriched user prompts.

3. **Query Enricher**:
   - Fetches metadata from the Glue catalog.
   - Enriches user queries with context.

4. **Query Executor**:
   - Executes SQL queries in Athena.
   - Retrieves and formats query results.

5. **Response Formatter**:
   - Converts query results or general query responses into user-friendly natural language.

6. **Prompts**:
   - Centralized storage for system and task-specific prompts.

---

## **Deployment**

### Prerequisites
- AWS account with permissions for Lambda, Athena, Glue, and Bedrock.
- S3 bucket for Athena query results.
- Python 3.x environment.

### Steps
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Configure AWS credentials:
   ```bash
   aws configure
   ```

3. Deploy the Lambda functions:
   - Package each module (`integration_handler`, `sql_generator`, `response_formatter`, etc.) as a separate Lambda function.
   - Assign appropriate IAM roles with necessary permissions for Glue, Athena, and Bedrock.

4. Set environment variables:
   - `REGION`: AWS region (e.g., `us-east-1`).
   - `ANTHROPIC_MODEL`: Model name for Bedrock LLM (e.g., `anthropic.claude-v2`).

5. Test the Lambda function using the provided sample events.

---

## **Sample Event Bodies**

### SQL Query Event
```json
{
  "request": "Fetch all active devices"
}
```

### General Query Event
```json
{
  "request": "Tell me something about Aqueduct"
}
```

---

## **Modules**

### **Integration Handler**
- **Purpose**: Coordinates query handling.
- **Input**: User query (SQL or general).
- **Output**: Final formatted response.
- **Key Functions**:
  - `lambda_integration_handler`: Main entry point.

### **SQL Generator**
- **Purpose**: Generates SQL queries using LLM.
- **Input**: Enriched user query.
- **Output**: SQL query tailored for Athena.

### **Query Enricher**
- **Purpose**: Enriches queries with metadata from Glue.
- **Input**: User query and database/catalog name.
- **Output**: Enriched query string.

### **Query Executor**
- **Purpose**: Executes SQL queries in Athena.
- **Input**: SQL query.
- **Output**: Extracted rows from Athena.

### **Response Formatter**
- **Purpose**: Converts query results or general queries into natural language.
- **Input**: Query results or general query.
- **Output**: User-friendly response string.

### **Prompts**
- **Purpose**: Stores system and task-specific prompts.
- **Files**: `prompts.py`.

---

## **Testing**

### Lambda Console Testing
1. Open the Lambda function in the AWS Management Console.
2. Click on **Test**.
3. Paste a sample event body (SQL or General) into the event input.
4. Run the test to validate functionality.

### Local Testing
- Use the `boto3` library to invoke Lambda functions locally.
- Mock responses for Bedrock, Glue, and Athena for unit testing.

---

## **Logging and Monitoring**
- Use AWS CloudWatch for monitoring Lambda execution.
- Log structured error messages for debugging.

---

## **Future Enhancements**
- Add support for multi-table metadata enrichment.
- Optimize SQL generation using prompt fine-tuning.
- Enhance error handling and retry mechanisms for Bedrock and Athena API calls.

---

## **Contact**
For questions or contributions, please reach out to the project maintainer.

