from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from pydantic.functional_validators import BeforeValidator
from bson import ObjectId
from typing_extensions import Annotated

# Serialize MongoDB ObjectId as string
PyObjectId = Annotated[str, BeforeValidator(str)]

class MinstatWorkerModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    okved_group: str = Field(..., description="OKVED sector name")
    year: int = Field(..., ge=1900, le=2100, description="Year of statistics")
    worker_num: float = Field(..., ge=0, description="Number of workers (in thousands)")

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "okved_group": "Обрабатывающие производства",
                "year": 2010,
                "worker_num": 245.751
            }
        },
    )

class UpdateMinstatWorkerModel(BaseModel):
    okved_group: str = Field(..., description="OKVED sector name")
    year: int = Field(..., ge=1900, le=2100, description="Year of statistics")
    worker_num: float = Field(..., ge=0, description="Number of workers (in thousands)")

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "okved_group": "Строительство",
                "year": 2010,
                "worker_num": 111.063
            }
        },
    )

class MinstatWorkerCollection(BaseModel):
    workers: List[MinstatWorkerModel]
