import streamlit as st
import requests

def buscar_orcid(query, max_results=5):
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
        credit_name = name_info.get("credit-name") or {}  # Fallback para {} se for None
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

def filtrar_dados_simulados(idx: int, filtro_pais: str, filtro_area: str, filtro_idioma: str) -> dict:
    """
    Gera dados simulados para os filtros e verifica se correspondem
    aos filtros selecionados.
    """
    # Dados simulados para demonstração
    idioma = "Português" if idx % 3 == 0 else "Espanhol"
    area = "Infraestrutura Sustentável" if idx % 2 == 0 else "Auditoria Pública"
    pais = "Brasil" if idx % 2 == 0 else "México"
    
    if (filtro_pais != "Todos" and filtro_pais != pais) or \
       (filtro_area != "Todas" and filtro_area != area) or \
       (filtro_idioma != "Todos" and filtro_idioma != idioma):
        return {}
    
    return {"idioma": idioma, "area": area, "pais": pais}

def show_especialistas():
    st.image("logo.png", width=250)
    st.title("🔎 Repositório de Especialistas")
    st.write("Pesquise por especialistas em infraestrutura sustentável, adaptação climática, auditoria pública e mais.")
    
    query = st.text_input("Digite um termo de busca (ex: biodiversidade, gênero, auditoria)")
    
    # Filtros: País, Área e Idioma
    col1, col2, col3 = st.columns(3)
    with col1:
        filtro_pais = st.selectbox("País", ["Todos", "Brasil", "México", "Argentina", "Bolívia", "Chile", "Colômbia", "Costa Rica", "Cuba", "Equador", "El Salvador", "Guatemala", "Honduras", "Nicarágua", "Panamá", "Paraguai", "Peru", "República Dominicana", "Uruguai", "Venezuela", "Belize", "Guiana", "Caribe"])
    with col2:
        filtro_area = st.selectbox("Área", ["Todas", "Infraestrutura Sustentável", "Auditoria Pública", "Biodiversidade", "Tecnologia e TICs"])
    with col3:
        filtro_idioma = st.selectbox("Idioma", ["Todos", "Português", "Espanhol", "Inglês"])
    
    if st.button("Buscar"):
        if not query.strip():
            st.warning("Digite um termo válido.")
        else:
            st.info(f"Buscando por: '{query}' ...")
            resultados = buscar_orcid(query)
            if not resultados:
                st.warning("Nenhum especialista encontrado.")
            else:
                st.success("Especialistas encontrados:")
                for idx, r in enumerate(resultados, start=1):
                    orcid_info = r.get('orcid-identifier', {})
                    orcid_id = orcid_info.get('path', 'N/A')
                    profile_url = f"https://orcid.org/{orcid_id}"
                    
                    # Obter dados reais do especialista (nome, bio e instituição)
                    detalhes = obter_detalhes_orcid(orcid_id)
                    name = detalhes.get("name", f"Especialista {idx}")
                    bio = detalhes.get("bio")
                    institution = detalhes.get("institution")
                    
                    # Aplicar dados simulados para os filtros
                    dados_simulados = filtrar_dados_simulados(idx, filtro_pais, filtro_area, filtro_idioma)
                    if not dados_simulados:
                        continue
                    idioma_exemplo = dados_simulados.get("idioma")
                    area_exemplo = dados_simulados.get("area")
                    pais_exemplo = dados_simulados.get("pais")
                    
                    with st.container():
                        col_img, col_info = st.columns([1, 4])
                        with col_img:
                            st.image("https://img.freepik.com/vetores-premium/auditoria-negocios-e-financas-minima-icon-logo_186868-31.jpg", width=80)
                        with col_info:
                            st.markdown(f"### {name}")
                            st.markdown(f"🔗 [Perfil ORCID]({profile_url})")
                            st.markdown(
                                f"📍 **País:** {pais_exemplo}   |   "
                                f"🧭 **Área:** {area_exemplo}   |   "
                                f"🗣️ **Idioma:** {idioma_exemplo}"
                            )
                            st.markdown(f"🏢 **Instituição:** {institution}")
                            bio_text = bio if len(bio) <= 250 else bio[:250] + "..."
                            st.markdown(f"📝 {bio_text}")
                        st.markdown("---")
    if st.button("Voltar ao Menu"):
        st.session_state.page = "menu"
        if hasattr(st, "experimental_rerun"):
            st.experimental_rerun()
        else:
            st.stop()
