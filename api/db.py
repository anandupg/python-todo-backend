from pymongo import MongoClient
from django.conf import settings
import sys

if not settings.MONGO_URI:
    print("CRITICAL ERROR: MONGO_URI is not set in environment or settings.py!", file=sys.stderr)
    # Don't raise error immediately to allow collecting static, but warn loudly
    client = None
    db = None
    todos_collection = None
else:
    try:
        print(f"Connecting to MongoDB...", file=sys.stderr)
        client = MongoClient(settings.MONGO_URI)
        # Send a ping to confirm a successful connection
        client.admin.command('ping')
        print("Successfully connected to MongoDB!", file=sys.stderr)
        
        db = client['todo_db']
        todos_collection = db['todos']
    except Exception as e:
        print(f"ERROR: Could not connect to MongoDB: {e}", file=sys.stderr)
        client = None
        db = None
        todos_collection = None
