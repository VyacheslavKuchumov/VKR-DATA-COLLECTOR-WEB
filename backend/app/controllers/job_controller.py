# app/controllers/job_controller.py

import uuid
import asyncio
import builtins
from pathlib import Path
from datetime import datetime
from fastapi.responses import Response
from fastapi import BackgroundTasks, HTTPException, status
from app.database import jobs_collection, hh_ru_api_data_collection
from app.websocket.connectionManager import manager
from app.models.job_model import JobModel, CreateJobModel
from app.scripts.hh_ru_scrape import ApiHhRu


async def run_and_stream(raw_job):
    """
    Runs ApiHhRu.fetch_and_store_vacancies() in a background thread,
    captures each print() into an asyncio.Queue, then in the async context
    broadcasts & logs each line in real time, and finally updates the job status.
    """
    # 1) mark as running
    await jobs_collection.update_one(
        {"job_id": raw_job.job_id},
        {"$set": {"status": "running"}}
    )

    # 2) set up a queue to shuttle lines from the thread into async land
    q: asyncio.Queue[str] = asyncio.Queue()
    loop = asyncio.get_running_loop()

    # 3) hijack print() in the worker thread to put lines into the queue
    orig_print = builtins.print

    def intercept_print(*args, **kwargs):
        line = " ".join(str(a) for a in args)
        # thread-safe enqueue
        loop.call_soon_threadsafe(q.put_nowait, line)
        # still print to server console
        orig_print(f"[{raw_job.job_id}]", line)

    builtins.print = intercept_print

    hh_ru_scraper = ApiHhRu(
        areas=raw_job.region['region_name'],
        token=raw_job.credentials['HH_RU_ACCESS_TOKEN'],
        collection=hh_ru_api_data_collection
    )

    # 4) schedule the blocking fetch in a separate thread
    worker_task = asyncio.create_task(
        asyncio.to_thread(hh_ru_scraper.fetch_and_store_vacancies)
    )

    exit_code = 0

    try:
        # 5) as long as the thread is running or there are queued lines,
        #    pull from the queue and broadcast/log them.
        while not worker_task.done() or not q.empty():
            try:
                line = await asyncio.wait_for(q.get(), timeout=0.1)
            except asyncio.TimeoutError:
                continue

            # broadcast & log
            await manager.broadcast(raw_job.job_id, line)
            await jobs_collection.update_one(
                {"job_id": raw_job.job_id},
                {"$push": {"logs": {"text": line, "timestamp": datetime.utcnow().isoformat()}}}
            )

        # if the worker raised, rethrow to catch below
        await worker_task

    except Exception as e:
        exit_code = 1
        err_line = f"❌ Exception in program: {e}"
        await manager.broadcast(raw_job.job_id, err_line)
        await jobs_collection.update_one(
            {"job_id": raw_job.job_id},
            {"$push": {"logs": {"text": err_line, "timestamp": datetime.utcnow().isoformat()}}}
        )

    finally:
        # restore original print()
        builtins.print = orig_print

    # 6) wrap up
    now = datetime.utcnow()
    final_msg = f"[{raw_job.job_id}] exited with code {exit_code}"
    await manager.broadcast(raw_job.job_id, final_msg)
    await jobs_collection.update_one(
        {"job_id": raw_job.job_id},
        {
            "$set": {
                "status": "finished",
                "finished_at": now,
                "exit_code": exit_code
            },
            "$push": {"logs": {"text": final_msg, "timestamp": now.isoformat()}}}
    )


async def create_job(background_tasks: BackgroundTasks, data: CreateJobModel) -> JobModel:
    job_id = str(uuid.uuid4())
    now = datetime.utcnow()

    await jobs_collection.insert_one({
        "job_id": job_id,
        "status": "pending",
        "created_at": now,
        "finished_at": None,
        "exit_code": None,
        "logs": [],
        "region": data.region,
        "credentials": data.credentials
    })
    raw_doc = await jobs_collection.find_one({"job_id": job_id})
    raw_job = JobModel(**raw_doc)

    background_tasks.add_task(run_and_stream, raw_job)
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
    Fetches a single Job by its UUID; raises 404 if not found.
    """
    raw = await jobs_collection.find_one({"job_id": job_id})
    if not raw:
        raise HTTPException(status_code=404, detail="Job not found")
    return JobModel(**raw)


async def delete_job(job_id: str) -> Response:
    """
    Deletes a job by its UUID; raises 404 if not found.
    """
    result = await jobs_collection.delete_one({"job_id": job_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Job not found")

    # Also disconnect any WebSocket connections for this job
    manager.disconnect(job_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
