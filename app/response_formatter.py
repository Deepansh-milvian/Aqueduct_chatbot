import json
from prompts import system_prompt, sql_response_enrichment_prompt, general_query_enrichment_prompt

def lambda_response_formatter(data, bedrock_runtime, is_general=False, model_id=None):
    """
    Formats the response for the user using Bedrock for natural language generation.

    :param data: The input data to format (e.g., SQL query results or general enrichment data).
    :param bedrock_runtime: Bedrock runtime client for invoking the LLM.
    :param is_general: Boolean flag to indicate if the data is for a general query.
    :param model_id: The ID of the model to use for formatting (should match with Bedrock's available models).
    :return: A natural language formatted response.
    """
    if is_general:
        # Use general enrichment data for formatting with system prompt
        prompt = f"""
        {system_prompt}

        {general_query_enrichment_prompt}

        User query:
        {data}
        """
    else:
        # Use SQL query result data for formatting with system prompt
        prompt = f"""
        {system_prompt}

        {sql_response_enrichment_prompt}

        Query Results:
        {data}
        """

    # Bedrock payload
    body = json.dumps({
        "prompt": prompt,
        "maxTokens": 8000,
        "temperature": 0.7,
        "topP": 1
    })

    # Call Bedrock to format the response
    try:
        if not model_id:
            raise ValueError("Model ID is required for Bedrock invocation.")

        response = bedrock_runtime.invoke_model(
            body=body,
            modelId=model_id,
            accept="application/json",
            contentType="application/json"
        )

        response_body = json.loads(response.get("body").read())
        formatted_response = response_body.get("completions")[0].get("data").get("text", "")

        return formatted_response

    except Exception as e:
        return f"Error generating response: {str(e)}"
