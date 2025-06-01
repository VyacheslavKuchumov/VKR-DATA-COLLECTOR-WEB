# app/controllers/job_controller.py

import uuid
import asyncio
import builtins
from pathlib import Path
from datetime import datetime
from fastapi.responses import Response
from fastapi import BackgroundTasks, HTTPException, status
from app.database import jobs_collection
from app.websocket.connectionManager import manager
from app.models.job_model import JobModel
from app.scripts.test_job import TestProgram


async def run_and_stream(job_id: str):
    """
    Runs TestProgram.run() in a background thread, captures each print()
    into an asyncio.Queue, then in the async context broadcasts & logs
    each line in real time, and finally updates the job status.
    """
    # 1) mark as running
    await jobs_collection.update_one(
        {"job_id": job_id},
        {"$set": {"status": "running"}}
    )

    # 2) set up a queue to shuttle lines from the thread into async land
    q: asyncio.Queue[str] = asyncio.Queue()

    # 3) hijack print() in the worker thread to put lines into the queue
    orig_print = builtins.print

    def intercept_print(*args, **kwargs):
        line = " ".join(str(a) for a in args)
        # push into queue for the async loop to pick up
        try:
            q.put_nowait(line)
        except asyncio.QueueFull:
            pass
        # still print to server console
        orig_print(f"[{job_id}]", line)

    builtins.print = intercept_print

    # 4) schedule the blocking run() in a separate thread
    worker_task = asyncio.create_task(
        asyncio.to_thread(TestProgram().run)
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
            await manager.broadcast(job_id, line)
            await jobs_collection.update_one(
                {"job_id": job_id},
                {"$push": {"logs":{"text": line, "timestamp": datetime.utcnow().isoformat()}}}
            )

        # if the worker raised, rethrow to catch below
        await worker_task
    except Exception as e:
        exit_code = 1
        err_line = f"❌ Exception in TestProgram: {e}"
        await manager.broadcast(job_id, err_line)
        await jobs_collection.update_one(
            {"job_id": job_id},
            {"$push": {"logs": {"text": err_line, "timestamp": datetime.utcnow().isoformat()}}}
        )
    finally:
        # restore original print()
        builtins.print = orig_print

    # 6) wrap up
    now = datetime.utcnow()
    final_msg = f"[{job_id}] exited with code {exit_code}"
    await manager.broadcast(job_id, final_msg)
    await jobs_collection.update_one(
        {"job_id": job_id},
        {
            "$set": {
                "status": "finished",
                "finished_at": now,
                "exit_code": exit_code
            },
            "$push": {"logs": {"text":final_msg, "timestamp": now.isoformat()}}
        }
    )


async def create_job(background_tasks: BackgroundTasks) -> JobModel:
    """
    Inserts a pending job (with empty logs), schedules run_and_stream,
    and returns the newly created JobModel.
    """
    job_id = str(uuid.uuid4())
    now = datetime.utcnow()

    await jobs_collection.insert_one({
        "job_id": job_id,
        "status": "pending",
        "created_at": now,
        "finished_at": None,
        "exit_code": None,
        "logs": []              # initialize logs array
    })

    background_tasks.add_task(run_and_stream, job_id)

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


async def delete_job(job_id: str) -> None:
    """
    Deletes a job by its UUID; raises 404 if not found.
    """
    result = await jobs_collection.delete_one({"job_id": job_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Also disconnect any WebSocket connections for this job
    manager.disconnect(job_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)