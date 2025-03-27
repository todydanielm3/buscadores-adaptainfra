import streamlit as st
import requests
import base64

def get_base64_image(file_path):
    """Lê o arquivo de imagem e retorna seu conteúdo codificado em base64."""
    with open(file_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

def buscar_orcid(query, max_results=100):
    """
    Consulta a API pública da ORCID por pesquisadores.
    """
    base_url = "https://pub.orcid.org/v3.0/search/?q=" + query
    headers = {'Accept': 'application/json'}
    try:
        response = requests.get(base_url, headers=headers, timeout=15)
        response.raise_for_status()
    except requests.RequestException as e:
        st.error(f"[ERRO] Falha na requisição: {e}")
        return []
    results = response.json().get('result', [])[:max_results]
    return results

def obter_detalhes_orcid(orcid_id: str) -> dict:
    """
    Busca dados adicionais do perfil ORCID para um especialista,
    incluindo o nome real, biografia e instituição.
    """
    url = f"https://pub.orcid.org/v3.0/{orcid_id}/person"
    headers = {'Accept': 'application/json'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        summary = response.json() or {}
        
        # Extração do nome do especialista
        name_info = summary.get('name') or {}
        credit_name = name_info.get("credit-name") or {}  # fallback se None
        if credit_name.get("value"):
            person_name = credit_name.get("value")
        else:
            given = (name_info.get("given-names") or {}).get("value", "")
            family = (name_info.get("family-name") or {}).get("value", "")
            person_name = f"{given} {family}".strip() if (given or family) else "Nome não disponível"
        
        bio = (summary.get('biography') or {}).get('content', 'Bio não disponível.')
        affiliations = summary.get('employments', {}).get('employment-summary', [])
        institution = (
            affiliations[0].get('organization', {}).get('name')
            if affiliations and affiliations[0].get('organization', {}).get('name')
            else 'Instituição não informada'
        )
        return {"name": person_name, "bio": bio, "institution": institution}
    except requests.RequestException:
        return {"name": "Nome não disponível", "bio": "Bio não disponível.", "institution": "Instituição não informada"}

def filtrar_dados_simulados(idx: int, filtro_area: str) -> dict:
    """
    Simula dados para o filtro de área de forma cíclica.
    """
    areas = [
        "AUDITORIA", "AMBIENTAL", "ECONÔMICO", 
        "SOCIAL", "TÉCNICO", "POLÍTICO E GOVERNAMENTAL", "REGIÃO AMAZÔNICA"
    ]
    area_simulada = areas[idx % len(areas)]
    if filtro_area != "Todas" and filtro_area != area_simulada:
        return {}
    return {"area": area_simulada}

def show_especialistas():
    # Cabeçalho com identidade visual usando a logo convertida em base64
    logo_base64 = get_base64_image("logo2.png")
    st.markdown(
        f"""
        <div style="text-align: center; margin-bottom: 30px;">
            <img src="data:image/png;base64,{logo_base64}" width="150">
            <h1 style="font-family: 'Roboto', sans-serif; color: #333;">Repositório de Expertos</h1>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Campo de busca: Especialidade
    especialidade = st.text_input("Especialidad")
    
    # Filtro: Área
    filtro_area = st.selectbox("Área", [
        "Todos", "AUDITORÍA", "AMBIENTAL", "ECONÓMICO",
"SOCIAL", "TÉCNICO", "POLÍTICO Y GUBERNAMENTAL", "AMAZÓNICO"
    ])
    
    if st.button("Buscar"):
        if not especialidade.strip():
            st.warning("Digite uma especialidade.")
        else:
            st.info(f"Buscando por especialistas em: '{especialidade}' ...")
            resultados = buscar_orcid(especialidade)
            if not resultados:
                st.warning("Nenhum especialista encontrado.")
            else:
                st.success("Especialistas encontrados:")
                for idx, r in enumerate(resultados, start=1):
                    orcid_info = r.get('orcid-identifier', {})
                    orcid_id = orcid_info.get('path', 'N/A')
                    profile_url = f"https://orcid.org/{orcid_id}"
                    
                    # Obter dados reais do especialista
                    detalhes = obter_detalhes_orcid(orcid_id)
                    name = detalhes.get("name", f"Especialista {idx}")
                    bio = detalhes.get("bio")
                    institution = detalhes.get("institution")
                    
                    # Aplicar filtro simulado para área
                    dados_simulados = filtrar_dados_simulados(idx, filtro_area)
                    if not dados_simulados:
                        continue
                    area_exemplo = dados_simulados.get("area")
                    
                    with st.container():
                        col_img, col_info = st.columns([1, 4])
                        with col_img:
                            st.image("https://img.freepik.com/vetores-premium/auditoria-negocios-e-financas-minima-icon-logo_186868-31.jpg", width=80)
                        with col_info:
                            st.markdown(f"### {name}")
                            st.markdown(f"🔗 [Perfil ORCID]({profile_url})")
                            st.markdown(f"🧭 **Área:** {area_exemplo}")
                            st.markdown(f"🏢 **Instituição:** {institution}")
                            bio_text = bio if len(bio) <= 250 else bio[:250] + "..."
                            st.markdown(f"📝 {bio_text}")
                        st.markdown("---")
    if st.button("volver al menú"):
        st.session_state.page = "menu"
        if hasattr(st, "experimental_rerun"):
            st.experimental_rerun()
        else:
            st.stop()
