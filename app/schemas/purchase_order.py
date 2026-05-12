import uuid
from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.enums.inventory_enums import POStatus


class PurchaseOrderBase(BaseModel):
    po_number: str
    order_date: date
    expected_delivery_date: date | None = None
    status: POStatus = POStatus.DRAFT
    notes: str | None = None
    total_amount: Decimal = Field(default=Decimal("0"), ge=0)


class PurchaseOrderCreate(PurchaseOrderBase):
    vendor_id: uuid.UUID
    store_id: uuid.UUID


class PurchaseOrderUpdate(BaseModel):
    expected_delivery_date: date | None = None
    status: POStatus | None = None
    notes: str | None = None
    total_amount: Decimal | None = Field(default=None, ge=0)


class PurchaseOrderResponse(PurchaseOrderBase):
    id: uuid.UUID
    vendor_id: uuid.UUID
    store_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
