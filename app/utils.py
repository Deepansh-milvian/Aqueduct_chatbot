
###########
# General-Purpose Utilities (Glue, Athena, and Authentication)
###########

import boto3
from argon2 import PasswordHasher

# Glue Metadata Extraction
def fetch_metadata(database_name):
    """
    Fetches schema metadata from the AWS Glue Data Catalog.

    Args:
        database_name (str): The name of the Glue database containing the tables.

    Returns:
        dict: Metadata containing table and column information.
    """
    glue_client = boto3.client('glue')
    tables = glue_client.get_tables(DatabaseName=database_name)['TableList']
    metadata = {table['Name']: [col['Name'] for col in table['StorageDescriptor']['Columns']] for table in tables}
    return metadata

# Password Hashing Utility
def hash_password(password):
    """
    Hashes a password using Argon2.

    Args:
        password (str): The password to hash.

    Returns:
        str: The hashed password.
    """
    hasher = PasswordHasher()
    return hasher.hash(password)
