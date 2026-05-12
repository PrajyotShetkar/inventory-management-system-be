import uuid
from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.enums.inventory_enums import ItemCategory


class ItemBase(BaseModel):
    item_name: str
    sku_code: str
    description: str | None = None
    category: ItemCategory | None = None
    cost_price: Decimal = Field(ge=0)
    sale_price: Decimal = Field(ge=0)
    discount_percent: Decimal = Field(default=Decimal("0"), ge=0, le=100)
    stock_quantity: int = Field(default=0, ge=0)
    reorder_level: int = Field(default=10, ge=0)
    last_restocked_date: date | None = None


class ItemCreate(ItemBase):
    store_id: uuid.UUID
    vendor_id: uuid.UUID | None = None
    final_price: Decimal | None = None
    margin_percent: Decimal | None = None
    inventory_value: Decimal | None = None


class ItemUpdate(BaseModel):
    item_name: str | None = None
    description: str | None = None
    category: ItemCategory | None = None
    cost_price: Decimal | None = Field(default=None, ge=0)
    sale_price: Decimal | None = Field(default=None, ge=0)
    discount_percent: Decimal | None = Field(default=None, ge=0, le=100)
    stock_quantity: int | None = Field(default=None, ge=0)
    reorder_level: int | None = Field(default=None, ge=0)
    last_restocked_date: date | None = None
    vendor_id: uuid.UUID | None = None
    final_price: Decimal | None = None
    margin_percent: Decimal | None = None
    inventory_value: Decimal | None = None


class ItemResponse(ItemBase):
    id: uuid.UUID
    store_id: uuid.UUID
    vendor_id: uuid.UUID | None
    final_price: Decimal | None
    margin_percent: Decimal | None
    inventory_value: Decimal | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
