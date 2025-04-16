import streamlit as st
import requests
import base64

def get_base64_image(file_path):
    """Lê o arquivo de imagem e retorna seu conteúdo codificado em base64."""
    with open(file_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

def search_ora(query: str, max_results=100):
    """
    Realiza la búsqueda en el repositorio ORA y retorna una lista de documentos.
    
    Parámetros:
      - query: Término de búsqueda.
      - max_results: Número máximo de resultados a retornar.
      
    Retorna:
      Una lista de diccionarios con los datos del documento (title, creator, date, download, etc.).
    """
    base_url = "https://apps.oraotca.org/api/v1/list_documents"
    params = {
        "filter": query,
        "size": max_results,
        "start": 0
    }
    try:
        response = requests.get(base_url, params=params, timeout=15)
        response.raise_for_status()
    except requests.RequestException as e:
        st.error(f"[ERROR] Falló la solicitud: {e}")
        return []
    data = response.json()
    results = data.get("data", [])
    return results

def show_ora_documents():
    # Cabeçalho com identidade visual
    logo_base64 = get_base64_image("logo2.png")
    st.markdown(
        f"""
        <div style="text-align: center; margin-bottom: 30px;">
            <img src="data:image/png;base64,{logo_base64}" width="150">
            <h1 style="font-family: 'Roboto', sans-serif; color: #333;">Búsqueda ORA</h1>
            <p style="font-family: 'Roboto', sans-serif;">Documentos del repositorio ORA</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Formulário para pesquisa – permite enviar com Enter
    with st.form(key="ora_form", clear_on_submit=False):
        query = st.text_input("Término", value="", placeholder="Ingrese el término de búsqueda")
        buscar_pressed = st.form_submit_button("Buscar")
    
    if buscar_pressed:
        if not query.strip():
            st.warning("Por favor, ingrese un término de búsqueda.")
        else:
            st.info(f"Buscando documentos ORA por: '{query}' ...")
            docs = search_ora(query, max_results=100)
            if not docs:
                st.warning("No se encontraron documentos.")
            else:
                for idx, doc in enumerate(docs, start=1):
                    title = doc.get("title", "Sin Título")
                    creator = doc.get("creator", "Sin Creador")
                    date = doc.get("date", "Fecha no disponible")
                    download = doc.get("download", None)
                    
                    st.subheader(f"Documento {idx}: {title}")
                    st.write(f"**Creador:** {creator}")
                    st.write(f"**Fecha:** {date}")
                    if download:
                        st.markdown(f"[Descargar documento]({download})")
                    else:
                        st.write("No disponible para descarga")
                    st.markdown("---")

if __name__ == "__main__":
    show_ora_documents()
