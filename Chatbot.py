import os
import base64
from pathlib import Path

from dotenv import load_dotenv          # pip install python-dotenv
import streamlit as st
from streamlit.errors import StreamlitSecretNotFoundError
import google.generativeai as genai

# ───── 1)  Carrega variáveis do .env (útil em desenvolvimento local) ─────
load_dotenv()

# ───── 2)  Lê a chave primeiro em st.secrets, depois nas variáveis de ambiente ──
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]          # só existe no deploy
except (StreamlitSecretNotFoundError, KeyError):
    API_KEY = os.getenv("GOOGLE_API_KEY")           # fallback local
    # ➜ se também não existir, API_KEY será None

if not API_KEY:
    st.error(
        "Chave da API do Gemini não encontrada. "
        "• Localmente: coloque GOOGLE_API_KEY no seu .env\n"
        "• No Streamlit Cloud: adicione em Settings ▸ Secrets"
    )
    st.stop()

genai.configure(api_key=API_KEY, transport="rest")  # REST evita timeouts gRPC

# ───── resto do Chatbot.py permanece igual ─────

# ─────────────────────── Utilitários ────────────────────────
ASSETS_DIR = Path(__file__).parent
IMG_PATH = ASSETS_DIR / "VerichIA.png"


def get_base64_image(file_path: Path | str) -> str:
    """Codifica uma imagem em base64 para embutir no HTML."""
    with open(file_path, "rb") as img:
        return base64.b64encode(img.read()).decode()


# ───────────────────── Função principal ─────────────────────
def show_chatbot() -> None:
    mini_logo_b64 = get_base64_image(IMG_PATH)

    # Cabeçalho + container HTML/CSS
    st.markdown(
        f"""
        <style>
          .chatbot-container {{
            position: relative;
            margin-bottom: 20px;
            border: 1px solid #ddd;
            border-radius: 5px;
            background: #f9f9f9;
          }}
          .chatbot-header {{
            cursor: pointer;
            display: flex;
            align-items: center;
            padding: 10px;
            background: linear-gradient(135deg,#008000,#800080,#0000FF,#FF0000);
            color: white;
            font-family: 'Roboto', sans-serif;
            border-radius: 5px 5px 0 0;
          }}
          .chatbot-header img {{ height: 30px; margin-right: 8px; }}
          .chatbot-content {{ display: none; padding: 10px; }}
        </style>

        <div class="chatbot-container">
          <div class="chatbot-header" onclick="toggleChatbot()">
            <img src="data:image/png;base64,{mini_logo_b64}" alt="Logo VerichIA">
            Assistente Virtual&nbsp;–&nbsp;VerichIA
          </div>
          <div class="chatbot-content" id="chatbot-content">
            <div id="streamlit-chat-block"></div>
          </div>
        </div>

        <script>
          function toggleChatbot(){{
            const c = document.getElementById("chatbot-content");
            c.style.display = (c.style.display === "none" || c.style.display === "") ? "block" : "none";
          }}
        </script>
        """,
        unsafe_allow_html=True,
    )

    # Área do chat
    container = st.empty()
    with container.container():
        st.markdown(
            f"<div style='text-align:center;margin-bottom:10px;'>"
            f"<img src='data:image/png;base64,{mini_logo_b64}' alt='Logo Grande' style='height:150px;'>"
            f"</div>",
            unsafe_allow_html=True,
        )

        prompt = st.text_area("Mensagem para VerichIA:")
        if st.button("Gerar resposta", use_container_width=True):

            # cria o modelo só uma vez
            if "gemini_flash" not in st.session_state:
                st.session_state.gemini_flash = genai.GenerativeModel(
                    "models/gemini-1.5-flash"
                )
            model = st.session_state.gemini_flash

            with st.spinner("VerichIA está pensando..."):
                try:
                    resposta = model.generate_content(
                        prompt,
                        request_options={"timeout": 120},
                    )
                    st.subheader("VerichIA:")
                    st.write(resposta.text)
                except Exception as e:
                    st.error(
                        f"⚠️ Não consegui obter resposta do modelo (erro: {e}). "
                        "Tente novamente em alguns instantes."
                    )


# Executa localmente para teste isolado
if __name__ == "__main__":
    st.set_page_config(page_title="Chatbot VerichIA", layout="centered")
    show_chatbot()
