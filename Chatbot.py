import os
import base64
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
ASSETS_DIR = Path(__file__).parent
IMG_PATH = ASSETS_DIR / "VerichIA.png"

def get_base64_image(file_path: Path | str) -> str:
    with open(file_path, "rb") as img:
        return base64.b64encode(img.read()).decode()

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
                    st.session_state.chat_history.append({"role": "model", "content": resposta})
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao gerar resposta: {e}")
