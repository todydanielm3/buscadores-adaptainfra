import os
import base64
from pathlib import Path
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# ─────────── Chave da API ─────────────────────────────────────
load_dotenv()
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
except Exception:
    API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error("Chave da API do Gemini não encontrada.")
    st.stop()

genai.configure(api_key=API_KEY, transport="rest")

ASSETS_DIR = Path(__file__).parent
IMG_PATH = ASSETS_DIR / "VerichIA.png"

def get_base64_image(file_path: Path | str) -> str:
    with open(file_path, "rb") as img:
        return base64.b64encode(img.read()).decode()

def show_chatbot() -> None:
    mini_logo_b64 = get_base64_image(IMG_PATH)

    # HTML/CSS do chat flutuante
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
        .chatbot-header img {{
            height: 24px;
            margin-right: 10px;
        }}
        .chatbot-body {{
            display: none;
            padding: 10px;
            overflow-y: auto;
            max-height: 400px;
        }}
        .chat-message {{
            background: #f1f1f1;
            margin-bottom: 8px;
            padding: 8px 10px;
            border-radius: 8px;
            max-width: 90%;
        }}
        .chat-user {{
            background: #DCF8C6;
            margin-left: auto;
            text-align: right;
        }}
        </style>
        <div class="chatbot-container">
            <div class="chatbot-header" onclick="toggleChatbot()">
                <img src="data:image/png;base64,{mini_logo_b64}" alt="logo">
                <span>Asistente</span>
            </div>
            <div class="chatbot-body" id="chat-body">
                <div id="chat-block"></div>
            </div>
        </div>
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

    # Área funcional invisível do Streamlit
    with st.container():
        if "gemini_flash" not in st.session_state:
            st.session_state.gemini_flash = genai.GenerativeModel("models/gemini-1.5-flash")
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        for i, msg in enumerate(st.session_state.chat_history):
            is_user = msg["role"] == "user"
            css_class = "chat-user" if is_user else ""
            st.markdown(
                f"<div class='chat-message {css_class}'>{msg['parts'][0]}</div>",
                unsafe_allow_html=True
            )

        prompt = st.chat_input("Mensaje al asistente:")
        if prompt:
            st.session_state.chat_history.append({"role": "user", "parts": [prompt]})

            with st.spinner("Pensando..."):
                try:
                    response = st.session_state.gemini_flash.generate_content(
                        st.session_state.chat_history,
                        request_options={"timeout": 60}
                    )
                    reply = response.text.strip()
                    st.session_state.chat_history.append({"role": "model", "parts": [reply]})
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao obter resposta: {e}")
