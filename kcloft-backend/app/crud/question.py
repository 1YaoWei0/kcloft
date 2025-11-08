from sqlalchemy.orm import Session
from .. import models
from ..schemas.question import QuestionCreate

def create_question(db: Session, question: QuestionCreate):
    db_question = models.Question(**question.dict())
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

def get_questions(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Question).offset(skip).limit(limit).all()