from sqlalchemy import Column, Integer, String, Text, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()


class Category(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return f"<{self.id} {self.name}>"


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)
    answer = Column(String)
    question = Column(Text)
    category_id = Column(Integer, ForeignKey("category.id"))

    def __repr__(self):
        return f"<{self.id} {self.answer}>"


if __name__ == "__main__":
    engine = create_engine("sqlite:///exercise.db", echo=True)
    Base.metadata.create_all(engine)
