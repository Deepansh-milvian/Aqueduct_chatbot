import boto3
import os
from config import REGION
# Load configuration

glue_client = boto3.client("glue", region_name=REGION)

def fetch_metadata_from_glue(database_name):
    """Fetch metadata context from Glue Catalog."""
    try:
        response = glue_client.get_tables(DatabaseName=database_name)
        tables = response.get("TableList", [])
        metadata_context = []
        for table in tables:
            table_name = table.get("Name")
            columns = table.get("StorageDescriptor", {}).get("Columns", [])
            column_details = " | ".join([col["Name"] + "(" + col["Type"] + ")" for col in columns])
            metadata_context.append(f"Table: {table_name}\nColumns: {column_details}")
        return "\n\n".join(metadata_context)
    except Exception as e:
        return f"Error retrieving metadata from Glue: {str(e)}"

def enrich_query(user_request, database_name):
    """Enrich user query with metadata context from Glue."""
    glue_context = fetch_metadata_from_glue(database_name)
    enriched_query = f"""
    User Request: {user_request}

    Glue Metadata: This contains the table names, schema and other information.
    {glue_context}
    """
    return enriched_query
