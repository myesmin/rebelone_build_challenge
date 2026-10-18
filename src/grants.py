"""Grants.gov: open and forecasted federal funding that matches a complaint signal."""
import hashlib
import html
import json
import time
from pathlib import Path

import requests

from config import GRANT_CATEGORIES, GRANT_KEYWORDS, GRANT_STATUSES, GRANTS_API

RAW = Path(__file__).resolve().parent.parent / "data" / "raw"


def _search(keyword: str, rows: int = 10) -> list[dict]:
    body = {"keyword": keyword, "oppStatuses": GRANT_STATUSES,
            "fundingCategories": GRANT_CATEGORIES, "rows": rows}
    key = hashlib.md5(json.dumps(body, sort_keys=True).encode()).hexdigest()[:16]
    cache = RAW / f"grants_{key}.json"
    if cache.exists():
        return json.loads(cache.read_text())
    for attempt in range(4):
        try:
            r = requests.post(GRANTS_API, json=body, timeout=60)
            hits = r.json()["data"]["oppHits"]
            RAW.mkdir(parents=True, exist_ok=True)
            cache.write_text(json.dumps(hits))
            time.sleep(0.5)
            return hits
        except (requests.RequestException, ValueError, KeyError):
            time.sleep(2 ** attempt)
    return []


def keywords_for(product: str, sub_product: str) -> list[str]:
    return GRANT_KEYWORDS.get(f"{product}|{sub_product}") or GRANT_KEYWORDS.get(product, [])


def match(product: str, sub_product: str, limit: int = 6) -> list[dict]:
    """De-duplicated US domestic opportunities for a signal's keyword phrases."""
    seen, out = set(), []
    for kw in keywords_for(product, sub_product):
        for o in _search(kw):
            # Skip embassy/public-diplomacy programs abroad: not a US domestic market signal.
            if o.get("agencyCode", "").startswith(("DOS-", "USAID")) or o["id"] in seen:
                continue
            # Full-text search also hits applicant boilerplate, so require every word of the
            # phrase in the title.
            title = html.unescape(o.get("title", "")).lower()
            if not all(w.lower() in title for w in kw.strip('"').split()):
                continue
            seen.add(o["id"])
            out.append({
                "number": o.get("number"), "title": html.unescape(o.get("title", "")),
                "agency": o.get("agency") or o.get("agencyCode"),
                "close": o.get("closeDate") or "rolling/forecast",
                "status": o.get("oppStatus"), "keyword": kw,
                "url": f"https://www.grants.gov/search-results-detail/{o['id']}",
            })
    return out[:limit]
