# Artigos.py  ─────────────────────────────────────────────────────────
from __future__ import annotations
import collections, requests, datetime
from typing import List, Dict, Any, Optional
import sys
from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st

sys.path.append(str(Path(__file__).parent.parent))

# Integrações externas
from olacefs_api import search_items, OlacefsAPIError          # OLACEFS Datos
from biblioteca_api import search_biblioteca, parse_biblioteca_item
from idi_api        import search_idi_documents, parse_idi_item
from db             import add_search_history, add_feedback, SessionLocal, SearchHistory  # grava BD
from recomendador   import gerar_clusters_termos, termos_relacionados

# ───────────────────────── utilidades comuns ───────────────────────
def _b64(path: str) -> str:
    # Garante que o caminho seja relativo à raiz do projeto
    full_path = Path(__file__).parent.parent / path
    with open(full_path, "rb") as img:
        import base64
        return base64.b64encode(img.read()).decode()

def _invert_abstract(idx: Optional[Dict[str, List[int]]]) -> str:
    if not idx:
        return "Resumen no disponible."
    ordered = [(p, w) for w, ps in idx.items() for p in ps]
    return " ".join(w for _, w in sorted(ordered))

def carregar_historico():
    with SessionLocal() as session:
        result = session.query(SearchHistory.term).all()
    df = pd.DataFrame(result, columns=["term"])
    return df

def _goto_busca(term: str) -> None:
    st.session_state.page = "inteligente"
    st.session_state.query = term
    st.query_params.update({"page": "inteligente", "q": term})

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
def detectar_idioma(texto: str) -> str:
    """Detecta se o termo está em português ou espanhol."""
    pt_palavras = ["não", "informação", "obrigado", "você", "como", "qual", "quem", "onde", "quando", "por quê", "porque"]
    es_palavras = ["no", "información", "gracias", "usted", "cómo", "cuál", "quién", "dónde", "cuándo", "por qué", "porque"]
    pt_count = sum(1 for p in pt_palavras if p in texto.lower())
    es_count = sum(1 for p in es_palavras if p in texto.lower())
    if es_count > pt_count:
        return "es"
    return "pt"

