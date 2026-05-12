import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class SaleLineItemBase(BaseModel):
    quantity_sold: int = Field(ge=1)
    unit_price: Decimal = Field(ge=0)
    discount_percent: Decimal = Field(default=Decimal("0"), ge=0, le=100)
    line_total: Decimal | None = None
    line_profit: Decimal | None = None


class SaleLineItemCreate(SaleLineItemBase):
    sale_id: uuid.UUID
    item_id: uuid.UUID


class SaleLineItemUpdate(BaseModel):
    quantity_sold: int | None = Field(default=None, ge=1)
    unit_price: Decimal | None = Field(default=None, ge=0)
    discount_percent: Decimal | None = Field(default=None, ge=0, le=100)
    line_total: Decimal | None = None
    line_profit: Decimal | None = None


class SaleLineItemResponse(SaleLineItemBase):
    id: uuid.UUID
    sale_id: uuid.UUID
    item_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
