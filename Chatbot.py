# Chatbot.py  – Cabeçalho / configuração
import os
import base64
from pathlib import Path
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv                              # python‑dotenv

# ─────────── Chave de API ────────────────────────────────────────────────
load_dotenv()                                               # (.env local)

try:                                                        # deploy
    API_KEY = st.secrets["GOOGLE_API_KEY"]
except Exception:                                           # local
    API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error(
        "Chave da API do Gemini não encontrada.\n"
        "• No Streamlit Cloud: Settings ▸ Secrets ▸ GOOGLE_API_KEY\n"
        "• Localmente: crie .env ou export GOOGLE_API_KEY=…"
    )
    st.stop()

# Usa REST (mais tolerante a time‑outs que gRPC)
genai.configure(api_key=API_KEY, transport="rest")

# ─────────── Utilitários ────────────────────────────────────────────────
ASSETS_DIR = Path(__file__).parent
IMG_PATH    = ASSETS_DIR / "VerichIA.png"


def get_base64_image(file_path: Path | str) -> str:
    with open(file_path, "rb") as img:
        return base64.b64encode(img.read()).decode()


# ─────────── Função principal ───────────────────────────────────────────
def show_chatbot() -> None:
    mini_logo_b64 = get_base64_image(IMG_PATH)

    # Cabeçalho + container HTML/CSS (mesmo de antes)
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
            Asistente Virtual&nbsp;–&nbsp;AI
          </div>
          <div class="chatbot-content" id="chatbot-content">
            <div id="streamlit-chat-block"></div>
          </div>
        </div>

        <script>
          function toggleChatbot(){{
            const c = document.getElementById("chatbot-content");
            c.style.display = (c.style.display === "none" || c.style.display === "")
                              ? "block" : "none";
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

        # ───── Entrada do usuário: Enter envia automático ─────
        user_prompt = st.chat_input("Mensaje a VerichIA:")
        send_clicked = st.button("Generar respuesta", use_container_width=True)

        # Decide se enviou (Enter ou botão)
        if (user_prompt and user_prompt.strip()) or send_clicked:
            prompt_text = user_prompt if user_prompt else ""   # botão = usa último valor
            if not prompt_text.strip():
                st.warning("Escreva uma mensagem primeiro.")
                st.stop()

            # cria o modelo só uma vez
            if "gemini_flash" not in st.session_state:
                st.session_state.gemini_flash = genai.GenerativeModel(
                    "models/gemini-1.5-flash"
                )
            model = st.session_state.gemini_flash

            with st.spinner("VerichIA está pensando..."):
                try:
                    resposta = model.generate_content(
                        prompt_text,
                        request_options={"timeout": 120},
                    )
                    st.subheader("AI:")
                    st.write(resposta.text)
                except Exception as e:
                    st.error(
                        f"⚠️ Não consegui obter resposta do modelo (erro: {e}). "
                        "Tente novamente em alguns instantes."
                    )


# ─────────── Execução isolada para testes locais ───────────────────────
if __name__ == "__main__":
    st.set_page_config(page_title="Chatbot AI", layout="centered")
    show_chatbot()
