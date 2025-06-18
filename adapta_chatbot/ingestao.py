# adapta_chatbot/ingestao.py
import os
from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader, TextLoader

docs_path = Path(__file__).parent / "docs"
vector_path = Path(__file__).parent / "vectordb"
vector_path.mkdir(exist_ok=True)

# Carrega todos os arquivos de texto e PDF
loaders = []
for file in docs_path.iterdir():
    if file.suffix == ".pdf":
        loaders.append(PyPDFLoader(str(file)))
    elif file.suffix in [".txt", ".md"]:
        loaders.append(TextLoader(str(file)))

# Lê e divide os documentos
docs = []
for loader in loaders:
    docs.extend(loader.load())

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
chunks = splitter.split_documents(docs)

# Embeddings com Gemini
embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
db = FAISS.from_documents(chunks, embedding)
db.save_local(str(vector_path))
print("✅ Vetores salvos com sucesso.")
