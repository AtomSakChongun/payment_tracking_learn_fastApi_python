from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)           # ชื่อรายการ เช่น "ค่าอาหาร", "เงินเดือน"
    amount = Column(Float, nullable=False)           # จำนวนเงิน
    type = Column(String, nullable=False)            # "income" = รายรับ, "expense" = รายจ่าย
    category = Column(String, nullable=True)         # หมวดหมู่ เช่น "อาหาร", "เดินทาง", "เงินเดือน"
    note = Column(String, nullable=True)             # หมายเหตุ
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)
    month = Column(String, unique=True, index=True, nullable=False)  # รูปแบบ "YYYY-MM"
    amount = Column(Float, nullable=False)                           # งบประมาณที่ตั้งไว้

