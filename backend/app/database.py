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

minstat_worker_collection = db.get_collection("minstat_workers")
hh_ru_dataset_collection = db.get_collection("hh_ru_dataset")
fgos_dataset_collection = db.get_collection("fgos_dataset")
kcp_dataset_collection = db.get_collection("kcp_dataset")
prof_standard_dataset_collection = db.get_collection("prof_standard_dataset")
classificator_prof_dataset_collection = db.get_collection("classificator_prof_dataset")
okved_dataset_collection = db.get_collection("okved_dataset")

hh_ru_api_data_collection = db.get_collection("hh_ru_api_data")
user_collection = db.get_collection("users")
data_source_collection = db.get_collection("data_sources")