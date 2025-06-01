from typing import Optional, List
from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel, Field
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated
from pydantic import ConfigDict

# serialize MongoDB ObjectId → str
PyObjectId = Annotated[str, BeforeValidator(str)]

class JobModel(BaseModel):
    """
    Full Job document as stored in MongoDB.
    """
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    job_id: str = Field(..., description="UUID used to identify this job")
    status: str = Field(..., description="pending | running | finished | error")
    created_at: datetime = Field(..., description="when the job was created")
    finished_at: Optional[datetime] = Field(
        None, description="when the job completed (if finished)"
    )
    exit_code: Optional[int] = Field(None, description="process exit code")
    logs: Optional[list] = Field(None, description="optional logs")

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ ObjectId: str, datetime: lambda dt: dt.isoformat() },
        json_schema_extra={
            "example": {
                "job_id": "123e4567-e89b-12d3-a456-426614174000",
                "status": "pending",
                "created_at": "2025-05-31T12:34:56.789Z",
                "finished_at": None,
                "exit_code": None
            }
        },
    )

class CreateJobModel(BaseModel):
    """
    What your POST /jobs endpoint expects.
    Timestamps & _id filled in server-side.
    """
    job_id: str = Field(..., description="UUID for this job")
    status: Optional[str] = Field("pending", description="initial status")

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ datetime: lambda dt: dt.isoformat() },
        json_schema_extra={
            "example": {
                "job_id": "123e4567-e89b-12d3-a456-426614174000",
                "status": "pending"
            }
        },
    )

class UpdateJobModel(BaseModel):
    """
    Fields you might update mid-flight or at completion.
    """
    status: Optional[str] = Field(None, description="new status")
    finished_at: Optional[datetime] = Field(None, description="completion timestamp")
    exit_code: Optional[int] = Field(None, description="process exit code")

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ datetime: lambda dt: dt.isoformat() },
        json_schema_extra={
            "example": {
                "status": "finished",
                "finished_at": "2025-05-31T12:45:00.000Z",
                "exit_code": 0
            }
        },
    )

class JobCollection(BaseModel):
    """
    Wrapper when returning a list of jobs.
    """
    jobs: List[JobModel]

