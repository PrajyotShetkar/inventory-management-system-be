import uuid

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.store import Store
from app.schemas.store import StoreCreate, StoreUpdate


class StoreService:

    @staticmethod
    async def get_all(db: AsyncSession) -> list[Store]:
        result = await db.execute(select(Store).order_by(Store.created_at.desc()))
        return list(result.scalars().all())

    @staticmethod
    async def get_by_id(db: AsyncSession, store_id: uuid.UUID) -> Store | None:
        result = await db.execute(select(Store).where(Store.id == store_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def create(db: AsyncSession, data: StoreCreate) -> Store:
        store = Store(**data.model_dump())
        db.add(store)
        await db.flush()
        await db.refresh(store)
        return store

    @staticmethod
    async def update(db: AsyncSession, store_id: uuid.UUID, data: StoreUpdate) -> Store | None:
        store = await StoreService.get_by_id(db, store_id)
        if not store:
            return None
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(store, field, value)
        await db.flush()
        await db.refresh(store)
        return store

    @staticmethod
    async def delete_by_id(db: AsyncSession, store_id: uuid.UUID) -> bool:
        store = await StoreService.get_by_id(db, store_id)
        if not store:
            return False
        await db.delete(store)
        await db.flush()
        return True

    @staticmethod
    async def delete_all(db: AsyncSession) -> int:
        result = await db.execute(delete(Store))
        await db.flush()
        return result.rowcount
