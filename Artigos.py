# Artigos.py
# ────────────────────────────────────────────────────────────────────
from __future__ import annotations
import base64, collections, requests
from typing import List, Dict, Any, Optional

import altair as alt
import pandas as pd
import streamlit as st

# Integrações externas
from olacefs_api   import search_items, OlacefsAPIError          # → OLACEFS Datos
from biblioteca_api import search_biblioteca, parse_biblioteca_item
from worldbank_api import search_worldbank_documents, parse_worldbank_item
from idi_api       import search_idi_documents,     parse_idi_item

# ═════════════════════════════ utilidades comuns ═════════════════════════════
def get_base64_image(path: str) -> str:
    with open(path, "rb") as img:
        return base64.b64encode(img.read()).decode()

def invert_abstract(index: Optional[Dict[str, List[int]]]) -> str:
    """Converte o inverted_index do OpenAlex em texto plano."""
    if not index:
        return "Resumen no disponible."
    ordered = [(p, w) for w, poss in index.items() for p in poss]
    return " ".join(w for _, w in sorted(ordered))

# ═════════════════════════════ OpenAlex helpers ══════════════════════════════
def search_openalex(q: str, max_results: int = 200) -> List[Dict[str, Any]]:
    url = "https://api.openalex.org/works"
    params = {"search": q, "per-page": max_results, "sort": "publication_date:desc"}
    try:
        r = requests.get(url, params=params, timeout=15)
        r.raise_for_status()
        return r.json().get("results", [])
    except requests.RequestException as exc:
        st.error(f"[Datos Generales] Falha na requisição: {exc}")
        return []

def parse_openalex(item: Dict[str, Any]) -> Dict[str, Any]:
    year = (item.get("publication_date") or "")[:4] or "desconocido"
    topics = [c.get("display_name") for c in item.get("concepts", [])]
    insts = {
        inst.get("display_name")
        for a in item.get("authorships", [])
        for inst in a.get("institutions", [])
        if inst.get("display_name")
    }
    return {
        "title": item.get("title", "Sin título"),
        "date": item.get("publication_date"),
        "year": year,
        "topics": topics,
        "institutions": list(insts),
        "type": item.get("type", "desconocido"),
        "abstract": invert_abstract(item.get("abstract_inverted_index")),
        "url": (
            item.get("doi")
            or item.get("primary_location", {}).get("landing_page_url")
            or "#"
        ),
    }

# ═════════════════════════════ interface principal ═══════════════════════════
def show_artigos() -> None:
    # — Cabeçalho —
    logo64 = get_base64_image("logo.png")
    st.markdown(
        f"""
        <div style="text-align:center;margin-bottom:30px">
          <img src="data:image/png;base64,{logo64}" width="150">
          <h1 style="font-family:Roboto,sans-serif;color:#333">Búsqueda inteligente</h1>
          <p style="font-family:Roboto,sans-serif">Conectando investigadores con publicaciones académicas</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # — Formulário —
    with st.form("search_form_artigos", clear_on_submit=False):
        query = st.text_input("Término", value="")
        tema  = st.selectbox(
            "Tema",
            [
                "Sin",
                "INFRAESTRUCTURA SOSTENIBLE, SOCIAL",
                "INFRAESTRUCTURA SOSTENIBLE, ECONÓMICO",
                "INFRAESTRUCTURA SOSTENIBLE, AMBIENTAL",
                "INFRAESTRUCTURA SOSTENIBLE, TÉCNICO",
                "INFRAESTRUCTURA SOSTENIBLE, POLÍTICO Y GUBERNAMENTAL",
                "INFRAESTRUCTURA SOSTENIBLE, REGIÓN AMAZÓNICA",
                "INFRAESTRUCTURA SOSTENIBLE, AUDITORÍA",
            ],
        )
        fonte = st.radio(
            "Fuente de datos",
            ["Datos Generales", "OLACEFS Biblioteca","IDI"],
            horizontal=True,
        )
        col1, col2 = st.columns(2)
        buscar = col1.form_submit_button("Buscar")
        volver = col2.form_submit_button("Volver al menú")

    if volver:
        st.session_state.page = "menu"
        st.query_params.update({"page": "menu"})
        st.stop()

    if not buscar:
        return
    if not query.strip():
        st.warning("Por favor, ingrese un término de búsqueda.")
        return

    q_final = f"{query.strip()} {tema}" if tema != "Sin" else query.strip()
    st.info(f"Buscando por **{q_final}** en **{fonte}** …")

    # — Delegação por fonte —
    try:
        if fonte == "Datos Generales":
            raw   = search_openalex(q_final, max_results=200)
            items = [parse_openalex(i) for i in raw]

        elif fonte == "OLACEFS Biblioteca":
            raw   = search_biblioteca(q_final)
            items = [parse_biblioteca_item(i) for i in raw]

        elif fonte == "World Bank":
            raw   = search_worldbank_documents(q_final, rows=200)
            items = [parse_worldbank_item(doc) for doc in raw]

        elif fonte == "IDI":
            raw   = search_idi_documents(q_final, limit=200)
            items = [parse_idi_item(doc) for doc in raw]

        else:
            st.warning("Fuente no reconocida.")
            return
    except Exception as exc:
        st.error(f"[{fonte}] {exc}")
        return

    if not items:
        st.warning("No se encontraron resultados.")
        return

    df = pd.DataFrame(items)
    # — Barra lateral —
    st.sidebar.metric("Total resultados", len(items))

    if "year" in df.columns:
        df_year = df["year"].value_counts().reset_index()
        df_year.columns = ["Año", "Frecuencia"]
        st.sidebar.altair_chart(
            alt.Chart(df_year).mark_bar().encode(
                x=alt.X("Año:N", title="Año"),
                y=alt.Y("Frecuencia:Q"),
            ).properties(width=250, height=200),
            use_container_width=True,
        )

    inst_counter = collections.Counter(
        inst for lst in df.get("institutions", []) for inst in (lst or [])
    )
    if inst_counter:
        st.sidebar.subheader("Instituciones")
        st.sidebar.table(
            pd.DataFrame(inst_counter.most_common(5), columns=["Institución", "Freq"])
        )

    if "type" in df.columns:
        type_count = df["type"].value_counts().reset_index()
        type_count.columns = ["Tipo", "Freq"]
        st.sidebar.subheader("Tipo de obra / formato")
        st.sidebar.table(type_count)

    # — Listagem —
    st.subheader("Resultados")
    for i, row in enumerate(items, start=1):
        st.markdown(f"### {i}. {row['title']}")
        if row.get("date"):
            st.write(f"**Fecha:** {row['date']}")
        if row.get("institutions"):
            st.write(f"**Institución:** {', '.join(row['institutions'])}")
        st.write(f"**Tipo:** {row['type']}")
        st.write(f"**Resumen / descripción:** {row['abstract'][:300]} …")
        st.markdown(f"[Enlace]({row['url']})")
        st.markdown("---")

    # — Feedback —
    st.markdown("##### ¿Te fue útil la búsqueda?")
    with st.form("feedback_form_artigos"):
        fb = st.text_area("Deja tu feedback", placeholder="Comentarios…")
        if st.form_submit_button("Enviar feedback"):
            from db import add_feedback
            add_feedback(fb, context=f"Artigos_{fonte}")
            st.success("¡Gracias por tu feedback!")

# Compatibilidade com buscadores.py
def show_inteligente() -> None:
    show_artigos()

# Execução isolada
if __name__ == "__main__":
    st.set_page_config("Debug Artigos", layout="centered")
    show_artigos()
