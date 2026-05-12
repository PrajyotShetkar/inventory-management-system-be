# Inventory Management System

FastAPI backend for inventory management. PostgreSQL is used as the database; Alembic manages migrations.

---

## Setup

### 1. Create and activate a virtual environment

```bash
python -m venv venv
```

**Windows**
```bash
venv\Scripts\activate
```

**macOS / Linux**
```bash
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Copy the example file and fill in your database credentials:

```bash
copy .env.example .env
```

Open `.env` and update the connection string:

```
DATABASE_URL=postgresql+asyncpg://your_user:your_password@localhost:5432/your_db
```

### 4. Run Alembic migrations

Generate the initial migration (only needed once, or after model changes):

```bash
alembic revision --autogenerate -m "initial"
```

Apply migrations to the database:

```bash
alembic upgrade head
```

### 5. Start the server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.
Interactive docs (Swagger UI) at `http://127.0.0.1:8000/docs`.

---

## API Endpoints

| Resource                    | Base URL                                  |
|-----------------------------|-------------------------------------------|
| Companies                   | `/api/v1/companies`                       |
| Stores                      | `/api/v1/stores`                          |
| Vendors                     | `/api/v1/vendors`                         |
| Items                       | `/api/v1/items`                           |
| Purchase Orders             | `/api/v1/purchase-orders`                 |
| Purchase Order Line Items   | `/api/v1/purchase-order-line-items`       |
| Sales Transactions          | `/api/v1/sales`                           |
| Sale Line Items             | `/api/v1/sale-line-items`                 |
| Inventory Logs              | `/api/v1/inventory-logs`                  |

All endpoints return a consistent response envelope:

```json
{
  "success": true,
  "message": "...",
  "data": {}
}
```
