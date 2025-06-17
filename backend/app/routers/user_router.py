from fastapi import APIRouter, Body, status
from app.models.user_model import UserModel, UpdateUserModel, UserCollection
from app.controllers.user_controller import (
    create_user,
    list_users,
    show_user,
    update_user,
    delete_user,
    show_user_by_email,
)

router = APIRouter()

@router.post(
    "/",
    response_model=UserModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
    response_description="Add new user",
)
async def post_user(user: UserModel = Body(...)):
    return await create_user(user)

@router.get(
    "/",
    response_model=UserCollection,
    response_model_by_alias=False,
    response_description="List all users",
)
async def get_users():
    return await list_users()

@router.get(
    "/auth/{email}",
    response_model=UserModel,
    response_model_by_alias=False,
    response_description="Get user by email",
)
async def get_user_by_email(email: str):
    return await show_user_by_email(email)

@router.get(
    "/{id}",
    response_model=UserModel,
    response_model_by_alias=False,
    response_description="Get a single user",
)
async def get_user(id: str):
    return await show_user(id)

@router.put(
    "/{id}",
    response_model=UserModel,
    response_model_by_alias=False,
    response_description="Update a user",
)
async def put_user(
    id: str,
    user: UpdateUserModel = Body(...),
):
    return await update_user(id, user)

@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="Delete a user",
)
async def delete_user_route(id: str):
    return await delete_user(id)
