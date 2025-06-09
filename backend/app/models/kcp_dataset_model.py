from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated
from bson import ObjectId

# Сериализация MongoDB ObjectId как строки
PyObjectId = Annotated[str, BeforeValidator(str)]

class KcpModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    year: int = Field(..., description="Год, к которому относится количество КЦП")
    study_field_code: str = Field(..., description="Код направления подготовки, например: 08.02.01")
    study_field_name: str = Field(..., description="Наименование направления подготовки")
    kcp_num: int = Field(..., description="Количество КЦП (контрольных цифр приема)")

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "year": 2024,
                "study_field_code": "08.02.01",
                "study_field_name": "Строительство и эксплуатация зданий и сооружений",
                "kcp_num": 295
            }
        },
    )

class UpdateKcpModel(BaseModel):
    year: int = Field(..., description="Год, к которому относится количество КЦП")
    study_field_code: str = Field(..., description="Код направления подготовки")
    study_field_name: str = Field(..., description="Наименование направления подготовки")
    kcp_num: int = Field(..., description="Количество КЦП")

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "year": 2023,
                "study_field_code": "08.02.01",
                "study_field_name": "Строительство и эксплуатация зданий и сооружений",
                "kcp_num": 865
            }
        },
    )

class KcpCollection(BaseModel):
    records: List[KcpModel]
