from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from schemas.payment import TransactionCreate, TransactionUpdate, TransactionResponse, TransactionSummary
import controllers.payment as transaction_controller

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.get("/summary", response_model=TransactionSummary)
def get_summary(db: Session = Depends(get_db)):
    """สรุปยอดรายรับ รายจ่าย และคงเหลือ"""
    return transaction_controller.get_summary(db)


@router.get("/", response_model=list[TransactionResponse])
def get_all_transactions(
    type: str | None = Query(default=None, description="กรองตามประเภท: income หรือ expense"),
    search: str | None = Query(default=None, description="ค้นหารายละเอียด หรือ หมวดหมู่"),
    start_date: date | None = Query(default=None, description="วันที่เริ่มต้น (YYYY-MM-DD)"),
    end_date: date | None = Query(default=None, description="วันที่สิ้นสุด (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
):
    """ดึงรายการทั้งหมด (กรองตาม type, ค้นหา, และช่วงวันที่ได้)"""
    return transaction_controller.get_all_transactions(
        db=db,
        type=type,
        search=search,
        start_date=start_date,
        end_date=end_date,
    )


@router.get("/{transaction_id}", response_model=TransactionResponse)
def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    """ดึงรายการตาม ID"""
    transaction = transaction_controller.get_transaction_by_id(db, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="ไม่พบรายการ")
    return transaction


@router.post("/", response_model=TransactionResponse, status_code=201)
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    """เพิ่มรายการรายรับหรือรายจ่าย"""
    return transaction_controller.create_transaction(db, transaction)


@router.put("/{transaction_id}", response_model=TransactionResponse)
def update_transaction(transaction_id: int, transaction: TransactionUpdate, db: Session = Depends(get_db)):
    """แก้ไขรายการ"""
    updated = transaction_controller.update_transaction(db, transaction_id, transaction)
    if not updated:
        raise HTTPException(status_code=404, detail="ไม่พบรายการ")
    return updated


@router.delete("/{transaction_id}", response_model=TransactionResponse)
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    """ลบรายการ"""
    deleted = transaction_controller.delete_transaction(db, transaction_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="ไม่พบรายการ")
    return deleted


@router.delete("/", status_code=200)
def reset_all_transactions(db: Session = Depends(get_db)):
    """ลบ transactions ทั้งหมด"""
    deleted_count = transaction_controller.reset_all_transactions(db)
    return {"message": f"ลบข้อมูลทั้งหมดแล้ว", "deleted_count": deleted_count}
