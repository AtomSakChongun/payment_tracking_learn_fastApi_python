# Budget API — ทุก Endpoint

Base URL: `http://localhost:8000`

---

## 1. ดึงงบประมาณของเดือน

```
GET /budgets/{month}
```

**Path Parameter**

| Parameter | Type | ตัวอย่าง |
|-----------|------|---------|
| month | string (YYYY-MM) | `2026-06` |

**ตัวอย่าง Request**

```bash
curl http://localhost:8000/budgets/2026-06
```

**Response — พบข้อมูล (200)**

```json
{
  "id": 1,
  "month": "2026-06",
  "amount": 5000.0
}
```

**Response — ยังไม่เคยตั้งค่า (200)**

```json
{
  "id": 0,
  "month": "2026-06",
  "amount": 0.0
}
```

> ไม่ return 404 ถ้าไม่พบ — คืน amount 0.0 แทน

---

## 2. ตั้งค่า / อัปเดตงบประมาณ (Upsert)

```
POST /budgets/
```

**Request Body**

```json
{
  "month": "2026-06",
  "amount": 5000.0
}
```

| Field | Type | เงื่อนไข |
|-------|------|---------|
| month | string | รูปแบบ `YYYY-MM` เท่านั้น |
| amount | float | ต้องมากกว่าหรือเท่ากับ 0 |

**ตัวอย่าง Request**

```bash
curl -X POST http://localhost:8000/budgets/ \
  -H "Content-Type: application/json" \
  -d '{"month": "2026-06", "amount": 5000}'
```

**Response (200)**

```json
{
  "id": 1,
  "month": "2026-06",
  "amount": 5000.0
}
```

> ถ้าเดือนนั้นมีอยู่แล้ว จะ **อัปเดต** amount  
> ถ้ายังไม่มี จะ **สร้างใหม่**

---

## 3. ลบงบประมาณของเดือน

```
DELETE /budgets/{month}
```

**Path Parameter**

| Parameter | Type | ตัวอย่าง |
|-----------|------|---------|
| month | string (YYYY-MM) | `2026-06` |

**ตัวอย่าง Request**

```bash
curl -X DELETE http://localhost:8000/budgets/2026-06
```

**Response — สำเร็จ (200)**

```json
{
  "message": "ลบงบประมาณเดือน 2026-06 สำเร็จ"
}
```

**Response — ไม่พบเดือนนั้น (404)**

```json
{
  "detail": "ไม่พบงบประมาณประจำเดือนนี้"
}
```

---

## สรุปทุก Endpoint

| Method | Path | คำอธิบาย | Status Code |
|--------|------|---------|-------------|
| GET | `/budgets/{month}` | ดึงงบประมาณของเดือน | 200 เสมอ |
| POST | `/budgets/` | ตั้งค่า / อัปเดตงบประมาณ | 200 |
| DELETE | `/budgets/{month}` | ลบงบประมาณของเดือน | 200 / 404 |

---

## Validation Rules

- `month` ต้องอยู่ในรูปแบบ `YYYY-MM` เท่านั้น เช่น `2026-06`  
  ถ้าส่งผิด format จะได้ `422 Unprocessable Entity`
- `amount` ต้องเป็น `>= 0` (ติดลบไม่ได้)

**ตัวอย่าง 422 เมื่อ month ผิด format**

```json
{
  "detail": [
    {
      "type": "string_pattern_mismatch",
      "loc": ["body", "month"],
      "msg": "String should match pattern '^\\d{4}-\\d{2}$'"
    }
  ]
}
```
