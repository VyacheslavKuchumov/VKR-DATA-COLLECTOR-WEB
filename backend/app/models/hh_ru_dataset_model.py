from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated
from bson import ObjectId

# Serialize MongoDB ObjectId as string
PyObjectId = Annotated[str, BeforeValidator(str)]

class HHRuDatasetModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    entry_date: datetime = Field(..., description="Date when the vacancy summary was recorded")
    professional_role: str = Field(..., description="Name of the professional role")
    vacancies_num: int = Field(..., ge=0, description="Number of vacancies for that role on that date")

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "entry_date": "2024-10-03",
                "professional_role": "Ветеринарный врач",
                "vacancies_num": 5
            }
        },
    )

class UpdateHHRuDatasetModel(BaseModel):
    entry_date: datetime = Field(..., description="Date when the vacancy summary was recorded")
    professional_role: str = Field(..., description="Name of the professional role")
    vacancies_num: int = Field(..., ge=0, description="Number of vacancies for that role on that date")

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "entry_date": "2024-10-04",
                "professional_role": "Продавец-консультант",
                "vacancies_num": 3
            }
        },
    )

class HHRuDatasetCollection(BaseModel):
    summaries: List[HHRuDatasetModel]
