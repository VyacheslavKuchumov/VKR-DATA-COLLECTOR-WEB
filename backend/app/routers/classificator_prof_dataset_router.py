from fastapi import APIRouter, Body, status

from app.models.classificator_prof_dataset_model import (
    ClassificatorProfDatasetModel,
    UpdateClassificatorProfDatasetModel,
    ClassificatorProfDatasetCollection,
)
from app.controllers.classificator_prof_dataset_controller import (
    create_prof_dataset,
    list_prof_datasets,
    show_prof_dataset,
    update_prof_dataset,
    delete_prof_dataset,
)

router = APIRouter()

@router.post(
    "/",
    response_model=ClassificatorProfDatasetModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
    response_description="Create a new profession dataset record",
)
async def post_prof_dataset(item: ClassificatorProfDatasetModel = Body(...)):
    return await create_prof_dataset(item)

@router.get(
    "/",
    response_model=ClassificatorProfDatasetCollection,
    response_model_by_alias=False,
    response_description="List all profession dataset records",
)
async def get_prof_datasets():
    return await list_prof_datasets()

@router.get(
    "/{id}",
    response_model=ClassificatorProfDatasetModel,
    response_model_by_alias=False,
    response_description="Get a single profession dataset record by ID",
)
async def get_prof_dataset(id: str):
    return await show_prof_dataset(id)

@router.put(
    "/{id}",
    response_model=ClassificatorProfDatasetModel,
    response_model_by_alias=False,
    response_description="Update an existing profession dataset record",
)
async def put_prof_dataset(
    id: str,
    updates: UpdateClassificatorProfDatasetModel = Body(...),
):
    return await update_prof_dataset(id, updates)

@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="Delete a profession dataset record",
)
async def delete_prof_dataset_route(id: str):
    return await delete_prof_dataset(id)
