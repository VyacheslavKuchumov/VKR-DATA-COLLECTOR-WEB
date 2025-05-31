import uuid
import asyncio
from pathlib import Path
from datetime import datetime

from fastapi import BackgroundTasks, HTTPException
from app.database import jobs_collection
from app.websocket.connectionManager import manager
from app.models.job_model import JobModel

async def run_and_stream(job_id: str):
    """
    Actually launches the external script, streams its stdout/stderr
    over websockets, and updates the Mongo document status.
    """
    # 1) mark as running
    await jobs_collection.update_one(
        {"job_id": job_id},
        {"$set": {"status": "running"}}
    )

    # 1) locate your script file:
    BASE_DIR = Path(__file__).resolve().parent.parent  # e.g. /path/to/app
    script_path = BASE_DIR / "scripts" / "test_job.py"

    if not script_path.exists():
        # fail fast if someone mis-named it
        await manager.broadcast(job_id, f"❌ Script not found: {script_path}")
        return

    # 2) launch the subprocess with full path
    process = await asyncio.create_subprocess_exec(
        "python",
        str(script_path),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
        cwd=str(BASE_DIR)           # optional: set working dir
    )

    # 3) stream its output exactly as before
    while True:
        line = await process.stdout.readline()
        if not line:
            break
        await manager.broadcast(job_id, line.decode().rstrip())

    # 4) wrap up
    exit_code = await process.wait()
    now = datetime.utcnow()
    await jobs_collection.update_one(
        {"job_id": job_id},
        {"$set": {
            "status": "finished",
            "finished_at": now,
            "exit_code": exit_code
        }}
    )

    final_msg = f"[{job_id}] exited with code {exit_code}"
    await manager.broadcast(job_id, final_msg)
    manager.cleanup(job_id)


async def create_job(background_tasks: BackgroundTasks) -> JobModel:
    """
    Creates a pending Job document, schedules the background task,
    and returns the freshly-inserted JobModel.
    """
    job_id = str(uuid.uuid4())
    now = datetime.utcnow()

    # insert initial record
    await jobs_collection.insert_one({
        "job_id": job_id,
        "status": "pending",
        "created_at": now,
        "finished_at": None,
        "exit_code": None
    })

    # schedule the runner
    background_tasks.add_task(run_and_stream, job_id)

    # fetch & return
    raw = await jobs_collection.find_one({"job_id": job_id})
    return JobModel(**raw)


async def list_jobs() -> list[JobModel]:
    """
    Returns up to 100 most recent jobs, newest first.
    """
    cursor = jobs_collection.find().sort("created_at", -1)
    docs = await cursor.to_list(length=100)
    return [JobModel(**doc) for doc in docs]


async def get_job(job_id: str) -> JobModel:
    """
    Fetches a single Job by its UUID; 404 if missing.
    """
    raw = await jobs_collection.find_one({"job_id": job_id})
    if not raw:
        raise HTTPException(status_code=404, detail="Job not found")
    return JobModel(**raw)
