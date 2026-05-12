import uuid

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.dependencies.db import DBSession
from app.schemas.item import ItemCreate, ItemResponse, ItemUpdate
from app.schemas.response_envelope import APIResponse
from app.services.item import ItemService

router = APIRouter()


@router.get("/", response_model=APIResponse[list[ItemResponse]])
async def get_all_items(db: DBSession):
    try:
        items = await ItemService.get_all(db)
        return APIResponse(
            success=True,
            message="Items retrieved successfully.",
            data=[ItemResponse.model_validate(i) for i in items],
        )
    except Exception:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Something went wrong while fetching items.", "data": None},
        )


@router.get("/{item_id}", response_model=APIResponse[ItemResponse])
async def get_item_by_id(item_id: uuid.UUID, db: DBSession):
    try:
        item = await ItemService.get_by_id(db, item_id)
        if not item:
            return JSONResponse(
                status_code=404,
                content={"success": False, "message": "Item not found.", "data": None},
            )
        return APIResponse(
            success=True,
            message="Item retrieved successfully.",
            data=ItemResponse.model_validate(item),
        )
    except Exception:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Something went wrong while fetching the item.", "data": None},
        )


@router.post("/", response_model=APIResponse[ItemResponse], status_code=201)
async def create_item(payload: ItemCreate, db: DBSession):
    try:
        item = await ItemService.create(db, payload)
        return APIResponse(
            success=True,
            message="Item created successfully.",
            data=ItemResponse.model_validate(item),
        )
    except Exception:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Something went wrong while creating the item.", "data": None},
        )


@router.patch("/{item_id}", response_model=APIResponse[ItemResponse])
async def update_item(item_id: uuid.UUID, payload: ItemUpdate, db: DBSession):
    try:
        item = await ItemService.update(db, item_id, payload)
        if not item:
            return JSONResponse(
                status_code=404,
                content={"success": False, "message": "Item not found.", "data": None},
            )
        return APIResponse(
            success=True,
            message="Item updated successfully.",
            data=ItemResponse.model_validate(item),
        )
    except Exception:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Something went wrong while updating the item.", "data": None},
        )


@router.delete("/", response_model=APIResponse[None])
async def delete_all_items(db: DBSession):
    try:
        count = await ItemService.delete_all(db)
        return APIResponse(
            success=True,
            message=f"{count} {'item' if count == 1 else 'items'} deleted successfully.",
            data=None,
        )
    except Exception:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Something went wrong while deleting items.", "data": None},
        )


@router.delete("/{item_id}", response_model=APIResponse[None])
async def delete_item_by_id(item_id: uuid.UUID, db: DBSession):
    try:
        deleted = await ItemService.delete_by_id(db, item_id)
        if not deleted:
            return JSONResponse(
                status_code=404,
                content={"success": False, "message": "Item not found.", "data": None},
            )
        return APIResponse(success=True, message="Item deleted successfully.", data=None)
    except Exception:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Something went wrong while deleting the item.", "data": None},
        )
