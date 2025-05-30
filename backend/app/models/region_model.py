from typing import Optional, List
from pydantic import BaseModel, Field
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated
from bson import ObjectId
from pydantic import ConfigDict

# для сериализации ObjectId в str
PyObjectId = Annotated[str, BeforeValidator(str)]

class RegionModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    region_name: str = Field(..., description="Название региона")
    country: str = Field(..., description="Страна")
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "region_name": "California",
                "country": "USA"
            }
        },
    )

class UpdateRegionModel(BaseModel):
    region_name: Optional[str] = Field(None, description="Название региона")
    country: Optional[str] = Field(None, description="Страна")

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "region_name": "California",
                "country": "USA"
            }
        },
    )

class RegionCollection(BaseModel):
    regions: List[RegionModel]
