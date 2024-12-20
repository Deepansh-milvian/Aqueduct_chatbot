
import json

def lambda_prompt_handler(event, context):
    """
    Handles user requests to determine if it's a SQL query or a general question.
    """
    user_request = event["request"]

    if "sql" in user_request.lower():
        response = {
            "type": "SQL",
            "message": "Processing SQL request",
            "request": user_request,
        }
    else:
        response = {
            "type": "General",
            "message": "Processing general question",
            "request": user_request,
        }

    return response
