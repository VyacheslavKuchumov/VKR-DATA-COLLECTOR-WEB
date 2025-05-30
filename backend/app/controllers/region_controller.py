from fastapi import HTTPException, status
from fastapi.responses import Response
from pymongo import ReturnDocument
from bson import ObjectId

from app.database import region_collection
from app.models.region_model import (
    RegionModel,
    UpdateRegionModel,
    RegionCollection,
)

async def create_region(region: RegionModel) -> RegionModel:
    # Подготовка данных и вставка в MongoDB
    payload = region.model_dump(by_alias=True, exclude=["id"])
    result = await region_collection.insert_one(payload)
    created = await region_collection.find_one({"_id": result.inserted_id})
    return RegionModel.model_validate(created)

async def list_regions() -> RegionCollection:
    # Получаем до 1000 регионов
    docs = await region_collection.find().to_list(1000)
    regions = [RegionModel.model_validate(d) for d in docs]
    return RegionCollection(regions=regions)

async def show_region(id: str) -> RegionModel:
    # Поиск по ObjectId
    try:
        oid = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail=f"Invalid id format: {id}")
    doc = await region_collection.find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail=f"Region {id} not found")
    return RegionModel.model_validate(doc)

async def update_region(id: str, updates: UpdateRegionModel) -> RegionModel:
    # Фильтруем только непустые поля
    try:
        oid = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail=f"Invalid id format: {id}")
    data = {k: v for k, v in updates.model_dump(by_alias=True).items() if v is not None}
    if data:
        updated = await region_collection.find_one_and_update(
            {"_id": oid},
            {"$set": data},
            return_document=ReturnDocument.AFTER,
        )
        if not updated:
            raise HTTPException(status_code=404, detail=f"Region {id} not found")
        return RegionModel.model_validate(updated)

    # Если нет изменений — возвращаем существующий
    existing = await region_collection.find_one({"_id": oid})
    if not existing:
        raise HTTPException(status_code=404, detail=f"Region {id} not found")
    return RegionModel.model_validate(existing)

async def delete_region(id: str) -> Response:
    # Удаляем регион
    try:
        oid = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail=f"Invalid id format: {id}")
    result = await region_collection.delete_one({"_id": oid})
    if result.deleted_count != 1:
        raise HTTPException(status_code=404, detail=f"Region {id} not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
