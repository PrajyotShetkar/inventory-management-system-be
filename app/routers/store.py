import uuid

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.dependencies.db import DBSession
from app.schemas.response_envelope import APIResponse
from app.schemas.store import StoreCreate, StoreResponse, StoreUpdate
from app.services.store import StoreService

router = APIRouter()


@router.get("/", response_model=APIResponse[list[StoreResponse]])
async def get_all_stores(db: DBSession):
    try:
        stores = await StoreService.get_all(db)
        return APIResponse(
            success=True,
            message="Stores retrieved successfully.",
            data=[StoreResponse.model_validate(s) for s in stores],
        )
    except Exception:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Something went wrong while fetching stores.", "data": None},
        )


@router.get("/{store_id}", response_model=APIResponse[StoreResponse])
async def get_store_by_id(store_id: uuid.UUID, db: DBSession):
    try:
        store = await StoreService.get_by_id(db, store_id)
        if not store:
            return JSONResponse(
                status_code=404,
                content={"success": False, "message": "Store not found.", "data": None},
            )
        return APIResponse(
            success=True,
            message="Store retrieved successfully.",
            data=StoreResponse.model_validate(store),
        )
    except Exception:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Something went wrong while fetching the store.", "data": None},
        )


@router.post("/", response_model=APIResponse[StoreResponse], status_code=201)
async def create_store(payload: StoreCreate, db: DBSession):
    try:
        store = await StoreService.create(db, payload)
        return APIResponse(
            success=True,
            message="Store created successfully.",
            data=StoreResponse.model_validate(store),
        )
    except Exception:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Something went wrong while creating the store.", "data": None},
        )


@router.patch("/{store_id}", response_model=APIResponse[StoreResponse])
async def update_store(store_id: uuid.UUID, payload: StoreUpdate, db: DBSession):
    try:
        store = await StoreService.update(db, store_id, payload)
        if not store:
            return JSONResponse(
                status_code=404,
                content={"success": False, "message": "Store not found.", "data": None},
            )
        return APIResponse(
            success=True,
            message="Store updated successfully.",
            data=StoreResponse.model_validate(store),
        )
    except Exception:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Something went wrong while updating the store.", "data": None},
        )


@router.delete("/", response_model=APIResponse[None])
async def delete_all_stores(db: DBSession):
    try:
        count = await StoreService.delete_all(db)
        return APIResponse(
            success=True,
            message=f"{count} {'store' if count == 1 else 'stores'} deleted successfully.",
            data=None,
        )
    except Exception:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Something went wrong while deleting stores.", "data": None},
        )


@router.delete("/{store_id}", response_model=APIResponse[None])
async def delete_store_by_id(store_id: uuid.UUID, db: DBSession):
    try:
        deleted = await StoreService.delete_by_id(db, store_id)
        if not deleted:
            return JSONResponse(
                status_code=404,
                content={"success": False, "message": "Store not found.", "data": None},
            )
        return APIResponse(success=True, message="Store deleted successfully.", data=None)
    except Exception:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Something went wrong while deleting the store.", "data": None},
        )
