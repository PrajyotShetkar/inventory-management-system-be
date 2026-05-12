import uuid

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.dependencies.db import DBSession
from app.schemas.company import CompanyCreate, CompanyResponse, CompanyUpdate
from app.schemas.response_envelope import APIResponse
from app.services.company import CompanyService

router = APIRouter()


@router.get("/", response_model=APIResponse[list[CompanyResponse]])
async def get_all_companies(db: DBSession):
    try:
        companies = await CompanyService.get_all(db)
        return APIResponse(
            success=True,
            message="Companies retrieved successfully.",
            data=[CompanyResponse.model_validate(c) for c in companies],
        )
    except Exception:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Something went wrong while fetching companies.", "data": None},
        )


@router.get("/{company_id}", response_model=APIResponse[CompanyResponse])
async def get_company_by_id(company_id: uuid.UUID, db: DBSession):
    try:
        company = await CompanyService.get_by_id(db, company_id)
        if not company:
            return JSONResponse(
                status_code=404,
                content={"success": False, "message": "Company not found.", "data": None},
            )
        return APIResponse(
            success=True,
            message="Company retrieved successfully.",
            data=CompanyResponse.model_validate(company),
        )
    except Exception:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Something went wrong while fetching the company.", "data": None},
        )


@router.post("/", response_model=APIResponse[CompanyResponse], status_code=201)
async def create_company(payload: CompanyCreate, db: DBSession):
    try:
        company = await CompanyService.create(db, payload)
        return APIResponse(
            success=True,
            message="Company created successfully.",
            data=CompanyResponse.model_validate(company),
        )
    except Exception:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Something went wrong while creating the company.", "data": None},
        )


@router.patch("/{company_id}", response_model=APIResponse[CompanyResponse])
async def update_company(company_id: uuid.UUID, payload: CompanyUpdate, db: DBSession):
    try:
        company = await CompanyService.update(db, company_id, payload)
        if not company:
            return JSONResponse(
                status_code=404,
                content={"success": False, "message": "Company not found.", "data": None},
            )
        return APIResponse(
            success=True,
            message="Company updated successfully.",
            data=CompanyResponse.model_validate(company),
        )
    except Exception:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Something went wrong while updating the company.", "data": None},
        )


@router.delete("/{company_id}", response_model=APIResponse[None])
async def delete_company_by_id(company_id: uuid.UUID, db: DBSession):
    try:
        deleted = await CompanyService.delete_by_id(db, company_id)
        if not deleted:
            return JSONResponse(
                status_code=404,
                content={"success": False, "message": "Company not found.", "data": None},
            )
        return APIResponse(success=True, message="Company deleted successfully.", data=None)
    except Exception:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Something went wrong while deleting the company.", "data": None},
        )


@router.delete("/", response_model=APIResponse[None])
async def delete_all_companies(db: DBSession):
    try:
        count = await CompanyService.delete_all(db)
        return APIResponse(
            success=True,
            message=f"{count} {'company' if count == 1 else 'companies'} deleted successfully.",
            data=None,
        )
    except Exception:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Something went wrong while deleting companies.", "data": None},
        )
