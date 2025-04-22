from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("ATLAS_URI"))
db = client["todo_db"]
todo_collection = db["todos"]
