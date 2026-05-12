import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.inventory_log import InventoryLog
from app.schemas.inventory_log import InventoryLogCreate


class InventoryLogService:

    @staticmethod
    async def get_all(db: AsyncSession) -> list[InventoryLog]:
        result = await db.execute(select(InventoryLog).order_by(InventoryLog.log_date.desc()))
        return list(result.scalars().all())

    @staticmethod
    async def get_by_id(db: AsyncSession, log_id: uuid.UUID) -> InventoryLog | None:
        result = await db.execute(select(InventoryLog).where(InventoryLog.id == log_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def create(db: AsyncSession, data: InventoryLogCreate) -> InventoryLog:
        log = InventoryLog(**data.model_dump())
        db.add(log)
        await db.flush()
        await db.refresh(log)
        return log
