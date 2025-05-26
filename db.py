from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from pathlib import Path
import datetime as _dt

DB_PATH = Path(__file__).with_name("buscadores.db")
engine   = create_engine(f"sqlite:///{DB_PATH}", echo=False, future=True)
Base     = declarative_base()
Session  = sessionmaker(bind=engine)

class SearchHistory(Base):
    __tablename__ = "search_history"
    id        = Column(Integer, primary_key=True)
    term      = Column(String(400), nullable=False)
    context   = Column(String(100), nullable=False)
    timestamp = Column(DateTime, default=_dt.datetime.utcnow)

class Feedback(Base):
    __tablename__ = "feedback"
    id        = Column(Integer, primary_key=True)
    context   = Column(String(100), nullable=False)
    feedback  = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=_dt.datetime.utcnow)

Base.metadata.create_all(engine)

def add_search_history(term: str, context: str) -> None:
    with Session() as db:
        db.add(SearchHistory(term=term, context=context))
        db.commit()

def add_feedback(text: str, context: str) -> None:
    if not text.strip():
        return
    with Session() as db:
        db.add(Feedback(context=context, feedback=text.strip()))
        db.commit()
