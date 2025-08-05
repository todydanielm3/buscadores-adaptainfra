# OLASIS - Sistema de Informação Sostenible (Novo Layout Olasis4.html)
import streamlit as st
st.set_page_config(
    page_title="OLASIS - Sistema de Información Sostenible", 
    layout="wide",
    initial_sidebar_state="expanded"
)

import base64
import sys
from pathlib import Path

# Importações diretas dos módulos na mesma pasta
from artigos import show_inteligente
from especialistas import show_especialistas
from chatbot import show_chatbot
from db_view import show_dados

# Dicionário de traduções - Completo baseado no HTML
TRANSLATIONS = {
    "es": {
        "olabot": "OLABOT",
        "what-is": "¿Qué es?",
        "tutorial": "Tutorial",
        "contact": "Contacto",
        "tagline": "Sistema de Información Sostenible",
        "search-placeholder": "Hola OLABOT, ¿cómo puedes ayudarme hoy?",
        "tooltip": "¿Cómo puedo ayudarte hoy?",
        "que-es-title": "Entienda el OLASIS-OLACEFS",
        "what-is-header": "¿Qué es el Buscador Inteligente?",
        "what-is-1": "Una herramienta para encontrar información relevante sobre auditoría de infraestructura verde en OLACEFS.",
        "what-is-2": "Ofrece resúmenes concisos y enlaces directos a artículos, documentos y estudios de caso completos.",
        "what-is-3": "Permite buscar por lecciones aprendidas, buenas prácticas y normas relacionadas.",
        "what-is-4": "Incluye perfiles y publicaciones de expertos e investigadores del área (con suporte a ORCID para identificação).",
        "what-is-5": "Es amigable, rápido y fácil de usar, diseñado para el día a día de los auditores.",
        "what-is-not-header": "¿Qué NO es el Buscador Inteligente?",
        "what-is-not-1": "No es un servicio de consultoría jurídica o técnica personalizada.",
        "what-is-not-2": "No garantiza información completa en todos los resúmenes; el acceso al enlace original es fundamental para detalles.",
        "what-is-not-3": "Puede haber retrasos en la actualización de metadatos o enlaces.",
        "what-is-not-4": "Actualmente, el enfoque es en infraestructura verde y temas relacionados con OLACEFS, pudiendo tener limitaciones en otros sectores o regiones.",
        "what-is-not-5": "No sustituye el análisis humano y el juicio profesional.",
        "tutorial-title": "¡Guía Rápida para el Éxito!",
        "tutorial-desc": "Mira nuestro video tutorial para aprender a navegar, buscar y aprovechar al máximo todas las funcionalidades del OLASIS.",
        "tutorial-btn": "Ver Tutorial",
        "info_articles": "+ de 250M artículos",
        "info_experts": "+ de 5.000 especialistas",
        "footer": "© 2025 OLASIS. Todos los derechos reservados.",
        "search_in_articles": "Buscar en Artículos",
        "search_in_experts": "Buscar en Especialistas",
        "ask_chatbot": "Preguntar al OLABOT",
        "chatbot_desc": "Hacer una pregunta al asistente inteligente",
        "articles": "Artículos",
        "experts": "Especialistas",
        "data": "Datos",
        "navigation": "Navegación",
        "language": "Idioma"
    },
    "en": {
        "olabot": "OLABOT",
        "what-is": "What is it?",
        "tutorial": "Tutorial",
        "contact": "Contact",
        "tagline": "Sustainable Information System",
        "search-placeholder": "Hello OLABOT, how can you help me today?",
        "tooltip": "How can I help you today?",
        "que-es-title": "Understand OLASIS-OLACEFS",
        "what-is-header": "What is the Smart Search?",
        "what-is-1": "A tool to find relevant information on green infrastructure auditing in OLACEFS.",
        "what-is-2": "Offers concise summaries and direct links to full articles, documents, and case studies.",
        "what-is-3": "Allows searching for lessons learned, best practices, and related standards.",
        "what-is-4": "Includes profiles and publications of experts and researchers in the field (with ORCID support for identification).",
        "what-is-5": "It is user-friendly, fast, and easy to use, designed for the daily work of auditors.",
        "what-is-not-header": "What is the Smart Search NOT?",
        "what-is-not-1": "It is not a personalized legal or technical consulting service.",
        "what-is-not-2": "It does not guarantee complete information in all summaries; access to the original link is essential for details.",
        "what-is-not-3": "There may be delays in updating metadata or links.",
        "what-is-not-4": "Currently, the focus is on green infrastructure and OLACEFS-related topics, and may have limitations in other sectors or regions.",
        "what-is-not-5": "It does not replace human analysis and professional judgment.",
        "tutorial-title": "Quick Guide to Success!",
        "tutorial-desc": "Watch our video tutorial to learn how to navigate, search, and make the most of all OLASIS features.",
        "tutorial-btn": "Watch Tutorial",
        "info_articles": "+ 3,000 articles",
        "info_experts": "+ 5,000 experts",
        "footer": "© 2025 OLASIS. All rights reserved.",
        "search_in_articles": "Search in Articles",
        "search_in_experts": "Search in Experts",
        "ask_chatbot": "Ask OLABOT",
        "chatbot_desc": "Ask a question to the intelligent assistant",
        "articles": "Articles",
        "experts": "Experts",
        "data": "Data",
        "navigation": "Navigation",
        "language": "Language"
    },
    "pt": {
        "olabot": "OLABOT",
        "what-is": "O que é?",
        "tutorial": "Tutorial",
        "contact": "Contato",
        "tagline": "Sistema de Informação Sustentável",
        "search-placeholder": "Olá OLABOT, como você pode me ajudar hoje?",
        "tooltip": "Como posso te ajudar hoje?",
        "que-es-title": "Entenda o OLASIS-OLACEFS",
        "what-is-header": "O que é o Buscador Inteligente?",
        "what-is-1": "Uma ferramenta para encontrar informações relevantes sobre auditoria de infraestrutura verde na OLACEFS.",
        "what-is-2": "Oferece resumos concisos e links diretos para artigos, documentos e estudos de caso completos.",
        "what-is-3": "Permite pesquisar por lições aprendidas, boas práticas e normas relacionadas.",
        "what-is-4": "Inclui perfis e publicações de especialistas e pesquisadores da área (com suporte ORCID para identificação).",
        "what-is-5": "É amigável, rápido e fácil de usar, projetado para o dia a dia dos auditores.",
        "what-is-not-header": "O que o Buscador Inteligente NÃO é?",
        "what-is-not-1": "Não é um serviço de consultoria jurídica ou técnica personalizada.",
        "what-is-not-2": "Não garante informações completas em todos os resumos; o acesso ao link original é fundamental para detalhes.",
        "what-is-not-3": "Pode haver atrasos na atualização de metadados ou links.",
        "what-is-not-4": "Atualmente, o foco é em infraestrutura verde e temas relacionados à OLACEFS, podendo ter limitações em outros setores ou regiões.",
        "what-is-not-5": "Não substitui a análise humana e o julgamento profissional.",
        "tutorial-title": "Guia Rápido para o Sucesso!",
        "tutorial-desc": "Assista ao nosso vídeo tutorial para aprender a navegar, pesquisar e aproveitar ao máximo todas as funcionalidades do OLASIS.",
        "tutorial-btn": "Ver Tutorial",
        "info_articles": "+ de 250M artigos",
        "info_experts": "+ de 5.000 especialistas",
        "footer": "© 2025 OLASIS. Todos os direitos reservados.",
        "search_in_articles": "Buscar em Artigos",
        "search_in_experts": "Buscar em Especialistas",
        "ask_chatbot": "Perguntar ao OLABOT",
        "chatbot_desc": "Fazer uma pergunta para o assistente inteligente",
        "articles": "Artigos",
        "experts": "Especialistas",
        "data": "Dados",
        "navigation": "Navegação",
        "language": "Idioma"
    }
}

