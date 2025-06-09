from fastapi import HTTPException, status
from fastapi.responses import Response
from pymongo import ReturnDocument
from bson import ObjectId

from app.database import okved_dataset_collection
from app.models.okved_dataset_model import (
    OkvedDatasetModel,
    UpdateOkvedDatasetModel,
    OkvedDatasetCollection,
)

async def create_okved_dataset(item: OkvedDatasetModel) -> OkvedDatasetModel:
    """
    Insert a new OKVED record into MongoDB and return the created document.
    """
    payload = item.model_dump(by_alias=True, exclude=["id"])
    result = await okved_dataset_collection.insert_one(payload)
    created_doc = await okved_dataset_collection.find_one({"_id": result.inserted_id})
    return OkvedDatasetModel.model_validate(created_doc)

async def list_okved_datasets() -> OkvedDatasetCollection:
    """
    Retrieve up to 1000 OKVED records.
    """
    docs = await okved_dataset_collection.find().to_list(1000)
    items = [OkvedDatasetModel.model_validate(d) for d in docs]
    return OkvedDatasetCollection(records=items)

async def show_okved_dataset(id: str) -> OkvedDatasetModel:
    """
    Retrieve a single OKVED record by its ObjectId.
    """
    try:
        oid = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail=f"Invalid id format: {id}")
    doc = await okved_dataset_collection.find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail=f"OKVED record {id} not found")
    return OkvedDatasetModel.model_validate(doc)

async def update_okved_dataset(id: str, updates: UpdateOkvedDatasetModel) -> OkvedDatasetModel:
    """
    Update fields of an existing OKVED record. Returns the updated document.
    """
    try:
        oid = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail=f"Invalid id format: {id}")
    data = updates.model_dump(by_alias=True)
    # Remove None values to avoid unsetting fields unintentionally
    data = {k: v for k, v in data.items() if v is not None}
    if data:
        updated = await okved_dataset_collection.find_one_and_update(
            {"_id": oid},
            {"$set": data},
            return_document=ReturnDocument.AFTER,
        )
        if not updated:
            raise HTTPException(status_code=404, detail=f"OKVED record {id} not found")
        return OkvedDatasetModel.model_validate(updated)
    # No changes requested; return existing
    existing = await okved_dataset_collection.find_one({"_id": oid})
    if not existing:
        raise HTTPException(status_code=404, detail=f"OKVED record {id} not found")
    return OkvedDatasetModel.model_validate(existing)

async def delete_okved_dataset(id: str) -> Response:
    """
    Delete an OKVED record by its ObjectId. Returns 204 on success.
    """
    try:
        oid = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail=f"Invalid id format: {id}")
    result = await okved_dataset_collection.delete_one({"_id": oid})
    if result.deleted_count != 1:
        raise HTTPException(status_code=404, detail=f"OKVED record {id} not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
