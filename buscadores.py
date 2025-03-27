import streamlit as st
from Artigos import show_inteligente
from Especialistas import show_especialistas

st.set_page_config(page_title="Buscador AdaptaInfra", layout="centered")

if 'page' not in st.session_state:
    st.session_state.page = "menu"

def show_menu():
    # CSS customizado para o menu
    st.markdown(
        """
        <style>
        .main-menu {
            text-align: center;
            padding-top: 100px;
            background: linear-gradient(135deg, #008000, #800080, #0000FF, #FF0000);
            color: white;
            padding: 50px;
            border-radius: 10px;
            margin-bottom: 30px;
        }
        .main-menu h1 {
            font-family: sans-serif;
            margin-bottom: 10px;
        }
        .main-menu p {
            font-size: 18px;
        }
        </style>
        <div class="main-menu">
            <img src="./logo.png" width="100">
            <h1>Buscador AdaptaInfra</h1>
            <p>Selecione uma das opções abaixo:</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Botões dispostos em duas colunas
    col1, col2 = st.columns(2)
    if col1.button("Buscador Inteligente", key="inteligente", use_container_width=True):
        st.session_state.page = "inteligente"
        if hasattr(st, "experimental_rerun"):
            st.experimental_rerun()
        else:
            st.stop()
    if col2.button("Buscador de Especialistas", key="especialistas", use_container_width=True):
        st.session_state.page = "especialistas"
        if hasattr(st, "experimental_rerun"):
            st.experimental_rerun()
        else:
            st.stop()
    
    # Espaço final minimalista
    st.markdown("<div style='padding-top: 50px;'></div>", unsafe_allow_html=True)

if st.session_state.page == "menu":
    show_menu()
elif st.session_state.page == "inteligente":
    show_inteligente()
elif st.session_state.page == "especialistas":
    show_especialistas()
