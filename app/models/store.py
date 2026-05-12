import uuid

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class Store(Base, TimestampMixin):
    __tablename__ = "stores"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    store_name: Mapped[str] = mapped_column(String(255), nullable=False)
    location: Mapped[str | None] = mapped_column(String(500), nullable=True)
    company_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("companies.id", ondelete="CASCADE"), nullable=False, index=True)
    manager_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    manager_email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    store_phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    company: Mapped["Company"] = relationship("Company", back_populates="stores")
    items: Mapped[list["Item"]] = relationship("Item", back_populates="store", cascade="all, delete-orphan")
    purchase_orders: Mapped[list["PurchaseOrder"]] = relationship("PurchaseOrder", back_populates="store")
    sales_transactions: Mapped[list["SalesTransaction"]] = relationship("SalesTransaction", back_populates="store")
    inventory_logs: Mapped[list["InventoryLog"]] = relationship("InventoryLog", back_populates="store")
