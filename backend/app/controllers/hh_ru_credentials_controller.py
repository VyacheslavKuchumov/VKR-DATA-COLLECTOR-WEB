from fastapi import HTTPException, status
from fastapi.responses import Response
from pymongo import ReturnDocument
from bson import ObjectId

from app.database import hh_ru_credentials_collection
from app.models.hh_ru_credentials_model import (
    HHRuCredentialsModel,
    UpdateHHRuCredentialsModel,
    HHRuCredentialsCollection,
)

async def create_hh_ru_credentials(credentials: HHRuCredentialsModel) -> HHRuCredentialsModel:
    """
    Создает новую запись с hh.ru credentials.
    """
    # Сериализуем по alias и исключаем поле id
    payload = credentials.model_dump(by_alias=True, exclude=["id"])
    result = await hh_ru_credentials_collection.insert_one(payload)
    created = await hh_ru_credentials_collection.find_one({"_id": result.inserted_id})
    return HHRuCredentialsModel.model_validate(created)

async def list_hh_ru_credentials() -> HHRuCredentialsCollection:
    """
    Возвращает до 1000 записей hh.ru credentials.
    """
    docs = await hh_ru_credentials_collection.find().to_list(1000)
    items = [HHRuCredentialsModel.model_validate(d) for d in docs]
    return HHRuCredentialsCollection(credentials=items)

async def show_hh_ru_credentials(id: str) -> HHRuCredentialsModel:
    """
    Показывает одну запись по id.
    """
    try:
        oid = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail=f"Invalid id format: {id}")
    doc = await hh_ru_credentials_collection.find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail=f"Credentials {id} not found")
    return HHRuCredentialsModel.model_validate(doc)

async def update_hh_ru_credentials(id: str, updates: UpdateHHRuCredentialsModel) -> HHRuCredentialsModel:
    """
    Обновляет переданные поля в записи hh.ru credentials.
    """
    try:
        oid = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail=f"Invalid id format: {id}")

    # Берем только непустые поля из модели обновления
    data = {
        k: v
        for k, v in updates.model_dump(by_alias=True).items()
        if v is not None
    }
    if data:
        updated = await hh_ru_credentials_collection.find_one_and_update(
            {"_id": oid},
            {"$set": data},
            return_document=ReturnDocument.AFTER,
        )
        if not updated:
            raise HTTPException(status_code=404, detail=f"Credentials {id} not found")
        return HHRuCredentialsModel.model_validate(updated)

    # Если нечего менять — возвращаем текущее состояние
    existing = await hh_ru_credentials_collection.find_one({"_id": oid})
    if not existing:
        raise HTTPException(status_code=404, detail=f"Credentials {id} not found")
    return HHRuCredentialsModel.model_validate(existing)

async def delete_hh_ru_credentials(id: str) -> Response:
    """
    Удаляет запись hh.ru credentials по id.
    """
    try:
        oid = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail=f"Invalid id format: {id}")

    result = await hh_ru_credentials_collection.delete_one({"_id": oid})
    if result.deleted_count != 1:
        raise HTTPException(status_code=404, detail=f"Credentials {id} not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
