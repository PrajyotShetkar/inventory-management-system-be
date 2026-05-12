import uuid

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.dependencies.db import DBSession
from app.schemas.purchase_order import PurchaseOrderCreate, PurchaseOrderResponse, PurchaseOrderUpdate
from app.schemas.response_envelope import APIResponse
from app.services.purchase_order import PurchaseOrderService

router = APIRouter()


@router.get("/", response_model=APIResponse[list[PurchaseOrderResponse]])
async def get_all_purchase_orders(db: DBSession):
    try:
        orders = await PurchaseOrderService.get_all(db)
        return APIResponse(
            success=True,
            message="Purchase orders retrieved successfully.",
            data=[PurchaseOrderResponse.model_validate(o) for o in orders],
        )
    except Exception:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Something went wrong while fetching purchase orders.", "data": None},
        )


@router.get("/{po_id}", response_model=APIResponse[PurchaseOrderResponse])
async def get_purchase_order_by_id(po_id: uuid.UUID, db: DBSession):
    try:
        order = await PurchaseOrderService.get_by_id(db, po_id)
        if not order:
            return JSONResponse(
                status_code=404,
                content={"success": False, "message": "Purchase order not found.", "data": None},
            )
        return APIResponse(
            success=True,
            message="Purchase order retrieved successfully.",
            data=PurchaseOrderResponse.model_validate(order),
        )
    except Exception:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Something went wrong while fetching the purchase order.", "data": None},
        )


@router.post("/", response_model=APIResponse[PurchaseOrderResponse], status_code=201)
async def create_purchase_order(payload: PurchaseOrderCreate, db: DBSession):
    try:
        order = await PurchaseOrderService.create(db, payload)
        return APIResponse(
            success=True,
            message="Purchase order created successfully.",
            data=PurchaseOrderResponse.model_validate(order),
        )
    except Exception:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Something went wrong while creating the purchase order.", "data": None},
        )


@router.patch("/{po_id}", response_model=APIResponse[PurchaseOrderResponse])
async def update_purchase_order(po_id: uuid.UUID, payload: PurchaseOrderUpdate, db: DBSession):
    try:
        order = await PurchaseOrderService.update(db, po_id, payload)
        if not order:
            return JSONResponse(
                status_code=404,
                content={"success": False, "message": "Purchase order not found.", "data": None},
            )
        return APIResponse(
            success=True,
            message="Purchase order updated successfully.",
            data=PurchaseOrderResponse.model_validate(order),
        )
    except Exception:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Something went wrong while updating the purchase order.", "data": None},
        )


@router.delete("/", response_model=APIResponse[None])
async def delete_all_purchase_orders(db: DBSession):
    try:
        count = await PurchaseOrderService.delete_all(db)
        return APIResponse(
            success=True,
            message=f"{count} purchase {'order' if count == 1 else 'orders'} deleted successfully.",
            data=None,
        )
    except Exception:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Something went wrong while deleting purchase orders.", "data": None},
        )


@router.delete("/{po_id}", response_model=APIResponse[None])
async def delete_purchase_order_by_id(po_id: uuid.UUID, db: DBSession):
    try:
        deleted = await PurchaseOrderService.delete_by_id(db, po_id)
        if not deleted:
            return JSONResponse(
                status_code=404,
                content={"success": False, "message": "Purchase order not found.", "data": None},
            )
        return APIResponse(success=True, message="Purchase order deleted successfully.", data=None)
    except Exception:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Something went wrong while deleting the purchase order.", "data": None},
        )
