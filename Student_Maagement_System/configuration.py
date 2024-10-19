import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the MongoDB link from environment variables
mongodb_link = os.getenv("MONGODB_LINK")

# Ensure that the MongoDB link is available
if not mongodb_link:
    raise ValueError("MONGODB_LINK environment variable not set.")

uri = mongodb_link

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

db = client.student_management_db
collection = db["student_data"]
