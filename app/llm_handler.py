
###########
# Handles All LLM Interactions
###########

from anthropic import AnthropicBedrock
from app.prompts import SYSTEM_PROMPT_GENIE, ENRICH_GENERAL_QUERY_PROMPT, SQL_GENERATION_PROMPT

def enrich_general_query(anthropic_client, user_query):
    """
    Enriches a general query using Anthropic Claude.

    Args:
        anthropic_client: The Anthropic client instance.
        user_query (str): The user's natural language query.

    Returns:
        str: The enriched query.
    """
    prompt = ENRICH_GENERAL_QUERY_PROMPT.format(user_query=user_query)
    response = anthropic_client.messages.create(
        model="claude-v2",
        max_tokens=8192,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT_GENIE},
            {"role": "user", "content": prompt},
        ]
    )
    return response.get("completion", "").strip()

def generate_sql_query(anthropic_client, metadata, user_query):
    """
    Generates a schema-aware SQL query.

    Args:
        anthropic_client: The Anthropic client instance.
        metadata (dict): Schema metadata.
        user_query (str): The user's natural language query.

    Returns:
        str: The SQL query.
    """
    prompt = SQL_GENERATION_PROMPT.format(metadata_context=metadata, user_query=user_query)
    response = anthropic_client.messages.create(
        model="claude-v2",
        max_tokens=8192,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT_GENIE},
            {"role": "user", "content": prompt},
        ]
    )
    return response.get("completion", "").strip()
