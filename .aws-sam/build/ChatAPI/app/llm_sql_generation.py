###########
# Leverages bedrock to generate context and schema aware SQL queries
###########

import boto3
import json
from app.config import DATABASE_NAME, REGION
from app.glue_metadata_extraction import fetch_metadata

# Create a Bedrock client
bedrock_client = boto3.client('bedrock', region_name=REGION)  # Replace 'your-region' with your AWS region

def enrich_sql_query(user_query):
    """
    Enriches a natural language query using AWS Bedrock and knowledge base metadata to generate a SQL query.

    Args:
        user_query (str): The user's natural language query.

    Returns:
        str: Enriched SQL query.
    """
    try:
        # Fetch metadata from Glue
        metadata = fetch_metadata(DATABASE_NAME)

        # Format the metadata for the prompt
        metadata_context = json.dumps(metadata, indent=2)

        # Define the prompt to provide schema/context information to Bedrock
        prompt = f"""
        You are a SQL expert. The user has asked the following question:

        "{user_query}"

        The data is stored in the database named '{DATABASE_NAME}', which includes the following schema metadata:

        {metadata_context}

        Generate an Athena-compatible SQL query that answers the user's question.
        Ensure the query uses the correct table and column names based on the provided schema metadata.
        Include filters or aggregation if required by the user query.
        """

        # Call the Bedrock API
        response = bedrock_client.invoke_model(
            modelId="amazon.titan-text",  # Replace with your chosen Bedrock model ID
            inputText=prompt,
            contentType="text/plain",
            accept="text/plain"
        )

        # Extract the response from Bedrock
        response_payload = response['body'].read().decode('utf-8')
        return response_payload.strip()

    except Exception as e:
        raise Exception(f"Failed to enrich query using Bedrock: {str(e)}")
