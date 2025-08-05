# buscadores.py - Versão Limpa e Corrigida  ─────────────────────────────────────
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

# Aplicar CSS limpo e moderno
def apply_clean_styles():
    st.markdown("""
    <style>
        /* CSS Limpo para OLASIS */
        :root {
            --color-ola: #004FA5;
            --color-sis: #0072BB;
            --color-text: #333;
            --color-background: #FFFFFF;
            --color-gray-medium: #e9ecef;
            --color-gray-dark: #6c757d;
        }
        
        /* Reset básico */
        .stApp {
            background-color: var(--color-background) !important;
        }
        
        /* Ocultar elementos padrão do Streamlit */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stDeployButton {display: none;}
        
        /* Container principal */
        .main-container {
            padding: 2rem 1rem;
            text-align: center;
            max-width: 1200px;
            margin: 0 auto;
        }
        
        /* Logo principal */
        .main-logo h1 {
            font-weight: 600;
            font-size: 3.5rem;
            color: var(--color-ola);
            margin: 1rem 0;
        }
        
        .logo-highlight {
            color: var(--color-sis);
        }
        
        .tagline {
            font-size: 1.2rem;
            color: var(--color-gray-dark);
            margin-bottom: 2rem;
        }
        
        /* Barra de busca */
        .search-input {
            width: 100%;
            max-width: 600px;
            padding: 1rem 2rem;
            font-size: 1.1rem;
            border: 2px solid #dfe1e5;
            border-radius: 50px;
            margin: 0 auto 2rem auto;
            display: block;
            outline: none;
        }
        
        .search-input:focus {
            border-color: var(--color-sis);
            box-shadow: 0 4px 15px rgba(0, 114, 187, 0.2);
        }
        
        /* Botões Streamlit */
        .stButton > button {
            background: linear-gradient(135deg, var(--color-sis), var(--color-ola)) !important;
            color: white !important;
            border: none !important;
            padding: 1rem 2rem !important;
            border-radius: 50px !important;
            font-size: 1rem !important;
            font-weight: 600 !important;
            width: 100% !important;
            height: 60px !important;
            transition: all 0.3s ease !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(0, 114, 187, 0.4) !important;
        }
        
        /* Info boxes */
        .info-section {
            display: flex;
            gap: 1rem;
            margin-top: 2rem;
            justify-content: center;
            flex-wrap: wrap;
        }
        
        .info-box {
            background-color: var(--color-sis);
            color: white;
            padding: 0.8rem 1.5rem;
            border-radius: 25px;
            font-weight: 500;
        }
        
        /* Responsividade */
        @media (max-width: 768px) {
            .main-logo h1 {
                font-size: 2.5rem;
            }
            
            .info-section {
                flex-direction: column;
                align-items: center;
            }
        }
    </style>
    """, unsafe_allow_html=True)

# ─────────────────────────────  Menu UI Limpo  ─────────────────────────────
def show_menu() -> None:
    apply_clean_styles()
    
    # Container principal
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Seletor de idioma no topo
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.selectbox("Idioma / Language", ["🇪🇸 Español", "🇺🇸 English", "🇧🇷 Português"], key="language")
    
    # Logo principal
    st.markdown("""
    <div class="main-logo">
        <h1>OLA<span class="logo-highlight">SIS</span></h1>
        <p class="tagline">Sistema de Información Sostenible</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Barra de busca
    st.markdown("""
    <input type="text" 
           class="search-input" 
           placeholder="Buscar artículos o especialistas..." 
           readonly>
    """, unsafe_allow_html=True)
    
    # Botões principais
    col1, col2, col3 = st.columns(3, gap="medium")
    
    with col1:
        if st.button("📚 Artículos & Publicaciones", key="articles_btn"):
            _goto("inteligente")
    
    with col2:
        if st.button("🔧 Herramientas OLACEFS", key="tools_btn"):
            _goto("olacefs")
    
    with col3:
        if st.button("👥 Personas Expertas", key="experts_btn"):
            _goto("especialistas")
    
    # Info boxes
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

# Chatbot na parte inferior apenas no menu
if page == "menu":
    st.markdown("<br><br>", unsafe_allow_html=True)
    show_chatbot()

# Rodapé
st.markdown("<br>", unsafe_allow_html=True)
st.caption("© 2025 Desarrollado por Daniel Moraes - OLASIS Sistema de Información Sostenible")
