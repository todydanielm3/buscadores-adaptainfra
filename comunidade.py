
import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Definir diretórios e arquivo de banco de dados
UPLOAD_DIR = "uploads"
DB_FILE = "comunidade_db.csv"

# Cria a pasta de uploads, se não existir
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

def save_upload(name, tema, uploaded_file):
    """Salva o arquivo enviado e retorna o nome do arquivo único."""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{timestamp}_{uploaded_file.name}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return filename

def add_entry_to_db(name, tema, filename):
    """Adiciona uma nova entrada no banco de dados (arquivo CSV)."""
    entry = {
        "nome": name,
        "tema": tema,
        "arquivo": filename,
        "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    if os.path.exists(DB_FILE):
        df = pd.read_csv(DB_FILE)
        df = df.append(entry, ignore_index=True)
    else:
        df = pd.DataFrame([entry])
    df.to_csv(DB_FILE, index=False)

def show_comunidade():
    st.image("logo.png", width=250)
    st.title("Comunidade +")
    st.write("Envie seu PDF e contribua para a comunidade!")
    
    with st.form("form_upload"):
        name = st.text_input("Nome completo do colaborador")
        tema = st.text_input("Tema")
        uploaded_file = st.file_uploader("Selecione um arquivo PDF", type=["pdf"])
        submitted = st.form_submit_button("Enviar")
        if submitted:
            if not name or not tema or uploaded_file is None:
                st.warning("Por favor, preencha todos os campos e envie um arquivo PDF.")
            else:
                filename = save_upload(name, tema, uploaded_file)
                add_entry_to_db(name, tema, filename)
                st.success("Seu envio foi registrado com sucesso!")
    
    st.write("---")
    st.header("Contribuições da Comunidade")
    if os.path.exists(DB_FILE):
        df = pd.read_csv(DB_FILE)
        if df.empty:
            st.info("Nenhuma contribuição registrada ainda.")
        else:
            # Exibe cada contribuição com um botão para download do PDF
            for _, row in df.iterrows():
                st.subheader(f"{row['nome']} - {row['tema']}")
                st.write(f"Enviado em: {row['data']}")
                file_path = os.path.join(UPLOAD_DIR, row['arquivo'])
                if os.path.exists(file_path):
                    with open(file_path, "rb") as pdf_file:
                        st.download_button(
                            label="Baixar PDF",
                            data=pdf_file,
                            file_name=row['arquivo'],
                            mime="application/pdf"
                        )
                st.markdown("---")
    else:
        st.info("Nenhuma contribuição registrada ainda.")
    if st.button("Voltar ao Menu"):
        st.session_state.page = "menu"

    

if __name__ == "__main__":
    show_comunidade()
