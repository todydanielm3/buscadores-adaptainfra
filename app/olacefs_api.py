# olacefs_api.py  ▸ acesso fino ao CKAN (https://datos.olacefs.com)
from __future__ import annotations
import time, urllib.parse
from typing import List, Dict
import requests

BASE_URL   = "https://datos.olacefs.com/api/3/action"
ENDPOINTS  = {
    "package_search" : f"{BASE_URL}/package_search",
    "resource_search": f"{BASE_URL}/resource_search",
}

class OlacefsAPIError(RuntimeError): ...

# ───────────────────────── helper interno ──────────────────────────
_MAX_409_RETRY = 3          # tenta de novo se o índice CKAN estiver rebuildando
_RETRY_DELAY   = 4          # segundos

def _ckan_call(url: str, params: dict) -> dict:
    tries = 0
    while True:
        try:
            r = requests.get(url, params=params, timeout=20)
            if r.status_code == 409 and tries < _MAX_409_RETRY:
                tries += 1
                time.sleep(_RETRY_DELAY)
                continue
            r.raise_for_status()
            data = r.json()
        except (requests.RequestException, ValueError) as exc:
            raise OlacefsAPIError(f"Falha na requisição CKAN: {exc}") from exc

        if not data.get("success"):
            raise OlacefsAPIError(f"CKAN retornou erro: {data}")
        return data["result"]

# ───────────────────────── interface pública ───────────────────────
def search_items(term: str, *, formats: List[str] | None = None,
                 max_rows: int = 100) -> List[Dict]:
    """
    Procura recursos **e** pacotes (qualquer formato).  
    A saída sempre traz a chave ``metadata`` normalizada.
    """
    # Escapa o termo — evita 409 quando ele contém “:” ou “/” etc.
    term_q = urllib.parse.quote_plus(term)

    fq_formats = ""
    if formats:
        fq_formats = " AND (" + " OR ".join(f'format:"{f}"' for f in formats) + ")"

    # 1) resources ----------------------------------------------------
    params_res = {"q": term_q, "fq": f"state:active{fq_formats}", "rows": max_rows}
    try:
        recursos = _ckan_call(ENDPOINTS["resource_search"], params_res)["results"]
    except OlacefsAPIError as e:
        print("⚠️ resource_search falhou:", e)
        recursos = []

    # 2) packages -----------------------------------------------------
    params_pkg = {"q": term_q, "rows": max_rows}
    pacotes = _ckan_call(ENDPOINTS["package_search"], params_pkg)["results"]

    # 3) unifica + normaliza -----------------------------------------
    out, vistos = [], set()

    def _wrap(obj: dict, origin: str) -> dict:
        """Empacota garantindo um dicionário .metadata uniforme."""
        if origin == "resource":
            meta = {
                "id"          : obj["id"],
                "title"       : obj.get("name") or obj.get("title"),
                "description" : obj.get("description", ""),
                "format"      : obj.get("format"),
                "url"         : obj.get("url"),
                "created"     : obj.get("created"),
                "date"        : obj.get("last_modified"),
                "organization": obj.get("organization", {}).get("title")
                                 if obj.get("organization") else None,
            }
        else:                      # package
            meta = {
                "id"          : obj["id"],
                "title"       : obj.get("title"),
                "description" : obj.get("notes", ""),
                "format"      : "package",
                "url"         : obj.get("url") or f"{BASE_URL}/dataset/{obj['name']}",
                "created"     : obj.get("metadata_created"),
                "date"        : obj.get("metadata_modified"),
                "organization": obj.get("organization", {}).get("title")
                                 if obj.get("organization") else None,
            }
        return {"__origin__": origin, "metadata": meta}

    for r in recursos:
        if r["id"] not in vistos:
            out.append(_wrap(r, "resource"))
            vistos.add(r["id"])

    for p in pacotes:
        if p["id"] not in vistos:
            out.append(_wrap(p, "package"))
            vistos.add(p["id"])

    return out
