import uuid

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.dependencies.db import DBSession
from app.schemas.response_envelope import APIResponse
from app.schemas.vendor import VendorCreate, VendorResponse, VendorUpdate
from app.services.vendor import VendorService

router = APIRouter()


@router.get("/", response_model=APIResponse[list[VendorResponse]])
async def get_all_vendors(db: DBSession):
    try:
        vendors = await VendorService.get_all(db)
        return APIResponse(
            success=True,
            message="Vendors retrieved successfully.",
            data=[VendorResponse.model_validate(v) for v in vendors],
        )
    except Exception:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Something went wrong while fetching vendors.", "data": None},
        )


@router.get("/{vendor_id}", response_model=APIResponse[VendorResponse])
async def get_vendor_by_id(vendor_id: uuid.UUID, db: DBSession):
    try:
        vendor = await VendorService.get_by_id(db, vendor_id)
        if not vendor:
            return JSONResponse(
                status_code=404,
                content={"success": False, "message": "Vendor not found.", "data": None},
            )
        return APIResponse(
            success=True,
            message="Vendor retrieved successfully.",
            data=VendorResponse.model_validate(vendor),
        )
    except Exception:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Something went wrong while fetching the vendor.", "data": None},
        )


@router.post("/", response_model=APIResponse[VendorResponse], status_code=201)
async def create_vendor(payload: VendorCreate, db: DBSession):
    try:
        vendor = await VendorService.create(db, payload)
        return APIResponse(
            success=True,
            message="Vendor created successfully.",
            data=VendorResponse.model_validate(vendor),
        )
    except Exception:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Something went wrong while creating the vendor.", "data": None},
        )


@router.patch("/{vendor_id}", response_model=APIResponse[VendorResponse])
async def update_vendor(vendor_id: uuid.UUID, payload: VendorUpdate, db: DBSession):
    try:
        vendor = await VendorService.update(db, vendor_id, payload)
        if not vendor:
            return JSONResponse(
                status_code=404,
                content={"success": False, "message": "Vendor not found.", "data": None},
            )
        return APIResponse(
            success=True,
            message="Vendor updated successfully.",
            data=VendorResponse.model_validate(vendor),
        )
    except Exception:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Something went wrong while updating the vendor.", "data": None},
        )


@router.delete("/", response_model=APIResponse[None])
async def delete_all_vendors(db: DBSession):
    try:
        count = await VendorService.delete_all(db)
        return APIResponse(
            success=True,
            message=f"{count} {'vendor' if count == 1 else 'vendors'} deleted successfully.",
            data=None,
        )
    except Exception:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Something went wrong while deleting vendors.", "data": None},
        )


@router.delete("/{vendor_id}", response_model=APIResponse[None])
async def delete_vendor_by_id(vendor_id: uuid.UUID, db: DBSession):
    try:
        deleted = await VendorService.delete_by_id(db, vendor_id)
        if not deleted:
            return JSONResponse(
                status_code=404,
                content={"success": False, "message": "Vendor not found.", "data": None},
            )
        return APIResponse(success=True, message="Vendor deleted successfully.", data=None)
    except Exception:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Something went wrong while deleting the vendor.", "data": None},
        )
