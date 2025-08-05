# buscadores.py  ─────────────────────────────────────────────────────────
import streamlit as st
st.set_page_config(
    page_title="OLASIS - Sistema de Información Sostenible", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

import base64
import sys
from pathlib import Path

# Importações diretas dos módulos na mesma pasta
from artigos import show_inteligente
from especialistas import show_especialistas
from olacefs import show_olacefs_search
from chatbot import show_chatbot
from db_view import show_dados

# Função utilitária para converter imagem em base64
def _img_b64(path: str) -> str:
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        return ""

# Aplicar CSS moderno inspirado no design OLASIS
def apply_modern_styles():
    st.markdown("""
    <style>
        /* --- Reset e Configurações Globais --- */
        :root {
            --color-ola: #004FA5;
            --color-sis: #0072BB;
            --color-active-link: #00ACEC;
            --color-text: #333;
            --color-background: #FFFFFF;
            --color-gray-light: #f8f9fa;
            --color-gray-medium: #e9ecef;
            --color-gray-dark: #6c757d;
            --font-main: 'Arial Narrow', Arial, sans-serif;
            --font-logo: 'Poppins', sans-serif;
        }
        
        /* Importação da fonte Poppins */
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
        
        /* Reset do Streamlit */
        .stApp {
            background-color: var(--color-background);
        }
        
        /* Ocultar elementos padrão do Streamlit */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stDeployButton {display: none;}
        
        /* Container principal - ajustado */
        .main-container {
            min-height: 80vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            padding: 2rem 1rem;
            margin-top: 1rem;
            font-family: var(--font-main);
        }
        
        /* Cabeçalho simplificado */
        .header-simple {
            text-align: center;
            padding: 1rem 0;
            border-bottom: 1px solid var(--color-gray-medium);
            margin-bottom: 2rem;
        }
        
        .nav-buttons {
            display: flex;
            justify-content: center;
            gap: 1rem;
            margin-top: 1rem;
        }
        
        .nav-btn {
            background: none;
            border: 1px solid var(--color-gray-medium);
            padding: 0.5rem 1rem;
            border-radius: 20px;
            color: var(--color-text);
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .nav-btn:hover {
            background-color: var(--color-sis);
            color: white;
        }
        
        .nav-btn.active {
            background-color: var(--color-sis);
            color: white;
        }
        
        /* Navegação */
        .nav-links {
            display: flex;
            gap: 1.5rem;
        }
        
        .nav-link {
            position: relative;
            text-decoration: none;
            color: var(--color-text);
            font-size: 1rem;
            padding: 0.5rem;
            transition: color 0.3s;
            cursor: pointer;
        }
        
        .nav-link:hover {
            color: var(--color-sis);
        }
        
        .nav-link::after {
            content: '';
            position: absolute;
            bottom: -5px;
            left: 0;
            width: 100%;
            height: 3px;
            background-color: var(--color-active-link);
            transform: scaleX(0);
            transition: transform 0.3s ease-in-out;
            transform-origin: center;
        }
        
        .nav-link:hover::after {
            transform: scaleX(1);
        }
        
        /* Logo principal */
        .main-logo {
            margin-bottom: 2.5rem;
        }
        
        .main-logo h1 {
            font-family: var(--font-logo);
            font-weight: 600;
            font-size: 4rem;
            letter-spacing: 2px;
            color: var(--color-ola);
            margin: 0;
        }
        
        .logo-highlight {
            color: var(--color-sis);
        }
        
        .tagline {
            font-size: 1.25rem;
            color: var(--color-gray-dark);
            margin-top: 0.5rem;
            margin-bottom: 0;
        }
        
        /* Botões modernos - versão aprimorada */
        .action-buttons {
            display: flex;
            gap: 2rem;
            margin-top: 3rem;
            justify-content: center;
            flex-wrap: wrap;
        }
        
        /* Customizações específicas para botões Streamlit */
        .stButton > button {
            background: linear-gradient(135deg, var(--color-sis), var(--color-ola)) !important;
            color: white !important;
            border: none !important;
            padding: 1rem 2rem !important;
            border-radius: 50px !important;
            font-size: 1.1rem !important;
            font-weight: 600 !important;
            cursor: pointer !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(0, 114, 187, 0.3) !important;
            width: 100% !important;
            height: 60px !important;
            font-family: var(--font-main) !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(0, 114, 187, 0.4) !important;
            background: linear-gradient(135deg, #0080CC, #0056A3) !important;
        }
        
        .stButton > button:active {
            transform: translateY(0) !important;
        }
        
        .stButton > button:focus {
            outline: none !important;
            box-shadow: 0 0 0 3px rgba(0, 114, 187, 0.2) !important;
        }
        
        /* Animação de entrada suave */
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .main-logo {
            animation: fadeInUp 0.8s ease-out;
        }
        
        .action-buttons {
            animation: fadeInUp 1s ease-out 0.2s both;
        }
        
        .info-section {
            animation: fadeInUp 1.2s ease-out 0.4s both;
        }
        
        /* Barra de busca moderna */
        .search-container {
            position: relative;
            max-width: 600px;
            margin: 0 auto 2rem auto;
            animation: fadeInUp 1s ease-out 0.1s both;
        }
        
        .search-input {
            width: 100%;
            padding: 1.2rem 3rem 1.2rem 2rem;
            font-size: 1.1rem;
            border: 2px solid #dfe1e5;
            border-radius: 50px;
            background-color: white;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            outline: none;
            font-family: var(--font-main);
            transition: all 0.3s ease;
        }
        
        .search-input:focus {
            border-color: var(--color-sis);
            box-shadow: 0 4px 15px rgba(0, 114, 187, 0.2);
        }
        
        .search-button {
            position: absolute;
            right: 15px;
            top: 50%;
            transform: translateY(-50%);
            background: none;
            border: none;
            cursor: pointer;
            padding: 0.5rem;
            transition: all 0.3s ease;
        }
        
        .search-button:hover svg {
            stroke: var(--color-sis);
        }
        
        /* Efeito de pulse nos info boxes */
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
        
        .info-box:hover {
            animation: pulse 0.6s ease-in-out;
        }
        
        /* Info boxes */
        .info-section {
            display: flex;
            gap: 1.5rem;
            margin-top: 2.5rem;
            justify-content: center;
            flex-wrap: wrap;
        }
        
        .info-box {
            font-size: 1rem;
            color: var(--color-background);
            background-color: var(--color-sis);
            padding: 0.8rem 1.5rem;
            border: none;
            border-radius: 25px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            font-weight: 500;
        }
        
        /* Responsividade simplificada */
        @media (max-width: 768px) {
            .main-logo h1 {
                font-size: 2.5rem;
            }
            
            .tagline {
                font-size: 1rem;
            }
            
            .stColumn {
                width: 100% !important;
                margin-bottom: 1rem !important;
            }
            
            .search-container {
                max-width: 90%;
            }
        }
        
        /* Animações suaves */
        * {
            transition: all 0.3s ease;
        }
    </style>
    """, unsafe_allow_html=True)

# ─────────────────────────────  Menu UI Moderno  ─────────────────────────────
def show_menu() -> None:
    apply_modern_styles()
    
    # Cabeçalho simplificado
    st.markdown("""
    <div class="header-simple">
        <div style="display: flex; justify-content: center; gap: 1rem; margin-bottom: 1rem;">
            <button class="nav-btn active">ES</button>
            <button class="nav-btn">EN</button>
            <button class="nav-btn">PT</button>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Container principal centralizado
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Logo principal
    st.markdown("""
    <div class="main-logo">
        <h1>OLA<span class="logo-highlight">SIS</span></h1>
        <p class="tagline">Sistema de Información Sostenible</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Área de ação principal
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Botões de ação principais
        st.markdown('<div class="action-buttons">', unsafe_allow_html=True)
        
        # Barra de busca simplificada
        st.markdown("""
        <div class="search-container">
            <input type="search" 
                   class="search-input"
                   placeholder="Buscar artículos o especialistas..." 
                   readonly>
        </div>
        """, unsafe_allow_html=True)
        
        col_btn1, col_btn2, col_btn3 = st.columns(3, gap="medium")
        
        with col_btn1:
            if st.button("📚 Artículos & Publicaciones", key="articles_btn", help="Buscar artículos y publicaciones especializadas"):
                _goto("inteligente")
        
        with col_btn2:
            if st.button("🔧 Herramientas OLACEFS", key="tools_btn", help="Acceder a herramientas y datos OLACEFS"):
                _goto("olacefs")
        
        with col_btn3:
            if st.button("👥 Personas Expertas", key="experts_btn", help="Encontrar especialistas y expertos"):
                _goto("especialistas")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Informações complementares
        st.markdown("""
        <div class="info-section">
            <div class="info-box">+ de 250M artículos</div>
            <div class="info-box">+ de 5.000 especialistas</div>
            <div class="info-box">Red OLACEFS</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

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
