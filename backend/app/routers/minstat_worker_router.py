from fastapi import APIRouter, Body, status

from app.models.minstat_worker_model import (
    MinstatWorkerModel,
    UpdateMinstatWorkerModel,
    MinstatWorkerCollection,
)
from app.controllers.minstat_worker_controller import (
    create_minstat_worker,
    list_minstat_workers,
    show_minstat_worker,
    update_minstat_worker,
    delete_minstat_worker,
)

router = APIRouter()

@router.post(
    "/",
    response_model=MinstatWorkerModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
    response_description="Add new minstat worker",
)
async def post_minstat_worker(worker: MinstatWorkerModel = Body(...)):
    return await create_minstat_worker(worker)

@router.get(
    "/",
    response_model=MinstatWorkerCollection,
    response_model_by_alias=False,
    response_description="List all minstat workers",
)
async def get_minstat_workers():
    return await list_minstat_workers()

@router.get(
    "/{id}",
    response_model=MinstatWorkerModel,
    response_model_by_alias=False,
    response_description="Get a single minstat worker",
)
async def get_minstat_worker(id: str):
    return await show_minstat_worker(id)

@router.put(
    "/{id}",
    response_model=MinstatWorkerModel,
    response_model_by_alias=False,
    response_description="Update a minstat worker",
)
async def put_minstat_worker(
    id: str,
    worker: UpdateMinstatWorkerModel = Body(...),
):
    return await update_minstat_worker(id, worker)

@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="Delete a minstat worker",
)
async def delete_minstat_worker_route(id: str):
    return await delete_minstat_worker(id)
