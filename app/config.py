import os

# Access environment variables
# DATABASE_NAME = os.environ.get("DATABASE_NAME")
# OUTPUT_BUCKET = os.environ.get("OUTPUT_BUCKET")
# REGION = os.environ.get("REGION")
# AGENT_ID = os.environ.get("AGENT_ID")

DATABASE_NAME = "aqueduct-genai-database"
OUTPUT_BUCKET = "s3://aqueduct-athena-query-results/"
REGION = "us-east-1"
AGENT_ID = "ETVT5IQBBJ"
ANTHROPIC_MODEL = "anthropic.claude-3-5-sonnet-20240620-v1:0"