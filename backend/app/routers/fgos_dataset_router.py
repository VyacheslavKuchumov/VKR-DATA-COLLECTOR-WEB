from fastapi import APIRouter, Body, status

from app.models.fgos_dataset_model import (
    FgosDatasetModel,
    UpdateFgosDatasetModel,
    FgosDatasetCollection,
)
from app.controllers.fgos_dataset_controller import (
    create_fgos_dataset,
    list_fgos_datasets,
    show_fgos_dataset,
    update_fgos_dataset,
    delete_fgos_dataset,
)

router = APIRouter()

@router.post(
    "/",
    response_model=FgosDatasetModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
    response_description="Create a new FGOS dataset record",
)
async def post_fgos_dataset(item: FgosDatasetModel = Body(...)):
    return await create_fgos_dataset(item)

@router.get(
    "/",
    response_model=FgosDatasetCollection,
    response_model_by_alias=False,
    response_description="List all FGOS dataset records",
)
async def get_fgos_datasets():
    return await list_fgos_datasets()

@router.get(
    "/{id}",
    response_model=FgosDatasetModel,
    response_model_by_alias=False,
    response_description="Get a single FGOS dataset record by ID",
)
async def get_fgos_dataset(id: str):
    return await show_fgos_dataset(id)

@router.put(
    "/{id}",
    response_model=FgosDatasetModel,
    response_model_by_alias=False,
    response_description="Update an existing FGOS dataset record",
)
async def put_fgos_dataset(
    id: str,
    updates: UpdateFgosDatasetModel = Body(...),
):
    return await update_fgos_dataset(id, updates)

@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="Delete a FGOS dataset record",
)
async def delete_fgos_dataset_route(id: str):
    return await delete_fgos_dataset(id)
