# สถาปัตยกรรมโปรเจต: Payment Tracking API

## ภาพรวม

API สำหรับติดตามรายรับ-รายจ่าย สร้างด้วย **FastAPI** + **SQLAlchemy** + **SQLite**  
ใช้โครงสร้างแบบ Layered Architecture (Router → Controller → Model)

---

## Tech Stack

| ส่วน | เทคโนโลยี |
|------|-----------|
| Web Framework | FastAPI |
| ORM | SQLAlchemy |
| Database | SQLite (`payments.db`) |
| Data Validation | Pydantic v2 |
| CORS | FastAPI CORSMiddleware |

---

## โครงสร้างไฟล์

```
payment_tracking_learn_fastApi_python/
│
├── main.py               # Entry point — สร้าง app, register routers, CORS
├── database.py           # Database connection, session, Base class
│
├── models/
│   └── payment.py        # SQLAlchemy ORM models (table definitions)
│
├── schemas/
│   └── payment.py        # Pydantic schemas (request/response validation)
│
├── controllers/
│   └── payment.py        # Business logic — query, create, update, delete
│
├── routers/
│   ├── payment.py        # HTTP routes สำหรับ /transactions
│   └── budget.py         # HTTP routes สำหรับ /budgets
│
└── payments.db           # SQLite database file
```

---

## Layers

```
Request
   │
   ▼
[Router]         routers/payment.py, routers/budget.py
   │              — รับ HTTP request, validate input ผ่าน Pydantic
   │              — inject DB session ผ่าน Depends(get_db)
   ▼
[Controller]     controllers/payment.py
   │              — Business logic ทั้งหมดอยู่ที่นี่
   │              — query filtering, aggregation, CRUD operations
   ▼
[Model/DB]       models/payment.py + database.py
                  — SQLAlchemy ORM models
                  — SQLite ผ่าน engine และ SessionLocal
```

---

## Database Models

### `transactions` table

| Column | Type | หมายเหตุ |
|--------|------|---------|
| id | Integer (PK) | auto increment |
| title | String | ชื่อรายการ (required) |
| amount | Float | จำนวนเงิน (required) |
| type | String | `"income"` หรือ `"expense"` |
| category | String | หมวดหมู่ (optional) |
| note | String | หมายเหตุ (optional) |
| created_at | DateTime | auto-set เมื่อสร้าง |
| updated_at | DateTime | auto-update เมื่อแก้ไข |

### `budgets` table

| Column | Type | หมายเหตุ |
|--------|------|---------|
| id | Integer (PK) | auto increment |
| month | String (unique) | รูปแบบ `YYYY-MM` |
| amount | Float | งบประมาณที่ตั้งไว้ |

---

## API Endpoints

### Transactions — `/transactions`

| Method | Path | คำอธิบาย |
|--------|------|---------|
| GET | `/transactions/` | ดึงรายการทั้งหมด (filter ได้ด้วย `type`, `search`, `start_date`, `end_date`) |
| GET | `/transactions/summary` | สรุปยอด: รายรับ, รายจ่าย, คงเหลือ |
| GET | `/transactions/{id}` | ดึงรายการตาม ID |
| POST | `/transactions/` | เพิ่มรายการใหม่ |
| PUT | `/transactions/{id}` | แก้ไขรายการ |
| DELETE | `/transactions/{id}` | ลบรายการตาม ID |
| DELETE | `/transactions/` | ลบรายการทั้งหมด (reset) |

### Budgets — `/budgets`

| Method | Path | คำอธิบาย |
|--------|------|---------|
| GET | `/budgets/{month}` | ดึงงบประมาณของเดือน (คืน `amount: 0.0` ถ้ายังไม่ตั้ง) |
| POST | `/budgets/` | ตั้งค่าหรืออัปเดตงบประมาณ (upsert) |
| DELETE | `/budgets/{month}` | ลบงบประมาณของเดือน |

---

## Pydantic Schemas

| Schema | ใช้สำหรับ |
|--------|---------|
| `TransactionCreate` | รับข้อมูลตอนสร้าง transaction ใหม่ |
| `TransactionUpdate` | รับข้อมูลตอนแก้ไข (ทุก field เป็น optional) |
| `TransactionResponse` | ส่งข้อมูลกลับ (include `id`, `created_at`, `updated_at`) |
| `TransactionSummary` | ส่งสรุปยอด (`total_income`, `total_expense`, `balance`) |
| `BudgetCreate` | รับข้อมูลตอนตั้งงบประมาณ (validate `YYYY-MM` format) |
| `BudgetResponse` | ส่งข้อมูล budget กลับ |

---

## CORS Configuration

รองรับ origin ต่อไปนี้สำหรับ local development:

- `http://localhost:3000` — React / Next.js
- `http://localhost:5173`, `http://localhost:5174` — Vite (Vue / React)

รองรับ method และ header ทั้งหมด (`*`)

---

## Data Flow ตัวอย่าง: สร้าง Transaction ใหม่

```
POST /transactions/
   Body: { title, amount, type, category, note }
         │
         ▼
   [Router] routers/payment.py
         — Pydantic validate ด้วย TransactionCreate
         │
         ▼
   [Controller] controllers/payment.py → create_transaction()
         — สร้าง Transaction ORM object
         — db.add() → db.commit() → db.refresh()
         │
         ▼
   [DB] SQLite transactions table
         │
         ▼
   Response: TransactionResponse (201 Created)
```
