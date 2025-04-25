from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

client = AsyncIOMotorClient(os.getenv("ATLAS_URI"))
db = client["todo_db"]
todo_collection = db["todos"]
job_collection = db["jobs"]
