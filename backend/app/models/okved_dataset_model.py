from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated
from bson import ObjectId

# Serialize MongoDB ObjectId as string
PyObjectId = Annotated[str, BeforeValidator(str)]

class OkvedDatasetModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    okved_code: str = Field(..., description="OKVED code, e.g., 'Раздел A'")
    okved_name: str = Field(..., description="Name corresponding to the OKVED code")

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "okved_code": "Раздел A",
                "okved_name": "Сельское, лесное хозяйство, охота, рыболовство и рыбоводство"
            }
        },
    )

class UpdateOkvedDatasetModel(BaseModel):
    okved_code: str = Field(..., description="OKVED code")
    okved_name: str = Field(..., description="Name corresponding to the OKVED code")

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "okved_code": "Раздел B",
                "okved_name": "Добыча полезных ископаемых"
            }
        },
    )

class OkvedDatasetCollection(BaseModel):
    records: List[OkvedDatasetModel]
