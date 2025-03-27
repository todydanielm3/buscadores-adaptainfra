
import streamlit as st
import openai

# Configure sua chave de API da OpenAI (idealmente, armazene essa chave em uma variável de ambiente)
openai.api_key = "SUA_CHAVE_API_AQUI"

def generate_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # ou gpt-4 se disponível
            messages=[
                {"role": "system", "content": "Você é um assistente útil e prestativo."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7,
        )
        message = response.choices[0].message["content"]
        return message
    except Exception as e:
        return f"Erro: {e}"

def show_chat():
    st.image("logo.png", width=250)
    st.title("Chat GPT Personalizado")
    st.write("Converse com o assistente personalizado!")
    
    # Inicia o histórico de conversas no session_state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Exibe a conversa
    for entry in st.session_state.chat_history:
        if entry["role"] == "Usuário":
            st.markdown(f"**Você:** {entry['content']}")
        else:
            st.markdown(f"**ChatGPT:** {entry['content']}")
    
    # Campo de entrada para o usuário
    user_input = st.text_input("Digite sua mensagem", key="chat_input")
    
    if st.button("Enviar"):
        if user_input:
            # Adiciona a mensagem do usuário ao histórico
            st.session_state.chat_history.append({"role": "Usuário", "content": user_input})
            # Gera a resposta do ChatGPT
            resposta = generate_response(user_input)
            st.session_state.chat_history.append({"role": "ChatGPT", "content": resposta})
            # Limpa o campo de entrada e atualiza a página
            st.experimental_rerun()

if __name__ == "__main__":
    show_chat()
