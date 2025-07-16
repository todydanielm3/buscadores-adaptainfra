import os, base64, re
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv

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
    mini_logo_b64 = _img_b64(IMG_PATH)

    # HTML/CSS do chatbot flutuante (igual ao seu)
    st.markdown(
        """<style>
        .chatbot-container{position:fixed;bottom:20px;right:20px;width:350px;max-height:600px;
        border:1px solid #ccc;border-radius:10px;background:#fff;z-index:1000;
        box-shadow:0 4px 12px rgba(0,0,0,.15);font-family:'Segoe UI',sans-serif}
        .chat-message{background:#f1f1f1;margin-bottom:8px;padding:8px 10px;border-radius:8px;
        max-width:90%;display:flex;align-items:flex-start}
        .chat-user{background:#DCF8C6;margin-left:auto;text-align:right;justify-content:flex-end}
        .chatbot-avatar{width:24px;height:24px;margin-right:8px;border-radius:12px}
        .chatbot-text{flex:1}
        </style>""",
        unsafe_allow_html=True,
    )

    # ───── Session state ──────────────────────────────
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "retriever" not in st.session_state:
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=API_KEY,
            transport="rest",           # ← CORREÇÃO
        )
        db = FAISS.load_local(
            "adapta_chatbot/vectordb", embeddings, allow_dangerous_deserialization=True
        )
        st.session_state.retriever = db.as_retriever(search_kwargs={"k": 4})

    if "qa_chain" not in st.session_state:
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=API_KEY,
            temperature=0.2,
            transport="rest",           # ← CORREÇÃO
        )
        st.session_state.qa_chain = RetrievalQA.from_chain_type(
            llm=llm, retriever=st.session_state.retriever, return_source_documents=false
        )

    if "gemini_llm" not in st.session_state:
        st.session_state.gemini_llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=API_KEY,
            temperature=0.7,
            transport="rest",           # ← CORREÇÃO
        )

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
    prompt = st.chat_input("Mensagem ao Chatbot:")
    if not prompt:
        return

    st.session_state.chat_history.append({"role": "user", "content": prompt})

    with st.spinner("Analisando..."):
        try:
            resposta = st.session_state.qa_chain.run(prompt)
        except Exception as exc:
            st.error(f"Erro na cadeia RAG: {exc}")
            resposta = ""

        if not resposta or resposta.strip().lower().startswith(("não sei", "no sé")):
            idioma = _detectar_idioma(prompt)
            sys_prompt = ("Responde siempre en español, de forma clara y objetiva."
                          if idioma == "es"
                          else "Responda sempre em português, de forma clara e objetiva.")
            try:
                resp = st.session_state.gemini_llm.invoke(prompt, system_instruction=sys_prompt)
                resposta = getattr(resp, "content", str(resp))
            except Exception as exc:
                resposta = f"Desculpe, ocorreu um erro inesperado: {exc}"

    st.session_state.chat_history.append({"role": "model", "content": resposta})
    st.rerun()
