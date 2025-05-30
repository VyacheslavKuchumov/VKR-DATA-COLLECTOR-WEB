from fastapi import APIRouter, Body, status
from app.models.region_model import RegionModel, UpdateRegionModel, RegionCollection
from app.controllers.region_controller import (
    create_region,
    list_regions,
    show_region,
    update_region,
    delete_region,
)

router = APIRouter()

@router.post(
    "/",
    response_model=RegionModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
    response_description="Add new region",
)
async def post_region(region: RegionModel = Body(...)):
    return await create_region(region)

@router.get(
    "/",
    response_model=RegionCollection,
    response_model_by_alias=False,
    response_description="List all regions",
)
async def get_regions():
    return await list_regions()

@router.get(
    "/{id}",
    response_model=RegionModel,
    response_model_by_alias=False,
    response_description="Get a single region",
)
async def get_region(id: str):
    return await show_region(id)

@router.put(
    "/{id}",
    response_model=RegionModel,
    response_model_by_alias=False,
    response_description="Update a region",
)
async def put_region(
    id: str,
    region: UpdateRegionModel = Body(...),
):
    return await update_region(id, region)

@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="Delete a region",
)
async def delete_region_route(id: str):
    return await delete_region(id)
