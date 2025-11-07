from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, models, database
from ..schemas.question import QuestionCreate, QuestionOut

router = APIRouter(prefix="/questions", tags=["questions"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=QuestionOut)
def create_question_endpoint(question: QuestionCreate, db: Session = Depends(get_db)):
    return crud.create_question(db, question)

@router.get("/", response_model=list[QuestionOut])
def read_questions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_questions(db, skip, limit)
