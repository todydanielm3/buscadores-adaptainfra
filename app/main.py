# buscadores.py  ─────────────────────────────────────────────────────────
import streamlit as st
st.set_page_config(page_title="Buscador Inteligente", layout="centered")

import base64

from artigos import show_inteligente
from app.especialistas import show_especialistas
from app.olacefs import show_olacefs_search
from app.chatbot import show_chatbot
from app.db_view import show_dados

# Função utilitária para converter imagem em base64
def _img_b64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# ─────────────────────────────  Menu UI  ─────────────────────────────
def show_menu() -> None:
    logo = _img_b64("assets/logo.png")
    st.markdown(
        f"""
        <div style="text-align:center;padding-top:70px">
          <img src="data:image/png;base64,{logo}" width="500">
          <h2 style="margin-bottom:4px">Buscador Inteligente</h2>
          <h6 style="margin-top:0">Conectando Investigación e Especialistas</h6>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([1, 1], gap="large")

    if col1.button("Artículos Publicações", use_container_width=True):
        _goto("inteligente")

    if col2.button("Personas Expertas", use_container_width=True):
        _goto("especialistas")

# ──────────────────────────  Navegação helper  ────────────────────────
def _goto(page: str) -> None:
    st.session_state.page = page
    st.query_params.update({"page": page})
    if hasattr(st, "rerun"):
        st.rerun()
    elif hasattr(st, "experimental_rerun"):
        st.experimental_rerun()
    else:
        st.warning("Sua versão do Streamlit não suporta rerun automático. Clique novamente.")

# ──────────────────────────────  Bootstrap  ───────────────────────────
if "page" not in st.session_state:
    st.session_state.page = st.query_params.get("page", "menu")

page = st.session_state.page

if page == "menu":
    show_menu()
elif page == "inteligente":
    show_inteligente()
elif page == "especialistas":
    show_especialistas()
elif page == "olacefs":
    show_olacefs_search()
elif page == "dados":
    show_dados()
else:
    _goto("menu")
    st.stop()

show_chatbot()
st.markdown("<div style='padding-top:40px'></div>", unsafe_allow_html=True)
st.caption("© 2025 Desarrollado por Daniel Moraes")
