import uuid

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate


class ItemService:

    @staticmethod
    async def get_all(db: AsyncSession) -> list[Item]:
        result = await db.execute(select(Item).order_by(Item.created_at.desc()))
        return list(result.scalars().all())

    @staticmethod
    async def get_by_id(db: AsyncSession, item_id: uuid.UUID) -> Item | None:
        result = await db.execute(select(Item).where(Item.id == item_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def create(db: AsyncSession, data: ItemCreate) -> Item:
        item = Item(**data.model_dump())
        db.add(item)
        await db.flush()
        await db.refresh(item)
        return item

    @staticmethod
    async def update(db: AsyncSession, item_id: uuid.UUID, data: ItemUpdate) -> Item | None:
        item = await ItemService.get_by_id(db, item_id)
        if not item:
            return None
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(item, field, value)
        await db.flush()
        await db.refresh(item)
        return item

    @staticmethod
    async def delete_by_id(db: AsyncSession, item_id: uuid.UUID) -> bool:
        item = await ItemService.get_by_id(db, item_id)
        if not item:
            return False
        await db.delete(item)
        await db.flush()
        return True

    @staticmethod
    async def delete_all(db: AsyncSession) -> int:
        result = await db.execute(delete(Item))
        await db.flush()
        return result.rowcount
