from fastapi import HTTPException, status
from fastapi.responses import Response
from pymongo import ReturnDocument
from bson import ObjectId

from app.database import kcp_dataset_collection
from app.models.kcp_dataset_model import (
    KcpModel,
    UpdateKcpModel,
    KcpCollection,
)

async def create_kcp_dataset(item: KcpModel) -> KcpModel:
    """
    Insert a new KCP record into MongoDB and return the created document.
    """
    payload = item.model_dump(by_alias=True, exclude=["id"])
    result = await kcp_dataset_collection.insert_one(payload)
    created_doc = await kcp_dataset_collection.find_one({"_id": result.inserted_id})
    return KcpModel.model_validate(created_doc)

async def list_kcp_datasets() -> KcpCollection:
    """
    Retrieve up to 1000 KCP records.
    """
    docs = await kcp_dataset_collection.find().to_list(1000)
    items = [KcpModel.model_validate(d) for d in docs]
    return KcpCollection(records=items)

async def show_kcp_dataset(id: str) -> KcpModel:
    """
    Retrieve a single KCP record by its ObjectId.
    """
    try:
        oid = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail=f"Invalid id format: {id}")
    doc = await kcp_dataset_collection.find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail=f"KCP record {id} not found")
    return KcpModel.model_validate(doc)

async def update_kcp_dataset(id: str, updates: UpdateKcpModel) -> KcpModel:
    """
    Update fields of an existing KCP record. Returns the updated document.
    """
    try:
        oid = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail=f"Invalid id format: {id}")
    data = updates.model_dump(by_alias=True)
    data = {k: v for k, v in data.items() if v is not None}
    if data:
        updated = await kcp_dataset_collection.find_one_and_update(
            {"_id": oid},
            {"$set": data},
            return_document=ReturnDocument.AFTER,
        )
        if not updated:
            raise HTTPException(status_code=404, detail=f"KCP record {id} not found")
        return KcpModel.model_validate(updated)
    existing = await kcp_dataset_collection.find_one({"_id": oid})
    if not existing:
        raise HTTPException(status_code=404, detail=f"KCP record {id} not found")
    return KcpModel.model_validate(existing)

async def delete_kcp_dataset(id: str) -> Response:
    """
    Delete a KCP record by its ObjectId. Returns 204 on success.
    """
    try:
        oid = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail=f"Invalid id format: {id}")
    result = await kcp_dataset_collection.delete_one({"_id": oid})
    if result.deleted_count != 1:
        raise HTTPException(status_code=404, detail=f"KCP record {id} not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
