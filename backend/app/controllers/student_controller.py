from fastapi import HTTPException, status
from fastapi.responses import Response
from pymongo import ReturnDocument
from bson import ObjectId

from app.database import student_collection
from app.models.student_model import (
    StudentModel,
    UpdateStudentModel,
    StudentCollection,
)

async def create_student(student: StudentModel) -> StudentModel:
    payload = student.model_dump(by_alias=True, exclude=["id"])
    result = await student_collection.insert_one(payload)
    created = await student_collection.find_one({"_id": result.inserted_id})
    return StudentModel.model_validate(created)

async def list_students() -> StudentCollection:
    docs = await student_collection.find().to_list(1000)
    return StudentCollection(students=[StudentModel.model_validate(d) for d in docs])

async def show_student(id: str) -> StudentModel:
    doc = await student_collection.find_one({"_id": ObjectId(id)})
    if not doc:
        raise HTTPException(status_code=404, detail=f"Student {id} not found")
    return StudentModel.model_validate(doc)

async def update_student(id: str, updates: UpdateStudentModel) -> StudentModel:
    data = {k: v for k, v in updates.model_dump(by_alias=True).items() if v is not None}
    if data:
        updated = await student_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": data},
            return_document=ReturnDocument.AFTER,
        )
        if not updated:
            raise HTTPException(status_code=404, detail=f"Student {id} not found")
        return StudentModel.model_validate(updated)

    # if no changes, return existing
    existing = await student_collection.find_one({"_id": ObjectId(id)})
    if not existing:
        raise HTTPException(status_code=404, detail=f"Student {id} not found")
    return StudentModel.model_validate(existing)

async def delete_student(id: str) -> Response:
    result = await student_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count != 1:
        raise HTTPException(status_code=404, detail=f"Student {id} not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
