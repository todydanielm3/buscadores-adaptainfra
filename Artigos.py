import streamlit as st
import requests
import base64
import pandas as pd
import altair as alt
from collections import Counter

def get_base64_image(file_path):
    """Lê o arquivo de imagem e retorna seu conteúdo codificado em base64."""
    with open(file_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

def invert_abstract(abstract_inverted_index):
    """Converte el resumen invertido en texto normal."""
    if not abstract_inverted_index:
        return "Resumen no disponible."
    word_positions = []
    for word, positions in abstract_inverted_index.items():
        for pos in positions:
            word_positions.append((pos, word))
    word_positions.sort(key=lambda x: x[0])
    return " ".join(wp[1] for wp in word_positions)

def search_openalex(query: str, max_results=200):
    """
    Realiza una búsqueda en OpenAlex y retorna una lista de diccionarios con metadatos.
    """
    base_url = "https://api.openalex.org/works"
    params = {
        'search': query,
        'per-page': max_results,
        'sort': 'publication_date:desc'
    }
    try:
        response = requests.get(base_url, params=params, timeout=15)
        response.raise_for_status()
    except requests.RequestException as e:
        st.error(f"[ERROR] Falló la solicitud: {e}")
        return []
    data = response.json()
    results = data.get('results', [])
    return results

def parse_openalex_item(item):
    """
    Extrae información relevante de cada registro:
    - Año (publication_date -> extrae el año)
    - Tópicos (concepts: lista de 'display_name')
    - Instituciones (extraídas de los datos de 'authorships')
    - Tipo de obra (campo 'type')
    """
    pub_date = item.get("publication_date", "")
    year = pub_date.split("-")[0] if pub_date else "Desconocido"
    
    # Extraer tópicos
    concepts_info = item.get("concepts", [])
    topics = [c.get("display_name", "Desconocido") for c in concepts_info]
    
    # Extraer instituciones de los autores (evitar duplicados)
    institutions = set()
    for author in item.get("authorships", []):
        for inst in author.get("institutions", []):
            name = inst.get("display_name")
            if name:
                institutions.add(name)
    
    # Tipo de obra
    work_type = item.get("type", "Desconocido")
    
    return {
        "year": year,
        "topics": topics,
        "institutions": list(institutions),
        "type": work_type
    }

def show_artigos():
    # Cabeçalho e identidade visual
    logo_base64 = get_base64_image("logo2.png")
    st.markdown(
        f"""
        <div style="text-align: center; margin-bottom: 30px;">
            <img src="data:image/png;base64,{logo_base64}" width="150">
            <h1 style="font-family: 'Roboto', sans-serif; color: #333;">Búsqueda inteligente</h1>
            <p style="font-family: 'Roboto', sans-serif;">Conectando investigadores con publicaciones académicas</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Formulário de búsqueda
    with st.form(key="search_form_artigos", clear_on_submit=False):
        query = st.text_input("Término", value=" ")
        tema = st.selectbox("Tema", [
            "Sin", 
            "INFRAESTRUCTURA SOSTENIBLE, SOCIAL",
            "INFRAESTRUCTURA SOSTENIBLE, ECONÓMICO",
            "INFRAESTRUCTURA SOSTENIBLE, AMBIENTAL",
            "INFRAESTRUCTURA SOSTENIBLE, TÉCNICO",
            "INFRAESTRUCTURA SOSTENIBLE, POLÍTICO Y GUBERNAMENTAL",
            "INFRAESTRUCTURA SOSTENIBLE, REGIÓN AMAZÓNICA",
            "INFRAESTRUCTURA SOSTENIBLE, AUDITORÍA"
        ])
        col1, col2 = st.columns(2)
        buscar_pressed = col1.form_submit_button("Buscar")
        volver_pressed = col2.form_submit_button("Volver al menú")
    
    if volver_pressed:
        st.session_state.page = "menu"
        st.query_params.from_dict({"page": "menu"})
        st.stop()
    
    if buscar_pressed:
        if not query.strip():
            st.warning("Por favor, ingrese un término de búsqueda.")
        else:
            # Concatena el término con el tema si éste es distinto de "Sin"
            query_final = query.strip() + " " + tema if tema != "Sin" else query.strip()
            st.info(f"Buscando por: '{query_final}' ...")
            items = search_openalex(query_final, max_results=200)
            if not items:
                st.warning("No se encontraron resultados.")
            else:
                # Procesa los items para obtener datos adicionales útiles para las estadísticas
                parsed_data = [parse_openalex_item(item) for item in items]
                df = pd.DataFrame(parsed_data)
                
                # ----------------- ESTADÍSTICAS -----------------
                # Número total de resultados
                total_resultados = len(items)
                st.sidebar.metric("Total Resultados", total_resultados)
                
                # Distribución por año: agrupar y contar
                if "year" in df.columns:
                    df_year = df["year"].value_counts().reset_index()
                    df_year.columns = ["Año", "Frequencia"]
                    chart_year = alt.Chart(df_year).mark_bar().encode(
                        x=alt.X("Año:N", title="Año"),
                        y=alt.Y("Frequencia:Q", title="Frequencia")
                    ).properties(width=250, height=200)
                    st.sidebar.altair_chart(chart_year, use_container_width=True)
                
                # Tópicos
                all_topics = []
                for lst in df["topics"].dropna():
                    all_topics.extend(lst)
                topics_count = Counter(all_topics)
                if topics_count:
                    top_topics = topics_count.most_common(5)
                    df_topics = pd.DataFrame(top_topics, columns=["Tópico", "Frequencia"])
                    st.sidebar.subheader("Tópicos Principales")
                    st.sidebar.table(df_topics)
                
                # Instituições
                all_inst = []
                for lst in df["institutions"].dropna():
                    all_inst.extend(lst)
                inst_count = Counter(all_inst)
                if inst_count:
                    top_inst = inst_count.most_common(5)
                    df_inst = pd.DataFrame(top_inst, columns=["Institución", "Frequencia"])
                    st.sidebar.subheader("Instituciones")
                    st.sidebar.table(df_inst)
                
                # Tipo de obra
                if "type" in df.columns:
                    type_count = df["type"].value_counts().reset_index()
                    type_count.columns = ["Tipo", "Frequencia"]
                    st.sidebar.subheader("Tipo de Obra")
                    st.sidebar.table(type_count)
                # ---------------------------------------------------
                
                # Exibe os resultados principais na área central
                for idx, item in enumerate(items, start=1):
                    title = item.get("title", "Sin Título")
                    pub_date = item.get("publication_date", "Fecha no disponible")
                    authors_data = item.get("authorships", [])
                    authors_list = []
                    for a in authors_data:
                        author_info = a.get("author", {})
                        author_name = author_info.get("display_name", "Autor desconocido")
                        authors_list.append(author_name)
                    authors_str = ", ".join(authors_list) if authors_list else "Ningún autor"
                    
                    link = item.get("doi") or "[Sin DOI]"
                    if link == "[Sin DOI]":
                        loc = item.get("primary_location", {})
                        link_alt = loc.get("landing_page_url") if loc else None
                        if link_alt:
                            link = link_alt
                    
                    abstract_inv = item.get("abstract_inverted_index", {})
                    abstract_text = invert_abstract(abstract_inv)
                    
                    st.markdown(f"### Artículo {idx}: {title}")
                    st.write(f"**Fecha de Publicación:** {pub_date}")
                    st.write(f"**Autores:** {authors_str}")
                    st.write(f"**Tema:** {tema if tema != 'Sin' else 'Sin tema'}")
                    st.write(f"**Resumen:** {abstract_text[:300]}{'...' if len(abstract_text) > 300 else ''}")
                    st.markdown(f"[Enlace del Artículo]({link})")
                    st.markdown("---")
    
    # Exibe también el historial de búsqueda y feedback en la parte inferior de la página principal
    st.markdown("---")
    st.subheader("Histórico de Búsqueda")
    if "search_history_ex" in st.session_state:
        for i, h in enumerate(st.session_state.search_history_ex, start=1):
            st.write(f"{i}. {h}")
    
    with st.form(key="feedback_form_artigos"):
        feedback = st.text_area("Deja tu feedback sobre la búsqueda", placeholder="Escribe tus comentarios...")
        enviar_feedback = st.form_submit_button("Enviar Feedback")
        if enviar_feedback:
            # Se tiene una función add_feedback importada desde db.py para guardar el feedback
            from db import add_feedback
            add_feedback(feedback, context="Artigos")
            st.success("¡Gracias por tu feedback!")

def show_inteligente():
    # Para compatibilidad, redireciona para show_artigos (caso ambos sejam equivalentes)
    show_artigos()

if __name__ == "__main__":
    show
