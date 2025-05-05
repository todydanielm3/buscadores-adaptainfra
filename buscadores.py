import streamlit as st
import base64
from Artigos import show_inteligente
from Especialistas import show_especialistas
from Chatbot import show_chatbot  # Importa a função do Chatbot

st.set_page_config(page_title="Plataforma AdaptaInfra", layout="centered")

if 'page' not in st.session_state:
    st.session_state.page = "menu"

def load_font_base64(file_path):
    with open(file_path, "rb") as font_file:
        return base64.b64encode(font_file.read()).decode()

# Carrega a fonte Roboto e injeta o CSS global
font_base64 = load_font_base64("Roboto-Regular.ttf")
css_font = f"""
<style>
@font-face {{
    font-family: 'Roboto';
    src: url("data:font/ttf;base64,{font_base64}") format('truetype');
    font-weight: normal;
    font-style: normal;
}}
body {{
    font-family: 'Roboto', sans-serif;
}}
</style>
"""
st.markdown(css_font, unsafe_allow_html=True)

def get_base64_image(file_path):
    with open(file_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

def show_menu():
    logo_base64 = get_base64_image("logo.png")
    st.markdown(
        f"""
        <style>
        .main-menu {{
            text-align: center;
            padding-top: 100px;
            color: black;
            padding: 50px;
            border-radius: 10px;
            margin-bottom: 30px;
        }}
        .main-menu h2 {{
            font-family: 'Roboto', sans-serif;
            margin-bottom: 10px;
        }}
        .main-menu h6 {{
            font-family: 'Roboto', sans-serif;
            font-weight: normal;
        }}
        </style>
        <div class="main-menu">
            <img src="data:image/png;base64,{logo_base64}" width="100">
            <h2>Buscador Inteligente</h2>
            <h6>Conectando Investigación y Especialistas</h6>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    col1, col2 = st.columns(2)
    if col1.button("Búsqueda de artículos y publicaciones", key="menu_inteligente", use_container_width=True):
        st.session_state.page = "inteligente"
        st.query_params.update({"page": "inteligente"})
    if col2.button("Buscador de personas expertas", key="menu_especialistas", use_container_width=True):
        st.session_state.page = "especialistas"
        st.query_params.update({"page": "especialistas"})
    

query_params = st.query_params
if "page" in query_params:
    st.session_state.page = query_params["page"]

if st.session_state.page == "menu":
    show_menu()
elif st.session_state.page == "inteligente":
    show_inteligente()
elif st.session_state.page == "especialistas":
    show_especialistas()

# Exibe o chatbot flutuante (definido em Chatbot.py)
show_chatbot()

st.markdown("<div style='padding-top: 50px;'></div>", unsafe_allow_html=True)
#st.caption("© 2025 AdaptaInfra – GIZ | Desarrollado por Daniel Moraes")
st.caption("© 2025 Desarrollado por Daniel Moraes")
