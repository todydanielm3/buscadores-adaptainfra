import base64
import streamlit as st

from Artigos import show_inteligente
from Especialistas import show_especialistas
from Olacefs import show_olacefs_search         # ← NOVO
from Chatbot   import show_chatbot

st.set_page_config(page_title="Buscador Inteligente", layout="centered")

# ------------------------------------------------------------------ utils
def get_base64_image(p):
    with open(p, "rb") as f:
        return base64.b64encode(f.read()).decode()

# ------------------------------------------------------------------ menu
def show_menu():
    logo = get_base64_image("logo.png")
    st.markdown(
        f"""
        <div style="text-align:center;padding-top:70px">
          <img src="data:image/png;base64,{logo}" width="100">
          <h2>Buscador Inteligente</h2>
          <h6>Conectando Investigación y Especialistas</h6>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col_mid, col2 = st.columns([1,1,1])
    if col1.button("Artículos y Publicaciones", use_container_width=True):
        st.session_state.page = "inteligente"
        st.query_params.update({"page": "inteligente"})

    if col_mid.button("OLACEFS", use_container_width=True,
                      type="primary",  # azul / texto branco
                      help="Busca dados no portal datos.olacefs.com"):
        st.session_state.page = "olacefs"
        st.query_params.update({"page": "olacefs"})

    if col2.button("Personas Expertas", use_container_width=True):
        st.session_state.page = "especialistas"
        st.query_params.update({"page": "especialistas"})


# ------------------------------------------------------------------ roteador
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

# chatbot flutuante
show_chatbot()
st.markdown("<div style='padding-top:40px'></div>", unsafe_allow_html=True)
st.caption("© 2025 Desarrollado por Daniel Moraes")
