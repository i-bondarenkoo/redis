from email.policy import default
from pydantic import BaseModel, ConfigDict, Field


class CreateSinger(BaseModel):
    name: str
    genre: str
    albums_count: int = Field(
        gt=0, description="Количество альбомов должно быть больше 0"
    )


class ResponseSinger(CreateSinger):
    id: int

    model_config = ConfigDict(from_attributes=True)


class UpdateSinger(BaseModel):
    name: str | None = None
    genre: str | None = None
    albums_count: int | None = Field(
        default=None, gt=0, description="Количество альбомов должно быть больше 0"
    )
