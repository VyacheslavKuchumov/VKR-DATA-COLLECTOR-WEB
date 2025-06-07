from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from pydantic.functional_validators import BeforeValidator
from bson import ObjectId
from typing_extensions import Annotated

# for serializing ObjectId as str
PyObjectId = Annotated[str, BeforeValidator(str)]

class UserModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str = Field(...)
    email: EmailStr = Field(...)
    role: str = Field(...)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "name": "Кучумов Вячеслав Дмитриевич",
                "email": "kuchumov@example.ru",
                "role": "Администратор",
            }
        },
    )

class UpdateUserModel(BaseModel):
    name: str = Field(...)
    email: EmailStr = Field(...)
    role: str = Field(...)

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "name": "Кучумов Вячеслав Дмитриевич",
                "email": "kuchumov@example.ru",
                "role": "Администратор",
            }
        },
    )

class UserCollection(BaseModel):
    users: List[UserModel]
