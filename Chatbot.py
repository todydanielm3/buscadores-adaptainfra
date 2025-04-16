import os
from dotenv import load_dotenv  # Certifique-se de ter o python-dotenv instalado.
import streamlit as st
import google.generativeai as genai
import base64

# Carrega as variáveis definidas no arquivo .env
load_dotenv()

# Obtém a chave da API a partir da variável de ambiente
API_KEY = os.environ.get("GOOGLE_API_KEY")
if not API_KEY:
    st.error("Chave da API não encontrada. Configure a variável de ambiente GOOGLE_API_KEY.")
    # Você pode encerrar a execução ou implementar outro tratamento
else:
    # Configura a biblioteca com a chave obtida
    genai.configure(api_key=API_KEY)

# Resto do código (como definição das funções get_base64_image, show_chatbot, etc.)

def get_base64_image(file_path):
    """Lê o arquivo de imagem e retorna seu conteúdo codificado em base64."""
    with open(file_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

def show_chatbot():
    # Lê a imagem para logo e converte para base64
    mini_logo_base64 = get_base64_image("VerichIA.png")

    # Cria um elemento HTML customizado para o chatbot (header com logo, etc.)
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
            background: linear-gradient(135deg, #008000, #800080, #0000FF, #FF0000);
            color: white;
            font-family: 'Roboto', sans-serif;
            border-radius: 5px 5px 0 0;
          }}
          .chatbot-header img {{
            height: 30px;
            margin-right: 8px;
          }}
          .chatbot-content {{
            display: none;
            padding: 10px;
          }}
        </style>
        <div class="chatbot-container">
          <div class="chatbot-header" onclick="toggleChatbot()">
            <img src="data:image/png;base64,{mini_logo_base64}" alt="Logo VerichIA">
            Assistente Virtual - VerichIA
          </div>
          <div class="chatbot-content" id="chatbot-content">
            <!-- Espaço reservado para o chat via st.empty() -->
            <div id="streamlit-chat-block"></div>
          </div>
        </div>
        <script>
          function toggleChatbot() {{
            var c = document.getElementById("chatbot-content");
            if (c.style.display === "none" || c.style.display === "") {{
                c.style.display = "block";
            }} else {{
                c.style.display = "none";
            }}
          }}
        </script>
        """,
        unsafe_allow_html=True
    )

    # Cria um container para inserir a lógica do chatbot
    container = st.empty()
    with container.container():
        st.markdown(
            "<div style='text-align: center; margin-bottom: 10px;'>"
            "<img src='data:image/png;base64,{0}' alt='Logo Grande' style='height:150px;'>"
            "</div>".format(mini_logo_base64),
            unsafe_allow_html=True
        )
        
        prompt = st.text_area("Mensagem para VerichIA:")
        if st.button("Gerar resposta"):
            model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
            resposta = model.generate_content(prompt)
            st.subheader("VerichIA:")
            st.write(resposta.text)

if __name__ == "__main__":
    show_chatbot()
