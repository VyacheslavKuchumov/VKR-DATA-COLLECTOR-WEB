from fastapi import APIRouter, Body, status

from app.models.prof_standard_dataset_model import (
    ProfStandardDatasetModel,
    UpdateProfStandardDatasetModel,
    ProfStandardDatasetCollection,
)
from app.controllers.prof_standard_dataset_controller import (
    create_prof_standard_dataset,
    list_prof_standard_datasets,
    show_prof_standard_dataset,
    update_prof_standard_dataset,
    delete_prof_standard_dataset,
)

router = APIRouter()

@router.post(
    "/",
    response_model=ProfStandardDatasetModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
    response_description="Create a new professional standard dataset record",
)
async def post_prof_standard_dataset(item: ProfStandardDatasetModel = Body(...)):
    return await create_prof_standard_dataset(item)

@router.get(
    "/",
    response_model=ProfStandardDatasetCollection,
    response_model_by_alias=False,
    response_description="List all professional standard dataset records",
)
async def get_prof_standard_datasets():
    return await list_prof_standard_datasets()

@router.get(
    "/{id}",
    response_model=ProfStandardDatasetModel,
    response_model_by_alias=False,
    response_description="Get a single professional standard dataset record by ID",
)
async def get_prof_standard_dataset(id: str):
    return await show_prof_standard_dataset(id)

@router.put(
    "/{id}",
    response_model=ProfStandardDatasetModel,
    response_model_by_alias=False,
    response_description="Update an existing professional standard dataset record",
)
async def put_prof_standard_dataset(
    id: str,
    updates: UpdateProfStandardDatasetModel = Body(...),
):
    return await update_prof_standard_dataset(id, updates)

@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="Delete a professional standard dataset record",
)
async def delete_prof_standard_dataset_route(id: str):
    return await delete_prof_standard_dataset(id)
