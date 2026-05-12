import uuid

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.dependencies.db import DBSession
from app.schemas.response_envelope import APIResponse
from app.schemas.sale_line_item import SaleLineItemCreate, SaleLineItemResponse, SaleLineItemUpdate
from app.services.sale_line_item import SaleLineItemService

router = APIRouter()


@router.get("/", response_model=APIResponse[list[SaleLineItemResponse]])
async def get_all_sale_line_items(db: DBSession):
    try:
        items = await SaleLineItemService.get_all(db)
        return APIResponse(
            success=True,
            message="Sale line items retrieved successfully.",
            data=[SaleLineItemResponse.model_validate(i) for i in items],
        )
    except Exception:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Something went wrong while fetching sale line items.", "data": None},
        )


@router.get("/{line_item_id}", response_model=APIResponse[SaleLineItemResponse])
async def get_sale_line_item_by_id(line_item_id: uuid.UUID, db: DBSession):
    try:
        item = await SaleLineItemService.get_by_id(db, line_item_id)
        if not item:
            return JSONResponse(
                status_code=404,
                content={"success": False, "message": "Sale line item not found.", "data": None},
            )
        return APIResponse(
            success=True,
            message="Sale line item retrieved successfully.",
            data=SaleLineItemResponse.model_validate(item),
        )
    except Exception:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Something went wrong while fetching the sale line item.", "data": None},
        )


@router.post("/", response_model=APIResponse[SaleLineItemResponse], status_code=201)
async def create_sale_line_item(payload: SaleLineItemCreate, db: DBSession):
    try:
        item = await SaleLineItemService.create(db, payload)
        return APIResponse(
            success=True,
            message="Sale line item created successfully.",
            data=SaleLineItemResponse.model_validate(item),
        )
    except Exception:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Something went wrong while creating the sale line item.", "data": None},
        )


@router.patch("/{line_item_id}", response_model=APIResponse[SaleLineItemResponse])
async def update_sale_line_item(line_item_id: uuid.UUID, payload: SaleLineItemUpdate, db: DBSession):
    try:
        item = await SaleLineItemService.update(db, line_item_id, payload)
        if not item:
            return JSONResponse(
                status_code=404,
                content={"success": False, "message": "Sale line item not found.", "data": None},
            )
        return APIResponse(
            success=True,
            message="Sale line item updated successfully.",
            data=SaleLineItemResponse.model_validate(item),
        )
    except Exception:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Something went wrong while updating the sale line item.", "data": None},
        )


@router.delete("/", response_model=APIResponse[None])
async def delete_all_sale_line_items(db: DBSession):
    try:
        count = await SaleLineItemService.delete_all(db)
        return APIResponse(
            success=True,
            message=f"{count} sale line {'item' if count == 1 else 'items'} deleted successfully.",
            data=None,
        )
    except Exception:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Something went wrong while deleting sale line items.", "data": None},
        )


@router.delete("/{line_item_id}", response_model=APIResponse[None])
async def delete_sale_line_item_by_id(line_item_id: uuid.UUID, db: DBSession):
    try:
        deleted = await SaleLineItemService.delete_by_id(db, line_item_id)
        if not deleted:
            return JSONResponse(
                status_code=404,
                content={"success": False, "message": "Sale line item not found.", "data": None},
            )
        return APIResponse(success=True, message="Sale line item deleted successfully.", data=None)
    except Exception:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Something went wrong while deleting the sale line item.", "data": None},
        )
