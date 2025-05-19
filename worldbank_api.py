# worldbank_api.py
import requests
from typing import List, Dict

class WorldBankAPIError(RuntimeError):
    """Erro de comunicação com a API de documentos do World Bank."""

def search_worldbank_documents(term: str, rows: int = 100) -> List[Dict]:
    """
    Busca documentos no portal do World Bank usando o termo informado.
    """
    base_url = "https://search.worldbank.org/api/v2/wds"
    params = {
        "format": "json",
        "q": term,
        "rows": rows,
    }
    try:
        r = requests.get(base_url, params=params, timeout=20)
        r.raise_for_status()
        data = r.json()
    except (requests.RequestException, ValueError) as e:
        raise WorldBankAPIError(f"Erro na requisição World Bank: {e}")

    documentos = data.get("documents", {})
    return list(documentos.values())

# worldbank_api.py

def parse_worldbank_item(doc: dict) -> dict:
    return {
        "title": doc.get("display_title", "Sin título"),
        "date": doc.get("ext_pub_date", ""),
        "year": doc.get("ext_pub_date", "")[:4] if doc.get("ext_pub_date") else "desconocido",
        "institutions": [doc.get("owner")] if doc.get("owner") else [],
        "type": doc.get("docty", "desconocido"),
        "abstract": doc.get("subsc", "Sin descripción"),
        "url": doc.get("pdfurl") or doc.get("url") or "#"
    }
