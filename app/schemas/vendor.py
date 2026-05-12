import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.enums.inventory_enums import PaymentTerms


class VendorBase(BaseModel):
    vendor_name: str
    contact_person: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    address: str | None = None
    payment_terms: PaymentTerms | None = None
    lead_time_days: int | None = Field(default=7, ge=1, le=365)
    is_active: bool = True


class VendorCreate(VendorBase):
    pass


class VendorUpdate(BaseModel):
    vendor_name: str | None = None
    contact_person: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    address: str | None = None
    payment_terms: PaymentTerms | None = None
    lead_time_days: int | None = Field(default=None, ge=1, le=365)
    is_active: bool | None = None


class VendorResponse(VendorBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
