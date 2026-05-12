import uuid
from decimal import Decimal

from sqlalchemy import ForeignKey, Integer, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class PurchaseOrderLineItem(Base, TimestampMixin):
    __tablename__ = "purchase_order_line_items"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    purchase_order_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("purchase_orders.id", ondelete="CASCADE"), nullable=False, index=True)
    item_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("items.id", ondelete="RESTRICT"), nullable=False, index=True)
    quantity_ordered: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_cost: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    line_total: Mapped[Decimal | None] = mapped_column(Numeric(14, 2), nullable=True)
    quantity_received: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    current_stock_snapshot: Mapped[int | None] = mapped_column(Integer, nullable=True)

    purchase_order: Mapped["PurchaseOrder"] = relationship("PurchaseOrder", back_populates="line_items")
    item: Mapped["Item"] = relationship("Item", back_populates="purchase_order_line_items")
