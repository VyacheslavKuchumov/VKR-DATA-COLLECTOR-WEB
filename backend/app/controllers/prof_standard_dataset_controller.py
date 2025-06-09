from fastapi import HTTPException, status
from fastapi.responses import Response
from pymongo import ReturnDocument
from bson import ObjectId

from app.database import prof_standard_dataset_collection
from app.models.prof_standard_dataset_model import (
    ProfStandardDatasetModel,
    UpdateProfStandardDatasetModel,
    ProfStandardDatasetCollection,
)

async def create_prof_standard_dataset(item: ProfStandardDatasetModel) -> ProfStandardDatasetModel:
    """
    Insert a new professional standard record into MongoDB and return the created document.
    """
    payload = item.model_dump(by_alias=True, exclude=["id"])
    result = await prof_standard_dataset_collection.insert_one(payload)
    created_doc = await prof_standard_dataset_collection.find_one({"_id": result.inserted_id})
    return ProfStandardDatasetModel.model_validate(created_doc)

async def list_prof_standard_datasets() -> ProfStandardDatasetCollection:
    """
    Retrieve up to 1000 professional standard records.
    """
    docs = await prof_standard_dataset_collection.find().to_list(1000)
    items = [ProfStandardDatasetModel.model_validate(d) for d in docs]
    return ProfStandardDatasetCollection(records=items)

async def show_prof_standard_dataset(id: str) -> ProfStandardDatasetModel:
    """
    Retrieve a single professional standard record by its ObjectId.
    """
    try:
        oid = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail=f"Invalid id format: {id}")
    doc = await prof_standard_dataset_collection.find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail=f"Professional standard record {id} not found")
    return ProfStandardDatasetModel.model_validate(doc)

async def update_prof_standard_dataset(id: str, updates: UpdateProfStandardDatasetModel) -> ProfStandardDatasetModel:
    """
    Update fields of an existing professional standard record. Returns the updated document.
    """
    try:
        oid = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail=f"Invalid id format: {id}")
    data = updates.model_dump(by_alias=True)
    data = {k: v for k, v in data.items() if v is not None}
    if data:
        updated = await prof_standard_dataset_collection.find_one_and_update(
            {"_id": oid},
            {"$set": data},
            return_document=ReturnDocument.AFTER,
        )
        if not updated:
            raise HTTPException(status_code=404, detail=f"Professional standard record {id} not found")
        return ProfStandardDatasetModel.model_validate(updated)
    existing = await prof_standard_dataset_collection.find_one({"_id": oid})
    if not existing:
        raise HTTPException(status_code=404, detail=f"Professional standard record {id} not found")
    return ProfStandardDatasetModel.model_validate(existing)

async def delete_prof_standard_dataset(id: str) -> Response:
    """
    Delete a professional standard record by its ObjectId. Returns 204 on success.
    """
    try:
        oid = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail=f"Invalid id format: {id}")
    result = await prof_standard_dataset_collection.delete_one({"_id": oid})
    if result.deleted_count != 1:
        raise HTTPException(status_code=404, detail=f"Professional standard record {id} not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
