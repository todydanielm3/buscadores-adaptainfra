# db.py
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
import datetime

# Cria a conexão com o banco SQLite (o arquivo será 'buscadores.db')
engine = create_engine('sqlite:///buscadores.db', echo=False)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

# Tabela para histórico de buscas
class SearchHistory(Base):
    __tablename__ = 'search_history'
    id = Column(Integer, primary_key=True, index=True)
    term = Column(String, nullable=False)
    context = Column(String, nullable=False)  # "Artigos" ou "Especialistas"
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

# Tabela para feedback
class Feedback(Base):
    __tablename__ = 'feedback'
    id = Column(Integer, primary_key=True, index=True)
    context = Column(String, nullable=False)
    feedback = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

# Cria as tabelas, se não existirem
Base.metadata.create_all(bind=engine)

def add_search_history(term, context):
    """Adiciona um registro de busca ao banco de dados."""
    db = SessionLocal()
    entry = SearchHistory(term=term, context=context)
    db.add(entry)
    db.commit()
    db.close()

def add_feedback(feedback_text, context):
    """Adiciona um registro de feedback ao banco de dados."""
    db = SessionLocal()
    entry = Feedback(context=context, feedback=feedback_text)
    db.add(entry)
    db.commit()
    db.close()
