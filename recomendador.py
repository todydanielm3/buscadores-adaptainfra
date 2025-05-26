# recomendador.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np

# Função para clusterizar termos buscados
def gerar_clusters_termos(df_buscas: pd.DataFrame, n_clusters: int = 5):
    vectorizer = TfidfVectorizer(max_features=300)
    X = vectorizer.fit_transform(df_buscas["term"])
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    df_buscas["cluster"] = kmeans.fit_predict(X)
    return df_buscas, kmeans

# Função para retornar termos relacionados
def termos_relacionados(termo: str, df_buscas: pd.DataFrame, kmeans, top_n=5):
    vectorizer = TfidfVectorizer(max_features=300)
    vectorizer.fit(df_buscas["term"])
    termo_vec = vectorizer.transform([termo])
    cluster = kmeans.predict(termo_vec)[0]
    termos_cluster = df_buscas[df_buscas["cluster"] == cluster]["term"]
    mais_frequentes = termos_cluster.value_counts().head(top_n).index.tolist()
    return [t for t in mais_frequentes if t != termo]
