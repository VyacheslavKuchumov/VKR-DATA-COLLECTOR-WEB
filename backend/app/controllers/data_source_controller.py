from fastapi import HTTPException, status
from fastapi.responses import Response
from pymongo import ReturnDocument
from bson import ObjectId

from app.database import data_source_collection
from app.models.data_source_model import (
    DataSourceModel,
    UpdateDataSourceModel,
    DataSourceCollection,
)

async def create_data_source(source: DataSourceModel) -> DataSourceModel:
    # Подготовка данных и вставка в MongoDB
    payload = source.model_dump(by_alias=True, exclude=["id"])
    result = await data_source_collection.insert_one(payload)
    created = await data_source_collection.find_one({"_id": result.inserted_id})
    return DataSourceModel.model_validate(created)

async def list_data_sources() -> DataSourceCollection:
    # Получаем до 1000 источников
    docs = await data_source_collection.find().to_list(1000)
    sources = [DataSourceModel.model_validate(d) for d in docs]
    return DataSourceCollection(sources=sources)

async def show_data_sources_by_type(source_type: str) -> DataSourceModel:
    # Поиск по source_type
    docs = await data_source_collection.find({"source_type": source_type}).to_list(1000)
    sources = [DataSourceModel.model_validate(d) for d in docs]
    return DataSourceCollection(sources=sources)


async def update_data_source(id: str, updates: UpdateDataSourceModel) -> DataSourceModel:
    # Фильтруем непустые поля
    try:
        oid = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail=f"Invalid id format: {id}")
    data = {
        k: v
        for k, v in updates.model_dump(by_alias=True).items()
        if v is not None
    }
    if data:
        updated = await data_source_collection.find_one_and_update(
            {"_id": oid},
            {"$set": data},
            return_document=ReturnDocument.AFTER,
        )
        if not updated:
            raise HTTPException(status_code=404, detail=f"DataSource {id} not found")
        return DataSourceModel.model_validate(updated)

    # Если нет изменений — возвращаем существующий
    existing = await data_source_collection.find_one({"_id": oid})
    if not existing:
        raise HTTPException(status_code=404, detail=f"DataSource {id} not found")
    return DataSourceModel.model_validate(existing)

async def delete_data_source(id: str) -> Response:
    # Удаляем источник
    try:
        oid = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail=f"Invalid id format: {id}")
    result = await data_source_collection.delete_one({"_id": oid})
    if result.deleted_count != 1:
        raise HTTPException(status_code=404, detail=f"DataSource {id} not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
