import boto3
from app.config import REGION
# Create a Glue client
glue_client = boto3.client('glue', region_name=REGION)  # Replace 'your-region' with your AWS region

def fetch_metadata(database_name):
    """
    Fetches schema metadata from the AWS Glue Data Catalog.

    Args:
        database_name (str): The name of the Glue database containing the tables.

    Returns:
        dict: Metadata containing table and column information.
    """
    try:
        # Fetch the list of tables in the Glue database
        tables = glue_client.get_tables(DatabaseName=database_name)
        metadata = {}

        for table in tables['TableList']:
            table_name = table['Name']
            columns = table['StorageDescriptor']['Columns']

            # Parse column metadata
            metadata[table_name] = {
                "columns": [
                    {"name": col['Name'], "type": col['Type'], "comment": col.get('Comment', '')}
                    for col in columns
                ],
                "description": table.get('Description', ''),
                "location": table['StorageDescriptor'].get('Location', '')
            }

        return metadata

    except Exception as e:
        raise Exception(f"Failed to fetch metadata from Glue Data Catalog: {str(e)}")
