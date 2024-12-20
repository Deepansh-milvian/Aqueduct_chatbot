import boto3
import json
from query_enricher import enrich_query
from prompts import sql_query_enrichment_prompt
import re

def sanitize_sql_query(sql_query):
    """
    Cleans and validates the SQL query generated by the LLM.
    """
    # Remove leading and trailing whitespace
    sanitized_query = sql_query.strip()

    # Remove unwanted leading characters (e.g., extra ')')
    if sanitized_query.startswith(")"):
        sanitized_query = sanitized_query[1:].strip()

    # Ensure the query ends with a semicolon
    if not sanitized_query.endswith(";"):
        sanitized_query += ";"

    # Validate basic SQL structure (e.g., starts with SELECT or other keywords)
    if not re.match(r"^(SELECT|INSERT|UPDATE|DELETE|WITH|CREATE|DROP|ALTER)", sanitized_query, re.IGNORECASE):
        raise ValueError(f"Invalid SQL query: {sanitized_query}")

    return sanitized_query


def lambda_sql_generator(enriched_request, bedrock_runtime, model_id):
    """
    Generates SQL query tailored for Athena by enriching the request with context.

    :param enriched_request: The enriched request containing user query and metadata context.
    :param bedrock_runtime: Bedrock runtime client for invoking the LLM.
    :param model_id: The ID of the model to use for SQL query generation.
    :return: A generated SQL query.
    """
    enriched_request = sql_query_enrichment_prompt + '\n'+ enriched_request

    # Bedrock payload
    payload = {
        "prompt": enriched_request,
        "maxTokens": 4000,
        "temperature": 0.7,
        "topP": 1
    }

    try:
        # Call Bedrock to generate SQL query
        response = bedrock_runtime.invoke_model(
            modelId=model_id,
            body=json.dumps(payload),
            contentType="application/json"
        )

        response_payload = json.loads(response["body"].read().decode("utf-8"))
        sql_query = response_payload.get("completions")[0].get("data").get("text", "")
        sanitized_query = sanitize_sql_query(sql_query)
        return sanitized_query

    except Exception as e:
        raise Exception(f"Error generating SQL query: {str(e)}")
