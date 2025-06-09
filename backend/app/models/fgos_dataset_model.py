from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated
from bson import ObjectId

# Serialize MongoDB ObjectId as string
PyObjectId = Annotated[str, BeforeValidator(str)]

class FgosDatasetModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    fgos_code: str = Field(..., description="FGOS code, e.g., 09.03.01")
    fgos_name: str = Field(..., description="Name of the FGOS program")
    fgos_prikaz: str = Field(..., description="Ministerial order (приказ) that established or amended the FGOS")

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "fgos_code": "09.03.01",
                "fgos_name": "Информатика и вычислительная техника",
                "fgos_prikaz": "Приказ Минобрнауки России от 19.09.2017 N 929 (ред. от 08.02.2021)"
            }
        },
    )

class UpdateFgosDatasetModel(BaseModel):
    fgos_code: str = Field(..., description="FGOS code")
    fgos_name: str = Field(..., description="Name of the FGOS program")
    fgos_prikaz: str = Field(..., description="Ministerial order (приказ)")

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "fgos_code": "44.03.01",
                "fgos_name": "Педагогическое образование",
                "fgos_prikaz": "Приказ Минобрнауки России от 22.02.2018 N 121 (ред. от 08.02.2021)"
            }
        },
    )

class FgosDatasetCollection(BaseModel):
    records: List[FgosDatasetModel]
