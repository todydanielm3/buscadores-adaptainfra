import streamlit as st
import requests
import base64

def get_base64_image(file_path):
    with open(file_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

def invert_abstract(abstract_inverted_index):
    if not abstract_inverted_index:
        return "Resumen no disponible."
    word_positions = []
    for word, positions in abstract_inverted_index.items():
        for pos in positions:
            word_positions.append((pos, word))
    word_positions.sort(key=lambda x: x[0])
    return " ".join(wp[1] for wp in word_positions)

def search_openalex(query: str, max_results=100):
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

# Mapeamento de temas do espanhol para o português
theme_translation = {
    'INFRAESTRUCTURA SOSTENIBLE, SOCIAL': 'infraestrutura sustentável, social',
    'INFRAESTRUCTURA SOSTENIBLE, ECONÓMICO': 'infraestrutura sustentável, econômico',
    'INFRAESTRUCTURA SOSTENIBLE, AMBIENTAL': 'infraestrutura sustentável, ambiental',
    'INFRAESTRUCTURA SOSTENIBLE, TÉCNICO': 'infraestrutura sustentável, técnico',
    'INFRAESTRUCTURA SOSTENIBLE, POLÍTICO Y GUBERNAMENTAL': 'infraestrutura sustentável, político e governamental',
    'INFRAESTRUCTURA SOSTENIBLE, REGIÓN AMAZÓNICA': 'infraestrutura sustentável, região amazônica',
    'INFRAESTRUCTURA SOSTENIBLE, AUDITORÍA': 'infraestrutura sustentável, auditoria'
}

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
        st.experimental_rerun()
    
    if buscar_pressed:
        if not query.strip():
            st.warning("Por favor, ingrese un término de búsqueda.")
        else:
            # Concatena o termo com o tema traduzido, se for diferente de "Sin"
            if tema != "Sin":
                tema_pt = theme_translation.get(tema, tema)
                query_final = query.strip() + " " + tema_pt
            else:
                query_final = query.strip()
            st.info(f"Buscando por: '{query_final}' ...")
            items = search_openalex(query_final, max_results=30)
            if not items:
                st.warning("No se encontraron resultados.")
            else:
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
                    
                    st.subheader(f"Artículo {idx}: {title}")
                    st.write(f"**Fecha de Publicación:** {pub_date}")
                    st.write(f"**Autores:** {authors_str}")
                    st.write(f"**Tema:** {tema if tema != 'Sin' else 'Sin tema'}")
                    st.write(f"**Resumen:** {abstract_text[:300]}{'...' if len(abstract_text) > 300 else ''}")
                    st.markdown(f"[Enlace del Artículo]({link})")