def apply_olasis4_styles():
    """CSS idêntico ao arquivo Olasis4.html"""
    st.markdown("""
    <style>
        /* --- Reset Básico e Configurações Globais --- */
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

        /* Importar fonte Poppins */
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600&display=swap');

        * { 
            margin: 0; 
            padding: 0; 
            box-sizing: border-box; 
        }
        
        html { 
            scroll-behavior: smooth; 
        }
        
        body {
            font-family: var(--font-main);
            background-color: var(--color-background);
            color: var(--color-text);
            overflow-x: hidden;
            transition: filter 0.3s ease;
        }
        
        /* Ocultar elementos padrão do Streamlit */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stDeployButton {display: none;}
        
        /* Configuração global do Streamlit */
        .stApp {
            background-color: var(--color-background) !important;
        }
        
        /* Classes Utilitárias */
        .hidden { 
            display: none !important; 
        }
        
        .visually-hidden { 
            position: absolute; 
            width: 1px; 
            height: 1px; 
            margin: -1px; 
            padding: 0; 
            overflow: hidden; 
            clip: rect(0, 0, 0, 0); 
            border: 0; 
        }

        /* --- Cabeçalho --- */
        .main-header {
            position: absolute; 
            top: 0; 
            left: 0; 
            width: 100%;
            display: flex; 
            justify-content: space-between; 
            align-items: center;
            padding: 1.5rem 2.5rem; 
            z-index: 1000;
        }
        
        .header-left, .header-right { 
            display: flex; 
            align-items: center; 
            gap: 1.5rem; 
        }
        
        .olabot-header-icon { 
            display: flex; 
            align-items: center; 
            gap: 0.5rem;
            text-decoration: none; 
            color: var(--color-text); 
        }

        .olabot-icon-placeholder-header {
            width: 32px; 
            height: 32px; 
            border-radius: 50%;
            background-color: var(--color-gray-medium); 
            border: 1px solid var(--color-gray-medium);
            display: flex; 
            justify-content: center; 
            align-items: center;
        }
        
        .olabot-icon-placeholder-header img { 
            width: 100%; 
            height: 100%; 
            object-fit: cover; 
            border-radius: 50%;
        }
        
        .olabot-header-icon span { 
            font-weight: bold; 
            font-size: 1rem; 
        }
        
        .header-nav { 
            display: flex; 
            gap: 1.5rem; 
        } 
        
        .header-nav a { 
            position: relative;
            text-decoration: none; 
            color: var(--color-text); 
            font-size: 1rem; 
            padding: 0.5rem; 
            transition: color 0.3s; 
            cursor: pointer;
        }
        
        .header-nav a:hover { 
            color: var(--color-sis); 
        }
        
        .header-nav a::after {
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
        
        .header-nav a.active::after,
        .header-nav a:hover::after {
            transform: scaleX(1);
        }

        .language-switcher { 
            display: flex; 
            border: 1px solid var(--color-gray-medium); 
            border-radius: 20px; 
            overflow: hidden; 
        }
        
        .language-switcher .lang-btn { 
            background: none; 
            border: none; 
            padding: 0.5rem 1rem; 
            cursor: pointer; 
            color: var(--color-text); 
            transition: all 0.3s; 
            font-family: var(--font-main); 
        }
        
        .language-switcher .lang-btn.active { 
            background-color: var(--color-sis); 
            color: var(--color-background); 
        }
        
        .accessibility-btn { 
            background: none; 
            border: none; 
            cursor: pointer; 
        }
        
        .accessibility-btn svg { 
            width: 28px; 
            height: 28px; 
            stroke: var(--color-text); 
        }

        /* --- Container Principal de Busca --- */
        .search-page {
            height: 100vh; 
            width: 100%; 
            display: flex; 
            flex-direction: column;
            justify-content: center; 
            align-items: center; 
            text-align: center; 
            padding: 1rem;
        }
        
        .logo-container { 
            margin-bottom: 2.5rem; 
        }
        
        .logo { 
            font-family: var(--font-logo); 
            font-weight: 600; 
            font-size: 6rem; 
            letter-spacing: 2px; 
            color: var(--color-ola); 
        }
        
        .logo-highlight { 
            color: var(--color-sis); 
        }
        
        .tagline { 
            font-size: 1.25rem; 
            color: var(--color-gray-dark); 
            margin-top: -1rem; 
        }

        /* --- Área de Busca --- */
        .search-area { 
            display: flex; 
            align-items: center; 
            gap: 1rem; 
            position: relative; 
            width: 100%; 
            max-width: 1050px; 
            justify-content: center; 
        }
        
        .search-wrapper { 
            flex-grow: 1; 
            max-width: 950px; 
        }
        
        .search-form { 
            display: flex; 
            width: 100%; 
            position: relative; 
        }
        
        .search-bar, .search-input { 
            width: 100%; 
            padding: 1.3rem 4.5rem 1.3rem 2.5rem; 
            font-size: 1.2rem; 
            font-family: var(--font-main); 
            border: 1px solid #dfe1e5; 
            border-radius: 50px; 
            background-color: var(--color-background); 
            box-shadow: 0 2px 10px rgba(0,0,0,0.1); 
            transition: box-shadow 0.3s, border-color 0.3s; 
        }
        
        .search-bar:focus, .search-input:focus { 
            outline: none; 
            box-shadow: 0 4px 15px rgba(0,0,0,0.15); 
            border-color: #dfe1e5; 
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
            display: flex; 
            align-items: center; 
            justify-content: center; 
        }
        
        .search-button svg { 
            stroke: var(--color-gray-dark); 
            transition: stroke 0.2s; 
        }
        
        .search-button:hover svg { 
            stroke: var(--color-sis); 
        }

        .olabot-inline-container { 
            position: relative; 
            flex-shrink: 0; 
        }
        
        .olabot-inline-btn { 
            width: 58px; 
            height: 58px; 
            border-radius: 50%; 
            background: var(--color-background); 
            border: 1px solid #dfe1e5; 
            cursor: pointer; 
            display: flex; 
            justify-content: center; 
            align-items: center; 
            padding: 0; 
            overflow: hidden; 
            box-shadow: 0 2px 10px rgba(0,0,0,0.1); 
            transition: box-shadow 0.3s; 
        }
        
        .olabot-inline-btn:hover { 
            box-shadow: 0 4px 15px rgba(0,0,0,0.15); 
        }
        
        .olabot-icon-placeholder-inline { 
            width: 100%; 
            height: 100%; 
            background-color: var(--color-sis); 
        }
        
        .olabot-icon-placeholder-inline img { 
            width: 100%; 
            height: 100%; 
            object-fit: cover; 
            border-radius: 50%;
        }

        .info-boxes { 
            display: flex; 
            gap: 1.5rem; 
            margin-top: 2.5rem; 
        }
        
        .info-box { 
            font-size: 1rem; 
            color: var(--color-background); 
            background-color: var(--color-sis); 
            padding: 0.7rem 1.5rem; 
            border: none; 
            border-radius: 20px; 
            box-shadow: 0 2px 10px rgba(0,0,0,0.07); 
        }

        /* --- Seções da Landing Page --- */
        .landing-content { 
            background-color: var(--color-gray-light); 
            padding-top: 1px; 
        }
        
        .content-section { 
            padding: 6rem 2rem; 
            max-width: 1000px; 
            margin: 0 auto; 
        }
        
        .tutorial-section { 
            padding-top: 2rem; 
        }
        
        .que-es-content-grid { 
            display: flex; 
            gap: 4rem; 
            align-items: flex-start; 
        }
        
        .que-es-content-column { 
            flex: 1; 
            text-align: justify; 
        }
        
        .que-es-title { 
            font-size: 2.5rem; 
            margin-bottom: 2.5rem; 
            color: var(--color-sis); 
            text-align: center; 
        }
        
        .que-es-subtitle { 
            font-size: 1.5rem; 
            margin-bottom: 1rem; 
            color: var(--color-text); 
            text-align: left;
        }
        
        .que-es-list { 
            list-style: none; 
            padding-left: 0; 
        }
        
        .que-es-list li { 
            font-size: 1.1rem; 
            line-height: 1.7; 
            margin-bottom: 1rem; 
        }
        
        .tutorial-content-grid { 
            display: flex; 
            gap: 3rem; 
            align-items: center; 
        }
        
        .video-placeholder { 
            flex: 1.2; 
            height: 320px; 
            background-color: var(--color-gray-medium); 
            border-radius: 12px; 
            display: flex; 
            justify-content: center; 
            align-items: center; 
            cursor: pointer; 
        }
        
        .play-button { 
            width: 80px; 
            height: 80px; 
            background-color: rgba(255,255,255,0.8); 
            border-radius: 50%; 
            display: flex; 
            justify-content: center; 
            align-items: center; 
            transition: transform 0.2s; 
        }
        
        .video-placeholder:hover .play-button { 
            transform: scale(1.1); 
        }
        
        .play-button svg { 
            fill: var(--color-text); 
        }
        
        .tutorial-text-content { 
            flex: 1; 
            text-align: left; 
        }
        
        .tutorial-title { 
            font-size: 2rem; 
            color: var(--color-sis); 
            margin-bottom: 1rem; 
        }
        
        .tutorial-description { 
            font-size: 1.1rem; 
            line-height: 1.6; 
            margin-bottom: 1.5rem; 
        }
        
        .cta-btn { 
            background-color: var(--color-sis); 
            color: white; 
            padding: 0.8rem 1.8rem; 
            border: none; 
            border-radius: 25px; 
            font-size: 1rem; 
            cursor: pointer; 
            box-shadow: 0 4px 15px rgba(0, 114, 187, 0.3); 
            transition: transform 0.2s; 
        }
        
        .cta-btn:hover { 
            transform: translateY(-2px); 
        }

        /* --- Estilos do Rodapé --- */
        .footer-section { 
            text-align: center; 
            padding: 4rem 2rem 2rem 2rem; 
            background-color: var(--color-gray-light); 
            color: var(--color-gray-dark); 
            font-size: 0.9rem; 
        }
        
        .logo-bar-container {
            margin-bottom: 3rem;
            min-height: 50px;
        }

        /* --- DESIGN RESPONSIVO --- */
        @media (max-width: 1024px) {
            .logo { 
                font-size: 5rem; 
            }
            
            .tagline { 
                font-size: 1.1rem; 
            }
            
            .search-area { 
                max-width: 90%; 
            }
            
            .content-section { 
                padding: 4rem 1.5rem; 
            }
            
            .que-es-content-grid { 
                flex-direction: column; 
                gap: 2.5rem; 
            }
            
            .tutorial-content-grid { 
                flex-direction: column; 
                gap: 2rem; 
            }
            
            .main-header { 
                padding: 1rem 1.5rem; 
            }
        }
        
        @media (max-width: 768px) {
            .main-header { 
                flex-direction: column; 
                gap: 1rem; 
                position: relative; 
            }
            
            .header-left, .header-right { 
                width: 100%; 
                justify-content: space-between; 
            }
            
            .header-left { 
                order: 1; 
            }
            
            .header-right { 
                order: 2; 
            }
            
            .olabot-header-icon { 
                margin-right: auto; 
            }
            
            .language-switcher { 
                margin-left: auto; 
            }
            
            .header-nav { 
                gap: 1rem; 
            }
            
            .header-nav a { 
                padding: 0.5rem 0.2rem; 
            }
            
            .logo { 
                font-size: 3.5rem; 
            }
            
            .tagline { 
                font-size: 1rem; 
            }
            
            .search-area { 
                flex-direction: column; 
                gap: 1.5rem; 
            }
            
            .search-page { 
                padding-top: 150px; 
            }
            
            .search-bar { 
                padding: 1.1rem 4rem 1.1rem 2rem; 
                font-size: 1rem; 
            }
            
            .olabot-inline-btn { 
                width: 50px; 
                height: 50px; 
            }
            
            .info-boxes { 
                flex-direction: column; 
                gap: 0.8rem; 
            }
        }

        /* Estilos específicos do Streamlit */
        .stButton > button {
            background: none !important;
            border: none !important;
            color: var(--color-text) !important;
            text-decoration: none !important;
            padding: 0.5rem !important;
            font-size: 1rem !important;
            cursor: pointer !important;
            transition: color 0.3s !important;
        }
        
        .stButton > button:hover {
            color: var(--color-sis) !important;
        }
        
        .stSelectbox > div > div {
            border: 1px solid var(--color-gray-medium) !important;
            border-radius: 20px !important;
            background: white !important;
        }
        
        .stSelectbox .st-bx {
            background-color: var(--color-sis) !important;
            color: var(--color-background) !important;
        }

        /* Sidebar sempre aberta e estilizada */
        .css-1d391kg {
            width: 300px !important;
            min-width: 300px !important;
        }
        
        .css-1lcbmhc {
            width: 300px !important;
            min-width: 300px !important;
        }
        
        .css-17eq0hr {
            width: 300px !important;
            min-width: 300px !important;
        }
        
        /* Forçar sidebar a sempre aparecer */
        section[data-testid="stSidebar"] {
            width: 300px !important;
            min-width: 300px !important;
            transform: translateX(0px) !important;
        }
        
        section[data-testid="stSidebar"] > div {
            width: 300px !important;
            min-width: 300px !important;
        }
        
        /* Botão de fechar sidebar - ocultar */
        button[kind="header"][data-testid="baseButton-header"] {
            display: none !important;
        }
        
        /* Estilizar botões da sidebar */
        .stButton > button {
            width: 100% !important;
            text-align: left !important;
            border-radius: 8px !important;
            margin-bottom: 0.5rem !important;
            padding: 0.75rem 1rem !important;
            background-color: transparent !important;
            border: 1px solid #e0e0e0 !important;
            transition: all 0.3s ease !important;
        }
        
        .stButton > button:hover {
            background-color: var(--color-gray-light) !important;
            border-color: var(--color-sis) !important;
            transform: translateX(5px) !important;
        }
        
        /* Estilizar selectbox da sidebar */
        .stSelectbox {
            margin-bottom: 1.5rem !important;
        }
    </style>
    """, unsafe_allow_html=True)

