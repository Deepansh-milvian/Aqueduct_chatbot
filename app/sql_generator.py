import boto3
import json
from query_enricher import enrich_query

def lambda_sql_generator(enriched_request, bedrock_runtime, model_id):
    """
    Generates SQL query tailored for Athena by enriching the request with context.

    :param enriched_request: The enriched request containing user query and metadata context.
    :param bedrock_runtime: Bedrock runtime client for invoking the LLM.
    :param model_id: The ID of the model to use for SQL query generation.
    :return: A generated SQL query.
    """
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

        return sql_query

    except Exception as e:
        raise Exception(f"Error generating SQL query: {str(e)}")
