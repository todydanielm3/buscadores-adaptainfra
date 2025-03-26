
import streamlit as st
import requests

def invert_abstract(abstract_inverted_index):
    """Converte resumo (abstract) invertido em texto normal."""
    if not abstract_inverted_index:
        return "Resumo não disponível."
    word_positions = []
    for word, positions in abstract_inverted_index.items():
        for pos in positions:
            word_positions.append((pos, word))
    word_positions.sort(key=lambda x: x[0])
    return " ".join(wp[1] for wp in word_positions)

def search_openalex(query: str, max_results=5):
    """
    Faz busca na OpenAlex. Retorna lista de dicionários com metadados.
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
        st.error(f"[ERRO] Falha na requisição: {e}")
        return []

    data = response.json()
    results = data.get('results', [])
    return results

def show_inteligente():
    st.image("logo.png", width=550)
    st.title("Búsqueda inteligente")
    st.write("Introduzca un término de búsqueda")
    query = st.text_input("Término", value=" ")
    if st.button("Buscar"):
        if not query.strip():
            st.warning("Por favor, digite algo para pesquisar.")
        else:
            st.info(f"Pesquisando por: '{query}' ...")
            items = search_openalex(query, max_results=5)
            if not items:
                st.warning("Nenhum resultado encontrado.")
            else:
                for idx, item in enumerate(items, start=1):
                    title = item.get("title", "Sem Título")
                    pub_date = item.get("publication_date", "Data não disponível")
                    authors_data = item.get("authorships", [])
                    authors_list = []
                    for a in authors_data:
                        author_info = a.get("author", {})
                        author_name = author_info.get("display_name", "Autor Desconhecido")
                        authors_list.append(author_name)
                    authors_str = ", ".join(authors_list) if authors_list else "Nenhum autor"
                    link = item.get("doi") or "[Sem DOI]"
                    if link == "[Sem DOI]":
                        loc = item.get("primary_location", {})
                        link_alt = loc.get("landing_page_url")
                        if link_alt:
                            link = link_alt
                    abstract_inv = item.get("abstract_inverted_index", {})
                    abstract_text = invert_abstract(abstract_inv)
                    
                    st.subheader(f"Artigo {idx}: {title}")
                    st.write(f"**Data de Publicação:** {pub_date}")
                    st.write(f"**Autores:** {authors_str}")
                    st.write(f"**Resumo:** {abstract_text[:300]}{'...' if len(abstract_text) > 300 else ''}")
                    st.markdown(f"[Link do Artigo]({link})")
    if st.button("Voltar ao Menu"):
        st.session_state.page = "menu"
        if hasattr(st, "experimental_rerun"):
            st.experimental_rerun()
        else:
            st.stop()
