"""Signal rubric. Mirrors .claude/skills/venture-screen/references/rubric.md (quantitative half)."""
import math
import re

from config import EXCLUDE_PRODUCTS, LMI_WEIGHTS, MIN_VOLUME


def lmi_weight(product: str, sub_product: str) -> int:
    return LMI_WEIGHTS.get((product, sub_product), LMI_WEIGHTS.get((product, "*"), 1))


def baseline_growth(prev: dict, curr: dict) -> float:
    p = sum(v for (prod, sub), v in prev.items() if sub == "*" and prod not in EXCLUDE_PRODUCTS)
    c = sum(v for (prod, sub), v in curr.items() if sub == "*" and prod not in EXCLUDE_PRODUCTS)
    return c / p if p else 1.0


def candidates(prev: dict, curr: dict) -> list[dict]:
    """Sub-products (and products without sub-products) with enough recent volume."""
    has_subs = {prod for (prod, sub) in curr if sub != "*"}
    base = baseline_growth(prev, curr)
    rows = []
    for (prod, sub), n in curr.items():
        if prod in EXCLUDE_PRODUCTS or n < MIN_VOLUME:
            continue
        if sub == "*" and prod in has_subs:
            continue
        if sub in ("I do not know", "Other debt", "Other type of mortgage"):
            continue  # catch-all buckets don't describe a customer
        p = prev.get((prod, sub), 0)
        growth = (n + 1) / (p + 1)
        rows.append({"product": prod, "sub_product": sub, "prev": p, "curr": n,
                     "growth": round(growth, 2), "rel_growth": round(growth / base, 2)})
    return rows


def _clip(x: float) -> float:
    return round(max(0.0, min(5.0, x)), 1)


def score(row: dict, det: dict | None = None, n_grants: int = 0) -> dict:
    # Growth vs baseline: 1.0x → 1, 1.5x → 3.5, 2x+ → 5
    s_growth = _clip(1 + (row["rel_growth"] - 1) * 5)
    # Volume, log scale: 300 → ~1, 3k → ~3, 30k+ → 5
    s_volume = _clip((math.log10(max(row["curr"], 1)) - 2) * 2 + 0.1)
    s_lmi = lmi_weight(row["product"], row["sub_product"])
    s_spread = s_buyer = None
    if det:
        # One company dominating = enforcement story, not a market.
        s_spread = _clip(5 * (1 - det["top_company_share"]) * min(det["n_states"], 50) / 50)
    s_buyer = _clip(n_grants)
    parts = [s_growth, s_volume, s_lmi] + ([s_spread] if s_spread is not None else []) + [s_buyer]
    weights = [0.30, 0.15, 0.25] + ([0.20] if s_spread is not None else []) + [0.10]
    total = sum(p * w for p, w in zip(parts, weights)) / sum(weights)
    return {**row, "s_growth": s_growth, "s_volume": s_volume, "s_lmi": s_lmi,
            "s_spread": s_spread, "s_buyer": s_buyer, "score": round(total, 2)}


def label(sig: dict) -> str:
    sub, prod = sig["sub_product"], sig["product"]
    if sub == "*":
        return prod
    if sub in ("Loan", "Lease"):  # vehicle sub-products are too generic on their own
        return f"Vehicle {sub.lower()}"
    return sub


def slug(sig: dict) -> str:
    return re.sub(r"[^a-z0-9]+", "-", label(sig).lower()).strip("-")[:40]
