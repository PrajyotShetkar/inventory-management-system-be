import uuid
from datetime import date
from decimal import Decimal

from sqlalchemy import Date, ForeignKey, Integer, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class Item(Base, TimestampMixin):
    __tablename__ = "items"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    item_name: Mapped[str] = mapped_column(String(255), nullable=False)
    sku_code: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    description: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    category: Mapped[str | None] = mapped_column(String(100), nullable=True)
    store_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("stores.id", ondelete="CASCADE"), nullable=False, index=True)
    vendor_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("vendors.id", ondelete="SET NULL"), nullable=True, index=True)
    cost_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    sale_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    discount_percent: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False, default=Decimal("0"))
    final_price: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    margin_percent: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), nullable=True)
    inventory_value: Mapped[Decimal | None] = mapped_column(Numeric(14, 2), nullable=True)
    stock_quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    reorder_level: Mapped[int] = mapped_column(Integer, nullable=False, default=10)
    last_restocked_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    store: Mapped["Store"] = relationship("Store", back_populates="items")
    vendor: Mapped["Vendor | None"] = relationship("Vendor", back_populates="items")
    purchase_order_line_items: Mapped[list["PurchaseOrderLineItem"]] = relationship("PurchaseOrderLineItem", back_populates="item")
    sale_line_items: Mapped[list["SaleLineItem"]] = relationship("SaleLineItem", back_populates="item")
    inventory_logs: Mapped[list["InventoryLog"]] = relationship("InventoryLog", back_populates="item")
