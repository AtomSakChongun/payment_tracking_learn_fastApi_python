from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas.payment import BudgetCreate, BudgetResponse
import controllers.payment as transaction_controller

router = APIRouter(prefix="/budgets", tags=["Budgets"])


@router.get("/{month}", response_model=BudgetResponse)
def get_budget(month: str, db: Session = Depends(get_db)):
    """ดึงงบประมาณประจำเดือน (ส่งกลับ amount=0.0 หากยังไม่ได้ตั้งค่า)"""
    budget = transaction_controller.get_budget_by_month(db, month)
    if not budget:
        return {"id": 0, "month": month, "amount": 0.0}
    return budget


@router.post("/", response_model=BudgetResponse)
def create_or_update_budget(budget: BudgetCreate, db: Session = Depends(get_db)):
    """ตั้งค่าหรือแก้ไขงบประมาณประจำเดือน"""
    return transaction_controller.set_budget(db, budget)


@router.delete("/{month}", status_code=200)
def delete_budget(month: str, db: Session = Depends(get_db)):
    """ลบงบประมาณประจำเดือน"""
    success = transaction_controller.delete_budget(db, month)
    if not success:
        raise HTTPException(status_code=404, detail="ไม่พบงบประมาณประจำเดือนนี้")
    return {"message": f"ลบงบประมาณเดือน {month} สำเร็จ"}
