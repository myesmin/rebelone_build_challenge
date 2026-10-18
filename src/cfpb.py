"""CFPB Consumer Complaint Database: aggregated counts via the public search API.

Notes from testing (Oct 2026):
- Narratives are no longer published (API or bulk CSV), so we work from structured fields.
- Aggregations act like facets: a field's own filter is ignored in its own aggregation,
  so one unfiltered call per window returns every product/sub-product count.
- Filter a sub-product with product="Product•Sub-product".
- Rapid requests get throttled with non-JSON responses; retry with backoff.
"""
import hashlib
import json
import time
from pathlib import Path

import requests

from config import CFPB_API

RAW = Path(__file__).resolve().parent.parent / "data" / "raw"
SEP = "•"  # •


def _get(params: list[tuple[str, str]]) -> dict:
    key = hashlib.md5(json.dumps(params).encode()).hexdigest()[:16]
    cache = RAW / f"cfpb_{key}.json"
    if cache.exists():
        return json.loads(cache.read_text())
    for attempt in range(5):
        try:
            r = requests.get(CFPB_API, params=params, timeout=60)
            data = r.json()
            if "aggregations" in data:
                RAW.mkdir(parents=True, exist_ok=True)
                cache.write_text(json.dumps(data))
                time.sleep(1.5)
                return data
        except (requests.RequestException, ValueError):
            pass
        time.sleep(2 ** attempt * 2)
    raise RuntimeError(f"CFPB API failed after retries: {params}")


def _buckets(aggs: dict, name: str) -> list[dict]:
    node = aggs[name]
    inner = next(v for k, v in node.items() if k != "doc_count")
    return inner["buckets"]


def _nested(bucket: dict) -> list[dict]:
    for k, v in bucket.items():
        if isinstance(v, dict) and "buckets" in v:
            return v["buckets"]
    return []


def window_counts(start: str, end: str) -> dict[tuple[str, str], int]:
    """{(product, sub_product or '*'): count} for one date window."""
    data = _get([("size", "0"), ("date_received_min", start), ("date_received_max", end)])
    out = {}
    for b in _buckets(data["aggregations"], "product"):
        out[(b["key"], "*")] = b["doc_count"]
        for s in _nested(b):
            out[(b["key"], s["key"])] = s["doc_count"]
    return out


def detail(product: str, sub_product: str, start: str, end: str) -> dict:
    """Issues, companies and states for one signal in one window."""
    value = product if sub_product == "*" else f"{product}{SEP}{sub_product}"
    data = _get([("size", "0"), ("date_received_min", start),
                 ("date_received_max", end), ("product", value)])
    a = data["aggregations"]
    total = data["hits"]["total"]["value"]
    issues = []
    for b in _buckets(a, "issue")[:6]:
        subs = [(s["key"], s["doc_count"]) for s in _nested(b)[:3]]
        issues.append({"issue": b["key"], "count": b["doc_count"], "sub_issues": subs})
    companies = [(b["key"], b["doc_count"]) for b in _buckets(a, "company")]
    states = [(b["key"], b["doc_count"]) for b in _buckets(a, "state")]
    return {
        "total": total,
        "issues": issues,
        "top_companies": companies[:5],
        "top_company_share": companies[0][1] / total if companies and total else 0,
        "top5_company_share": sum(c for _, c in companies[:5]) / total if total else 0,
        "n_companies": len(companies),
        "top_states": states[:5],
        "n_states": len(states),
    }
