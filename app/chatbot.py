import os, base64, re
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv

# Importações condicionais para o Gemini
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("Gemini não disponível - modo simplificado ativado")

# ─────────── Chave da API ─────────────────────────────────────
load_dotenv()
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
except Exception:
    API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error("Chave da API do Gemini não encontrada.")
    st.stop()

# ─────────── Imagem do chatbot ────────────────────────────────
ASSETS_DIR = Path(__file__).parent.parent / "assets"
IMG_PATH = ASSETS_DIR / "VerichIA.png"

def _img_b64(file_path: Path | str) -> str:
    with open(file_path, "rb") as img:
        return base64.b64encode(img.read()).decode()

def _detectar_idioma(txt: str) -> str:
    pt_kw = ["não","informação","por favor","obrigado","você","como","qual","quem","onde","quando",
             "por quê","porque","responda","me fale","me diga"]
    es_kw = ["no","información","por favor","gracias","usted","cómo","cuál","quién","dónde","cuándo",
             "por qué","porque","responde","dime","cuéntame"]
    pt = sum(1 for p in pt_kw if re.search(rf"\b{p}\b", txt.lower()))
    es = sum(1 for p in es_kw if re.search(rf"\b{p}\b", txt.lower()))
    return "es" if es > pt else "pt"

# ─────────── Função principal ─────────────────────────────────
def show_chatbot() -> None:
    # Verificar se há pergunta na URL
    question_from_url = st.query_params.get("question", "")
    
    mini_logo_b64 = _img_b64(IMG_PATH)

    # Interface visual do chatbot
    st.markdown(
        f"""
        <div style="text-align: center; margin-bottom: 30px;">
            <img src="data:image/png;base64,{mini_logo_b64}" width="80">
            <h1 style="font-family: 'Roboto', sans-serif; color: #333;">OLABOT</h1>
            <p style="font-family: 'Roboto', sans-serif;">Assistente Inteligente OLACEFS</p>
        </div>
        
        <style>
        .chat-message {{
            display: flex;
            align-items: flex-start;
            margin: 1rem 0;
            padding: 1rem;
            border-radius: 10px;
            background-color: #f8f9fa;
        }}
        .chat-user {{
            background-color: #007bff;
            color: white;
            margin-left: auto;
            max-width: 70%;
            justify-content: flex-end;
        }}
        .chatbot-avatar {{
            width: 40px;
            height: 40px;
            border-radius: 50%;
            margin-right: 10px;
        }}
        .chatbot-text {{
            flex: 1;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    # ───── Session state ──────────────────────────────
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # ───── LLM simplificado (sem RAG) ─────────────────────────────
    if "gemini_llm" not in st.session_state and API_KEY and GEMINI_AVAILABLE:
        try:
            st.session_state.gemini_llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                google_api_key=API_KEY,
                temperature=0.7,
                transport="rest",
            )
        except Exception as e:
            st.session_state.gemini_llm = None
            print(f"Erro ao inicializar Gemini: {e}")
    elif not API_KEY or not GEMINI_AVAILABLE:
        st.session_state.gemini_llm = None

    # ───── Render histórico ───────────────────────────
    for m in st.session_state.chat_history:
        if m["role"] == "user":
            st.markdown(f"<div class='chat-message chat-user'>{m['content']}</div>",
                        unsafe_allow_html=True)
        else:
            st.markdown(
                f"""<div class='chat-message'>
                       <img src="data:image/png;base64,{mini_logo_b64}" class='chatbot-avatar'>
                       <div class='chatbot-text'>{m['content']}</div></div>""",
                unsafe_allow_html=True,
            )

    # ───── Entrada do usuário ─────────────────────────
    # Se há pergunta da URL, processar automaticamente
    if question_from_url and not st.session_state.get("url_question_processed", False):
        prompt = question_from_url
        st.session_state.url_question_processed = True
        # Limpar o parâmetro da URL para evitar repetição  
        st.query_params.pop("question", None)
        
        # Mostrar a pergunta do usuário
        st.markdown(f"<div class='chat-message chat-user'>{prompt}</div>",
                    unsafe_allow_html=True)
        
        # Processar automaticamente
        auto_process = True
    else:
        prompt = st.chat_input("Mensagem ao Chatbot:")
        auto_process = False
    
    # ───── Botão Voltar logo abaixo da barra de entrada ─────────────────────────
    if not prompt and not auto_process:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🏠 Voltar ao Menu"):
            st.session_state.page = "menu"
            st.query_params.update({"page": "menu"})
            st.rerun()
        return

    # ───── Rodapé no final da página ─────────────────────────
    st.markdown(
        """
        """,
        unsafe_allow_html=True
    )
    
    if not prompt and not auto_process:
        return

    # Processar mensagem (tanto manual quanto automática)
    if prompt:
        st.session_state.chat_history.append({"role": "user", "content": prompt})

        with st.spinner("Analisando..."):
            try:
                if st.session_state.gemini_llm:
                    # Detectar idioma e configurar resposta
                    idioma = _detectar_idioma(prompt)
                    sys_prompt = ("Eres OLABOT, un asistente de OLACEFS especializado en auditoría, "
                                 "infraestrutura sustentável e transparência. Responde siempre en español, "
                                 "de forma clara, útil e profissional."
                                 if idioma == "es"
                                 else "Você é OLABOT, um assistente da OLACEFS especializado em auditoria, "
                                 "infraestrutura sustentável e transparência. Responda sempre em português, "
                                 "de forma clara, útil e profissional.")
                    
                    # Contexto específico para OLASIS
                    context = f"{sys_prompt}\n\nContexto: OLASIS é o Sistema de Información Sostenible da OLACEFS."
                    full_prompt = f"{context}\n\nPergunta: {prompt}"
                    
                    resp = st.session_state.gemini_llm.invoke(full_prompt)
                    resposta = getattr(resp, "content", str(resp))
                else:
                    # Resposta padrão sem API
                    resposta = ("¡Hola! Soy OLABOT de OLACEFS. Actualmente estoy en modo simplificado. "
                               "¿En qué puedo ayudarte com informações sobre auditoria e infraestrutura sustentável?"
                               if _detectar_idioma(prompt) == "es"
                               else "Olá! Sou OLABOT da OLACEFS. Atualmente estou em modo simplificado. "
                               "Como posso ajudar com informações sobre auditoria e infraestrutura sustentável?")
            except Exception as exc:
                resposta = (f"Disculpa, ocurrió un error inesperado. Por favor, intenta de nuevo."
                           if _detectar_idioma(prompt) == "es"
                           else f"Desculpe, ocorreu um erro inesperado. Por favor, tente novamente.")

        st.session_state.chat_history.append({"role": "model", "content": resposta})
        st.rerun()
