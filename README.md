# Payment Tracking API 🐍

โปรเจตนี้สร้างขึ้นเพื่อ **ศึกษา Python** ผ่านการสร้าง REST API จริง  
โดยใช้ FastAPI เป็น framework หลัก พร้อม SQLAlchemy และ SQLite เป็น database

---

## สิ่งที่ได้เรียนรู้

### Python พื้นฐาน
- **Type Hints** — การกำหนด type ให้ตัวแปรและ function เช่น `str | None`, `list[str]`
- **Decorator** — การใช้ `@app.get()`, `@router.post()` เพื่อกำหนด route
- **Dependency Injection** — ส่ง DB session เข้า function ผ่าน `Depends()`
- **f-string** — การ format string แบบ `f"ลบข้อมูล {count} รายการ"`
- **List / Dict** — การจัดการ collection ใน Python
- **OOP** — การสร้าง class, inheritance เช่น `class Transaction(Base)`

### Libraries ที่ใช้

| Library | เรียนรู้อะไร |
|---------|------------|
| **FastAPI** | สร้าง REST API, routing, middleware, CORS |
| **SQLAlchemy** | ORM, สร้าง model, query database ผ่าน Python |
| **Pydantic v2** | Validate ข้อมูล, schema สำหรับ request/response |
| **SQLite** | Database เบื้องต้น, ไม่ต้องติดตั้ง server แยก |
| **Uvicorn** | ASGI server สำหรับรัน FastAPI |

---

## Concepts ที่ฝึกในโปรเจตนี้

### 1. Layered Architecture
แบ่งโค้ดออกเป็น layer ชัดเจน ไม่ปนกัน

```
Router → Controller → Model
```

- **Router** — รับ HTTP request เท่านั้น
- **Controller** — logic ทั้งหมดอยู่ที่นี่
- **Model** — กำหนด structure ของ database

### 2. Pydantic Schemas
แยก schema สำหรับ Create / Update / Response ออกจากกัน

```python
class TransactionCreate(BaseModel):
    title: str = Field(..., min_length=1)
    amount: float = Field(..., gt=0)
    type: Literal["income", "expense"]
```

### 3. SQLAlchemy ORM
เขียน Python แทนการเขียน SQL ตรงๆ

```python
db.query(Transaction).filter(Transaction.type == "income").all()
```

### 4. Dependency Injection ใน FastAPI

```python
def get_all(db: Session = Depends(get_db)):
    ...
```

### 5. Query Filtering
รับ query params และ filter ข้อมูลแบบ dynamic

```python
@router.get("/")
def get_all(type: str | None = Query(default=None), ...):
```

---

## วิธีรันโปรเจต

### 1. สร้าง virtual environment

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
```

### 2. ติดตั้ง dependencies

```bash
pip install fastapi sqlalchemy uvicorn
```

### 3. รัน server

```bash
uvicorn main:app --reload
```

### 4. เปิด API Docs

```
http://localhost:8000/docs
```

---

## โครงสร้างโปรเจต

```
├── main.py            # Entry point
├── database.py        # DB connection
├── models/            # SQLAlchemy models
├── schemas/           # Pydantic schemas
├── controllers/       # Business logic
├── routers/           # HTTP routes
└── payments.db        # SQLite database
```

---

## API หลักๆ

```
GET    /transactions/          ดึงรายการทั้งหมด
POST   /transactions/          เพิ่มรายการ
PUT    /transactions/{id}      แก้ไขรายการ
DELETE /transactions/{id}      ลบรายการ
GET    /transactions/summary   สรุปยอดรายรับ-รายจ่าย

GET    /budgets/{month}        ดึงงบประมาณ
POST   /budgets/               ตั้งงบประมาณ
```
