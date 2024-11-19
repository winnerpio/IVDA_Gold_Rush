from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://olympic:gold@olympiccluster.yxmi4.mongodb.net/"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["olympic_db"]
collection = db["athletes"]

try:
    # Insert multiple documents
    multiple_docs = [
        {"id": 1, "name": "Alice", "age": 25, "sport": "Tennis"},
        {"id": 2, "name": "Bob", "age": 32, "sport": "Basketball"},
        {"id": 3, "name": "Charlie", "age": 18, "sport": "Football"}
    ]
    result_many = collection.insert_many(multiple_docs)
    print(f"Inserted document IDs: {result_many.inserted_ids}")

except Exception as e:
    print(f"An error occurred: {e}")