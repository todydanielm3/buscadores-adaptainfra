# migrate_fonte.py
from sqlalchemy import create_engine, text

# caminho relativo para buscadores.db
engine = create_engine("sqlite:///buscadores.db")

with engine.begin() as conn:
    # verifica se a coluna já existe
    res = conn.execute(
        text("""
            PRAGMA table_info(search_history);
        """)
    ).fetchall()
    colunas = [row[1] for row in res]

    if "fonte" not in colunas:
        conn.execute(text(
            "ALTER TABLE search_history ADD COLUMN fonte TEXT;"
        ))
        print("✅ Coluna 'fonte' adicionada.")
    else:
        print("ℹ️ Coluna 'fonte' já existe – nada a fazer.")
