from fastapi import HTTPException, status
from fastapi.responses import Response
from pymongo import ReturnDocument, ASCENDING
from bson import ObjectId

from app.database import fgos_dataset_collection
from app.models.fgos_dataset_model import (
    FgosDatasetModel,
    UpdateFgosDatasetModel,
    FgosDatasetCollection,
)

async def create_fgos_dataset(item: FgosDatasetModel) -> FgosDatasetModel:
    """
    Insert a new FGOS record into MongoDB and return the created document.
    """
    payload = item.model_dump(by_alias=True, exclude=["id"])
    result = await fgos_dataset_collection.insert_one(payload)
    created_doc = await fgos_dataset_collection.find_one({"_id": result.inserted_id})
    return FgosDatasetModel.model_validate(created_doc)

async def list_fgos_datasets() -> FgosDatasetCollection:
    """
    Retrieve up to 1000 FGOS records.
    """
    docs = await fgos_dataset_collection.find().sort("fgos_code", ASCENDING).to_list(1000)
    items = [FgosDatasetModel.model_validate(d) for d in docs]
    return FgosDatasetCollection(records=items)

async def show_fgos_dataset(id: str) -> FgosDatasetModel:
    """
    Retrieve a single FGOS record by its ObjectId.
    """
    try:
        oid = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail=f"Invalid id format: {id}")
    doc = await fgos_dataset_collection.find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail=f"FGOS record {id} not found")
    return FgosDatasetModel.model_validate(doc)

async def update_fgos_dataset(id: str, updates: UpdateFgosDatasetModel) -> FgosDatasetModel:
    """
    Update fields of an existing FGOS record. Returns the updated document.
    """
    try:
        oid = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail=f"Invalid id format: {id}")
    data = updates.model_dump(by_alias=True)
    data = {k: v for k, v in data.items() if v is not None}
    if data:
        updated = await fgos_dataset_collection.find_one_and_update(
            {"_id": oid},
            {"$set": data},
            return_document=ReturnDocument.AFTER,
        )
        if not updated:
            raise HTTPException(status_code=404, detail=f"FGOS record {id} not found")
        return FgosDatasetModel.model_validate(updated)
    existing = await fgos_dataset_collection.find_one({"_id": oid})
    if not existing:
        raise HTTPException(status_code=404, detail=f"FGOS record {id} not found")
    return FgosDatasetModel.model_validate(existing)

async def delete_fgos_dataset(id: str) -> Response:
    """
    Delete an FGOS record by its ObjectId. Returns 204 on success.
    """
    try:
        oid = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail=f"Invalid id format: {id}")
    result = await fgos_dataset_collection.delete_one({"_id": oid})
    if result.deleted_count != 1:
        raise HTTPException(status_code=404, detail=f"FGOS record {id} not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
