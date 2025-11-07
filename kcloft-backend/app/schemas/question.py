from pydantic import BaseModel
from typing import Optional

class QuestionBase(BaseModel):
    question_text: str
    choice_a: str
    choice_b: str
    choice_c: Optional[str]
    choice_d: Optional[str]
    correct_answer: str
    explanation: Optional[str]
    tags: Optional[str]

class QuestionCreate(QuestionBase):
    pass

class QuestionOut(QuestionBase):
    id: int
    class Config:
        orm_mode = True
