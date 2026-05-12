import uuid

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.company import Company
from app.schemas.company import CompanyCreate, CompanyUpdate


class CompanyService:

    @staticmethod
    async def get_all(db: AsyncSession) -> list[Company]:
        result = await db.execute(select(Company).order_by(Company.created_at.desc()))
        return list(result.scalars().all())

    @staticmethod
    async def get_by_id(db: AsyncSession, company_id: uuid.UUID) -> Company | None:
        result = await db.execute(select(Company).where(Company.id == company_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def create(db: AsyncSession, data: CompanyCreate) -> Company:
        company = Company(**data.model_dump())
        db.add(company)
        await db.flush()
        await db.refresh(company)
        return company

    @staticmethod
    async def update(db: AsyncSession, company_id: uuid.UUID, data: CompanyUpdate) -> Company | None:
        company = await CompanyService.get_by_id(db, company_id)
        if not company:
            return None
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(company, field, value)
        await db.flush()
        await db.refresh(company)
        return company

    @staticmethod
    async def delete_by_id(db: AsyncSession, company_id: uuid.UUID) -> bool:
        company = await CompanyService.get_by_id(db, company_id)
        if not company:
            return False
        await db.delete(company)
        await db.flush()
        return True

    @staticmethod
    async def delete_all(db: AsyncSession) -> int:
        result = await db.execute(delete(Company))
        await db.flush()
        return result.rowcount
