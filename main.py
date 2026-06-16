from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from routers import payment as transaction_router
from routers import budget as budget_router

# สร้าง table ใน SQLite อัตโนมัติ
import models.payment
Base.metadata.create_all(bind=engine)

app = FastAPI(title="รายรับรายจ่าย API")

# Configure CORS
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5174",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(transaction_router.router)
app.include_router(budget_router.router)


@app.get("/")
def read_root():
    return {"message": "รายรับรายจ่าย API is running"}