def render_header(t, current_lang):
    """Renderiza o cabeçalho baseado no HTML Olasis4"""
    # Determinar qual botão de idioma está ativo
    es_active = "active" if current_lang == "es" else ""
    en_active = "active" if current_lang == "en" else ""
    pt_active = "active" if current_lang == "pt" else ""

    return f"""
    <header class="main-header">
        <div class="header-left">
            <a href="javascript:void(0)" class="olabot-header-icon" title="Abrir OLABOT">
                <div class="olabot-icon-placeholder-header">
                    <img src="https://i.ibb.co/20Jycz8Q/Olacita.png" alt="Ícone OLABOT">
                </div>
                <span>{t["olabot"]}</span>
            </a>
            <nav class="header-nav">
                <a href="#que-es">{t["what-is"]}</a>
                <a href="#tutorial">{t["tutorial"]}</a>
                <a href="https://olacefs.com/contacto/" target="_blank">{t["contact"]}</a>
            </nav>
        </div>
        <div class="header-right">
            <div class="language-switcher" id="language-switcher">
                <button class="lang-btn {es_active}" data-lang="es" onclick="changeLanguage('es')">ES</button>
                <button class="lang-btn {en_active}" data-lang="en" onclick="changeLanguage('en')">EN</button>
                <button class="lang-btn {pt_active}" data-lang="pt" onclick="changeLanguage('pt')">PT</button>
            </div>
            <button class="accessibility-btn" title="Modo de daltonismo">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                    <circle cx="12" cy="12" r="3"></circle>
                </svg>
                <span class="visually-hidden">Activar modo daltonismo</span>
            </button>
        </div>
    </header>
    """

