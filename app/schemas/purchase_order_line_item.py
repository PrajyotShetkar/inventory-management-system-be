import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class PurchaseOrderLineItemBase(BaseModel):
    quantity_ordered: int = Field(ge=1)
    unit_cost: Decimal = Field(ge=0)
    line_total: Decimal | None = None
    quantity_received: int = Field(default=0, ge=0)
    current_stock_snapshot: int | None = None


class PurchaseOrderLineItemCreate(PurchaseOrderLineItemBase):
    purchase_order_id: uuid.UUID
    item_id: uuid.UUID


class PurchaseOrderLineItemUpdate(BaseModel):
    quantity_ordered: int | None = Field(default=None, ge=1)
    unit_cost: Decimal | None = Field(default=None, ge=0)
    line_total: Decimal | None = None
    quantity_received: int | None = Field(default=None, ge=0)


class PurchaseOrderLineItemResponse(PurchaseOrderLineItemBase):
    id: uuid.UUID
    purchase_order_id: uuid.UUID
    item_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
