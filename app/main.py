from fastapi import FastAPI

from app.routers import (
    company,
    inventory_log,
    item,
    purchase_order,
    purchase_order_line_item,
    sale_line_item,
    sales_transaction,
    store,
    vendor,
)

app = FastAPI(
    title="Inventory Management System",
    version="0.1.0",
)

app.include_router(company.router, prefix="/api/v1/companies", tags=["Companies"])
app.include_router(store.router, prefix="/api/v1/stores", tags=["Stores"])
app.include_router(vendor.router, prefix="/api/v1/vendors", tags=["Vendors"])
app.include_router(item.router, prefix="/api/v1/items", tags=["Items"])
app.include_router(purchase_order.router, prefix="/api/v1/purchase-orders", tags=["Purchase Orders"])
app.include_router(purchase_order_line_item.router, prefix="/api/v1/purchase-order-line-items", tags=["Purchase Order Line Items"])
app.include_router(sales_transaction.router, prefix="/api/v1/sales", tags=["Sales"])
app.include_router(sale_line_item.router, prefix="/api/v1/sale-line-items", tags=["Sale Line Items"])
app.include_router(inventory_log.router, prefix="/api/v1/inventory-logs", tags=["Inventory Logs"])


if __name__ == "__main__":
    import os
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)

