# idi_api.py
import requests, re
from bs4 import BeautifulSoup
from typing import List, Dict

IDI_BASE = "https://www.idi.no"
IDI_SECTIONS = [
    "/our-resources/idi-reporting",
    "/our-resources/idi-administrative",
    "/our-resources/global-public-goods",
    "/our-resources/global-sai-stocktaking-reports-and-research",
    "/our-resources/professional-sais",
    "/our-resources/relevant-sais",
    "/our-resources/well-governed-sais",
    "/our-resources/independent-sais",
]

def _clean(txt: str) -> str:
    return BeautifulSoup(txt, "html.parser").get_text(strip=True)

def search_idi_documents(term: str, *, rows: int = 200) -> List[Dict]:
    term_low = term.lower()
    docs: list[dict] = []

    for sec in IDI_SECTIONS:
        try:
            html = requests.get(IDI_BASE + sec, timeout=20).text
        except Exception:
            continue
        soup = BeautifulSoup(html, "html.parser")
        for a in soup.select("a[href*='/file']"):
            title = _clean(a.text)
            if term_low in title.lower():
                url = a["href"]
                if not url.startswith("http"):
                    url = IDI_BASE + url
                docs.append(
                    {
                        "title": title or "Documento sin título",
                        "url": url,
                        "type": "PDF" if url.lower().endswith(".pdf") else "file",
                        "source": IDI_BASE + sec,
                    }
                )
            if len(docs) >= rows:
                return docs
    return docs

def parse_idi_item(item: Dict) -> Dict:
    return {
        "title"       : item["title"],
        "date"        : None,
        "year"        : "desconocido",
        "topics"      : [],
        "institutions": ["IDI"],
        "type"        : item["type"],
        "abstract"    : f"Documento obtenido de {item['source']}",
        "url"         : item["url"],
    }
