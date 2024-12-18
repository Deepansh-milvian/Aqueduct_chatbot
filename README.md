---

# **AQUEDUCT - CONTEXT AND SCHEMA AWARE CHATBOT**

This project provides an application layer to process user chat requests, generate SQL queries, execute them in Amazon Athena, and return natural language responses using AWS Bedrock.

---

## **Features**

- **Unified Schema Querying**: Supports querying unified data from DynamoDB and Timestream via Athena.
- **Natural Language Processing**: Leverages AWS Bedrock to interpret user queries and generate conversational responses.
- **API Integration**: Exposes an API endpoint using AWS Lambda and API Gateway for real-time interactions.

---

## **Architecture**

### **1. Components**
- **API Gateway**: Handles HTTP requests from users.
- **AWS Lambda**: Acts as the application layer to:
  - Interpret user queries.
  - Interact with AWS Bedrock for SQL query generation.
  - Execute SQL queries in Athena.
  - Use Bedrock to format results into natural language responses.
- **AWS Glue**: Provides metadata for the database schema via Crawlers.
- **Amazon Athena**: Executes SQL queries on unified data.
- **AWS Bedrock**: Generates natural language responses.

### **2. Workflow**

1. User sends a natural language query to the API.
2. Lambda processes the query and uses Bedrock to generate a context-aware SQL query.
3. SQL query is executed in Athena.
4. Results from Athena are sent back to Bedrock to generate a conversational response.
5. Lambda returns the response to the user.

---

## **Setup Instructions**

### **1. Prerequisites**
- AWS account with the following services set up:
  - **Glue**: Crawlers for metadata collection.
  - **Athena**: Query engine for unified data.
  - **Bedrock**: LLM service for query enrichment and response generation.
- Python 3.9+ installed locally.
- AWS CLI configured with appropriate IAM permissions:
  - `glue:GetTables`
  - `athena:StartQueryExecution`
  - `athena:GetQueryExecution`
  - `athena:GetQueryResults`
  - `bedrock:InvokeModel`

### **2. Clone the Repository**
```bash
git clone <repository-url>
cd <repository-folder>
```

### **3. Install Dependencies**
Install the required Python dependencies:
```bash
pip install -r requirements.txt
```

### **4. Configure the Project**
Update the `config.py` file with your AWS settings:
```python
DATABASE_NAME = "your_glue_database"
OUTPUT_BUCKET = "s3://your-athena-output-bucket/"
REGION = "your-region"
AGENT_ID = "your-bedrock-agent-id
```

### **5. Deploy the Application**
Deploy the project using AWS SAM:
1. **Build**:
    ```bash
    sam build
    ```
2. **Deploy**:
    ```bash
    sam deploy --guided
    ```

---

## **API Documentation**

### **Endpoint**
```
POST /chat
```

### **Request**
- **Headers**:
  - `Content-Type: application/json`
- **Body**:
```json
{
  "query": "What is the average temperature in Room A over the last week?"
}
```

### **Response**
- **Success (200)**:
```json
{
  "response": "The average temperature in Room A over the last week is 22.5°C."
}
```
- **Error (400 or 500)**:
```json
{
  "error": "Error message detailing what went wrong."
}
```

---

## **Project Structure**

```
project/
├── app/
│   ├── handler.py              # Lambda function handler
│   ├── athena.py               # Athena query execution logic
│   ├── llm_sql_generation.py      # LLM query enrichment
│   ├── llm_response_generation.py # Bedrock response generation
│   ├── response.py             # Parsing and formatting responses
│   ├── glue_metadata_extraction.py       # Fetch metadata from Glue
│   └── config.py               # Configuration settings
│   └── llm_gq_generation.py    # LLM general query generator
│   └── general_query_handler.py    # Handles general user queries
├── tests/
│   ├── test_handler.py         # Tests for handler.py
│   ├── test_athena.py          # Tests for athena.py
│   ├── test_llm.py             # Tests for llm_integration.py
│   ├── test_response.py        # Tests for response.py
│   └── test_knowledge_base.py  # Tests for knowledge_base.py
├── requirements.txt            # Python dependencies
├── template.yaml               # AWS SAM template for deployment
└── README.md                   # Project documentation
```

---

## **Testing**

### **Run Unit Tests**
Run the included unit tests to verify functionality:
```bash
pytest tests/
```

### **Test the API**
Use tools like Postman or `curl` to test the API.

Example:
```bash
curl -X POST https://<api-gateway-url>/chat \
-H "Content-Type: application/json" \
-d '{"query": "What is the average temperature in Room A over the last week?"}'
```

---

## **Future Enhancements**
1. **Multi-Language Support**:
   - Support queries in multiple languages using Bedrock's multilingual capabilities.
2. **Enhanced Security**:
   - Implement API Gateway authorization (e.g., AWS Cognito).
3. **Scalability**:
   - Add caching for frequently executed queries to reduce latency.
4. **Analytics**:
   - Log query patterns for user behavior analysis.

---

## **License**
This project is licensed under the MIT License. See the LICENSE file for details.

---