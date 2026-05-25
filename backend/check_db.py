import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
client = MongoClient(os.getenv('MONGO_URI'))
db = client.get_database()
print("Database name:", db.name)
print("Collections:", db.list_collection_names())
print("Mentor count:", db.users.count_documents({"role": "mentor"}))

# Show one mentor if exists
mentor = db.users.find_one({"role": "mentor"})
if mentor:
    print("Sample mentor:", mentor.get('name'), mentor.get('email'))
else:
    print("No mentors found.")