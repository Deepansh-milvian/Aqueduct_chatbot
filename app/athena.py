import boto3
import time
from app.config import REGION, DATABASE_NAME, OUTPUT_BUCKET

athena_client = boto3.client('athena')


def execute_query(query):
    response = athena_client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={"Database": DATABASE_NAME},
        ResultConfiguration={"OutputLocation": OUTPUT_BUCKET}
    )
    query_execution_id = response["QueryExecutionId"]
    
    status = "RUNNING"
    while status in ["RUNNING", "QUEUED"]:
        response = athena_client.get_query_execution(QueryExecutionId=query_execution_id)
        status = response["QueryExecution"]["Status"]["State"]
        if status in ["SUCCEEDED", "FAILED", "CANCELLED"]:
            break
        time.sleep(1)
    
    if status == "SUCCEEDED":
        result_response = athena_client.get_query_results(QueryExecutionId=query_execution_id)
        return result_response["ResultSet"]["Rows"]
    else:
        raise Exception(f"Query failed with status: {status}")
    
    
def is_athena_query(query):
    """
    Identifies whether a query is related to Athena by matching SQL-related keywords
    and phrases that indicate structured query requests.

    Args:
        query (str): The user's query.

    Returns:
        bool: True if the query is Athena-related, otherwise False.
    """
    # Common SQL keywords and operations
    sql_keywords = [
        "select", "from", "where", "join", "group by", "order by", "limit",
        "sum", "average", "avg", "count", "min", "max", "distinct",
        "union", "intersect", "except", "having", "offset"
    ]

    # Data-related phrases indicating potential Athena queries
    data_phrases = [
        "show me", "find the", "list all", "how many", "get the",
        "query the", "calculate", "compare", "summarize", "total", "filter"
    ]

    # Convert query to lowercase for case-insensitive matching
    query_lower = query.lower()

    # Check for any SQL-related keywords or data-related phrases
    if any(keyword in query_lower for keyword in sql_keywords):
        return True
    if any(phrase in query_lower for phrase in data_phrases):
        return True

    # If no match, assume it is not an Athena-related query
    return False
