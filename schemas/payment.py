from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Literal


# Schema สำหรับรับข้อมูลตอน Create
class TransactionCreate(BaseModel):
    title: str = Field(..., min_length=1, description="ชื่อรายการ")
    amount: float = Field(..., gt=0, description="จำนวนเงิน (ต้องมากกว่า 0)")
    type: Literal["income", "expense"] = Field(..., description="ประเภท: income=รายรับ, expense=รายจ่าย")
    category: str | None = Field(default=None, description="หมวดหมู่")
    note: str | None = Field(default=None, description="หมายเหตุ")


# Schema สำหรับรับข้อมูลตอน Update
class TransactionUpdate(BaseModel):
    title: str | None = None
    amount: float | None = Field(default=None, gt=0)
    type: Literal["income", "expense"] | None = None
    category: str | None = None
    note: str | None = None


# Schema สำหรับส่งข้อมูลกลับ (Response)
class TransactionResponse(BaseModel):
    id: int
    title: str
    amount: float
    type: str
    category: str | None = None
    note: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = {"from_attributes": True}


# Schema สรุปยอด
class TransactionSummary(BaseModel):
    total_income: float
    total_expense: float
    balance: float
