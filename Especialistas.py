import streamlit as st
import requests
import base64

def get_base64_image(file_path):
    """Lê o arquivo de imagem e retorna seu conteúdo codificado em base64."""
    with open(file_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

def buscar_orcid(query, max_results=30):
    """
    Consulta a API pública da ORCID por pesquisadores utilizando o termo de especialidad.
    """
    base_url = "https://pub.orcid.org/v3.0/search/?q=" + query
    headers = {'Accept': 'application/json'}
    try:
        response = requests.get(base_url, headers=headers, timeout=15)
        response.raise_for_status()
    except requests.RequestException as e:
        st.error(f"[ERROR] Falló la solicitud: {e}")
        return []
    results = response.json().get('result', [])[:max_results]
    return results

def obter_detalhes_orcid(orcid_id: str) -> dict:
    """
    Obtiene datos adicionales del perfil ORCID para un especialista,
    incluyendo el nombre real, biografía e institución.
    """
    url = f"https://pub.orcid.org/v3.0/{orcid_id}/person"
    headers = {'Accept': 'application/json'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        summary = response.json() or {}
        
        # Extracción del nombre del especialista
        name_info = summary.get('name') or {}
        credit_name = name_info.get("credit-name") or {}
        if credit_name.get("value"):
            person_name = credit_name.get("value")
        else:
            given = (name_info.get("given-names") or {}).get("value", "")
            family = (name_info.get("family-name") or {}).get("value", "")
            person_name = f"{given} {family}".strip() if (given or family) else "Nombre no disponible"
        
        bio = (summary.get('biography') or {}).get('content', 'Bio no disponible.')
        affiliations = summary.get('employments', {}).get('employment-summary', [])
        institution = (
            affiliations[0].get('organization', {}).get('name')
            if affiliations and affiliations[0].get('organization', {}).get('name')
            else 'Institución no informada'
        )
        return {"name": person_name, "bio": bio, "institution": institution}
    except requests.RequestException:
        return {"name": "Nombre no disponible", "bio": "Bio no disponible.", "institution": "Institución no informada"}

def show_especialistas():
    # Encabezado con identidad visual usando la logo convertida a base64
    logo_base64 = get_base64_image("logo2.png")
    st.markdown(
        f"""
        <div style="text-align: center; margin-bottom: 30px;">
            <img src="data:image/png;base64,{logo_base64}" width="150">
            <h1 style="font-family: 'Roboto', sans-serif; color: #333;">Búsqueda de Expertos</h1>
            <p style="font-family: 'Roboto', sans-serif;">Conectando investigación y profesionales</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Campo de búsqueda: Especialidad
    especialidad = st.text_input("Especialidad", placeholder="Ingrese la especialidad...")
    
    if st.button("Buscar"):
        if not especialidad.strip():
            st.warning("Por favor, ingrese una especialidad.")
        else:
            st.info(f"Buscando especialistas con publicaciones relacionadas a: '{especialidad}' ...")
            resultados = buscar_orcid(especialidad)
            if not resultados:
                st.warning("No se encontraron especialistas.")
            else:
                st.success("Especialistas encontrados:")
                for idx, r in enumerate(resultados, start=1):
                    orcid_info = r.get('orcid-identifier', {})
                    orcid_id = orcid_info.get('path', 'N/A')
                    profile_url = f"https://orcid.org/{orcid_id}"
                    
                    # Obtener datos reales del especialista
                    detalles = obter_detalhes_orcid(orcid_id)
                    name = detalles.get("name", f"Especialista {idx}")
                    bio = detalles.get("bio")
                    institution = detalles.get("institution")
                    
                    with st.container():
                        col_img, col_info = st.columns([1, 4])
                        with col_img:
                            st.image("https://img.freepik.com/vetores-premium/auditoria-negocios-e-financas-minima-icon-logo_186868-31.jpg", width=80)
                        with col_info:
                            st.markdown(f"### {name}")
                            st.markdown(f"🔗 [Perfil ORCID]({profile_url})")
                            st.markdown(f"🏢 **Institución:** {institution}")
                            bio_text = bio if len(bio) <= 250 else bio[:250] + "..."
                            st.markdown(f"📝 {bio_text}")
                        st.markdown("---")
                        
    if st.button("Volver al menú"):
        st.session_state.page = "menu"
        if hasattr(st, "experimental_rerun"):
            st.experimental_rerun()
        else:
            st.stop()