def render_search_page(t):
    """Renderiza a página principal de busca baseada no HTML Olasis4"""
    return f"""
    <main class="search-page">
        <div class="logo-container">
            <h1 class="logo">OLA<span class="logo-highlight">SIS</span></h1>
            <p class="tagline">{t["tagline"]}</p>
        </div>
        <div class="search-area">
            <div class="search-wrapper">
                <div class="search-container">
                    <form class="search-form">
                        <input type="search" placeholder="{t["search-placeholder"]}" class="search-input" required>
                        <button type="submit" class="search-button" title="Conversar com OLABOT">
                            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                                <circle cx="11" cy="11" r="8"></circle>
                                <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                            </svg>
                        </button>
                    </form>
                </div>
            </div>
            <div class="olabot-inline-container">
                <button class="olabot-inline-btn" onclick="openChatbot()">
                    <div class="olabot-icon-placeholder-inline">
                        <img src="https://i.ibb.co/20Jycz8Q/Olacita.png" alt="Ícone OLABOT Chat">
                    </div>
                </button>
            </div>
        </div>
        <div class="info-boxes">
            <div class="info-box">{t["info_articles"]}</div>
            <div class="info-box">{t["info_experts"]}</div>
        </div>
    </main>
    """

def render_landing_content(t):
    """Renderiza o conteúdo da landing page baseado no HTML Olasis4"""
    return f"""
    <div class="landing-content">
        <section class="content-section">
            <h2 class="que-es-title">{t["que-es-title"]}</h2>
            <div class="que-es-content-grid">
                <div class="que-es-content-column">
                    <h3 class="que-es-subtitle">{t["what-is-header"]}</h3>
                    <ul class="que-es-list">
                        <li>{t["what-is-1"]}</li>
                        <li>{t["what-is-2"]}</li>
                        <li>{t["what-is-3"]}</li>
                        <li>{t["what-is-4"]}</li>
                        <li>{t["what-is-5"]}</li>
                    </ul>
                </div>
                <div class="que-es-content-column">
                    <h3 class="que-es-subtitle">{t["what-is-not-header"]}</h3>
                    <ul class="que-es-list">
                        <li>{t["what-is-not-1"]}</li>
                        <li>{t["what-is-not-2"]}</li>
                        <li>{t["what-is-not-3"]}</li>
                        <li>{t["what-is-not-4"]}</li>
                        <li>{t["what-is-not-5"]}</li>
                    </ul>
                </div>
            </div>
        </section>
        <section class="content-section tutorial-section">
            <div class="tutorial-content-grid">
                <div class="video-placeholder">
                    <div class="play-button">
                        <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24">
                            <path d="M8 5v14l11-7z"></path>
                        </svg>
                    </div>
                </div>
                <div class="tutorial-text-content">
                    <h3 class="tutorial-title">{t["tutorial-title"]}</h3>
                    <p class="tutorial-description">{t["tutorial-desc"]}</p>
                    <button class="cta-btn">{t["tutorial-btn"]}</button>
                </div>
            </div>
        </section>
        <footer class="footer-section">
            <div class="logo-bar-container">
                <img src="https://i.ibb.co/tpyTSFD2/Barra-de-Logos-em-Espanhol.png" alt="Barra de Logos" style="max-width: 100%; height: auto;" />
            </div>
            <p>{t["footer"]}</p>
        </footer>
    </div>
    """

