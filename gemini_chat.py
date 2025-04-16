import streamlit as st
import google.generativeai as genai

# Configure aqui a sua chave de API do Google Generative AI
API_KEY = "AIzaSyCyafUCrwzxm8DCxn3XCmGULnynruRWL30"

# Inicializa o cliente com a API key
genai.configure(api_key=API_KEY)

def main():
    st.title("Chatbot Gemini - gemini-1.5-flash (Padrão)")

    st.write("Este exemplo usa o modelo 'gemini-1.5-flash' para gerar respostas.")

    # Campo de texto para o prompt
    prompt = st.text_area("Digite sua pergunta ou mensagem:")

    # Botão para gerar a resposta
    if st.button("Gerar Resposta"):
        # Usa sempre o modelo gemini-1.5-flash, sem opção de escolha
        model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

        # Chama o método de geração de conteúdo (texto)
        resposta = model.generate_content(prompt)

        st.subheader("Resposta do Modelo:")
        st.write(resposta.text)

if __name__ == "__main__":
    main()
