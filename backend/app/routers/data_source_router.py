from fastapi import APIRouter, Body, status
from app.models.data_source_model import (
    DataSourceModel,
    UpdateDataSourceModel,
    DataSourceCollection,
)
from app.controllers.data_source_controller import (
    create_data_source,
    list_data_sources,
    show_data_sources_by_type,
    update_data_source,
    delete_data_source,
)

router = APIRouter()

@router.post(
    "/",
    response_model=DataSourceModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
    response_description="Add new data source",
)
async def post_data_source(source: DataSourceModel = Body(...)):
    return await create_data_source(source)

@router.get(
    "/",
    response_model=DataSourceCollection,
    response_model_by_alias=False,
    response_description="List all data sources",
)
async def get_data_sources():
    return await list_data_sources()

@router.get(
    "/type/{source_type}",
    response_model=DataSourceCollection,
    response_model_by_alias=False,
    response_description="Get sources by source_type",
)
async def get_data_source_by_type(source_type: str):
    return await show_data_sources_by_type(source_type)

@router.put(
    "/{id}",
    response_model=DataSourceModel,
    response_model_by_alias=False,
    response_description="Update a data source",
)
async def put_data_source(
    id: str,
    source: UpdateDataSourceModel = Body(...),
):
    return await update_data_source(id, source)

@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="Delete a data source",
)
async def delete_data_source_route(id: str):
    return await delete_data_source(id)
