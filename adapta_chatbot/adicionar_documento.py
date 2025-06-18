import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import (
    UnstructuredPDFLoader,
    UnstructuredMarkdownLoader,
    UnstructuredWordDocumentLoader,
    TextLoader,
)

# ────────────── CONFIGURAÇÕES ──────────────
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise ValueError("❌ API KEY do Google Gemini não encontrada.")

EMBEDDINGS = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=API_KEY)

VDB_PATH = "adapta_chatbot/vectordb"
EXT_TO_LOADER = {
    ".md": UnstructuredMarkdownLoader,
    ".pdf": UnstructuredPDFLoader,
    ".docx": UnstructuredWordDocumentLoader,
    ".txt": TextLoader,
}

# ────────────── FUNÇÃO PRINCIPAL ──────────────
def adicionar_arquivo(caminho_arquivo: str):
    caminho = Path(caminho_arquivo)
    if not caminho.exists():
        print(f"❌ Arquivo '{caminho}' não encontrado.")
        return

    ext = caminho.suffix.lower()
    if ext not in EXT_TO_LOADER:
        print(f"❌ Extensão '{ext}' não suportada.")
        return

    print(f"📄 Carregando arquivo '{caminho.name}'...")
    loader_cls = EXT_TO_LOADER[ext]
    loader = loader_cls(str(caminho))
    novo_documento = loader.load()

    print("🔎 Carregando base existente...")
    db = FAISS.load_local(VDB_PATH, EMBEDDINGS, allow_dangerous_deserialization=True)

    print("➕ Adicionando novo conteúdo à base...")
    novo_db = FAISS.from_documents(novo_documento, EMBEDDINGS)
    db.merge_from(novo_db)

    print("💾 Salvando base atualizada...")
    db.save_local(VDB_PATH)

    print(f"✅ Documento '{caminho.name}' adicionado com sucesso à base vetorial.")

# ────────────── EXECUÇÃO VIA TERMINAL ──────────────
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Uso: python3 adicionar_documento.py caminho/para/arquivo.md")
    else:
        adicionar_arquivo(sys.argv[1])
