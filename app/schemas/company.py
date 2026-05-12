import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

from app.enums.inventory_enums import IndustryType


class CompanyBase(BaseModel):
    company_name: str
    industry_type: IndustryType
    contact_email: EmailStr | None = None
    contact_phone: str | None = None
    is_active: bool = True


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(BaseModel):
    company_name: str | None = None
    industry_type: IndustryType | None = None
    contact_email: EmailStr | None = None
    contact_phone: str | None = None
    is_active: bool | None = None


class CompanyResponse(CompanyBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
