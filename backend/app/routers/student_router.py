from fastapi import APIRouter, Body, status
from app.models.student_model import StudentModel, UpdateStudentModel, StudentCollection
from app.controllers.student_controller import (
    create_student,
    list_students,
    show_student,
    update_student,
    delete_student,
)

router = APIRouter()

@router.post(
    "/",
    response_model=StudentModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
    response_description="Add new student",
)
async def post_student(student: StudentModel = Body(...)):
    return await create_student(student)

@router.get(
    "/",
    response_model=StudentCollection,
    response_model_by_alias=False,
    response_description="List all students",
)
async def get_students():
    return await list_students()

@router.get(
    "/{id}",
    response_model=StudentModel,
    response_model_by_alias=False,
    response_description="Get a single student",
)
async def get_student(id: str):
    return await show_student(id)

@router.put(
    "/{id}",
    response_model=StudentModel,
    response_model_by_alias=False,
    response_description="Update a student",
)
async def put_student(
    id: str,
    student: UpdateStudentModel = Body(...),
):
    return await update_student(id, student)

@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="Delete a student",
)
async def delete_student_route(id: str):
    return await delete_student(id)
