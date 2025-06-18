# adapta_chatbot/busca_semantica.py
from langchain.vectorstores import FAISS
from langchain.embeddings import GoogleGenerativeAIEmbeddings
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatGoogleGenerativeAI
import os

vector_path = "./adapta_chatbot/vectordb"
embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
db = FAISS.load_local(vector_path, embedding)

def responder_pergunta(pergunta: str) -> str:
    documentos = db.similarity_search(pergunta, k=4)
    model = ChatGoogleGenerativeAI(model="models/gemini-1.5-flash")
    chain = load_qa_chain(model, chain_type="stuff")
    resposta = chain.run(input_documents=documentos, question=pergunta)
    return resposta
