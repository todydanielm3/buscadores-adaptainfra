# Artigos.py
# ────────────────────────────────────────────────────────────────────

import base64
import collections
import requests
from typing import List, Dict, Any, Optional

import altair as alt
import pandas as pd
import streamlit as st

# local imports (make sure these two files live alongside this one)
from olacefs_api import OlacefsAPIError, search_items
from biblioteca_api import search_biblioteca, parse_biblioteca_item

# ═════════════════════════════════ utilitários comuns ═════════════════

def get_base64_image(path: str) -> str:
    """Load an image file and return base64‐encoded string."""
    with open(path, "rb") as img:
        return base64.b64encode(img.read()).decode()

def invert_abstract(index: Optional[Dict[str, List[int]]]) -> str:
    """Convert OpenAlex abstract_inverted_index into plain text."""
    if not index:
        return "Resumen no disponible."
    word_positions: List[tuple[int,str]] = []
    for word, poss in index.items():
        for p in poss:
            word_positions.append((p, word))
    word_positions.sort(key=lambda x: x[0])
    return " ".join(w for _, w in word_positions)


# ═══════════════════════════════ OpenAlex helpers ═══════════════════

def search_openalex(q: str, max_results: int = 200) -> List[Dict[str, Any]]:
    url = "https://api.openalex.org/works"
    params = {"search": q, "per-page": max_results, "sort": "publication_date:desc"}
    try:
        r = requests.get(url, params=params, timeout=15)
        r.raise_for_status()
        return r.json().get("results", [])
    except requests.RequestException as exc:
        st.error(f"[OpenAlex] Falha na requisição: {exc}")
        return []

def parse_openalex(item: Dict[str, Any]) -> Dict[str, Any]:
    title = item.get("title", "Sin título")
    date = item.get("publication_date", "")
    year = date.split("-")[0] if date else "desconocido"
    topics = [c.get("display_name","") for c in item.get("concepts",[])]
    insts = {
        inst.get("display_name")
        for a in item.get("authorships",[])
        for inst in a.get("institutions",[])
        if inst.get("display_name")
    }
    abstract = invert_abstract(item.get("abstract_inverted_index"))
    url = item.get("doi") or item.get("primary_location",{}).get("landing_page_url","")
    return {
        "title": title,
        "date": date,
        "year": year,
        "topics": topics,
        "institutions": list(insts),
        "type": item.get("type","desconocido"),
        "abstract": abstract,
        "url": url or "#",
    }


# ══════════════════════════════ OLACEFS Datos helpers ═════════════════════
def parse_olacefs(item: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize CKAN resource/package into our schema."""
    meta = item["metadata"]
    dt = meta.get("date") or meta.get("created") or ""
    year = dt[:4] if dt else "desconocido"
    return {
        "title": meta.get("title","Sin título"),
        "date": dt,
        "year": year,
        "topics": [],
        "institutions": [meta.get("organization")] if meta.get("organization") else [],
        "type": meta.get("format","desconocido"),
        "abstract": meta.get("description",""),
        "url": meta.get("url","#"),
    }


# ══════════════════════════════ Main interface ════════════════════════

def show_artigos() -> None:
    # header
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

    # form
    with st.form("search_form_artigos", clear_on_submit=False):
        query = st.text_input("Término")
        tema = st.selectbox(
            "Tema",
            ["Sin",
             "INFRAESTRUCTURA SOSTENIBLE, SOCIAL",
             "INFRAESTRUCTURA SOSTENIBLE, ECONÓMICO",
             "INFRAESTRUCTURA SOSTENIBLE, AMBIENTAL",
             "INFRAESTRUCTURA SOSTENIBLE, TÉCNICO",
             "INFRAESTRUCTURA SOSTENIBLE, POLÍTICO Y GUBERNAMENTAL",
             "INFRAESTRUCTURA SOSTENIBLE, REGIÓN AMAZÓNICA",
             "INFRAESTRUCTURA SOSTENIBLE, AUDITORÍA"]
        )
        fonte = st.radio("Fuente de datos", ["OpenAlex", "OLACEFS Biblioteca"], horizontal=True)
        c1, c2 = st.columns(2)
        buscar = c1.form_submit_button("Buscar")
        voltar = c2.form_submit_button("Volver al menú")

    if voltar:
        st.session_state.page = "menu"
        st.query_params.update({"page":"menu"})
        st.stop()

    if not buscar:
        return

    if not query.strip():
        st.warning("Por favor, ingrese un término de búsqueda.")
        return

    q_final = f"{query.strip()} {tema}" if tema!="Sin" else query.strip()
    st.info(f"Buscando por **{q_final}** en **{fonte}** …")

    # fetch & parse
    items: List[Dict[str,Any]] = []
    if fonte=="OpenAlex":
        raw = search_openalex(q_final, max_results=200)
        items = [parse_openalex(i) for i in raw]
    else:  # OLACEFS Biblioteca
        try:
            raw = search_biblioteca(q_final, limit=200)
        except Exception as e:
            st.error(f"[Biblioteca] {e}")
            return
        # parse and drop any None
        items = [x for x in (parse_biblioteca_item(i) for i in raw) if x]

    if not items:
        st.warning("No se encontraron resultados.")
        return

    df = pd.DataFrame(items)

    # sidebar stats
    st.sidebar.metric("Total resultados", len(items))
    df_year = df["year"].value_counts().reset_index()
    df_year.columns = ["Año","Frecuencia"]
    chart = alt.Chart(df_year).mark_bar().encode(
        x=alt.X("Año:N"), y=alt.Y("Frecuencia:Q")
    ).properties(width=250, height=200)
    st.sidebar.altair_chart(chart, use_container_width=True)

    insts = collections.Counter(inst for lst in df["institutions"] for inst in lst)
    if insts:
        st.sidebar.subheader("Instituciones")
        st.sidebar.table(pd.DataFrame(insts.most_common(5), columns=["Inst","Freq"]))

    types = df["type"].value_counts().reset_index()
    types.columns = ["Tipo","Freq"]
    st.sidebar.subheader("Tipo/Formato")
    st.sidebar.table(types)

    # main listing
    st.subheader("Resultados")
    for i,row in enumerate(items, start=1):
        st.markdown(f"### {i}. {row['title']}")
        if row.get("date"):
            st.write("**Fecha:**", row["date"])
        if row.get("institutions"):
            st.write("**Institución:**", ", ".join(row["institutions"]))
        st.write("**Tipo:**", row["type"])
        st.write("**Resumen:**", row["abstract"][:300] + ("…" if len(row["abstract"])>300 else ""))
        st.markdown(f"[Enlace]({row['url']})")
        st.markdown("---")

    # feedback
    st.markdown("##### ¿Te fue útil la búsqueda?")
    with st.form("feedback_form"):
        fb = st.text_area("Deja tu feedback")
        if st.form_submit_button("Enviar"):
            from db import add_feedback
            add_feedback(fb, context=f"Artigos_{fonte}")
            st.success("¡Gracias por tu feedback!")


def show_inteligente() -> None:
    show_artigos()


if __name__=="__main__":
    st.set_page_config("Debug Artigos", layout="centered")
    show_artigos()
