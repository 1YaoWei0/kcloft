from fastapi import FastAPI
from app.routers import question
from app.database import Base, engine

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="KCLoft MVP API")

app.include_router(question.router)
