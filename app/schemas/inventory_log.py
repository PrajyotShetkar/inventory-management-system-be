import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.enums.inventory_enums import ChangeType


class InventoryLogBase(BaseModel):
    change_type: ChangeType
    quantity_change: int
    reference_number: str | None = None
    notes: str | None = None


class InventoryLogCreate(InventoryLogBase):
    item_id: uuid.UUID
    store_id: uuid.UUID


class InventoryLogResponse(InventoryLogBase):
    id: uuid.UUID
    item_id: uuid.UUID
    store_id: uuid.UUID
    log_date: datetime
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
