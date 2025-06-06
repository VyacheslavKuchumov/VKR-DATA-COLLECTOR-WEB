from fastapi import APIRouter, BackgroundTasks
from typing import List

from app.controllers.job_controller import create_job, list_jobs, get_job, delete_job
from app.models.job_model import JobModel, CreateJobModel

router = APIRouter()


@router.post("/", response_model=JobModel)
async def post_job(background_tasks: BackgroundTasks, data: CreateJobModel):
    """
    Start a new background job; returns the Job record (including created_at).
    """
    return await create_job(background_tasks, data)


@router.get("/", response_model=List[JobModel])
async def get_jobs():
    """
    List recent jobs, newest first.
    """
    return await list_jobs()


@router.get("/{job_id}", response_model=JobModel)
async def get_single_job(job_id: str):
    """
    Fetch a single job by its job_id.
    """
    return await get_job(job_id)

@router.delete("/{job_id}", status_code=204)
async def delete_single_job(job_id: str):
    """
    Delete a job by its job_id.
    """
    return await delete_job(job_id)
