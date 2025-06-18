# adapta_chatbot/criar_base.py
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import FAISS
import os

# Caminho da pasta com arquivos .md
DOCS_DIR = "./docs/"

# Coleta todos os arquivos Markdown
def carregar_documentos_md():
    docs = []
    for nome_arquivo in os.listdir(DOCS_DIR):
        if nome_arquivo.endswith(".md"):
            caminho = os.path.join(DOCS_DIR, nome_arquivo)
            loader = UnstructuredMarkdownLoader(caminho)
            docs.extend(loader.load())
    return docs

def main():
    print("⏳ Carregando arquivos Markdown...")
    documentos = carregar_documentos_md()

    print("✂️ Separando em blocos...")
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    blocos = splitter.split_documents(documentos)

    print("🧠 Gerando embeddings...")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    print("💾 Salvando em FAISS...")
    faiss_index = FAISS.from_documents(blocos, embeddings)
    faiss_index.save_local("./vectordb/")

    print("✅ Base vetorial criada com sucesso!")

if __name__ == "__main__":
    main()
