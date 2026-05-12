import uuid

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.dependencies.db import DBSession
from app.schemas.response_envelope import APIResponse
from app.schemas.sales_transaction import SalesTransactionCreate, SalesTransactionResponse, SalesTransactionUpdate
from app.services.sales_transaction import SalesTransactionService

router = APIRouter()


@router.get("/", response_model=APIResponse[list[SalesTransactionResponse]])
async def get_all_sales(db: DBSession):
    try:
        sales = await SalesTransactionService.get_all(db)
        return APIResponse(
            success=True,
            message="Sales transactions retrieved successfully.",
            data=[SalesTransactionResponse.model_validate(s) for s in sales],
        )
    except Exception:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Something went wrong while fetching sales transactions.", "data": None},
        )


@router.get("/{sale_id}", response_model=APIResponse[SalesTransactionResponse])
async def get_sale_by_id(sale_id: uuid.UUID, db: DBSession):
    try:
        sale = await SalesTransactionService.get_by_id(db, sale_id)
        if not sale:
            return JSONResponse(
                status_code=404,
                content={"success": False, "message": "Sales transaction not found.", "data": None},
            )
        return APIResponse(
            success=True,
            message="Sales transaction retrieved successfully.",
            data=SalesTransactionResponse.model_validate(sale),
        )
    except Exception:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Something went wrong while fetching the sales transaction.", "data": None},
        )


@router.post("/", response_model=APIResponse[SalesTransactionResponse], status_code=201)
async def create_sale(payload: SalesTransactionCreate, db: DBSession):
    try:
        sale = await SalesTransactionService.create(db, payload)
        return APIResponse(
            success=True,
            message="Sales transaction created successfully.",
            data=SalesTransactionResponse.model_validate(sale),
        )
    except Exception:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Something went wrong while creating the sales transaction.", "data": None},
        )


@router.patch("/{sale_id}", response_model=APIResponse[SalesTransactionResponse])
async def update_sale(sale_id: uuid.UUID, payload: SalesTransactionUpdate, db: DBSession):
    try:
        sale = await SalesTransactionService.update(db, sale_id, payload)
        if not sale:
            return JSONResponse(
                status_code=404,
                content={"success": False, "message": "Sales transaction not found.", "data": None},
            )
        return APIResponse(
            success=True,
            message="Sales transaction updated successfully.",
            data=SalesTransactionResponse.model_validate(sale),
        )
    except Exception:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Something went wrong while updating the sales transaction.", "data": None},
        )


@router.delete("/", response_model=APIResponse[None])
async def delete_all_sales(db: DBSession):
    try:
        count = await SalesTransactionService.delete_all(db)
        return APIResponse(
            success=True,
            message=f"{count} sales {'transaction' if count == 1 else 'transactions'} deleted successfully.",
            data=None,
        )
    except Exception:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Something went wrong while deleting sales transactions.", "data": None},
        )


@router.delete("/{sale_id}", response_model=APIResponse[None])
async def delete_sale_by_id(sale_id: uuid.UUID, db: DBSession):
    try:
        deleted = await SalesTransactionService.delete_by_id(db, sale_id)
        if not deleted:
            return JSONResponse(
                status_code=404,
                content={"success": False, "message": "Sales transaction not found.", "data": None},
            )
        return APIResponse(success=True, message="Sales transaction deleted successfully.", data=None)
    except Exception:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Something went wrong while deleting the sales transaction.", "data": None},
        )
