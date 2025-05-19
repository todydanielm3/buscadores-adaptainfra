# idi_api.py
import requests
from bs4 import BeautifulSoup
from typing import List, Dict

IDI_BASE_URL = "https://www.idi.no"
IDI_RESOURCE_PAGES = [
    "/our-resources/idi-reporting",
    "/our-resources/idi-administrative",
    "/our-resources/global-public-goods",
    "/our-resources/global-sai-stocktaking-reports-and-research",
    "/our-resources/professional-sais",
    "/our-resources/relevant-sais",
    "/our-resources/well-governed-sais",
    "/our-resources/independent-sais",
]

def _html_to_text(html: str) -> str:
    return BeautifulSoup(html, "html.parser").get_text(strip=True)

def fetch_idi_documents() -> List[Dict]:
    results = []
    for page in IDI_RESOURCE_PAGES:
        full_url = f"{IDI_BASE_URL}{page}"
        try:
            r = requests.get(full_url, timeout=20)
            r.raise_for_status()
            soup = BeautifulSoup(r.text, "html.parser")
            links = soup.select("a[href*='/file']")
            for link in links:
                title = link.text.strip()
                url = link.get("href")
                if not url.startswith("http"):
                    url = IDI_BASE_URL + url
                results.append({
                    "title": title or "Documento sin título",
                    "url": url,
                    "type": "PDF",
                    "source": full_url,
                })
        except Exception as e:
            print(f"Erro ao acessar {full_url}: {e}")
    return results

def parse_idi_item(item: Dict) -> Dict:
    return {
        "title": item.get("title"),
        "date": None,  # Não disponível diretamente
        "year": "desconocido",
        "topics": [],
        "institutions": ["IDI"],
        "type": item.get("type", "PDF"),
        "abstract": f"Documento obtido de {item.get('source')}",
        "url": item.get("url")
    }

# idi_api.py -------------------------------------------------------------
from unidecode import unidecode      # pip install Unidecode
from rapidfuzz import fuzz, process   # pip install rapidfuzz
# ...

def search_idi_documents(term: str, *, max_items: int = 100, **kwargs) -> List[Dict]:
    """
    Busca documentos nos recursos do IDI.
    Aceita também `limit=` como sinônimo de `max_items` via **kwargs.
    """
    # compatibilidade com chamada usando limit=
    if "limit" in kwargs and not kwargs.get("max_items"):
        max_items = kwargs["limit"]

    all_docs = fetch_idi_documents()          # função já existente
    term_l   = term.lower()
    filtered = [
        doc for doc in all_docs
        if term_l in doc["title"].lower()
    ]
    return filtered[:max_items]
