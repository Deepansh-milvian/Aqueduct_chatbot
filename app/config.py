import os

# Access environment variables
DATABASE_NAME = os.environ.get("DATABASE_NAME")
OUTPUT_BUCKET = os.environ.get("OUTPUT_BUCKET")
REGION = os.environ.get("REGION")
AGENT_ID = os.environ.get("AGENT_ID")