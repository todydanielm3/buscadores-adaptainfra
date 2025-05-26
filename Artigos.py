# Artigos.py  ─────────────────────────────────────────────────────────
from __future__ import annotations
import base64, collections, requests, datetime
from typing import List, Dict, Any, Optional

import altair as alt
import pandas as pd
import streamlit as st

# Integrações externas
from olacefs_api    import search_items, OlacefsAPIError          # OLACEFS Datos
from biblioteca_api import search_biblioteca, parse_biblioteca_item
from idi_api        import search_idi_documents, parse_idi_item
from db             import add_search_history, add_feedback       # grava BD

# ───────────────────────── utilidades comuns ───────────────────────
def _b64(path: str) -> str:
    with open(path, "rb") as img:
        return base64.b64encode(img.read()).decode()

def _invert_abstract(idx: Optional[Dict[str, List[int]]]) -> str:
    if not idx:
        return "Resumen no disponible."
    ordered = [(p, w) for w, ps in idx.items() for p in ps]
    return " ".join(w for _, w in sorted(ordered))

# ───────────────────────── OpenAlex helpers ────────────────────────
def _openalex_search(q: str, n: int = 200) -> list[dict]:
    url = "https://api.openalex.org/works"
    params = {"search": q, "per-page": n, "sort": "publication_date:desc"}
    try:
        r = requests.get(url, params=params, timeout=20)
        r.raise_for_status()
        return r.json().get("results", [])
    except requests.RequestException as exc:
        st.error(f"[OpenAlex] Falha: {exc}")
        return []

def _openalex_parse(it: dict) -> dict:
    year = (it.get("publication_date") or "")[:4] or "desconocido"
    topics = [c.get("display_name") for c in it.get("concepts", [])]
    insts  = {
        i.get("display_name")
        for a in it.get("authorships", [])
        for i in a.get("institutions", [])
        if i.get("display_name")
    }
    return {
        "title"       : it.get("title", "Sin título"),
        "date"        : it.get("publication_date"),
        "year"        : year,
        "topics"      : topics,
        "institutions": list(insts),
        "type"        : it.get("type", "desconocido"),
        "abstract"    : _invert_abstract(it.get("abstract_inverted_index")),
        "url"         : it.get("doi")
                        or it.get("primary_location", {}).get("landing_page_url", "#"),
    }

# ───────────────────────── interface principal ──────────────────────
def show_artigos() -> None:
    # Cabeçalho
    st.markdown(
        f"""
        <div style="text-align:center;margin-bottom:26px">
          <img src="data:image/png;base64,{_b64('logo.png')}" width="120">
          <h2 style="margin-bottom:4px">Búsqueda inteligente</h2>
          <h6 style="margin-top:0">Conectando investigación y especialistas</h6>
        </div>""",
        unsafe_allow_html=True,
    )

    # Formulário
    with st.form("form_busca", clear_on_submit=False):
        termo = st.text_input("Término")
        tema  = st.selectbox(
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
        fonte = st.radio(
            "Fuente de datos",
            ["Datos Generales", "OLACEFS Biblioteca", "IDI"],
            horizontal=True,
        )
        col1, col2 = st.columns(2)
        ok   = col1.form_submit_button("Buscar")
        menu = col2.form_submit_button("Volver al menú")

    if menu:
        st.session_state.page = "menu"
        st.query_params.update({"page": "menu"})
        st.stop()
    if not ok:
        return
    if not termo.strip():
        st.warning("Ingrese un término de búsqueda.")
        return

    q = f"{termo.strip()} {tema}" if tema != "Sin" else termo.strip()
    st.info(f"Buscando **{q}** en **{fonte}**…")

    # Busca conforme fonte
    try:
        if fonte == "Datos Generales":
            raw   = _openalex_search(q)
            itens = [_openalex_parse(r) for r in raw]

        elif fonte == "OLACEFS Biblioteca":
            raw   = search_biblioteca(q)
            itens = [parse_biblioteca_item(r) for r in raw]

        elif fonte == "IDI":
            raw   = search_idi_documents(q, rows=200)
            itens = [parse_idi_item(r) for r in raw]

        else:  # segurança
            st.error("Fonte desconhecida.")
            return
    except Exception as exc:
        st.error(f"[{fonte}] {exc}")
        return

    # Salva histórico
    add_search_history(q, f"Artigos_{fonte}")

    if not itens:
        st.warning("No se encontraron resultados.")
        return

    df = pd.DataFrame(itens)

    # Estatísticas
    st.sidebar.metric("Total resultados", len(df))

    if "year" in df:
        df_year = (
            df["year"].value_counts()
            .rename_axis("Año")
            .reset_index(name="Frecuencia")
            .sort_values("Año")
        )
        st.sidebar.altair_chart(
            alt.Chart(df_year)
            .mark_bar()
            .encode(x="Año:N", y="Frecuencia:Q"),
            use_container_width=True,
        )

    insts = collections.Counter(i for lst in df["institutions"] for i in (lst or []))
    if insts:
        st.sidebar.subheader("Instituciones")
        st.sidebar.table(
            pd.DataFrame(insts.most_common(5), columns=["Institución", "Freq"])
        )

    types = df["type"].value_counts().reset_index()
    types.columns = ["Tipo", "Freq"]
    st.sidebar.subheader("Formato / tipo")
    st.sidebar.table(types)

    # Resultados
    st.subheader("Resultados")
    for i, row in enumerate(itens, 1):
        st.markdown(f"### {i}. {row['title']}")
        if row["date"]:
            st.write("**Fecha:**", row["date"])
        if row["institutions"]:
            st.write("**Institución:**", ", ".join(row["institutions"]))
        st.write("**Tipo:**", row["type"])
        st.write("**Resumen / descripción:**", row["abstract"][:400], "…")
        st.markdown(f"[Enlace]({row['url']})")
        st.markdown("---")

    # Feedback
    with st.form("fb"):
        txt = st.text_area("¿Te fue útil la búsqueda?", placeholder="Comentarios…")
        if st.form_submit_button("Enviar"):
            add_feedback(txt, f"Artigos_{fonte}")
            st.success("¡Gracias!")

# Alias para buscadores.py
def show_inteligente(): show_artigos()

if __name__ == "__main__":
    st.set_page_config("Debug Artigos", layout="centered")
    show_artigos()
