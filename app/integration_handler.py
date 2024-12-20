import json
import boto3
from prompt_handler import lambda_prompt_handler
from query_enricher import enrich_query
from sql_generator import lambda_sql_generator
from query_executor import lambda_query_execution
from response_formatter import lambda_response_formatter
from app.config import REGION, ANTHROPIC_MODEL

# Initialize the Bedrock client for models
bedrock = boto3.client(
    service_name='bedrock',
    region_name=REGION
)

# Initialize the Bedrock runtime client
bedrock_runtime = boto3.client(
    service_name='bedrock-runtime',
    region_name=REGION
)

def lambda_integration_handler(event, context):
    """
    Main function that integrates all steps.
    """
    # Step 1: Identify request type
    prompt_response = lambda_prompt_handler(event, context)

    # Retrieve the appropriate model
    foundation_models = bedrock.list_foundation_models()
    matching_model = next(
        (model for model in foundation_models["modelSummaries"] if model.get("modelName") == ANTHROPIC_MODEL),
        None
    )

    if not matching_model:
        return {"error": "Model not found."}

    model_id = matching_model["modelId"]

    if prompt_response["type"] == "SQL":
        # Step 2: Enrich and Generate SQL Query
        database_name = "YourGlueDatabaseName"  # Replace with the actual database name
        enriched_prompt = enrich_query(prompt_response["request"], database_name)

        # Step 3: Generate SQL Query using sql_generator
        sql_query = lambda_sql_generator(enriched_prompt, bedrock_runtime, model_id)

        # Step 4: Execute SQL Query using query_executor
        query_response = lambda_query_execution({"sql_query": sql_query}, context)

        if "error" in query_response:
            return {"error": query_response["error"]}

        # Step 5: Format the response using response_formatter
        formatted_response = lambda_response_formatter(query_response["data"], bedrock_runtime, is_general=False, model_id=model_id)

        return {"response": formatted_response}

    elif prompt_response["type"] == "General":
        # Step 2: Enrich the General Query
        enriched_prompt = enrich_query(prompt_response["request"], "General")

        # Step 3: Generate a response using response_formatter
        formatted_response = lambda_response_formatter(enriched_prompt, bedrock_runtime, is_general=True, model_id=model_id)

        return {"response": formatted_response}

    else:
        return {"error": "Invalid request type"}
