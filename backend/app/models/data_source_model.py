from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from pydantic.functional_validators import BeforeValidator
from bson import ObjectId
from typing_extensions import Annotated

# for serializing ObjectId as str
PyObjectId = Annotated[str, BeforeValidator(str)]

class DataSourceModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str = Field(...)
    link: str = Field(...)
    source_type: str = Field(...)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "name": "Реестр ФГОСов",
                "link": "https://example.com/data-source",
                "source_type": "fgos",
            }
        },
    )

class UpdateDataSourceModel(BaseModel):
    name: str = Field(...)
    link: str = Field(...)

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "name": "Реестр ФГОСов",
                "link": "https://example.com/data-source",
            }
        },
    )

class DataSourceCollection(BaseModel):
    sources: List[DataSourceModel]
