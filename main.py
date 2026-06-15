from fastapi import FastAPI
from database import Base, engine
from routers import payment as transaction_router

# สร้าง table ใน SQLite อัตโนมัติ
import models.payment
Base.metadata.create_all(bind=engine)

app = FastAPI(title="รายรับรายจ่าย API")

# Register routers
app.include_router(transaction_router.router)


@app.get("/")
def read_root():
    return {"message": "รายรับรายจ่าย API is running"}
