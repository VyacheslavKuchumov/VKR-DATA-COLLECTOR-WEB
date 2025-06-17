from fastapi import HTTPException, status
from fastapi.responses import Response
from pymongo import ReturnDocument
from bson import ObjectId

from app.database import user_collection
from app.models.user_model import (
    UserModel,
    UpdateUserModel,
    UserCollection,
)

async def create_user(user: UserModel) -> UserModel:
    # Подготовка данных и вставка в MongoDB
    payload = user.model_dump(by_alias=True, exclude=["id"])
    result = await user_collection.insert_one(payload)
    created = await user_collection.find_one({"_id": result.inserted_id})
    return UserModel.model_validate(created)

async def list_users() -> UserCollection:
    # Получаем до 1000 пользователей
    docs = await user_collection.find().to_list(1000)
    users = [UserModel.model_validate(d) for d in docs]
    return UserCollection(users=users)

# поиск пользователя по email
async def show_user_by_email(email: str) -> UserModel:
    # Поиск по email
    doc = await user_collection.find_one({"email": email})
    if not doc:
        raise HTTPException(status_code=404, detail=f"User with email {email} not found")
    return UserModel.model_validate(doc)

async def show_user(id: str) -> UserModel:
    # Поиск по ObjectId
    try:
        oid = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail=f"Invalid id format: {id}")
    doc = await user_collection.find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail=f"User {id} not found")
    return UserModel.model_validate(doc)

async def update_user(id: str, updates: UpdateUserModel) -> UserModel:
    # Фильтруем только непустые поля
    try:
        oid = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail=f"Invalid id format: {id}")
    data = {k: v for k, v in updates.model_dump(by_alias=True).items() if v is not None}
    if data:
        updated = await user_collection.find_one_and_update(
            {"_id": oid},
            {"$set": data},
            return_document=ReturnDocument.AFTER,
        )
        if not updated:
            raise HTTPException(status_code=404, detail=f"User {id} not found")
        return UserModel.model_validate(updated)

    # Если нет изменений — возвращаем существующий
    existing = await user_collection.find_one({"_id": oid})
    if not existing:
        raise HTTPException(status_code=404, detail=f"User {id} not found")
    return UserModel.model_validate(existing)

async def delete_user(id: str) -> Response:
    # Удаляем пользователя
    try:
        oid = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail=f"Invalid id format: {id}")
    result = await user_collection.delete_one({"_id": oid})
    if result.deleted_count != 1:
        raise HTTPException(status_code=404, detail=f"User {id} not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
