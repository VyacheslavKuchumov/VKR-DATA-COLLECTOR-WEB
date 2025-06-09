from fastapi import APIRouter, Body, status

from app.models.kcp_dataset_model import (
    KcpModel,
    UpdateKcpModel,
    KcpCollection,
)
from app.controllers.kcp_dataset_controller import (
    create_kcp_dataset,
    list_kcp_datasets,
    show_kcp_dataset,
    update_kcp_dataset,
    delete_kcp_dataset,
)

router = APIRouter()

@router.post(
    "/",
    response_model=KcpModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
    response_description="Create a new KCP dataset record",
)
async def post_kcp_dataset(item: KcpModel = Body(...)):
    return await create_kcp_dataset(item)

@router.get(
    "/",
    response_model=KcpCollection,
    response_model_by_alias=False,
    response_description="List all KCP dataset records",
)
async def get_kcp_datasets():
    return await list_kcp_datasets()

@router.get(
    "/{id}",
    response_model=KcpModel,
    response_model_by_alias=False,
    response_description="Get a single KCP dataset record by ID",
)
async def get_kcp_dataset(id: str):
    return await show_kcp_dataset(id)

@router.put(
    "/{id}",
    response_model=KcpModel,
    response_model_by_alias=False,
    response_description="Update an existing KCP dataset record",
)
async def put_kcp_dataset(
    id: str,
    updates: UpdateKcpModel = Body(...),
):
    return await update_kcp_dataset(id, updates)

@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="Delete a KCP dataset record",
)
async def delete_kcp_dataset_route(id: str):
    return await delete_kcp_dataset(id)