def show_olasis_homepage():
    """Interface principal baseada no design Olasis4.html"""
    apply_olasis4_styles()
    
    # Detectar idioma da URL ou usar padrão
    lang_param = st.query_params.get("lang", "es")
    if lang_param not in TRANSLATIONS:
        lang_param = "es"
    
    # Inicializar idioma
    if "current_language" not in st.session_state:
        st.session_state.current_language = lang_param
    
    # Atualizar idioma se mudou na URL
    if st.session_state.current_language != lang_param:
        st.session_state.current_language = lang_param
        st.rerun()
    
    # Obter traduções
    t = TRANSLATIONS[st.session_state.current_language]
    
    # Seletor de idioma discreto no sidebar (temporário para funcionamento)
    with st.sidebar:        
        st.markdown(f"### {t['language']} / Language")
        lang_options = {
            "🇪🇸 Español": "es",
            "🇺🇸 English": "en", 
            "🇧🇷 Português": "pt"
        }
        
        selected_lang = st.selectbox(
            "Selecione o idioma",
            options=list(lang_options.keys()),
            index=0,
            key="lang_selector"
        )
        
        st.session_state.current_language = lang_options[selected_lang]
        
        # Adicionar botões de navegação no sidebar
        st.markdown(f"### {t['navigation']}")
        if st.button(t["articles"], key="nav_articles"):
            _goto("inteligente")
        if st.button(t["experts"], key="nav_experts"):  
            _goto("especialistas")
        if st.button("OLABOT", key="nav_chatbot"):
            _goto("chatbot")
        if st.button(t["contact"], key="nav_contact"):
            js_code = "window.open('https://olacefs.com/contacto/', '_blank');"
            st.components.v1.html(f"<script>{js_code}</script>", height=0)
        if st.button(t["data"], key="nav_data"):
            _goto("dados")
    
    # Obter traduções
    t = TRANSLATIONS[st.session_state.current_language]
    
    # Renderizar a interface principal
    header_html = render_header(t, st.session_state.current_language)
    search_page_html = render_search_page(t)
    landing_content_html = render_landing_content(t)
    
    # Combinar todo o HTML
    full_html = header_html + search_page_html + landing_content_html
    
    # Renderizar tudo
    st.markdown(full_html, unsafe_allow_html=True)
    
    # JavaScript para interatividade
    st.markdown(f"""
    <script>
    // Função para trocar idioma
    function changeLanguage(lang) {{
        const currentUrl = new URL(window.location);
        currentUrl.searchParams.set('lang', lang);
        window.location.href = currentUrl.toString();
    }}
    
    // Função para abrir o chatbot
    function openChatbot() {{
        const currentUrl = new URL(window.location);
        currentUrl.searchParams.set('page', 'chatbot');
        window.location.href = currentUrl.toString();
    }}
    
    // Função para conversar com OLABOT
    function chatWithOlabot(message) {{
        const currentUrl = new URL(window.location);
        currentUrl.searchParams.set('page', 'chatbot');
        currentUrl.searchParams.set('question', message);
        window.location.href = currentUrl.toString();
    }}
    
    document.addEventListener('DOMContentLoaded', function() {{
        // Barra de busca direta para OLABOT
        const searchInput = document.querySelector('.search-input');
        const searchForm = document.querySelector('.search-form');
        
        if (searchForm) {{
            searchForm.addEventListener('submit', function(e) {{
                e.preventDefault();
                const query = searchInput ? searchInput.value.trim() : '';
                if (query) {{
                    // Sempre direcionar para OLABOT
                    chatWithOlabot(query);
                }}
            }});
        }}
        
        // Enter no input também submete
        if (searchInput) {{
            searchInput.addEventListener('keypress', function(e) {{
                if (e.key === 'Enter') {{
                    e.preventDefault();
                    const query = this.value.trim();
                    if (query) {{
                        chatWithOlabot(query);
                    }}
                }}
            }});
        }}
    }});
    </script>
    """, unsafe_allow_html=True)

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
    show_olasis_homepage()
elif page == "inteligente":
    show_inteligente()
elif page == "especialistas":
    show_especialistas()
elif page == "dados":
    show_dados()
elif page == "chatbot":
    show_chatbot()
else:
    _goto("menu")
    st.stop()

# Rodapé dinâmico (somente nas páginas internas)
if page != "menu":
    if "current_language" in st.session_state:
        footer_text = TRANSLATIONS[st.session_state.current_language]['footer']
    else:
        footer_text = TRANSLATIONS['es']['footer']
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.caption(footer_text)
