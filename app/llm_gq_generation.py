###########
# Leverages bedrock to generate context and schema aware SQL queries
###########

import boto3
import json
from app.config import DATABASE_NAME, REGION
from app.glue_metadata_extraction import fetch_metadata

# Create a Bedrock client
bedrock_client = boto3.client('bedrock', region_name=REGION)  # Replace 'your-region' with your AWS region

def enrich_general_query(user_query):
    """
    Enriches a general query using AWS Bedrock Foundation Model for clearer, context-rich refinement.

    Args:
        user_query (str): The user's natural language query.

    Returns:
        str: The enriched query with added clarity and context.
    """
    try:
        # Define the prompt for query enrichment
        prompt = f"""
User Query: "{user_query}"

Context: Refine this query to make it clearer, context-rich, and concise for a product expert to understand. 
Focus on ensuring the query is direct, unambiguous, and actionable.
        """

        # Invoke Bedrock FM to enrich the query
        response = bedrock_client.invoke_model(
            modelId="amazon.titan-text",  # Replace with the appropriate Bedrock model ID
            inputText=prompt,
            contentType="text/plain",
            accept="text/plain"
        )

        # Extract the enriched query from Bedrock's response
        enriched_query = response['body'].read().decode('utf-8')
        return enriched_query.strip()

    except Exception as e:
        raise Exception(f"Failed to enrich general query using Bedrock: {str(e)}")
