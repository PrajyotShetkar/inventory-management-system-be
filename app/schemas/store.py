import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class StoreBase(BaseModel):
    store_name: str
    location: str | None = None
    manager_name: str | None = None
    manager_email: EmailStr | None = None
    store_phone: str | None = None
    is_active: bool = True


class StoreCreate(StoreBase):
    company_id: uuid.UUID


class StoreUpdate(BaseModel):
    store_name: str | None = None
    location: str | None = None
    manager_name: str | None = None
    manager_email: EmailStr | None = None
    store_phone: str | None = None
    is_active: bool | None = None


class StoreResponse(StoreBase):
    id: uuid.UUID
    company_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
