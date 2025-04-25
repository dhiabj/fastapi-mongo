from fastapi import APIRouter
from config.database import job_collection
from schema.job import list_serial

router = APIRouter()


@router.get("/jobs")
async def get_jobs():
    jobs_list = await job_collection.find().to_list(length=None)  # Fetch all documents
    jobs = list_serial(jobs_list)  # Serialize the list
    return jobs
