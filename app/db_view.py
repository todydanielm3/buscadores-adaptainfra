# db_view.py  – visualiza o conteúdo de buscadores.db em /?page=dados
import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name("buscadores.db")

def _query_df(sql: str) -> pd.DataFrame:
    with sqlite3.connect(DB_PATH) as con:
        return pd.read_sql_query(sql, con)

def show_dados() -> None:
    st.header("📊 Dados armazenados")
    st.caption(f"Base: {DB_PATH}")

    # exemplo simples: tabs para cada tabela
    tabelas = _query_df(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    )["name"].tolist()

    if not tabelas:
        st.info("Nenhuma tabela encontrada.")
        return

    for nome in tabelas:
        with st.expander(f"🔍 {nome}"):
            df = _query_df(f"SELECT * FROM {nome} LIMIT 1000")
            st.dataframe(df, use_container_width=True)
