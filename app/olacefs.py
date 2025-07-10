import streamlit as st
import base64
from typing import List

from olacefs_api import search_items, OlacefsAPIError


def _b64(img_path: str) -> str:
    with open(img_path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def _render_result(item: dict, idx: int) -> None:
    st.markdown(f"### {idx}. {item['metadata'].get('title', 'Sin título')}")
    
    desc = item['metadata'].get('description')
    if desc:
        st.write(f"**Descripción:** {desc}")

    org = item['metadata'].get('organization')
    if org:
        st.write(f"**Organización:** {org}")

    ftype = item['metadata'].get('format')
    if ftype:
        st.write(f"**Formato:** {ftype}")

    url = item['metadata'].get("url") or (
        f"https://datos.olacefs.com/dataset/{item.get('id', '')}"
        if item.get("id") else "https://datos.olacefs.com/"
    )
    
    st.markdown(f"[Enlace al recurso]({url})")
    st.markdown("---")


def show_olacefs_search() -> None:
    logo = _b64("logo.png")
    st.markdown(
        f"""
        <div style="text-align:center;margin-bottom:25px">
          <img src="data:image/png;base64,{logo}" width="120">
          <h1 style="font-family:Roboto,sans-serif">Busca OLACEFS</h1>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("form_olacefs"):
        termo   = st.text_input("Término de busca")
        formatos: List[str] = st.multiselect(
            "Filtrar por formato (opcional)",
            ["PDF", "CSV", "XLSX", "JSON", "XML", "ZIP"],
        )
        col1, col2 = st.columns(2)
        buscar  = col1.form_submit_button("Buscar")
        voltar  = col2.form_submit_button("Volver al menú")

    if voltar:
        st.session_state.page = "menu"
        st.query_params.update({"page": "menu"})
        st.stop()

    if not buscar:
        return

    if not termo.strip():
        st.warning("Digite um termo.")
        return

    try:
        resultados = search_items(termo.strip(), formats=formatos or None, max_rows=100)
    except OlacefsAPIError as err:
        st.error(f"❌ Falha na API OLACEFS: {err}")
        return

    if not resultados:
        st.info("Nenhum resultado.")
        return

    st.success(f"{len(resultados)} resultados encontrados.")
    for i, itm in enumerate(resultados, start=1):
        _render_result(itm, i)
