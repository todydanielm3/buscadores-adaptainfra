import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import Base, SearchHistory  # Certifique-se de que db.py define a classe SearchHistory e Base.
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import pickle
import datetime

def load_data():
    """
    Conecta ao banco de dados SQLite (buscadores.db) e extrai os termos do histórico de buscas.
    Retorna um DataFrame com as colunas 'term' e 'timestamp'.
    """
    # Cria a conexão com o banco de dados
    engine = create_engine("sqlite:///buscadores.db")
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Consulta todos os registros da tabela SearchHistory
    results = session.query(SearchHistory).all()
    session.close()
    
    # Monta uma lista de dicionários com os dados
    data = [{
        "term": entry.term,
        "timestamp": entry.timestamp if entry.timestamp else datetime.datetime.utcnow()
    } for entry in results]
    
    df = pd.DataFrame(data)
    return df

def train_model(df, n_clusters=5):
    """
    Pré-processa o texto, vetoriza os termos usando TF-IDF e treina um modelo KMeans
    para agrupar as buscas em n_clusters. Exibe as principais palavras de cada cluster e
    retorna o modelo treinado, o vectorizer e o DataFrame com os clusters atribuídos.
    """
    # Verifica se há dados
    if df.empty:
        print("Nenhum histórico de busca encontrado!")
        return None, None, df

    # Pré-processamento: converte os termos para minúsculo
    df["term_clean"] = df["term"].str.lower()

    # Vetorização usando TF-IDF (com remoção de stopwords em inglês – pode ser customizado)
    vectorizer = TfidfVectorizer(stop_words="english")
    X = vectorizer.fit_transform(df["term_clean"])

    # Treina o modelo de clusterização KMeans
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(X)

    # Atribui os rótulos de cluster a cada termo
    df["cluster"] = kmeans.labels_

    # Exibe as 10 palavras mais relevantes de cada cluster
    print("Principais palavras por cluster:")
    order_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names_out()
    for i in range(n_clusters):
        top_words = [terms[ind] for ind in order_centroids[i, :10]]
        print(f"Cluster {i}: " + ", ".join(top_words))

    return kmeans, vectorizer, df

def save_model(model, vectorizer, model_file="kmeans_model.pkl", vectorizer_file="tfidf_vectorizer.pkl"):
    """
    Salva o modelo treinado e o TF-IDF vectorizer em arquivos pickle.
    """
    with open(model_file, "wb") as f:
        pickle.dump(model, f)
    with open(vectorizer_file, "wb") as f:
        pickle.dump(vectorizer, f)
    print("Modelo e vectorizer salvos com sucesso!")

def main():
    # Carrega os dados do histórico de buscas
    df = load_data()
    if df.empty:
        print("Não há histórico de buscas para treinar o modelo.")
        return

    # Treina o modelo definindo um número de clusters (ex.: 5)
    n_clusters = 5
    model, vectorizer, df = train_model(df, n_clusters=n_clusters)
    if model is not None and vectorizer is not None:
        # Salva o modelo e o vectorizer para uso posterior
        save_model(model, vectorizer)
        # Exibe as atribuições de clusters para cada termo
        print("\nAtribuição de clusters para cada termo:")
        print(df[["term", "cluster"]])
    else:
        print("Falha no treinamento do modelo.")

if __name__ == "__main__":
    main()
