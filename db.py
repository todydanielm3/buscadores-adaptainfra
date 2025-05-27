from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from pathlib import Path
import datetime as _dt

# Caminho seguro para Streamlit Cloud (pasta onde o código está)
DB_PATH = Path(__file__).parent / "buscadores.db"
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)

# ORM Base e sessão
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

# ───────────── Tabelas ─────────────
class SearchHistory(Base):
    __tablename__ = "search_history"
    id        = Column(Integer, primary_key=True)
    term      = Column(String(256), nullable=False)
    context   = Column(String(100), nullable=False)
    timestamp = Column(DateTime, default=_dt.datetime.utcnow)

class Feedback(Base):
    __tablename__ = "feedback"
    id        = Column(Integer, primary_key=True)
    context   = Column(String(100), nullable=False)
    feedback  = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=_dt.datetime.utcnow)

# Cria as tabelas no banco de dados, se ainda não existirem
Base.metadata.create_all(engine)

# ───────────── Funções utilitárias ─────────────
def add_search_history(term: str, context: str) -> None:
    with SessionLocal() as db:
        db.add(SearchHistory(term=term, context=context))
        db.commit()

def add_feedback(text: str, context: str) -> None:
    if not text.strip():
        return
    with SessionLocal() as db:
        db.add(Feedback(context=context, feedback=text.strip()))
        db.commit()
