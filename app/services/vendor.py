import uuid

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.vendor import Vendor
from app.schemas.vendor import VendorCreate, VendorUpdate


class VendorService:

    @staticmethod
    async def get_all(db: AsyncSession) -> list[Vendor]:
        result = await db.execute(select(Vendor).order_by(Vendor.created_at.desc()))
        return list(result.scalars().all())

    @staticmethod
    async def get_by_id(db: AsyncSession, vendor_id: uuid.UUID) -> Vendor | None:
        result = await db.execute(select(Vendor).where(Vendor.id == vendor_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def create(db: AsyncSession, data: VendorCreate) -> Vendor:
        vendor = Vendor(**data.model_dump())
        db.add(vendor)
        await db.flush()
        await db.refresh(vendor)
        return vendor

    @staticmethod
    async def update(db: AsyncSession, vendor_id: uuid.UUID, data: VendorUpdate) -> Vendor | None:
        vendor = await VendorService.get_by_id(db, vendor_id)
        if not vendor:
            return None
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(vendor, field, value)
        await db.flush()
        await db.refresh(vendor)
        return vendor

    @staticmethod
    async def delete_by_id(db: AsyncSession, vendor_id: uuid.UUID) -> bool:
        vendor = await VendorService.get_by_id(db, vendor_id)
        if not vendor:
            return False
        await db.delete(vendor)
        await db.flush()
        return True

    @staticmethod
    async def delete_all(db: AsyncSession) -> int:
        result = await db.execute(delete(Vendor))
        await db.flush()
        return result.rowcount
