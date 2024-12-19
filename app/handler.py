###########
# Entry point for the application. 
# Handles the api POST request and returns a response from bedrock.
###########


import json
from app.llm_sql_generation import enrich_sql_query
from app.llm_gq_generation import enrich_general_query
from app.athena import execute_query
from app.response import format_response
from app.athena import is_athena_query
from app.general_query_handler import handle_general_query


# def lambda_handler(event, context):
#     try:
#         # Parse the input request
#         request_body = json.loads(event["body"])
#         user_query = request_body.get("query")

#         if not user_query:
#             return {
#                 "statusCode": 400,
#                 "body": json.dumps({"error": "Query is required"})
#             }
def lambda_handler(user_query):
    try:
        # Identify query intent (Athena-related or General)
        if is_athena_query(user_query):
            # Athena-related query workflow
            enriched_query = enrich_sql_query(user_query)  # Use LLM to generate SQL
            print("query enriched")
            query_results = execute_query(enriched_query)  # Execute the SQL in Athena
            response = format_response(query_results)  # Generate a natural language response
        else:
            # General knowledge base query workflow
            enriched_gq_query = enrich_general_query(user_query)
            response = handle_general_query(enriched_gq_query)

        return {
            "statusCode": 200,
            "body": json.dumps({"response": response})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }



user_query = "What is the total number of devices deployed currently?"
response = lambda_handler(user_query)
print(response)
