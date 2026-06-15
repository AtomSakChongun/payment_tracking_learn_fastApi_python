from sqlalchemy.orm import Session
from sqlalchemy import func
from models.payment import Transaction
from schemas.payment import TransactionCreate, TransactionUpdate


def get_all_transactions(db: Session, type: str | None = None):
    query = db.query(Transaction)
    if type:
        query = query.filter(Transaction.type == type)
    return query.order_by(Transaction.created_at.desc()).all()


def get_transaction_by_id(db: Session, transaction_id: int):
    return db.query(Transaction).filter(Transaction.id == transaction_id).first()


def create_transaction(db: Session, transaction: TransactionCreate):
    db_transaction = Transaction(
        title=transaction.title,
        amount=transaction.amount,
        type=transaction.type,
        category=transaction.category,
        note=transaction.note,
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


def update_transaction(db: Session, transaction_id: int, transaction: TransactionUpdate):
    db_transaction = get_transaction_by_id(db, transaction_id)
    if not db_transaction:
        return None

    update_data = transaction.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_transaction, key, value)

    db.commit()
    db.refresh(db_transaction)
    return db_transaction


def delete_transaction(db: Session, transaction_id: int):
    db_transaction = get_transaction_by_id(db, transaction_id)
    if not db_transaction:
        return None

    db.delete(db_transaction)
    db.commit()
    return db_transaction


def get_summary(db: Session):
    total_income = db.query(func.sum(Transaction.amount)).filter(Transaction.type == "income").scalar() or 0.0
    total_expense = db.query(func.sum(Transaction.amount)).filter(Transaction.type == "expense").scalar() or 0.0
    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": total_income - total_expense,
    }


def reset_all_transactions(db: Session):
    deleted_count = db.query(Transaction).delete()
    db.commit()
    return deleted_count
