import streamlit as st
st.set_page_config(page_title="Plataforma AdaptaInfra", layout="centered")

import base64
from Artigos import show_inteligente
from Especialistas import show_especialistas

if 'page' not in st.session_state:
    st.session_state.page = "menu"

def load_font_base64(file_path):
    """Lê o arquivo da fonte e retorna seu conteúdo em base64."""
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
    """Retorna o conteúdo base64 da imagem."""
    with open(file_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

def show_menu():
    # Converte a logo para base64
    logo_base64 = get_base64_image("logo.png")
    
    st.markdown(
        f"""
        <style>
        .main-menu {{
            text-align: center;
            padding-top: 100px;
            background: linear-gradient(135deg, #008000, #800080, #0000FF, #FF0000);
            color: white;
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
        .main-menu p {{
            font-size: 18px;
        }}
        </style>
        <div class="main-menu">
            <img src="data:image/png;base64,{logo_base64}" width="200">
            <h2>Plataforma AdaptaInfra</h2>
            <h6>Conectando Investigación y Especialistas</h6>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Botões dispostos em duas colunas
    col1, col2 = st.columns(2)
    if col1.button("Búsqueda inteligente", key="inteligente", use_container_width=True):
        st.session_state.page = "inteligente"
        if hasattr(st, "experimental_rerun"):
            st.experimental_rerun()
        else:
            st.stop()
    if col2.button("Repositorio de expertos", key="especialistas", use_container_width=True):
        st.session_state.page = "especialistas"
        if hasattr(st, "experimental_rerun"):
            st.experimental_rerun()
        else:
            st.stop()
    
    st.markdown("<div style='padding-top: 50px;'></div>", unsafe_allow_html=True)
    st.caption("© 2025 AdaptaInfra – GIZ | Desarrollado por Daniel Moraes")

if st.session_state.page == "menu":
    show_menu()
elif st.session_state.page == "inteligente":
    show_inteligente()
elif st.session_state.page == "especialistas":
    show_especialistas()
