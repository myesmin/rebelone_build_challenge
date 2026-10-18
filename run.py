"""Rebel One idea source: CFPB complaint growth × Grants.gov funding → ranked venture signals.

    python run.py              # full run (Claude API if ANTHROPIC_API_KEY is set)
    python run.py --no-llm     # data + prompts only; analyze with /find-signals or claude.ai
    python run.py --top 8      # number of signals to keep
"""
import argparse
import csv
import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

import cfpb  # noqa: E402
import grants  # noqa: E402
import llm  # noqa: E402
import score  # noqa: E402
from score import label, slug  # noqa: E402
from config import windows  # noqa: E402

OUT = ROOT / "output"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-llm", action="store_true")
    ap.add_argument("--top", type=int, default=8)
    args = ap.parse_args()

    win = windows()
    (p0, p1), (c0, c1) = win
    print(f"Windows: {p0}..{p1} vs {c0}..{c1}")

    prev, curr = cfpb.window_counts(p0, p1), cfpb.window_counts(c0, c1)
    base = score.baseline_growth(prev, curr)
    rows = [score.score(r) for r in score.candidates(prev, curr)]
    rows.sort(key=lambda r: -r["score"])
    print(f"{len(rows)} candidates; baseline growth {base:.2f}x. Enriching top {args.top * 2}…")

    enriched = []
    for r in rows[: args.top * 2]:
        det = cfpb.detail(r["product"], r["sub_product"], c0, c1)
        g = grants.match(r["product"], r["sub_product"])
        enriched.append((score.score(r, det, len(g)), det, g))
    enriched.sort(key=lambda t: -t[0]["score"])
    top = enriched[: args.top]

    OUT.mkdir(exist_ok=True)
    (OUT / "claude_prompts").mkdir(exist_ok=True)
    for old in (OUT / "claude_prompts").glob("*.md"):  # ranks change between runs
        old.unlink()
    (OUT / "analyses").mkdir(exist_ok=True)
    use_api = not args.no_llm and llm.has_key()
    if not args.no_llm and not use_api:
        print("No ANTHROPIC_API_KEY found; writing prompts only (see README: no-key path).")

    with open(OUT / "signals.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["rank", "product", "sub_product", "prev", "curr", "growth",
                                          "rel_growth", "s_growth", "s_volume", "s_lmi", "s_spread",
                                          "s_buyer", "score", "top_company", "top_company_share",
                                          "n_states", "n_grants"])
        w.writeheader()
        for i, (s, det, g) in enumerate(enriched, 1):
            w.writerow({"rank": i, **{k: s[k] for k in w.fieldnames if k in s},
                        "top_company": det["top_companies"][0][0] if det["top_companies"] else "",
                        "top_company_share": round(det["top_company_share"], 3),
                        "n_states": det["n_states"], "n_grants": len(g)})

    sections = []
    for i, (s, det, g) in enumerate(top, 1):
        name = slug(s)
        pack = llm.signal_pack(s, det, g, win)
        (OUT / "claude_prompts" / f"{i:02d}_{name}.md").write_text(llm.prompt_file(pack))
        (OUT / "claude_prompts" / f"{i:02d}_{name}.pack.md").write_text(pack)
        analysis_path = OUT / "analyses" / f"{name}.md"
        if use_api and not analysis_path.exists():
            print(f"  Claude → {name}")
            analysis_path.write_text(llm.analyze(pack))
        analysis = analysis_path.read_text() if analysis_path.exists() else (
            f"_Not analyzed yet. Run `/find-signals` in Claude Code, or paste "
            f"`output/claude_prompts/{i:02d}_{name}.md` into claude.ai and save the answer to "
            f"`output/analyses/{name}.md`._")
        sections.append(f"## {i}. {label(s)}"
                        f" (score {s['score']})\n\n{pack.split(chr(10), 1)[1]}\n\n"
                        f"### Claude analysis\n\n{analysis}\n")

    table = ["| # | Signal | Complaints (prev → recent) | Growth | vs baseline | LMI | Spread | Grants | Score |",
             "|---|---|---|---|---|---|---|---|---|"]
    for i, (s, det, g) in enumerate(top, 1):
        table.append(f"| {i} | {label(s)} <br><sub>{s['product']}</sub> | {s['prev']:,} → {s['curr']:,} | "
                     f"{s['growth']}x | {s['rel_growth']}x | {s['s_lmi']} | {s['s_spread']} | "
                     f"{len(g)} | **{s['score']}** |")

    report = f"""# Rebel One idea source: complaint signals
_Generated {date.today().isoformat()} · windows {p0}..{p1} vs {c0}..{c1} · baseline growth \
{base:.2f}x (all products except credit reporting)_

**Method.** Pull every CFPB consumer complaint count by product and sub-product for two \
12-month windows. Rank sub-products by growth relative to the baseline, volume, and LMI \
relevance. Enrich the leaders with company concentration, geographic spread and matching \
open federal grants (Grants.gov). Then Claude screens each signal against the rubric in \
`.claude/skills/venture-screen/references/rubric.md`.

{chr(10).join(table)}

{chr(10).join(sections)}
"""
    (OUT / "report.md").write_text(report)
    totals = {"prev_all": sum(v for (_, sub), v in prev.items() if sub == "*"),
              "curr_all": sum(v for (_, sub), v in curr.items() if sub == "*")}
    (OUT / "run_meta.json").write_text(json.dumps({"windows": win, "baseline": base,
                                                   "candidates": len(rows), "llm": use_api,
                                                   "generated": date.today().isoformat(),
                                                   **totals}))
    import dashboard
    dashboard.build()
    print(f"Wrote {OUT/'report.md'}, {OUT/'signals.csv'}, {len(top)} prompts.")


if __name__ == "__main__":
    main()
