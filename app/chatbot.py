import os
import base64
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv
import re

from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI

from langchain_core.documents import Document
from langchain.chains import RetrievalQA

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

def get_base64_image(file_path: Path | str) -> str:
    with open(file_path, "rb") as img:
        return base64.b64encode(img.read()).decode()

def detectar_idioma(texto: str) -> str:
    """Detecta se o texto está em português ou espanhol (simples, por palavras-chave)."""
    pt_palavras = ["não", "informação", "por favor", "obrigado", "você", "como", "qual", "quem", "onde", "quando", "por quê", "porque", "responda", "me fale", "me diga"]
    es_palavras = ["no", "información", "por favor", "gracias", "usted", "cómo", "cuál", "quién", "dónde", "cuándo", "por qué", "porque", "responde", "dime", "cuéntame"]
    pt_count = sum(1 for p in pt_palavras if re.search(rf"\b{p}\b", texto.lower()))
    es_count = sum(1 for p in es_palavras if re.search(rf"\b{p}\b", texto.lower()))
    if es_count > pt_count:
        return "es"
    return "pt"

# ─────────── Função principal ─────────────────────────────────
def show_chatbot() -> None:
    mini_logo_b64 = get_base64_image(IMG_PATH)

    # HTML/CSS do chatbot flutuante
    st.markdown(
        f"""
        <style>
        .chatbot-container {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 350px;
            max-height: 600px;
            border: 1px solid #ccc;
            border-radius: 10px;
            background: white;
            z-index: 1000;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            font-family: 'Segoe UI', sans-serif;
        }}
        .chat-message {{
            background: #f1f1f1;
            margin-bottom: 8px;
            padding: 8px 10px;
            border-radius: 8px;
            max-width: 90%;
            display: flex;
            align-items: flex-start;
        }}
        .chat-user {{
            background: #DCF8C6;
            margin-left: auto;
            text-align: right;
            justify-content: flex-end;
        }}
        .chatbot-avatar {{
            width: 24px;
            height: 24px;
            margin-right: 8px;
            border-radius: 12px;
        }}
        .chatbot-text {{
            flex: 1;
        }}
        </style>
        <script>
        function toggleChatbot() {{
            var body = document.getElementById("chat-body");
            if (body.style.display === "block") {{
                body.style.display = "none";
            }} else {{
                body.style.display = "block";
            }}
        }}
        </script>
        """,
        unsafe_allow_html=True,
    )

    # Inicializa sessão e modelo
    with st.container():
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        # Carrega vetor e embeddings uma única vez
        if "retriever" not in st.session_state:
            embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=API_KEY)
            db = FAISS.load_local("adapta_chatbot/vectordb", embeddings, allow_dangerous_deserialization=True)
            retriever = db.as_retriever(search_kwargs={"k": 4})
            st.session_state.retriever = retriever

        # Cria cadeia de RAG
        if "qa_chain" not in st.session_state:
            llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                google_api_key=API_KEY,
                temperature=0.2,
            )
            st.session_state.qa_chain = RetrievalQA.from_chain_type(
                llm=llm,
                retriever=st.session_state.retriever,
                return_source_documents=False
            )

        # Cria modelo Gemini puro para fallback
        if "gemini_llm" not in st.session_state:
            st.session_state.gemini_llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                google_api_key=API_KEY,
                temperature=0.7,
            )

        # Mostra histórico
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(
                    f"<div class='chat-message chat-user'>{msg['content']}</div>",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"""
                    <div class='chat-message'>
                        <img src="data:image/png;base64,{mini_logo_b64}" class="chatbot-avatar">
                        <div class='chatbot-text'>{msg['content']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        # Entrada do usuário
        prompt = st.chat_input("Mensagem ao Chatbot:")
        if prompt:
            st.session_state.chat_history.append({"role": "user", "content": prompt})

            with st.spinner("Analisando..."):
                try:
                    resposta = st.session_state.qa_chain.run(prompt)
                    resposta_lower = resposta.strip().lower() if resposta else ""

                    padroes_fora_contexto = [
                        "não sei",
                        "não sei responder",
                        "não tenho essa informação",
                        "desculpe, não sei responder a isso.",
                        "não encontrei",
                        "não há informações",
                        "não há informação",
                        "não possuo informações",
                        "não possuo essa informação",
                        "não foi possível encontrar",
                        "não localizei",
                        "não existe informação",
                        "não há dados",
                        "não há registros",
                        "não há conhecimento",
                        "não há contexto",
                        "não há resposta",
                        "não tenho conhecimento",
                        "não tenho dados",
                        "não tenho registro",
                        "não tenho contexto",
                        "não tenho resposta",
                        "não foi encontrado",
                        "não foi localizada",
                        "não foi possível localizar",
                        "não foi possível responder",
                        "não há informações sobre",
                        "não há informações disponíveis",
                        "não há informações relevantes",
                        "não há informações neste contexto",
                        "não há informações para",
                        "não há informações no contexto",
                        "não há informações suficientes",
                        "não há informações específicas",
                        "não há informações detalhadas",
                        "não há informações relacionadas",
                        "não há informações pertinentes",
                        "não há informações encontradas",
                        "não há informações cadastradas",
                        "não há informações registradas",
                        "não há informações armazenadas",
                        "não há informações disponíveis no momento",
                        "não há informações disponíveis para",
                        "não há informações disponíveis sobre",
                        "não há informações disponíveis neste contexto",
                        "não há informações disponíveis no contexto",
                        "não há informações disponíveis suficientes",
                        "não há informações disponíveis específicas",
                        "não há informações disponíveis detalhadas",
                        "não há informações disponíveis relacionadas",
                        "não há informações disponíveis pertinentes",
                        "não há informações disponíveis encontradas",
                        "não há informações disponíveis cadastradas",
                        "não há informações disponíveis registradas",
                        "não há informações disponíveis armazenadas",
                        "não há informações disponíveis no momento para",
                        "não há informações disponíveis no momento sobre",
                        "não há informações disponíveis no momento neste contexto",
                        "não há informações disponíveis no momento no contexto",
                        "não há informações disponíveis no momento suficientes",
                        "não há informações disponíveis no momento específicas",
                        "não há informações disponíveis no momento detalhadas",
                        "não há informações disponíveis no momento relacionadas",
                        "não há informações disponíveis no momento pertinentes",
                        "não há informações disponíveis no momento encontradas",
                        "não há informações disponíveis no momento cadastradas",
                        "não há informações disponíveis no momento registradas",
                        "não há informações disponíveis no momento armazenadas",
                        "sinto muito",
                        "desculpe",
                    ]

                    # Detecta idioma do prompt
                    idioma = detectar_idioma(prompt)
                    if idioma == "es":
                        system_prompt = "Responde sempre em español, de forma clara e objetiva."
                    else:
                        system_prompt = "Responda sempre em português, de forma clara e objetiva."

                    # Se a resposta for vazia ou contiver qualquer padrão acima, usa fallback Gemini
                    if (
                        not resposta
                        or any(p in resposta_lower for p in padroes_fora_contexto)
                    ):
                        resposta = st.session_state.gemini_llm.invoke(
                            prompt,
                            system_instruction=system_prompt
                        )
                        if hasattr(resposta, "content"):
                            resposta = resposta.content

                    st.session_state.chat_history.append({"role": "model", "content": resposta})
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao gerar resposta: {e}")