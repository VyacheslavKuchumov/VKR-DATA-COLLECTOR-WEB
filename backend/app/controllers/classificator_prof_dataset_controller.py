from fastapi import HTTPException, status
from fastapi.responses import Response
from pymongo import ReturnDocument
from bson import ObjectId

from app.database import classificator_prof_dataset_collection
from app.models.classificator_prof_dataset_model import (
    ClassificatorProfDatasetModel,
    UpdateClassificatorProfDatasetModel,
    ClassificatorProfDatasetCollection,
)

async def create_prof_dataset(item: ClassificatorProfDatasetModel) -> ClassificatorProfDatasetModel:
    """
    Insert a new profession record into MongoDB and return the created document.
    """
    payload = item.model_dump(by_alias=True, exclude=["id"])
    result = await classificator_prof_dataset_collection.insert_one(payload)
    created_doc = await classificator_prof_dataset_collection.find_one({"_id": result.inserted_id})
    return ClassificatorProfDatasetModel.model_validate(created_doc)

async def list_prof_datasets() -> ClassificatorProfDatasetCollection:
    """
    Retrieve up to 1000 profession records.
    """
    docs = await classificator_prof_dataset_collection.find().to_list(1000)
    items = [ClassificatorProfDatasetModel.model_validate(d) for d in docs]
    return ClassificatorProfDatasetCollection(records=items)

async def show_prof_dataset(id: str) -> ClassificatorProfDatasetModel:
    """
    Retrieve a single profession record by its ObjectId.
    """
    try:
        oid = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail=f"Invalid id format: {id}")
    doc = await classificator_prof_dataset_collection.find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail=f"Profession record {id} not found")
    return ClassificatorProfDatasetModel.model_validate(doc)

async def update_prof_dataset(id: str, updates: UpdateClassificatorProfDatasetModel) -> ClassificatorProfDatasetModel:
    """
    Update fields of an existing profession record. Returns the updated document.
    """
    try:
        oid = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail=f"Invalid id format: {id}")
    data = updates.model_dump(by_alias=True)
    data = {k: v for k, v in data.items() if v is not None}
    if data:
        updated = await classificator_prof_dataset_collection.find_one_and_update(
            {"_id": oid},
            {"$set": data},
            return_document=ReturnDocument.AFTER,
        )
        if not updated:
            raise HTTPException(status_code=404, detail=f"Profession record {id} not found")
        return ClassificatorProfDatasetModel.model_validate(updated)
    existing = await classificator_prof_dataset_collection.find_one({"_id": oid})
    if not existing:
        raise HTTPException(status_code=404, detail=f"Profession record {id} not found")
    return ClassificatorProfDatasetModel.model_validate(existing)

async def delete_prof_dataset(id: str) -> Response:
    """
    Delete a profession record by its ObjectId. Returns 204 on success.
    """
    try:
        oid = ObjectId(id)
    except Exception:
        raise HTTPException(status_code=400, detail=f"Invalid id format: {id}")
    result = await classificator_prof_dataset_collection.delete_one({"_id": oid})
    if result.deleted_count != 1:
        raise HTTPException(status_code=404, detail=f"Profession record {id} not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)