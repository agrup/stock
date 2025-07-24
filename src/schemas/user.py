from pydantic import BaseModel, EmailStr, Field, ConfigDict


class CreateUserSchema(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr


class UserResponseSchema(BaseModel):
    name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)
