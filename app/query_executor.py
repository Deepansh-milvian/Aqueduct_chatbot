import boto3
import os
import time
from botocore.exceptions import ClientError
from config import DATABASE_NAME, OUTPUT_BUCKET, REGION

# Load configuration
athena_client = boto3.client("athena", region_name=REGION)

def lambda_query_execution(event, context):
    """
    Executes the SQL query using Athena and retrieves results.
    """
    sql_query = event["sql_query"] +";"

    try:
        # Start the Athena query execution
        response = athena_client.start_query_execution(
            QueryString=sql_query,
            QueryExecutionContext={"Database": DATABASE_NAME},
            ResultConfiguration={"OutputLocation": OUTPUT_BUCKET},
        )

        query_execution_id = response["QueryExecutionId"]

        # Wait for the query to complete
        query_status = None
        while query_status not in ["SUCCEEDED", "FAILED", "CANCELLED"]:
            query_status_response = athena_client.get_query_execution(QueryExecutionId=query_execution_id)
            query_status = query_status_response["QueryExecution"]["Status"]["State"]

            if query_status == "FAILED":
                raise Exception("Athena query failed")

            if query_status == "CANCELLED":
                raise Exception("Athena query was cancelled")

            time.sleep(2)  # Wait before polling again

        # Fetch query results
        result_response = athena_client.get_query_results(QueryExecutionId=query_execution_id)
        rows = result_response.get("ResultSet", {}).get("Rows", [])

        # Parse the rows to extract data
        extracted_data = []
        headers = [col["VarCharValue"] for col in rows[0]["Data"]]
        for row in rows[1:]:
            extracted_data.append({
                headers[i]: row["Data"][i].get("VarCharValue", None) for i in range(len(headers))
            })

        return {"data": extracted_data}

    except ClientError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}
