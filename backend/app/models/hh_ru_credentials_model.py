from typing import Optional
from pydantic import BaseModel, Field
from pydantic import ConfigDict
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated
from bson import ObjectId

# для сериализации ObjectId в str
PyObjectId = Annotated[str, BeforeValidator(str)]


class HHRuCredentialsModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    HH_RU_ACCESS_TOKEN: Optional[str] = Field(
        None, alias="HH_RU_ACCESS_TOKEN", description="Access token для API hh.ru"
    )
    HH_RU_REFRESH_TOKEN: Optional[str] = Field(
        None, alias="HH_RU_REFRESH_TOKEN", description="Refresh token для API hh.ru"
    )
    HH_RU_CLIENT_ID: str = Field(
        ..., alias="HH_RU_CLIENT_ID", description="Client ID для API hh.ru"
    )
    HH_RU_CLIENT_SECRET: str = Field(
        ..., alias="HH_RU_CLIENT_SECRET", description="Client secret для API hh.ru"
    )
    HH_RU_REDIRECT_URI: str = Field(
        ..., alias="HH_RU_REDIRECT_URI", description="Redirect URI для API hh.ru"
    )


    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "_id": "60f7c2ab3e1f4e4d2a1b2c3d",
                "HH_RU_ACCESS_TOKEN": "abcdef123456",
                "HH_RU_REFRESH_TOKEN": "uvwxyz789012",
                "HH_RU_CLIENT_ID": "my_client_id",
                "HH_RU_CLIENT_SECRET": "my_client_secret",
                "HH_RU_REDIRECT_URI": "https://myapp.com/callback"
            }
        },
    )

class UpdateHHRuCredentialsModel(BaseModel):
    HH_RU_ACCESS_TOKEN: Optional[str] = Field(
        None, alias="HH_RU_ACCESS_TOKEN", description="Access token для API hh.ru"
    )
    HH_RU_REFRESH_TOKEN: Optional[str] = Field(
        None, alias="HH_RU_REFRESH_TOKEN", description="Refresh token для API hh.ru"
    )
    HH_RU_CLIENT_ID: Optional[str] = Field(
        None, alias="HH_RU_CLIENT_ID", description="Client ID для API hh.ru"
    )
    HH_RU_CLIENT_SECRET: Optional[str] = Field(
        None, alias="HH_RU_CLIENT_SECRET", description="Client secret для API hh.ru"
    )
    HH_RU_REDIRECT_URI: Optional[str] = Field(
        None, alias="HH_RU_REDIRECT_URI", description="Redirect URI для API hh.ru"
    )

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "_id": "60f7c2ab3e1f4e4d2a1b2c3d",
                "HH_RU_ACCESS_TOKEN": "new_access_token",
                "HH_RU_REFRESH_TOKEN": "new_refresh_token"
            }
        },
    )

class HHRuCredentialsCollection(BaseModel):
    credentials: list[HHRuCredentialsModel]
