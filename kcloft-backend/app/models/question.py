from sqlalchemy import Column, Integer, String, Text
from ..database import Base

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(Text, nullable=False)
    choice_a = Column(String, nullable=False)
    choice_b = Column(String, nullable=False)
    choice_c = Column(String, nullable=True)
    choice_d = Column(String, nullable=True)
    correct_answer = Column(String, nullable=False)
    explanation = Column(Text, nullable=True)
    tags = Column(String, nullable=True)
