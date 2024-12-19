
###########
# Handles Glue and Athena Interactions
###########

import boto3

def fetch_metadata(glue_client, database_name):
    """
    Fetches schema metadata from the AWS Glue Data Catalog.

    Args:
        glue_client: Boto3 Glue client.
        database_name (str): The name of the Glue database containing the tables.

    Returns:
        dict: Metadata containing table and column information.
    """
    tables = glue_client.get_tables(DatabaseName=database_name)['TableList']
    metadata = {table['Name']: [col['Name'] for col in table['StorageDescriptor']['Columns']] for table in tables}
    return metadata
