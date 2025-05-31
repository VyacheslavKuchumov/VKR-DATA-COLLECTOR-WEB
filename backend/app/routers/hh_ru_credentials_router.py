from fastapi import APIRouter, Body, status

from app.models.hh_ru_credentials_model import (
    HHRuCredentialsModel,
    UpdateHHRuCredentialsModel,
    HHRuCredentialsCollection,
)
from app.controllers.hh_ru_credentials_controller import (
    create_hh_ru_credentials,
    list_hh_ru_credentials,
    show_hh_ru_credentials,
    update_hh_ru_credentials,
    delete_hh_ru_credentials,
)

router = APIRouter()

@router.post(
    "/",
    response_model=HHRuCredentialsModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
    response_description="Add new hh.ru credentials",
)
async def post_hh_ru_credentials(
    credentials: HHRuCredentialsModel = Body(...),
):
    return await create_hh_ru_credentials(credentials)

@router.get(
    "/",
    response_model=HHRuCredentialsCollection,
    response_model_by_alias=False,
    response_description="List all hh.ru credentials",
)
async def get_hh_ru_credentials():
    return await list_hh_ru_credentials()

@router.get(
    "/{id}",
    response_model=HHRuCredentialsModel,
    response_model_by_alias=False,
    response_description="Get a single hh.ru credentials record",
)
async def get_hh_ru_credentials_by_id(id: str):
    return await show_hh_ru_credentials(id)

@router.put(
    "/{id}",
    response_model=HHRuCredentialsModel,
    response_model_by_alias=False,
    response_description="Update hh.ru credentials",
)
async def put_hh_ru_credentials(
    id: str,
    credentials: UpdateHHRuCredentialsModel = Body(...),
):
    return await update_hh_ru_credentials(id, credentials)

@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="Delete hh.ru credentials",
)
async def delete_hh_ru_credentials_route(id: str):
    return await delete_hh_ru_credentials(id)
