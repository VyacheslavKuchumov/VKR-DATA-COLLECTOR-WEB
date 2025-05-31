# app/db.py
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import Depends
from app.config import Settings

# Load MongoDB URI from your config
MONGO_DETAILS = Settings().MONGODB_URI  # e.g. "mongodb://localhost:27017"

# Create a single client instance
client = AsyncIOMotorClient(MONGO_DETAILS)

db = client.app_db
student_collection = db.get_collection("students")
region_collection = db.get_collection("regions")
hh_ru_credentials_collection = db.get_collection("hh_ru_credentials")
jobs_collection = db.get_collection("jobs")
