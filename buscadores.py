import streamlit as st
from Artigos import show_inteligente
from Especialistas import show_especialistas
from comunidade import show_comunidade

st.set_page_config(page_title="Buscador AdaptaInfra", layout="centered")

if 'page' not in st.session_state:
    st.session_state.page = "menu"

def show_menu():
    st.image("logo.png", width=250)
    st.title("Plataforma Adaptativa")
    #st.write("Escolha um dos buscadores abaixo:")
    col1, col2, col3 = st.columns(3)
    if col1.button("Buscador Inteligente"):
        st.session_state.page = "inteligente"
        if hasattr(st, "experimental_rerun"):
            st.experimental_rerun()
        else:
            st.stop()
    if col2.button("Buscador de Especialistas"):
        st.session_state.page = "especialistas"
        if hasattr(st, "experimental_rerun"):
            st.experimental_rerun()
        else:
            st.stop()
    if col3.button("Comunidade +"):
        st.session_state.page = "comunidade"
        if hasattr(st, "experimental_rerun"):
            st.experimental_rerun()
        else:
            st.stop()

if st.session_state.page == "menu":
    show_menu()
elif st.session_state.page == "inteligente":
    show_inteligente()
elif st.session_state.page == "especialistas":
    show_especialistas()
elif st.session_state.page == "comunidade":
    show_comunidade()
