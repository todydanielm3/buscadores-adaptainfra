import streamlit as st
# A partir da versão 0.27 do 'openai', já é possível configurar
# base_url customizado para compatibilidade com outras LLMs.
from openai import OpenAI

# Ajuste para a sua própria chave de API da DeepSeek:
DEEPSEEK_API_KEY = "sk-4bd02ce0e38d444cb96ba0d30dcc039b"


def chamar_deepseek(mensagem: str) -> str:
    """
    Exemplo de função chamando a API DeepSeek via SDK OpenAI.
    """
    # Inicializa um cliente OpenAI “customizado” para DeepSeek
    client = OpenAI(
        api_key=DEEPSEEK_API_KEY,
        base_url="https://api.deepseek.com",  # Ou https://api.deepseek.com/v1
    )

    # Modelo "deepseek-chat" (DeepSeek-V3) ou "deepseek-reasoner" (DeepSeek-R1)
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": mensagem},
        ],
        stream=False  # se quiser streaming, defina True
    )

    # Retorna o texto gerado
    return response.choices[0].message.content


def main():
    st.title("Chatbot (DeepSeek) com Streamlit")

    # Inicializa o histórico de conversas na sessão
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    # Exibe as mensagens anteriores (histórico)
    for msg in st.session_state["messages"]:
        if msg["role"] == "user":
            st.markdown(f"**Você**: {msg['content']}")
        else:
            st.markdown(f"**Assistente**: {msg['content']}")

    # Campo de texto para o usuário digitar
    user_input = st.text_input("Digite sua pergunta e pressione Enter:", key="user_input")
    if user_input:
        # Registra a pergunta do usuário
        st.session_state["messages"].append({"role": "user", "content": user_input})

        # Faz a chamada à DeepSeek
        resposta = chamar_deepseek(user_input)

        # Registra a resposta da IA no histórico
        st.session_state["messages"].append({"role": "assistant", "content": resposta})

        # Limpa o campo de input e recarrega a interface
        st.experimental_rerun()


if __name__ == "__main__":
    main()
