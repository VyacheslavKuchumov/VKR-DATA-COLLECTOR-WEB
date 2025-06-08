from fastapi import HTTPException, status
from fastapi.responses import Response
from pymongo import ReturnDocument
from bson import ObjectId

from app.database import minstat_worker_collection
from app.models.minstat_worker_model import (
    MinstatWorkerModel,
    UpdateMinstatWorkerModel,
    MinstatWorkerCollection,
)

async def create_minstat_worker(worker: MinstatWorkerModel) -> MinstatWorkerModel:
    # Подготовка и вставка записи в MongoDB
    payload = worker.model_dump(by_alias=True, exclude=["id"])
    result = await minstat_worker_collection.insert_one(payload)
    created = await minstat_worker_collection.find_one({"_id": result.inserted_id})
    return MinstatWorkerModel.model_validate(created)

async def list_minstat_workers() -> MinstatWorkerCollection:
    # Получаем до 1000 записей
    docs = await minstat_worker_collection.find().to_list(1000)
    workers = [MinstatWorkerModel.model_validate(d) for d in docs]
    return MinstatWorkerCollection(workers=workers)

async def show_minstat_worker(id: str) -> MinstatWorkerModel:
    # Поиск по ObjectId
    try:
        oid = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail=f"Invalid id format: {id}")
    doc = await minstat_worker_collection.find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail=f"Worker {id} not found")
    return MinstatWorkerModel.model_validate(doc)

async def update_minstat_worker(id: str, updates: UpdateMinstatWorkerModel) -> MinstatWorkerModel:
    # Обновление записи по ObjectId
    try:
        oid = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail=f"Invalid id format: {id}")
    data = {k: v for k, v in updates.model_dump(by_alias=True).items() if v is not None}
    if data:
        updated = await minstat_worker_collection.find_one_and_update(
            {"_id": oid},
            {"$set": data},
            return_document=ReturnDocument.AFTER,
        )
        if not updated:
            raise HTTPException(status_code=404, detail=f"Worker {id} not found")
        return MinstatWorkerModel.model_validate(updated)

    # Если нет изменений — вернуть текущую запись
    existing = await minstat_worker_collection.find_one({"_id": oid})
    if not existing:
        raise HTTPException(status_code=404, detail=f"Worker {id} not found")
    return MinstatWorkerModel.model_validate(existing)

async def delete_minstat_worker(id: str) -> Response:
    # Удаление по id
    try:
        oid = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail=f"Invalid id format: {id}")
    result = await minstat_worker_collection.delete_one({"_id": oid})
    if result.deleted_count != 1:
        raise HTTPException(status_code=404, detail=f"Worker {id} not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
