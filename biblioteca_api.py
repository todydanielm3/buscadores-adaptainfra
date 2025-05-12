# biblioteca_api.py

import re
import requests
from typing import List, Dict, Any

# ── exception for library searches ─────────────────────────────────────────────
class BibliotecaAPIError(RuntimeError):
    """Erro ao chamar o endpoint de Biblioteca OLACEFS."""

# ── helper to strip HTML tags ───────────────────────────────────────────────────
def _html_to_text(html: str) -> str:
    # simple regex‑based stripper
    return re.sub(r"<[^>]+>", "", html).strip()

# ── parse one WP post into our unified record ──────────────────────────────────
def parse_biblioteca_item(item: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "title":     _html_to_text(item.get("title", {}).get("rendered", "")),
        "date":      item.get("date", ""),
        "year":      item.get("date", "")[:4] if item.get("date") else "desconocido",
        "topics":    [],      # no taxonomy
        "institutions": [],
        "type":      item.get("type", "post"),
        "abstract":  _html_to_text(item.get("excerpt", {}).get("rendered", "")),
        "url":       item.get("link", "#"),
    }

# ── search the OLACEFS WordPress “Biblioteca” ───────────────────────────────────
def search_biblioteca(term: str, limit: int = 10) -> List[Dict[str, Any]]:
    """
    • term  → texto livre  
    • limit → número máximo de posts desejados (WordPress caps per_page at 100)
    """
    per_page = min(limit, 100)    # WP REST API max is 100
    url = "https://olacefs.com/wp-json/wp/v2/posts"
    params = {
        "search":   term,
        "per_page": per_page,
        "status":   "publish",
    }
    try:
        r = requests.get(url, params=params, timeout=20)
        r.raise_for_status()
        return r.json()           # this is a list of dicts
    except requests.RequestException as e:
        raise BibliotecaAPIError(f"Falha na Biblioteca API: {e}") from e
