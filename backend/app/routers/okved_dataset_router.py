from fastapi import APIRouter, Body, status

from app.models.okved_dataset_model import (
    OkvedDatasetModel,
    UpdateOkvedDatasetModel,
    OkvedDatasetCollection,
)
from app.controllers.okved_dataset_controller import (
    create_okved_dataset,
    list_okved_datasets,
    show_okved_dataset,
    update_okved_dataset,
    delete_okved_dataset,
)

router = APIRouter()

@router.post(
    "/",
    response_model=OkvedDatasetModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
    response_description="Create a new OKVED dataset record",
)
async def post_okved_dataset(item: OkvedDatasetModel = Body(...)) -> OkvedDatasetModel:
    return await create_okved_dataset(item)

@router.get(
    "/",
    response_model=OkvedDatasetCollection,
    response_model_by_alias=False,
    response_description="List all OKVED dataset records",
)
async def get_okved_datasets() -> OkvedDatasetCollection:
    return await list_okved_datasets()

@router.get(
    "/{id}",
    response_model=OkvedDatasetModel,
    response_model_by_alias=False,
    response_description="Get a single OKVED dataset record by ID",
)
async def get_okved_dataset(id: str) -> OkvedDatasetModel:
    return await show_okved_dataset(id)

@router.put(
    "/{id}",
    response_model=OkvedDatasetModel,
    response_model_by_alias=False,
    response_description="Update an existing OKVED dataset record",
)
async def put_okved_dataset(
    id: str,
    updates: UpdateOkvedDatasetModel = Body(...),
) -> OkvedDatasetModel:
    return await update_okved_dataset(id, updates)

@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="Delete an OKVED dataset record",
)
async def delete_okved_dataset_route(id: str) -> None:
    await delete_okved_dataset(id)
