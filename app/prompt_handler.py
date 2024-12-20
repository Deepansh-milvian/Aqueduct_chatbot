import json
import boto3
from config import REGION

# Initialize the Bedrock runtime client
bedrock_runtime = boto3.client(
    service_name='bedrock-runtime',
    region_name=REGION
)

def lambda_prompt_handler(event, context, model_id):
    """
    Handles user requests to determine if it's a SQL query or a general question by sending it to Bedrock.
    """
    user_request = event.get("request", "").strip()

    if not user_request:
        return {"error": "No query provided in the request."}

    # Prepare the prompt for Bedrock
    prompt = f"""
    You are an intelligent query specialist that identifies the type of user query. Please classify the following query into one of two categories:
    - "SQL" if it is a database-related question or includes SQL-like syntax.
    - "General" if it is a general question that does not require database operations.

    Query:
    {user_request}

    Respond with just "SQL" or "General".
    """

    body = json.dumps({
        "prompt": prompt,
        "maxTokens": 100,
        "temperature": 0.0
    })

    try:
        # Call Bedrock to classify the query
        response = bedrock_runtime.invoke_model(
            body=body,
            modelId=model_id,
            accept="application/json",
            contentType="application/json"
        )

        # Parse the response
        response_body = json.loads(response.get("body").read())
        completions = response_body.get("completions", [])
        
        if not completions:
            return {"error": "No completions received from Bedrock."}

        query_type = completions[0].get("data", {}).get("text", "").strip()

        if query_type == "SQL":
            return {
                "type": "SQL",
                "message": "Processing SQL request",
                "request": user_request,
            }
        elif query_type == "General":
            return {
                "type": "General",
                "message": "Processing general question",
                "request": user_request,
            }
        else:
            return {"error": f"Unexpected classification result: {query_type}"}

    except Exception as e:
        return {"error": f"Error classifying query: {str(e)}"}
