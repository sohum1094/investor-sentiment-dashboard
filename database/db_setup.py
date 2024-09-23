from pymongo import MongoClient
import os

client = MongoClient(os.getenv('DATABASE_URL'))
db = client['sentiment_dashboard']

def init_db():
    # Create necessary collections
    db.create_collection("companies")
    db.create_collection("sentiments")
