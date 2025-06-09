from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated
from bson import ObjectId

# Сериализация MongoDB ObjectId как строки
PyObjectId = Annotated[str, BeforeValidator(str)]

class ProfStandardDatasetModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    prof_standard_code: str = Field(..., description="Код профессионального стандарта, например: 01.001")
    prof_standard_sphere: str = Field(..., description="Сфера деятельности, например: Образование и наука")
    prof_standard_type: str = Field(..., description="Тип профессиональной деятельности")
    prof_standard_name: str = Field(..., description="Наименование профессионального стандарта")

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "prof_standard_code": "01.001",
                "prof_standard_sphere": "Образование и наука",
                "prof_standard_type": "Дошкольное образование\nНачальное общее образование\nОсновное общее образование\nСреднее общее образование",
                "prof_standard_name": "Педагог (педагогическая деятельность в сфере дошкольного, начального общего, основного общего, среднего общего образования) (воспитатель, учитель)"
            }
        },
    )

class UpdateProfStandardDatasetModel(BaseModel):
    prof_standard_code: str = Field(..., description="Код профессионального стандарта")
    prof_standard_sphere: str = Field(..., description="Сфера деятельности")
    prof_standard_type: str = Field(..., description="Тип профессиональной деятельности")
    prof_standard_name: str = Field(..., description="Наименование профессионального стандарта")

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "prof_standard_code": "06.001",
                "prof_standard_sphere": "Связь, информационные и коммуникационные технологии",
                "prof_standard_type": "Разработка компьютерного программного обеспечения",
                "prof_standard_name": "Программист"
            }
        },
    )

class ProfStandardDatasetCollection(BaseModel):
    records: List[ProfStandardDatasetModel]
