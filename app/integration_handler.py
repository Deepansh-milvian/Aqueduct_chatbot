import json
import boto3
from prompt_handler import lambda_prompt_handler
from query_enricher import enrich_query
from sql_generator import lambda_sql_generator
from query_executor import lambda_query_execution
from response_formatter import lambda_response_formatter
from config import REGION, ANTHROPIC_MODEL, DATABASE_NAME
from prompts import system_prompt, general_query_enrichment_prompt
import logging

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

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

def lambda_handler(event, context):
    """
    Main function that integrates all steps.
    """

    # Retrieve the appropriate model
    foundation_models = bedrock.list_foundation_models()
    matching_model = next(
        (model for model in foundation_models["modelSummaries"] if model.get("modelName") == ANTHROPIC_MODEL),
        None
    )

    if not matching_model:
        return {"error": "Model not found."}

    model_id = matching_model["modelId"]
    
    # Step 1: Identify request type
    prompt_response = lambda_prompt_handler(event, context, model_id)
    logger.info("Full prompt response: %s", prompt_response)

    logger.info("Prompt response: %s", prompt_response.get("message", "No message available"))

    if prompt_response["type"] == "SQL":

        # Step 2: Enrich SQL Query
        enriched_prompt = enrich_query(prompt_response["request"], DATABASE_NAME)
        logger.info("SQL query enrichment using glue metadata is complete, %s", enriched_prompt)
        # Step 3: Generate SQL Query using sql_generator
        sql_query = lambda_sql_generator(enriched_prompt, bedrock_runtime, model_id)
        logger.info("SQL query generation complete, %s", sql_query)

        # Step 4: Execute SQL Query using query_executor
        query_response = lambda_query_execution({"sql_query": sql_query}, context)
        logger.info("Response to the query from Athena, %s", query_response)

        if "error" in query_response:
            return {"error": query_response["error"]}

        # Step 5: Format the response using response_formatter
        formatted_response = lambda_response_formatter(query_response["data"], bedrock_runtime, is_general=False, model_id=model_id)

        return {"response": formatted_response}

    elif prompt_response["type"] == "General":
        # Step 2: Enrich the General Query
        enriched_prompt = enrich_query(prompt_response["request"], DATABASE_NAME)

        # Step 3: Generate a response using response_formatter
        formatted_response = lambda_response_formatter(enriched_prompt, bedrock_runtime, is_general=True, model_id=model_id)
        # Step 4: Use the updated query to generate the final response
        enriched_prompt_with_context = f"System Context: {system_prompt}\nKeeping the above in mind, Answer the following general user question: {formatted_response}"
        # Bedrock payload
        body = json.dumps({
            "prompt": enriched_prompt_with_context,
            "maxTokens": 4000,
            "temperature": 0.7,
            "topP": 1
        })

        if not model_id:
            raise ValueError("Model ID is required for Bedrock invocation.")

        response = bedrock_runtime.invoke_model(
            body=body,
            modelId=model_id,
            accept="application/json",
            contentType="application/json"
        )

        response_body = json.loads(response.get("body").read())
        final_response = response_body.get("completions")[0].get("data").get("text", "")

        return {"Final LLM response": final_response}

    else:
        return {"error": "Invalid request type"}
