import uuid

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.sale_line_item import SaleLineItem
from app.schemas.sale_line_item import SaleLineItemCreate, SaleLineItemUpdate


class SaleLineItemService:

    @staticmethod
    async def get_all(db: AsyncSession) -> list[SaleLineItem]:
        result = await db.execute(select(SaleLineItem).order_by(SaleLineItem.created_at.desc()))
        return list(result.scalars().all())

    @staticmethod
    async def get_by_id(db: AsyncSession, line_item_id: uuid.UUID) -> SaleLineItem | None:
        result = await db.execute(select(SaleLineItem).where(SaleLineItem.id == line_item_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def create(db: AsyncSession, data: SaleLineItemCreate) -> SaleLineItem:
        line_item = SaleLineItem(**data.model_dump())
        db.add(line_item)
        await db.flush()
        await db.refresh(line_item)
        return line_item

    @staticmethod
    async def update(db: AsyncSession, line_item_id: uuid.UUID, data: SaleLineItemUpdate) -> SaleLineItem | None:
        line_item = await SaleLineItemService.get_by_id(db, line_item_id)
        if not line_item:
            return None
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(line_item, field, value)
        await db.flush()
        await db.refresh(line_item)
        return line_item

    @staticmethod
    async def delete_by_id(db: AsyncSession, line_item_id: uuid.UUID) -> bool:
        line_item = await SaleLineItemService.get_by_id(db, line_item_id)
        if not line_item:
            return False
        await db.delete(line_item)
        await db.flush()
        return True

    @staticmethod
    async def delete_all(db: AsyncSession) -> int:
        result = await db.execute(delete(SaleLineItem))
        await db.flush()
        return result.rowcount
