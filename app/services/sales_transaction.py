import uuid

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.sales_transaction import SalesTransaction
from app.schemas.sales_transaction import SalesTransactionCreate, SalesTransactionUpdate


class SalesTransactionService:

    @staticmethod
    async def get_all(db: AsyncSession) -> list[SalesTransaction]:
        result = await db.execute(select(SalesTransaction).order_by(SalesTransaction.created_at.desc()))
        return list(result.scalars().all())

    @staticmethod
    async def get_by_id(db: AsyncSession, sale_id: uuid.UUID) -> SalesTransaction | None:
        result = await db.execute(select(SalesTransaction).where(SalesTransaction.id == sale_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def create(db: AsyncSession, data: SalesTransactionCreate) -> SalesTransaction:
        sale = SalesTransaction(**data.model_dump())
        db.add(sale)
        await db.flush()
        await db.refresh(sale)
        return sale

    @staticmethod
    async def update(db: AsyncSession, sale_id: uuid.UUID, data: SalesTransactionUpdate) -> SalesTransaction | None:
        sale = await SalesTransactionService.get_by_id(db, sale_id)
        if not sale:
            return None
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(sale, field, value)
        await db.flush()
        await db.refresh(sale)
        return sale

    @staticmethod
    async def delete_by_id(db: AsyncSession, sale_id: uuid.UUID) -> bool:
        sale = await SalesTransactionService.get_by_id(db, sale_id)
        if not sale:
            return False
        await db.delete(sale)
        await db.flush()
        return True

    @staticmethod
    async def delete_all(db: AsyncSession) -> int:
        result = await db.execute(delete(SalesTransaction))
        await db.flush()
        return result.rowcount
