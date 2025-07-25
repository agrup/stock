from pydantic import BaseModel, ConfigDict, Field


class CreateCategorySchema(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: str | None = Field(None, max_length=255)


class UpdateCategorySchema(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=100)
    description: str | None = Field(None, max_length=255)


class CategoryResponseSchema(BaseModel):
    id: int
    name: str
    description: str | None

    model_config = ConfigDict(from_attributes=True)