def show_artigos() -> None:
    # Verificar se há busca na URL
    search_from_url = st.query_params.get("search", "")
    
    # Cabeçalho
    st.markdown(
        f"""
        <div style="text-align:center;margin-bottom:26px">
          <img src="data:image/png;base64,{_b64('assets/logo.png')}" width="500">
          <h2 style="margin-bottom:4px">Búsqueda inteligente</h2>
          <h6 style="margin-top:0">Conectando investigación y especialistas</h6>
        </div>""",
        unsafe_allow_html=True,
    )

    # Formulário
    with st.form("form_busca", clear_on_submit=False):
        # Usar busca da URL como valor inicial se existir
        termo = st.text_input("Término", value=search_from_url)
        fonte = st.radio(
            "Fuente de datos",
            ["Datos Generales", "OLACEFS Biblioteca"],
            horizontal=True,
        )
        col1, col2 = st.columns(2)
        ok   = col1.form_submit_button("Buscar")
        menu = col2.form_submit_button("Volver al menú")

    # Se há busca da URL, executar automaticamente
    if search_from_url and not ok:
        termo = search_from_url
        fonte = "Datos Generales"  # Fonte padrão
        ok = True
        # Limpar o parâmetro de busca da URL para evitar repetição
        st.query_params.pop("search", None)

    if menu:
        st.session_state.page = "menu"
        st.query_params.update({"page": "menu"})
        st.stop()
    if not ok:
        return
    if not termo.strip():
        idioma = detectar_idioma(termo)
        msg = "Ingrese un término de búsqueda." if idioma == "es" else "Digite um termo de busca."
        st.warning(msg)
        return

    idioma = detectar_idioma(termo)
    msg_busca = f"Buscando **{termo.strip()}** en **{fonte}**…" if idioma == "es" else f"Buscando **{termo.strip()}** em **{fonte}**…"
    st.info(msg_busca)

    # Busca conforme fonte
    try:
        if fonte == "Datos Generales":
            raw   = _openalex_search(termo.strip())
            itens = [_openalex_parse(r) for r in raw]

        elif fonte == "OLACEFS Biblioteca":
            raw   = search_biblioteca(termo.strip())
            itens = [parse_biblioteca_item(r) for r in raw]

        else:
            msg = "Fuente desconocida." if idioma == "es" else "Fonte desconhecida."
            st.error(msg)
            return
    except Exception as exc:
        msg = f"[{fonte}] Error: {exc}" if idioma == "es" else f"[{fonte}] Erro: {exc}"
        st.error(msg)
        return

    add_search_history(termo.strip(), f"Artigos_{fonte}")

    if not itens:
        msg = "No se encontraron resultados." if idioma == "es" else "Nenhum resultado encontrado."
        st.warning(msg)
        return

    df = pd.DataFrame(itens)

    # Estatísticas
    st.sidebar.metric("Total resultados", len(df))

    if "year" in df:
        df_year = (
            df["year"].value_counts()
            .rename_axis("Año" if idioma == "es" else "Ano")
            .reset_index(name="Frecuencia" if idioma == "es" else "Frequência")
            .sort_values("Año" if idioma == "es" else "Ano")
        )
        st.sidebar.altair_chart(
            alt.Chart(df_year)
            .mark_bar()
            .encode(x="Año:N" if idioma == "es" else "Ano:N", y="Frecuencia:Q" if idioma == "es" else "Frequência:Q"),
            use_container_width=True,
        )

    insts = collections.Counter(i for lst in df["institutions"] for i in (lst or []))
    if insts:
        st.sidebar.subheader("Instituciones" if idioma == "es" else "Instituições")
        st.sidebar.table(
            pd.DataFrame(insts.most_common(5), columns=["Institución" if idioma == "es" else "Instituição", "Freq"])
        )

    types = df["type"].value_counts().reset_index()
    types.columns = ["Tipo", "Freq"]
    st.sidebar.subheader("Formato / tipo")

    st.subheader("Resultados" if idioma == "es" else "Resultados")
    for i, row in enumerate(itens, 1):
        st.markdown(f"### {i}. {row['title']}")
        if row["date"]:
            st.write("**Fecha:**" if idioma == "es" else "**Data:**", row["date"])
        if row["institutions"]:
            st.write("**Institución:**" if idioma == "es" else "**Instituição:**", ", ".join(row["institutions"]))
        st.write("**Tipo:**", row["type"])
        st.write("**Resumen / descripción:**" if idioma == "es" else "**Resumo / descrição:**", row["abstract"][:400], "…")
        st.markdown(f"[Enlace]({row['url']})" if idioma == "es" else f"[Link]({row['url']})")
        st.markdown("---")

    # Sugestões
    df_hist = carregar_historico()
    if not df_hist.empty:
        if len(df_hist) >= 5:
            df_clusterizado, modelo_kmeans = gerar_clusters_termos(df_hist)
            sugestoes = termos_relacionados(termo.strip(), df_clusterizado, modelo_kmeans)
            if sugestoes:
                st.subheader("🔁 Sugerencias basadas en su búsqueda:" if idioma == "es" else "🔁 Sugestões baseadas em sua busca:")
                for s in sugestoes:
                    st.button(s, on_click=lambda termo=s: _goto_busca(termo))
        else:
            st.sidebar.info("Busque más términos para recibir sugerencias inteligentes." if idioma == "es" else "Busque mais termos para receber sugestões inteligentes.")

    # Feedback
    with st.form("fb"):
        txt = st.text_area("¿Te fue útil la búsqueda?" if idioma == "es" else "A busca foi útil?", placeholder="Comentarios…" if idioma == "es" else "Comentários…")
        if st.form_submit_button("Enviar"):
            add_feedback(txt, f"Artigos_{fonte}")
            st.success("¡Gracias!" if idioma == "es" else "Obrigado!")

# Alias para buscadores.py
def show_inteligente(): show_artigos()

if __name__ == "__main__":
    st.set_page_config("Debug Artigos", layout="centered")
    show_artigos()
