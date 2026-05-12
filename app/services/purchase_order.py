import uuid

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.purchase_order import PurchaseOrder
from app.schemas.purchase_order import PurchaseOrderCreate, PurchaseOrderUpdate


class PurchaseOrderService:

    @staticmethod
    async def get_all(db: AsyncSession) -> list[PurchaseOrder]:
        result = await db.execute(select(PurchaseOrder).order_by(PurchaseOrder.created_at.desc()))
        return list(result.scalars().all())

    @staticmethod
    async def get_by_id(db: AsyncSession, po_id: uuid.UUID) -> PurchaseOrder | None:
        result = await db.execute(select(PurchaseOrder).where(PurchaseOrder.id == po_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def create(db: AsyncSession, data: PurchaseOrderCreate) -> PurchaseOrder:
        po = PurchaseOrder(**data.model_dump())
        db.add(po)
        await db.flush()
        await db.refresh(po)
        return po

    @staticmethod
    async def update(db: AsyncSession, po_id: uuid.UUID, data: PurchaseOrderUpdate) -> PurchaseOrder | None:
        po = await PurchaseOrderService.get_by_id(db, po_id)
        if not po:
            return None
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(po, field, value)
        await db.flush()
        await db.refresh(po)
        return po

    @staticmethod
    async def delete_by_id(db: AsyncSession, po_id: uuid.UUID) -> bool:
        po = await PurchaseOrderService.get_by_id(db, po_id)
        if not po:
            return False
        await db.delete(po)
        await db.flush()
        return True

    @staticmethod
    async def delete_all(db: AsyncSession) -> int:
        result = await db.execute(delete(PurchaseOrder))
        await db.flush()
        return result.rowcount
