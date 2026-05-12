import uuid
from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.enums.inventory_enums import PaymentMethod, SaleStatus


class SalesTransactionBase(BaseModel):
    sale_number: str
    customer_name: str | None = None
    customer_email: EmailStr | None = None
    sale_date: date
    payment_method: PaymentMethod | None = None
    status: SaleStatus = SaleStatus.COMPLETED
    notes: str | None = None
    total_amount: Decimal = Field(default=Decimal("0"), ge=0)


class SalesTransactionCreate(SalesTransactionBase):
    store_id: uuid.UUID


class SalesTransactionUpdate(BaseModel):
    customer_name: str | None = None
    customer_email: EmailStr | None = None
    payment_method: PaymentMethod | None = None
    status: SaleStatus | None = None
    notes: str | None = None
    total_amount: Decimal | None = Field(default=None, ge=0)


class SalesTransactionResponse(SalesTransactionBase):
    id: uuid.UUID
    store_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
