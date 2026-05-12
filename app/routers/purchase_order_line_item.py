import uuid

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.dependencies.db import DBSession
from app.schemas.purchase_order_line_item import (
    PurchaseOrderLineItemCreate,
    PurchaseOrderLineItemResponse,
    PurchaseOrderLineItemUpdate,
)
from app.schemas.response_envelope import APIResponse
from app.services.purchase_order_line_item import PurchaseOrderLineItemService

router = APIRouter()


@router.get("/", response_model=APIResponse[list[PurchaseOrderLineItemResponse]])
async def get_all_po_line_items(db: DBSession):
    try:
        items = await PurchaseOrderLineItemService.get_all(db)
        return APIResponse(
            success=True,
            message="Purchase order line items retrieved successfully.",
            data=[PurchaseOrderLineItemResponse.model_validate(i) for i in items],
        )
    except Exception:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Something went wrong while fetching purchase order line items.", "data": None},
        )


@router.get("/{line_item_id}", response_model=APIResponse[PurchaseOrderLineItemResponse])
async def get_po_line_item_by_id(line_item_id: uuid.UUID, db: DBSession):
    try:
        item = await PurchaseOrderLineItemService.get_by_id(db, line_item_id)
        if not item:
            return JSONResponse(
                status_code=404,
                content={"success": False, "message": "Purchase order line item not found.", "data": None},
            )
        return APIResponse(
            success=True,
            message="Purchase order line item retrieved successfully.",
            data=PurchaseOrderLineItemResponse.model_validate(item),
        )
    except Exception:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Something went wrong while fetching the purchase order line item.", "data": None},
        )


@router.post("/", response_model=APIResponse[PurchaseOrderLineItemResponse], status_code=201)
async def create_po_line_item(payload: PurchaseOrderLineItemCreate, db: DBSession):
    try:
        item = await PurchaseOrderLineItemService.create(db, payload)
        return APIResponse(
            success=True,
            message="Purchase order line item created successfully.",
            data=PurchaseOrderLineItemResponse.model_validate(item),
        )
    except Exception:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Something went wrong while creating the purchase order line item.", "data": None},
        )


@router.patch("/{line_item_id}", response_model=APIResponse[PurchaseOrderLineItemResponse])
async def update_po_line_item(line_item_id: uuid.UUID, payload: PurchaseOrderLineItemUpdate, db: DBSession):
    try:
        item = await PurchaseOrderLineItemService.update(db, line_item_id, payload)
        if not item:
            return JSONResponse(
                status_code=404,
                content={"success": False, "message": "Purchase order line item not found.", "data": None},
            )
        return APIResponse(
            success=True,
            message="Purchase order line item updated successfully.",
            data=PurchaseOrderLineItemResponse.model_validate(item),
        )
    except Exception:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Something went wrong while updating the purchase order line item.", "data": None},
        )


@router.delete("/", response_model=APIResponse[None])
async def delete_all_po_line_items(db: DBSession):
    try:
        count = await PurchaseOrderLineItemService.delete_all(db)
        return APIResponse(
            success=True,
            message=f"{count} purchase order line {'item' if count == 1 else 'items'} deleted successfully.",
            data=None,
        )
    except Exception:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Something went wrong while deleting purchase order line items.", "data": None},
        )


@router.delete("/{line_item_id}", response_model=APIResponse[None])
async def delete_po_line_item_by_id(line_item_id: uuid.UUID, db: DBSession):
    try:
        deleted = await PurchaseOrderLineItemService.delete_by_id(db, line_item_id)
        if not deleted:
            return JSONResponse(
                status_code=404,
                content={"success": False, "message": "Purchase order line item not found.", "data": None},
            )
        return APIResponse(success=True, message="Purchase order line item deleted successfully.", data=None)
    except Exception:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Something went wrong while deleting the purchase order line item.", "data": None},
        )
