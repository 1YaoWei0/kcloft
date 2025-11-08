from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, database
from ..crud import question as crud_question
from ..schemas.question import QuestionCreate, QuestionOut
from ..auth import verify_token

router = APIRouter(prefix="/questions", tags=["questions"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=QuestionOut, dependencies=[Depends(verify_token)])
def create_question_endpoint(question: QuestionCreate, db: Session = Depends(get_db)):
    return crud_question.create_question(db, question)

@router.get("/", response_model=list[QuestionOut], dependencies=[Depends(verify_token)])
def read_questions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud_question.get_questions(db, skip, limit)
