from fastapi import APIRouter, Body, status

from app.models.hh_ru_dataset_model import (
    HHRuDatasetModel,
    UpdateHHRuDatasetModel,
    HHRuDatasetCollection,
)
from app.controllers.hh_ru_dataset_controller import (
    create_hh_ru_dataset,
    list_hh_ru_datasets,
    show_hh_ru_dataset,
    update_hh_ru_dataset,
    delete_hh_ru_dataset,
)

router = APIRouter()

@router.post(
    "/",
    response_model=HHRuDatasetModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
    response_description="Create a new HH.ru dataset summary",
)
async def post_hh_ru_dataset(item: HHRuDatasetModel = Body(...)):
    return await create_hh_ru_dataset(item)

@router.get(
    "/",
    response_model=HHRuDatasetCollection,
    response_model_by_alias=False,
    response_description="List all HH.ru dataset summaries",
)
async def get_hh_ru_datasets():
    return await list_hh_ru_datasets()

@router.get(
    "/{id}",
    response_model=HHRuDatasetModel,
    response_model_by_alias=False,
    response_description="Get a single HH.ru dataset summary by ID",
)
async def get_hh_ru_dataset(id: str):
    return await show_hh_ru_dataset(id)

@router.put(
    "/{id}",
    response_model=HHRuDatasetModel,
    response_model_by_alias=False,
    response_description="Update an existing HH.ru dataset summary",
)
async def put_hh_ru_dataset(
    id: str,
    updates: UpdateHHRuDatasetModel = Body(...),
):
    return await update_hh_ru_dataset(id, updates)

@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="Delete an HH.ru dataset summary",
)
async def delete_hh_ru_dataset_route(id: str):
    return await delete_hh_ru_dataset(id)
