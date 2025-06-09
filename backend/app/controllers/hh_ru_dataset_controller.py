# app/controllers/hh_ru_dataset_controller.py

from fastapi import HTTPException, status
from fastapi.responses import Response
from pymongo import ReturnDocument
from bson import ObjectId

from app.database import hh_ru_dataset_collection
from app.models.hh_ru_dataset_model import (
    HHRuDatasetModel,
    UpdateHHRuDatasetModel,
    HHRuDatasetCollection,
)

async def create_hh_ru_dataset(item: HHRuDatasetModel) -> HHRuDatasetModel:
    """
    Insert a new summary record into MongoDB and return the created document.
    """
    payload = item.model_dump(by_alias=True, exclude=["id"])
    result = await hh_ru_dataset_collection.insert_one(payload)
    created_doc = await hh_ru_dataset_collection.find_one({"_id": result.inserted_id})
    return HHRuDatasetModel.model_validate(created_doc)

async def list_hh_ru_datasets() -> HHRuDatasetCollection:
    """
    Retrieve up to 1000 summary records.
    """
    docs = await hh_ru_dataset_collection.find().to_list(1000)
    items = [HHRuDatasetModel.model_validate(d) for d in docs]
    return HHRuDatasetCollection(summaries=items)

async def show_hh_ru_dataset(id: str) -> HHRuDatasetModel:
    """
    Retrieve a single summary by its ObjectId.
    """
    try:
        oid = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail=f"Invalid id format: {id}")
    doc = await hh_ru_dataset_collection.find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail=f"Summary {id} not found")
    return HHRuDatasetModel.model_validate(doc)

async def update_hh_ru_dataset(id: str, updates: UpdateHHRuDatasetModel) -> HHRuDatasetModel:
    """
    Update fields of an existing summary. Returns the updated document.
    """
    try:
        oid = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail=f"Invalid id format: {id}")
    data = updates.model_dump(by_alias=True)
    # Remove None values so we don't overwrite with nulls
    data = {k: v for k, v in data.items() if v is not None}
    if data:
        updated = await hh_ru_dataset_collection.find_one_and_update(
            {"_id": oid},
            {"$set": data},
            return_document=ReturnDocument.AFTER,
        )
        if not updated:
            raise HTTPException(status_code=404, detail=f"Summary {id} not found")
        return HHRuDatasetModel.model_validate(updated)
    # No changes—return existing
    existing = await hh_ru_dataset_collection.find_one({"_id": oid})
    if not existing:
        raise HTTPException(status_code=404, detail=f"Summary {id} not found")
    return HHRuDatasetModel.model_validate(existing)

async def delete_hh_ru_dataset(id: str) -> Response:
    """
    Delete a summary by its ObjectId. Returns 204 on success.
    """
    try:
        oid = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail=f"Invalid id format: {id}")
    result = await hh_ru_dataset_collection.delete_one({"_id": oid})
    if result.deleted_count != 1:
        raise HTTPException(status_code=404, detail=f"Summary {id} not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
