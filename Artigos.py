import streamlit as st
import requests
import base64

def get_base64_image(file_path):
    """Lê o arquivo de imagem e retorna seu conteúdo codificado em base64."""
    with open(file_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

def invert_abstract(abstract_inverted_index):
    """Converte resumen (abstract) invertido en texto normal."""
    if not abstract_inverted_index:
        return "Resumen no disponible."
    word_positions = []
    for word, positions in abstract_inverted_index.items():
        for pos in positions:
            word_positions.append((pos, word))
    word_positions.sort(key=lambda x: x[0])
    return " ".join(wp[1] for wp in word_positions)

def search_openalex(query: str, max_results=100):
    """
    Realiza la búsqueda en OpenAlex y retorna una lista de diccionarios con metadatos.
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

def show_inteligente():
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
    
    with st.form(key="search_form_artigos", clear_on_submit=False):
        query = st.text_input("Término", value=" ")
        tema = st.selectbox("Tema", [
            "Todo", 
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
    if buscar_pressed:
        if not query.strip():
            st.warning("Por favor, ingrese un término de búsqueda.")
        else:
            st.info(f"Buscando por: '{query}' y tema: '{tema}' ...")
            items = search_openalex(query, max_results=30)
            displayed_items = []
            simulated_themes = [
                "INFRAESTRUCTURA SOSTENIBLE, SOCIAL",
                "INFRAESTRUCTURA SOSTENIBLE, ECONÓMICO",
                "INFRAESTRUCTURA SOSTENIBLE, AMBIENTAL",
                "INFRAESTRUCTURA SOSTENIBLE, TÉCNICO",
                "INFRAESTRUCTURA SOSTENIBLE, POLÍTICO Y GUBERNAMENTAL",
                "INFRAESTRUCTURA SOSTENIBLE, REGIÓN AMAZÓNICA",
                "INFRAESTRUCTURA SOSTENIBLE, AUDITORÍA"
            ]
            for idx, item in enumerate(items, start=0):
                simulated_theme = simulated_themes[idx % len(simulated_themes)]
                if tema != "Todo" and tema not in simulated_theme:
                    continue
                item["simulated_theme"] = simulated_theme
                displayed_items.append(item)
            if not displayed_items:
                st.warning("No se encontraron resultados con los filtros aplicados.")
            else:
                for idx, item in enumerate(displayed_items, start=1):
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
                        link_alt = loc.get("landing_page_url")
                        if link_alt:
                            link = link_alt
                    
                    abstract_inv = item.get("abstract_inverted_index", {})
                    abstract_text = invert_abstract(abstract_inv)
                    
                    st.subheader(f"Artículo {idx}: {title}")
                    st.write(f"**Fecha de Publicación:** {pub_date}")
                    st.write(f"**Autores:** {authors_str}")
                    st.write(f"**Tema:** {item.get('simulated_theme')}")
                    st.write(f"**Resumen:** {abstract_text[:300]}{'...' if len(abstract_text) > 300 else ''}")
                    st.markdown(f"[Enlace del Artículo]({link})")
