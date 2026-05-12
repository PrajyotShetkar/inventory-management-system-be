import uuid
from decimal import Decimal

from sqlalchemy import ForeignKey, Integer, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class SaleLineItem(Base, TimestampMixin):
    __tablename__ = "sale_line_items"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sale_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("sales_transactions.id", ondelete="CASCADE"), nullable=False, index=True)
    item_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("items.id", ondelete="RESTRICT"), nullable=False, index=True)
    quantity_sold: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    discount_percent: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False, default=Decimal("0"))
    line_total: Mapped[Decimal | None] = mapped_column(Numeric(14, 2), nullable=True)
    line_profit: Mapped[Decimal | None] = mapped_column(Numeric(14, 2), nullable=True)

    sale: Mapped["SalesTransaction"] = relationship("SalesTransaction", back_populates="line_items")
    item: Mapped["Item"] = relationship("Item", back_populates="sale_line_items")
