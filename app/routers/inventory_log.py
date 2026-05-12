import uuid

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.dependencies.db import DBSession
from app.schemas.inventory_log import InventoryLogCreate, InventoryLogResponse
from app.schemas.response_envelope import APIResponse
from app.services.inventory_log import InventoryLogService

router = APIRouter()


@router.get("/", response_model=APIResponse[list[InventoryLogResponse]])
async def get_all_inventory_logs(db: DBSession):
    try:
        logs = await InventoryLogService.get_all(db)
        return APIResponse(
            success=True,
            message="Inventory logs retrieved successfully.",
            data=[InventoryLogResponse.model_validate(l) for l in logs],
        )
    except Exception:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Something went wrong while fetching inventory logs.", "data": None},
        )


@router.get("/{log_id}", response_model=APIResponse[InventoryLogResponse])
async def get_inventory_log_by_id(log_id: uuid.UUID, db: DBSession):
    try:
        log = await InventoryLogService.get_by_id(db, log_id)
        if not log:
            return JSONResponse(
                status_code=404,
                content={"success": False, "message": "Inventory log not found.", "data": None},
            )
        return APIResponse(
            success=True,
            message="Inventory log retrieved successfully.",
            data=InventoryLogResponse.model_validate(log),
        )
    except Exception:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Something went wrong while fetching the inventory log.", "data": None},
        )


@router.post("/", response_model=APIResponse[InventoryLogResponse], status_code=201)
async def create_inventory_log(payload: InventoryLogCreate, db: DBSession):
    try:
        log = await InventoryLogService.create(db, payload)
        return APIResponse(
            success=True,
            message="Inventory log created successfully.",
            data=InventoryLogResponse.model_validate(log),
        )
    except Exception:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Something went wrong while creating the inventory log.", "data": None},
        )
