from pydantic import BaseModel, ConfigDict, EmailStr, Field


class SupplierBaseSchema(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    contact_person: str | None = Field(None, max_length=100)
    email: EmailStr | None = None
    phone: str | None = Field(None, max_length=20)


class CreateSupplierSchema(SupplierBaseSchema):
    pass


class UpdateSupplierSchema(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=100)
    contact_person: str | None = Field(None, max_length=100)
    email: EmailStr | None = None
    phone: str | None = Field(None, max_length=20)


class SupplierResponseSchema(SupplierBaseSchema):
    id: int
    model_config = ConfigDict(from_attributes=True)