from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated
from bson import ObjectId

# Serialize MongoDB ObjectId as string
PyObjectId = Annotated[str, BeforeValidator(str)]

class ClassificatorProfDatasetModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    prof_code: str = Field(..., description="Profession code, e.g., 10003")
    prof_name: str = Field(..., description="Name of the profession, e.g., 'Авербандщик'")

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "prof_code": "10003",
                "prof_name": "Авербандщик"
            }
        },
    )

class UpdateClassificatorProfDatasetModel(BaseModel):
    prof_code: str = Field(..., description="Profession code, e.g., 10003")
    prof_name: str = Field(..., description="Name of the profession, e.g., 'Авербандщик'")

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "prof_code": "10005",
                "prof_name": "Авиационный механик (техник) по планеру и двигателям"
            }
        },
    )

class ClassificatorProfDatasetCollection(BaseModel):
    records: List[ClassificatorProfDatasetModel]
