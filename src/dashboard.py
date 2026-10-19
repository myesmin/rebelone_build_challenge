"""Static dashboard: output/ → docs/index.html (single file, no server; GitHub Pages-ready)."""
import csv
import html
import json
import re
import sys
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))  # config.py, when run standalone

from score import label, slug  # noqa: E402

OUT = ROOT / "output"
DOCS = ROOT / "docs"


def _verdict(memo: str) -> str:
    m = re.search(r"\*\*Verdict:\s*(Pursue|Watch|Discard)", memo or "")
    return m.group(1) if m else ""


def _first_sentence(memo: str) -> str:
    m = re.search(r"\*\*Verdict:[^*]*\*\*\.?\s*(.+)", memo or "")
    return m.group(1).strip().replace("*", "") if m else ""


def _section(pack: str, name: str) -> str:
    m = re.search(rf"## {name}.*?\n(.*?)(?=\n## |\Z)", pack, flags=re.S)
    return m.group(1) if m else ""


def _issues(pack: str) -> list[dict]:
    out = []
    for line in _section(pack, "Top issues").splitlines():
        m = re.match(r"- (.+?): ([\d,]+)", line)
        if m:
            out.append({"issue": m.group(1), "n": int(m.group(2).replace(",", ""))})
    return out[:4]


def _grants(pack: str) -> list[str]:
    return [l[2:].split(":")[0] for l in _section(pack, "Matching federal funding").splitlines()
            if l.startswith("- ") and "none found" not in l]


def build() -> Path:
    meta = json.loads((OUT / "run_meta.json").read_text())
    rows = list(csv.DictReader(open(OUT / "signals.csv")))
    packs = {re.sub(r"^\d+_", "", p.name[:-8]): p.read_text()
             for p in (OUT / "claude_prompts").glob("*.pack.md")}
    signals = []
    for r in rows:
        s = slug(r)
        memo_p, api_p = OUT / "analyses" / f"{s}.md", OUT / "analyses_api" / f"{s}.md"
        memo = memo_p.read_text() if memo_p.exists() else ""
        api = api_p.read_text() if api_p.exists() else ""
        pack = packs.get(s, "")
        signals.append({
            "rank": int(r["rank"]), "label": label(r), "product": r["product"], "slug": s,
            "prev": int(r["prev"]), "curr": int(r["curr"]), "growth": float(r["growth"]),
            "rel": float(r["rel_growth"]), "score": float(r["score"]), "lmi": float(r["s_lmi"]),
            "top_company": r["top_company"], "top_share": float(r["top_company_share"]),
            "n_states": int(r["n_states"]), "n_grants": int(r["n_grants"]),
            "grants": _grants(pack), "issues": _issues(pack),
            "verdict": _verdict(memo), "api": _verdict(api),
            "why": html.escape(_first_sentence(memo)),
            "memo": markdown.markdown(memo, extensions=["tables"]) if memo else "",
            "api_memo": markdown.markdown(api, extensions=["tables"]) if api else "",
        })
    (p0, p1), (c0, c1) = meta["windows"]
    meta_out = {"baseline": round(meta["baseline"], 2), "candidates": meta["candidates"],
                "total": meta.get("curr_all", 0), "prev_total": meta.get("prev_all", 0),
                "windows": f"{p0} → {p1} vs {c0} → {c1}", "generated": meta.get("generated", c1)}
    page = TEMPLATE.replace("__DATA__", json.dumps(signals)).replace("__META__", json.dumps(meta_out))
    DOCS.mkdir(exist_ok=True)
    out = DOCS / "index.html"
    out.write_text(page)
    return out


TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Rebel One · Idea Source Dashboard</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root {
  --bg: #0b1129; --bg2: rgba(120,150,255,.05); --panel: rgba(22,32,72,.62); --panel2: rgba(30,42,90,.6);
  --line: rgba(110,140,255,.14); --grid: rgba(110,140,255,.09);
  --ink: #e9eeff; --ink2: #a7b2d6; --ink3: #6f7ba6;
  --accent: #3aa0ff; --accent-soft: rgba(58,160,255,.15);
  --muted-bar: rgba(140,160,220,.28); --pursue: #34d6f5; --watch: #2f74e8; --discard: #55618f; --alert: #e0708a;
  --quad: rgba(58,160,255,.06); --quad-line: rgba(58,160,255,.3); --quad-ink: #8fd0ff; --limit-ink: #f2a3b6;
  --limit-zone: rgba(224,112,138,.07); --empty-dot: rgba(140,160,220,.06); --dot-ring: rgba(255,255,255,.35);
  --tip-bg: rgba(12,18,48,.94); --body-bg: radial-gradient(1100px 700px at 85% -15%, rgba(58,120,255,.14) 0%, transparent 60%),
    radial-gradient(900px 600px at -10% 40%, rgba(52,214,245,.06) 0%, transparent 60%),
    radial-gradient(800px 500px at 50% 110%, rgba(58,120,255,.08) 0%, transparent 60%), #0b1129;
}
:root[data-theme="light"] {
  --bg: #eef3fb; --bg2: rgba(40,70,140,.04); --panel: rgba(255,255,255,.72); --panel2: rgba(255,255,255,.85);
  --line: rgba(40,70,140,.14); --grid: rgba(40,70,140,.09);
  --ink: #0f1b3d; --ink2: #44527a; --ink3: #6b779c;
  --accent: #1f6fe0; --accent-soft: rgba(31,111,224,.10);
  --muted-bar: rgba(70,90,150,.22); --pursue: #0b9fc2; --watch: #2f6fe8; --discard: #8b94b5; --alert: #c84a66;
  --quad: rgba(31,111,224,.06); --quad-line: rgba(31,111,224,.35); --quad-ink: #1f5fc4; --limit-ink: #b23a57;
  --limit-zone: rgba(200,74,102,.07); --empty-dot: rgba(70,90,150,.06); --dot-ring: #fff;
  --tip-bg: rgba(255,255,255,.96); --body-bg: radial-gradient(1100px 700px at 85% -15%, rgba(58,120,255,.12) 0%, transparent 60%),
    radial-gradient(900px 600px at -10% 40%, rgba(52,214,245,.10) 0%, transparent 60%), #eef3fb;
}
:root[data-theme="light"] .chip.Pursue { background: rgba(11,159,194,.10); color: #06708a; border-color: rgba(11,159,194,.35); }
:root[data-theme="light"] .chip.Watch { background: rgba(47,111,232,.10); color: #1f4fb0; border-color: rgba(47,111,232,.35); }
:root[data-theme="light"] .chip.Discard { background: rgba(139,148,181,.14); color: #4c5578; border-color: rgba(139,148,181,.4); }
:root[data-theme="light"] .agree { color: #06708a; } :root[data-theme="light"] .flag { color: #b23a57; }
:root[data-theme="light"] .panel, :root[data-theme="light"] .kpi { box-shadow: 0 6px 24px rgba(30,50,110,.08); }
:root[data-theme="light"] .tip { box-shadow: 0 10px 30px rgba(30,50,110,.18); }
svg .t-quad { fill: var(--quad-ink); } svg .t-limit { fill: var(--limit-ink); }
.theme-btn { background: var(--bg2); border: 1px solid var(--line); color: var(--ink); border-radius: 999px; padding: 6px 12px;
  font: inherit; font-size: 13px; cursor: pointer; margin-left: 6px; }
.theme-btn:hover { background: var(--accent-soft); }
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body { margin: 0; background: var(--body-bg); background-attachment: fixed; transition: background .3s;
  color: var(--ink); font: 14px/1.5 Inter, -apple-system, "Segoe UI", sans-serif; min-height: 100vh; }
.wrap { max-width: 1320px; margin: 0 auto; padding: 20px 24px 60px; }
.topbar { display: flex; align-items: center; justify-content: space-between; gap: 16px; padding: 14px 22px;
  border-radius: 16px; background: rgba(255,255,255,.04); border: 1px solid var(--line);
  backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px); }
.brand { display: flex; align-items: center; gap: 12px; }
.logo { width: 38px; height: 38px; border-radius: 11px; background: var(--accent-soft); color: var(--accent); border: 1px solid rgba(58,160,255,.35); display: grid; place-items: center;
  font-weight: 800; font-size: 15px; letter-spacing: -.02em; }
.brand b { font-size: 16px; font-weight: 600; display: block; line-height: 1.1; } .brand span { font-size: 11.5px; color: var(--ink3); }
.nav { display: flex; gap: 6px; flex-wrap: wrap; }
.nav a { color: var(--ink2); text-decoration: none; font-size: 13px; font-weight: 500; padding: 7px 13px; border-radius: 999px; }
.nav a:hover { background: rgba(255,255,255,.06); color: var(--ink); }
.hero { display: flex; justify-content: space-between; align-items: flex-end; gap: 20px; margin: 26px 4px 18px; flex-wrap: wrap; }
.hero h1 { margin: 0; font-size: 28px; font-weight: 700; letter-spacing: -.02em; }
.hero h1 .a { color: var(--ink); } .hero h1 .b { color: var(--accent); }
.hero p { margin: 6px 0 0; color: var(--ink2); max-width: 760px; }
.pill { display: inline-flex; gap: 8px; align-items: center; background: var(--panel); backdrop-filter: blur(12px); border: 1px solid var(--line);
  border-radius: 12px; padding: 8px 12px; color: var(--ink2); font-size: 12.5px; }
.kpis { display: grid; grid-template-columns: repeat(5, 1fr); gap: 14px; }
.kpi { position: relative; overflow: hidden; background: var(--panel); backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px); border: 1px solid var(--line);
  border-radius: 16px; padding: 16px 16px 14px; display: flex; gap: 14px; align-items: center; }
.kpi .ic { width: 42px; height: 42px; border-radius: 12px; background: var(--accent-soft) !important; border: 1px solid rgba(58,160,255,.3); display: grid; place-items: center; flex: none; }
.kpi .ic svg { width: 24px; height: 24px; }
.kpi .k { font-size: 11px; letter-spacing: .08em; text-transform: uppercase; color: var(--ink2); font-weight: 600; }
.kpi .v { font-size: 26px; font-weight: 700; letter-spacing: -.02em; line-height: 1.15; font-variant-numeric: tabular-nums; }
.kpi .s { font-size: 12px; color: var(--ink3); }
.grid { display: grid; grid-template-columns: repeat(12, 1fr); gap: 14px; margin-top: 14px; }
.panel { background: var(--panel); backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px); box-shadow: inset 0 1px 0 rgba(255,255,255,.05); border: 1px solid var(--line); border-radius: 16px; padding: 18px 18px 12px; min-width: 0; }
.panel h2 { margin: 0; font-size: 15.5px; font-weight: 600; } .q { color: var(--ink2); font-size: 12.5px; margin: 3px 0 10px; }
.read { color: var(--ink3); font-size: 12px; margin: 6px 0 4px; } .read b { color: var(--ink); font-weight: 600; }
.ph { display: flex; justify-content: space-between; align-items: flex-start; gap: 12px; }
.c7 { grid-column: span 7; } .c5 { grid-column: span 5; } .c6 { grid-column: span 6; } .c12 { grid-column: span 12; }
svg { display: block; width: 100%; overflow: visible; }
svg text { fill: var(--ink2); font-family: Inter, sans-serif; font-size: 11.5px; }
svg .t-ink { fill: var(--ink); } svg .t-strong { fill: var(--ink); font-weight: 700; } svg .t-dim { fill: var(--ink3); }
.legend { display: flex; flex-wrap: wrap; gap: 14px; font-size: 12px; color: var(--ink2); margin: 2px 0 6px; }
.legend i { display: inline-block; width: 10px; height: 10px; border-radius: 3px; margin-right: 6px; vertical-align: -1px; }
.legend i.ln { width: 16px; height: 0; border-top: 2px dashed currentColor; border-radius: 0; vertical-align: 3px; }
.seg { display: inline-flex; background: var(--bg2); border: 1px solid var(--line); border-radius: 10px; padding: 3px; flex: none; }
.seg button { background: transparent; color: var(--ink2); border: 0; padding: 5px 11px; border-radius: 7px; font: inherit; font-size: 12px; cursor: pointer; }
.seg button[aria-pressed="true"] { background: var(--accent-soft); color: var(--ink); font-weight: 600; box-shadow: inset 0 0 0 1px rgba(58,160,255,.45); }
.hover-row { cursor: pointer; outline: none; } .hover-row:hover .hl, .hover-row:focus .hl { fill: rgba(255,255,255,.05); }
.chip { display: inline-flex; align-items: center; gap: 6px; font-size: 11.5px; font-weight: 700; border-radius: 999px; padding: 3px 10px; white-space: nowrap; }
.chip { font-weight: 600; } .chip.Pursue { background: rgba(52,214,245,.12); color: #8fe8fb; border: 1px solid rgba(52,214,245,.4); }
.chip.Watch { background: rgba(47,116,232,.16); color: #9fc0ff; border: 1px solid rgba(47,116,232,.45); }
.chip.Discard { background: rgba(85,97,143,.18); color: #aab3d6; border: 1px solid rgba(85,97,143,.45); }
.chip.none { color: var(--ink3); border: 1px dashed var(--line); }
table.t { width: 100%; border-collapse: collapse; font-size: 13px; font-variant-numeric: tabular-nums; }
table.t th { text-align: left; color: var(--ink3); font-weight: 600; font-size: 11.5px; text-transform: uppercase; letter-spacing: .05em; padding: 8px; border-bottom: 1px solid var(--line); }
table.t td { padding: 9px 8px; border-bottom: 1px solid var(--grid); } table.t .n { text-align: right; }
table.t tr:hover td { background: rgba(255,255,255,.03); }
.agree { color: #8fe8fb; font-weight: 600; } .flag { color: #f2b8c6; font-weight: 600; }
.cards { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-top: 14px; }
.sig { scroll-margin-top: 16px; }
.sig h3 { margin: 0; font-size: 17px; } .prod { color: var(--ink3); font-size: 12px; }
.verd { display: grid; gap: 5px; justify-items: end; font-size: 11px; color: var(--ink3); }
.mini { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; margin: 14px 0; }
.mini div { background: var(--bg2); border: 1px solid var(--line); border-radius: 12px; padding: 8px 10px; font-size: 11px; color: var(--ink3); }
.mini b { display: block; font-size: 18px; color: var(--ink); font-variant-numeric: tabular-nums; }
.why { color: var(--ink2); margin: 0 0 12px; }
.iss { margin: 4px 0 12px; } .iss .r { display: grid; grid-template-columns: 1fr 64px; gap: 10px; align-items: center; margin: 6px 0; font-size: 12.5px; }
.iss .bar { height: 7px; border-radius: 4px; background: var(--grid); overflow: hidden; margin-top: 4px; }
.iss .bar span { display: block; height: 100%; border-radius: 4px; background: linear-gradient(90deg, #2f6fe8, #34d6f5); }
.iss .nn { text-align: right; color: var(--ink2); font-variant-numeric: tabular-nums; }
.isshead { font-size: 11px; text-transform: uppercase; letter-spacing: .06em; color: var(--ink3); font-weight: 600; }
details { border-top: 1px solid var(--grid); padding-top: 8px; margin-top: 10px; }
details summary { cursor: pointer; color: var(--accent); font-size: 13px; font-weight: 600; }
.memo { font-size: 13.5px; color: var(--ink2); } .memo h3 { display: none; } .memo strong { color: var(--ink); }
.memo table { border-collapse: collapse; } .memo td, .memo th { border: 1px solid var(--line); padding: 4px 10px; }
.rub { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }
.rub div { background: var(--bg2); border: 1px solid var(--line); border-radius: 14px; padding: 12px 14px; }
.rub b { display: block; margin-bottom: 3px; } .rub p { margin: 0; color: var(--ink2); font-size: 13px; }
.tip { position: fixed; pointer-events: none; background: var(--tip-bg); backdrop-filter: blur(10px); color: var(--ink); border: 1px solid var(--line); border-radius: 12px;
  padding: 10px 12px; font-size: 12.5px; box-shadow: 0 10px 30px rgba(0,0,0,.4); max-width: 320px; opacity: 0; transition: opacity .08s; z-index: 20; }
.tip .m { color: var(--ink3); }
footer { color: var(--ink3); font-size: 12px; margin-top: 26px; } a { color: var(--accent); }
h2.sec { font-size: 19px; margin: 30px 4px 0; }
@media (max-width: 1100px) { .kpis { grid-template-columns: repeat(3, 1fr); } .c7,.c5,.c6 { grid-column: span 12; } .cards, .rub { grid-template-columns: 1fr; } }
</style>
</head>
<body>
<div class="wrap">

<div class="topbar">
  <div class="brand"><div class="logo">R1</div><div><b>Rebel One · Idea Source</b><span>Consumer complaints × federal funding</span></div></div>
  <nav class="nav"><a href="#overview">Overview</a><a href="#growth">Growth</a><a href="#noise">Noise filters</a><a href="#signals">Signals</a><a href="#method">Method</a>
    <button class="theme-btn" id="themeBtn" type="button" aria-label="Toggle day and night mode">☀ Day</button></nav>
</div>

<div class="hero" id="overview">
  <div>
    <h1><span class="a">Where families are hurting,</span> <span class="b">and who's paying to fix it</span></h1>
    <p>Bills tell you the rules changed. <b>Complaints</b> tell you who's hurting. <b>Grants</b> tell you who's paying to fix it.
      Built from the CFPB Consumer Complaint Database and Grants.gov, and screened twice by Claude.</p>
  </div>
  <div class="pill" id="win"></div>
</div>

<div class="kpis" id="kpis"></div>

<div class="grid">
  <div class="panel c7">
    <h2>Opportunity map</h2><p class="q">Which problems are big <i>and</i> growing faster than the market?</p>
    <div class="legend"><span><i style="background:var(--pursue)"></i>Pursue</span><span><i style="background:var(--watch)"></i>Watch</span><span><i style="background:var(--discard)"></i>Discard</span><span><i style="background:transparent;border:1.5px solid var(--ink3)"></i>Not screened</span><span>Bubble size = relevance to low- and middle-income families</span></div>
    <svg id="map"></svg>
    <p class="read">How to read it: the <b>top-right</b> is the sweet spot, with lots of complaints growing faster than complaints overall. Hover any bubble; click to open its memo.</p>
  </div>
  <div class="c5" style="display:grid;gap:14px;align-content:start">
    <div class="panel">
      <h2>Screening funnel</h2><p class="q">How many problems survive each filter?</p>
      <svg id="funnel"></svg>
    </div>
    <div class="panel">
      <div class="ph"><div><h2>Verdicts</h2><p class="q">What Claude recommended for the 8 screened signals</p></div>
        <div class="seg" id="donutSeg"><button data-k="verdict" aria-pressed="true">Review</button><button data-k="api" aria-pressed="false">API</button></div></div>
      <svg id="donut"></svg>
    </div>
  </div>
</div>

<div class="grid" id="growth">
  <div class="panel c6">
    <div class="ph"><div><h2>Growth vs the market</h2><p class="q">Year-over-year complaint growth by problem</p></div>
      <div class="seg" id="gSeg"><button data-s="growth" aria-pressed="true">By growth</button><button data-s="score" aria-pressed="false">By score</button></div></div>
    <div class="legend"><span><i style="background:linear-gradient(90deg,#2f6fe8,#34d6f5)"></i>Faster than market</span><span><i style="background:var(--muted-bar)"></i>At or below market</span><span style="color:var(--ink)"><i class="ln"></i>Market baseline</span></div>
    <svg id="gbars"></svg>
  </div>
  <div class="panel c6">
    <h2>Last year vs this year</h2><p class="q">The complaint volumes behind the growth, for the 8 screened signals</p>
    <div class="legend"><span><i style="background:var(--muted-bar)"></i>Oct 2024 – Sep 2025</span><span><i style="background:linear-gradient(90deg,#2f6fe8,#34d6f5)"></i>Oct 2025 – Sep 2026</span></div>
    <svg id="pair"></svg>
  </div>
</div>

<div class="grid" id="noise">
  <div class="panel c6">
    <h2>Is it one bad company?</h2><p class="q">Share of complaints aimed at the single largest company</p>
    <div class="legend"><span><i style="background:linear-gradient(90deg,#2f6fe8,#34d6f5)"></i>Spread across many companies (a market)</span><span><i style="background:var(--alert)"></i>Over 40%: a story for regulators</span></div>
    <svg id="conc"></svg>
  </div>
  <div class="panel c6">
    <h2>Two screens, one decision</h2><p class="q">Claude Code (review) and the Claude API screened each signal with the same rules</p>
    <table class="t" id="agree"></table>
    <p class="read">Where the screens disagree, a person makes the call. They agreed on <b id="agreeN"></b> signals.</p>
  </div>
</div>

<h2 class="sec" id="signals">Screened signals</h2>
<div class="ph" style="margin:8px 4px 0;align-items:center"><p class="q" style="margin:0">Each card shows the top complaint issues and both Claude memos.</p>
  <div class="seg" id="fSeg"><button data-f="all" aria-pressed="true">All</button><button data-f="Pursue" aria-pressed="false">Pursue</button><button data-f="Watch" aria-pressed="false">Watch</button><button data-f="Discard" aria-pressed="false">Discard</button></div></div>
<div class="cards" id="cards"></div>

<h2 class="sec" id="method">How we separate signal from noise</h2>
<div class="panel" style="margin-top:12px">
  <div class="rub">
    <div><b>Growth vs the market</b><p>Raw growth misleads. Each problem is compared with all complaints (credit reporting excluded, about 6M a year).</p></div>
    <div><b>Spread</b><p>If one company is more than 40% of complaints, it's a story for regulators, not a market.</p></div>
    <div><b>Lasting, not one-off</b><p>"Fees I didn't expect" counts more than "account frozen during a system change."</p></div>
    <div><b>Relevance to low- and middle-income families</b><p>Payday loans, benefit cards, FHA and USDA mortgages, money transfers, and medical or rental debt score highest.</p></div>
    <div><b>A buyer exists</b><p>A matching open grant, employer, lender or agency. No grant can also mean an open market.</p></div>
    <div><b>Two screens</b><p>Claude Code and the Claude API decide Pursue, Watch or Discard separately. Disagreements go to a person.</p></div>
  </div>
</div>

<div class="panel" style="margin-top:14px">
  <h2>All 16 enriched candidates</h2><p class="q">Table view of every chart above</p>
  <div style="overflow-x:auto"><table class="t" id="table"></table></div>
</div>

<footer>Sources: <a href="https://www.consumerfinance.gov/data-research/consumer-complaints/">CFPB Consumer Complaint Database</a> (public API) ·
  <a href="https://www.grants.gov/">Grants.gov</a> (search2 API). Complaints aren't verified by CFPB and don't measure total harm.
  CFPB stopped publishing complaint narratives in 2026, so memos use structured fields only. Built with Claude Code ·
  <a href="https://github.com/myesmin/rebelone_build_challenge">Source code</a></footer>
</div>
<div class="tip" id="tip"></div>

<script>
const DATA = __DATA__, META = __META__;
const themeBtn = document.getElementById("themeBtn");
function setTheme(t) { document.documentElement.dataset.theme = t; themeBtn.textContent = t === "light" ? "☾ Night" : "☀ Day";
  try { localStorage.setItem("r1-theme", t); } catch (e) {} }
setTheme((() => { try { return localStorage.getItem("r1-theme"); } catch (e) { return null; } })() || "dark");
themeBtn.onclick = () => setTheme(document.documentElement.dataset.theme === "light" ? "dark" : "light");
const VC = {Pursue: "var(--pursue)", Watch: "var(--watch)", Discard: "var(--discard)"};
const fmt = n => n.toLocaleString("en-US"), pct = x => Math.round(x * 100) + "%";
const short = n => n >= 1e6 ? (n / 1e6).toFixed(1) + "M" : n >= 1e3 ? (n / 1e3).toFixed(1).replace(".0", "") + "k" : String(n);
const chip = v => v ? `<span class="chip ${v}">${{Pursue: "✓", Watch: "◐", Discard: "✕"}[v]} ${v}</span>` : `<span class="chip none">–</span>`;
const screened = DATA.filter(d => d.memo);
const tip = document.getElementById("tip");
function showTip(e, h) { tip.innerHTML = h; const r = e.currentTarget.getBoundingClientRect();
  const x = e.clientX || r.left + 60, y = e.clientY || r.top; tip.style.left = Math.min(x + 14, innerWidth - 340) + "px"; tip.style.top = (y + 14) + "px"; tip.style.opacity = 1; }
function hideTip() { tip.style.opacity = 0; }
function tipFor(d) { return `<b>${d.label}</b> <span class="m">· ${d.product}</span><br>${fmt(d.prev)} → <b>${fmt(d.curr)}</b> complaints
  (${d.growth.toFixed(2)}x; ${d.rel.toFixed(2)}x the market)<br><span class="m">Top company:</span> ${d.top_company} (${pct(d.top_share)})<br>
  <span class="m">States:</span> ${d.n_states} · <span class="m">Grants:</span> ${d.n_grants} · <span class="m">Score:</span> ${d.score.toFixed(2)}
  ${d.verdict ? `<br><span class="m">Review:</span> ${d.verdict} · <span class="m">API:</span> ${d.api || "–"}` : "<br><span class='m'>Not screened by Claude</span>"}`; }
function bindRows(svg) { svg.querySelectorAll("[data-i]").forEach(g => { const d = DATA[+g.dataset.i];
  g.addEventListener("mousemove", e => showTip(e, tipFor(d))); g.addEventListener("focus", e => showTip(e, tipFor(d)));
  g.addEventListener("mouseleave", hideTip); g.addEventListener("blur", hideTip);
  const go = () => { const el = document.getElementById("sig-" + d.slug); if (el) { el.scrollIntoView({behavior: "smooth"}); el.querySelector("details")?.setAttribute("open", ""); } };
  g.addEventListener("click", go); g.addEventListener("keydown", e => e.key === "Enter" && go()); }); }
const W = el => Math.max(320, el.getBoundingClientRect().width || 600);
const gradDefs = `<defs><linearGradient id="gt" x1="0" x2="1"><stop offset="0" stop-color="#2f6fe8"/><stop offset="1" stop-color="#34d6f5"/></linearGradient></defs>`;
const rbar = (x, y, w, h, fill) => w <= 0 ? "" : `<path d="M${x},${y} h${Math.max(0, w - 4)} a4,4 0 0 1 4,4 v${h - 8} a4,4 0 0 1 -4,4 h-${Math.max(0, w - 4)} z" fill="${fill}"/>`;
const setSvg = (svg, w, h, s) => { svg.setAttribute("viewBox", `0 0 ${w} ${h}`); svg.setAttribute("height", h); svg.innerHTML = s; };

// Header + KPIs
document.getElementById("win").innerHTML = META.windows;
const fastest = [...DATA].sort((a, b) => b.growth - a.growth)[0];
const nP = screened.filter(d => d.verdict === "Pursue").length, nAgree = screened.filter(d => d.api && d.api === d.verdict).length;
const icon = (bg, path) => `<div class="ic" style="background:${bg}"><svg viewBox="0 0 24 24" fill="none" stroke="#5fb6ff" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">${path}</svg></div>`;
document.getElementById("kpis").innerHTML = [
  [icon("linear-gradient(135deg,#2f8ff0,#22c7a0)", '<path d="M4 4h16v12H7l-3 3z"/><path d="M8 9h8M8 12h5"/>'), "Complaints analyzed", short(META.total), `last 12 months · was ${short(META.prev_total)}`],
  [icon("linear-gradient(135deg,#7a5cff,#2f8ff0)", '<path d="M3 17l6-6 4 4 8-8"/><path d="M15 7h6v6"/>'), "Market baseline", "+" + Math.round((META.baseline - 1) * 100) + "%", "growth of all complaints (excl. credit reports)"],
  [icon("linear-gradient(135deg,#f6b73c,#ff7b54)", '<path d="M12 3l2.6 5.6 6.1.7-4.5 4.2 1.2 6L12 16.5 6.6 19.5l1.2-6L3.3 9.3l6.1-.7z"/>'), "Fastest grower", "+" + Math.round((fastest.growth - 1) * 100) + "%", fastest.label + " (mostly BNPL)"],
  [icon("linear-gradient(135deg,#22c7a0,#33d17a)", '<path d="M4 5h16l-6 7v6l-4 2v-8z"/>'), "Screened", `${META.candidates} → ${screened.length}`, "problems → Claude venture memos"],
  [icon("linear-gradient(135deg,#33d17a,#1aa5a0)", '<path d="M5 12l4 4L19 6"/>'), "Pursue", String(nP), `screens agree on ${nAgree} of ${screened.length}`],
].map(([ic, k, v, s]) => `<div class="kpi">${ic}<div><div class="k">${k}</div><div class="v">${v}</div><div class="s">${s}</div></div></div>`).join("");

// Opportunity map: x = volume (log), y = growth vs market
function drawMap() {
  const svg = document.getElementById("map"), w = W(svg), h = 400, L = 56, R = 16, T = 12, B = 42, pw = w - L - R, ph = h - T - B;
  const lx0 = Math.log10(250), lx1 = Math.log10(40000), x = v => L + (Math.log10(v) - lx0) / (lx1 - lx0) * pw;
  const yMin = 0.9, yMax = 1.72, y = v => T + (yMax - v) / (yMax - yMin) * ph;
  let s = "";
  s += `<rect x="${x(3000)}" y="${y(yMax)}" width="${x(40000) - x(3000)}" height="${y(1.0) - y(yMax)}" rx="12" fill="var(--quad)" stroke="var(--quad-line)" stroke-dasharray="4 4"/>`;
  s += `<text x="${x(40000) - 12}" y="${y(yMax) + 20}" text-anchor="end" class="t-quad" style="font-weight:600">Big and growing faster than the market</text>`;
  [300, 1000, 3000, 10000, 30000].forEach(t => { s += `<line x1="${x(t)}" x2="${x(t)}" y1="${T}" y2="${T + ph}" stroke="var(--grid)"/><text x="${x(t)}" y="${T + ph + 18}" text-anchor="middle">${short(t)}</text>`; });
  [1.0, 1.2, 1.4, 1.6].forEach(t => { s += `<line x1="${L}" x2="${L + pw}" y1="${y(t)}" y2="${y(t)}" stroke="var(--grid)"/><text x="${L - 8}" y="${y(t) + 4}" text-anchor="end">${t.toFixed(1)}x</text>`; });
  s += `<line x1="${L}" x2="${L + pw}" y1="${y(1)}" y2="${y(1)}" stroke="var(--ink)" stroke-width="1.5" stroke-dasharray="5 4"/>`;
  s += `<text x="${L + 8}" y="${y(1) + 16}" class="t-ink">Market baseline (1.0x)</text>`;
  s += `<text x="${L + pw / 2}" y="${h - 4}" text-anchor="middle" class="t-dim">Complaints in the last 12 months (log scale) →</text>`;
  s += `<text transform="translate(14 ${T + ph / 2}) rotate(-90)" text-anchor="middle" class="t-dim">Growth vs the market →</text>`;
  const pts = DATA.map((d, i) => ({d, i, cx: x(d.curr), cy: y(Math.min(Math.max(d.rel, yMin), yMax)), r: 5 + d.lmi * 2.2})).sort((a, b) => b.r - a.r);
  pts.forEach(p => { const c = VC[p.d.verdict]; s += `<g class="hover-row" tabindex="0" data-i="${p.i}"><circle cx="${p.cx}" cy="${p.cy}" r="${p.r + 6}" fill="transparent"/>
    <circle cx="${p.cx}" cy="${p.cy}" r="${p.r}" fill="${c || "var(--empty-dot)"}" fill-opacity="${c ? .75 : 1}" stroke="${c ? "var(--dot-ring)" : "var(--ink3)"}" stroke-width="${c ? 2 : 1.5}"/></g>`; });
  const placed = [];
  pts.filter(p => p.d.verdict).sort((a, b) => a.cy - b.cy).forEach(p => {
    let ly = p.cy + 4, lx = p.cx + p.r + 7, anchor = "start";
    if (lx + p.d.label.length * 7 > L + pw) { lx = p.cx - p.r - 7; anchor = "end"; }
    while (placed.some(q => Math.abs(q.y - ly) < 15 && Math.abs(q.x - lx) < 130)) ly += 15;
    placed.push({x: lx, y: ly}); s += `<text x="${lx}" y="${ly}" text-anchor="${anchor}" class="t-ink" style="font-weight:600;pointer-events:none">${p.d.label}</text>`; });
  setSvg(svg, w, h, s); bindRows(svg);
}

// Funnel
function drawFunnel() {
  const svg = document.getElementById("funnel"), w = W(svg);
  const both = screened.filter(d => d.verdict === "Pursue" && d.api === "Pursue").length;
  const st = [["problems with 300+ complaints", META.candidates], ["enriched with issues, companies, grants", DATA.length],
    ["screened by Claude", screened.length], ["marked Pursue (review)", nP], ["Pursue from both screens", both]];
  const rowH = 40, h = st.length * rowH, maxW = w * 0.5; let s = gradDefs;
  st.forEach(([name, n], i) => { const bw = Math.max(10, n / st[0][1] * maxW), yy = i * rowH, x0 = (maxW - bw) / 2;
    s += `<rect x="${x0}" y="${yy + 4}" width="${bw}" height="${rowH - 10}" rx="8" fill="url(#gt)" fill-opacity="${0.95 - i * 0.12}"/>`;
    s += `<text x="${maxW / 2}" y="${yy + 24}" text-anchor="middle" style="fill:var(--ink);font-weight:700;font-size:14px">${n}</text>`;
    s += `<text x="${maxW + 14}" y="${yy + 20}" class="t-ink">${name}</text>`;
    if (i) s += `<text x="${maxW + 14}" y="${yy + 34}" class="t-dim">${Math.round(n / st[i - 1][1] * 100)}% of the step before</text>`; });
  setSvg(svg, w, h, s);
}

// Donut
let donutKey = "verdict";
function drawDonut() {
  const svg = document.getElementById("donut"), w = W(svg), h = 168, cx = 84, cy = 82, R = 72, r = 50;
  const parts = ["Pursue", "Watch", "Discard"].map(v => [v, screened.filter(d => d[donutKey] === v)]);
  const tot = parts.reduce((a, p) => a + p[1].length, 0); let a0 = -Math.PI / 2, s = "";
  const arc = (a1, a2) => { const g = 0.035, p = (rad, a) => [cx + rad * Math.cos(a), cy + rad * Math.sin(a)], lg = a2 - a1 > Math.PI ? 1 : 0;
    const [x1, y1] = p(R, a1 + g), [x2, y2] = p(R, a2 - g), [x3, y3] = p(r, a2 - g), [x4, y4] = p(r, a1 + g);
    return `M${x1},${y1} A${R},${R} 0 ${lg} 1 ${x2},${y2} L${x3},${y3} A${r},${r} 0 ${lg} 0 ${x4},${y4}Z`; };
  parts.forEach(([v, ds]) => { if (!ds.length) return; const a1 = a0 + ds.length / tot * 2 * Math.PI; s += `<path d="${arc(a0, a1)}" fill="${VC[v]}" fill-opacity=".8"/>`; a0 = a1; });
  s += `<text x="${cx}" y="${cy + 4}" text-anchor="middle" class="t-strong" style="font-size:28px">${tot}</text><text x="${cx}" y="${cy + 22}" text-anchor="middle">screened</text>`;
  parts.forEach(([v, ds], i) => { const yy = 34 + i * 46, lx = 186;
    s += `<rect x="${lx}" y="${yy - 11}" width="12" height="12" rx="3" fill="${VC[v]}"/><text x="${lx + 20}" y="${yy}" class="t-ink" style="font-weight:700">${v}</text>`;
    s += `<text x="${w - 4}" y="${yy}" text-anchor="end" class="t-strong" style="font-size:17px">${ds.length}</text>`;
    const names = ds.map(d => d.label).join(", "); s += `<text x="${lx + 20}" y="${yy + 16}" class="t-dim">${names.length > 52 ? names.slice(0, 50) + "…" : names || "none"}</text>`; });
  setSvg(svg, w, h, s);
}
document.querySelectorAll("#donutSeg button").forEach(b => b.onclick = () => { donutKey = b.dataset.k;
  document.querySelectorAll("#donutSeg button").forEach(o => o.setAttribute("aria-pressed", o === b)); drawDonut(); });

// Growth bars vs baseline
let gSort = "growth";
function drawGrowth() {
  const svg = document.getElementById("gbars"), w = W(svg), rows = [...DATA].sort((a, b) => b[gSort] - a[gSort]);
  const L = 176, R = 52, T = 24, rowH = 25, pw = w - L - R, h = T + rows.length * rowH + 24, max = 2, base = META.baseline;
  const x = v => L + v / max * pw; let s = gradDefs;
  [0, 0.5, 1, 1.5, 2].forEach(t => { s += `<line x1="${x(t)}" x2="${x(t)}" y1="${T - 4}" y2="${h - 24}" stroke="var(--grid)"/><text x="${x(t)}" y="${h - 6}" text-anchor="middle">${t.toFixed(1)}x</text>`; });
  rows.forEach((d, i) => { const yy = T + i * rowH, up = d.growth > base;
    s += `<g class="hover-row" tabindex="0" data-i="${DATA.indexOf(d)}"><rect class="hl" x="0" y="${yy}" width="${w}" height="${rowH}" rx="6" fill="transparent"/>
      <text x="${L - 10}" y="${yy + 17}" text-anchor="end" class="${d.verdict ? "t-ink" : ""}" style="${d.verdict ? "font-weight:600" : ""}">${d.label}</text>
      ${rbar(x(0), yy + 5, x(d.growth) - x(0), 15, up ? "url(#gt)" : "var(--muted-bar)")}
      <text x="${x(d.growth) + 8}" y="${yy + 17}" class="t-ink" style="font-weight:600">+${Math.round((d.growth - 1) * 100)}%</text></g>`; });
  s += `<line x1="${x(base)}" x2="${x(base)}" y1="${T - 12}" y2="${h - 24}" stroke="var(--ink)" stroke-width="1.5" stroke-dasharray="5 4"/>`;
  s += `<text x="${x(base) + 6}" y="${T - 10}" class="t-ink" style="font-weight:600">market +${Math.round((base - 1) * 100)}%</text>`;
  setSvg(svg, w, h, s); bindRows(svg);
}
document.querySelectorAll("#gSeg button").forEach(b => b.onclick = () => { gSort = b.dataset.s;
  document.querySelectorAll("#gSeg button").forEach(o => o.setAttribute("aria-pressed", o === b)); drawGrowth(); });

// Paired bars: last year vs this year
function drawPair() {
  const svg = document.getElementById("pair"), w = W(svg), rows = [...screened].sort((a, b) => b.curr - a.curr);
  const L = 150, R = 56, T = 6, rowH = 50, pw = w - L - R, h = T + rows.length * rowH + 24, max = Math.ceil(Math.max(...rows.map(d => d.curr)) / 5000) * 5000;
  const x = v => L + v / max * pw; let s = gradDefs;
  for (let t = 0; t <= max; t += 5000) s += `<line x1="${x(t)}" x2="${x(t)}" y1="${T}" y2="${h - 24}" stroke="var(--grid)"/><text x="${x(t)}" y="${h - 6}" text-anchor="middle">${short(t)}</text>`;
  rows.forEach((d, i) => { const yy = T + i * rowH;
    s += `<g class="hover-row" tabindex="0" data-i="${DATA.indexOf(d)}"><rect class="hl" x="0" y="${yy}" width="${w}" height="${rowH}" rx="6" fill="transparent"/>
      <text x="${L - 10}" y="${yy + 22}" text-anchor="end" class="t-ink" style="font-weight:600">${d.label}</text>
      <text x="${L - 10}" y="${yy + 37}" text-anchor="end" class="t-dim">+${Math.round((d.growth - 1) * 100)}%</text>
      ${rbar(x(0), yy + 8, x(d.prev) - x(0), 13, "var(--muted-bar)")}${rbar(x(0), yy + 25, x(d.curr) - x(0), 16, "url(#gt)")}
      <text x="${x(d.prev) + 6}" y="${yy + 18}" class="t-dim">${short(d.prev)}</text>
      <text x="${x(d.curr) + 6}" y="${yy + 37}" class="t-ink" style="font-weight:700">${short(d.curr)}</text></g>`; });
  setSvg(svg, w, h, s); bindRows(svg);
}

// Concentration
function drawConc() {
  const svg = document.getElementById("conc"), w = W(svg), rows = [...DATA].sort((a, b) => b.top_share - a.top_share);
  const L = 176, R = 160, T = 24, rowH = 25, pw = w - L - R, h = T + rows.length * rowH + 24, x = v => L + v / 0.6 * pw; let s = "";
  s += `<rect x="${x(0.4)}" y="${T - 6}" width="${x(0.6) - x(0.4)}" height="${h - 24 - T + 6}" rx="6" fill="var(--limit-zone)"/>`;
  [0, 0.2, 0.4, 0.6].forEach(t => { s += `<line x1="${x(t)}" x2="${x(t)}" y1="${T - 6}" y2="${h - 24}" stroke="var(--grid)"/><text x="${x(t)}" y="${h - 6}" text-anchor="middle">${pct(t)}</text>`; });
  rows.forEach((d, i) => { const yy = T + i * rowH, bad = d.top_share > 0.4;
    s += `<g class="hover-row" tabindex="0" data-i="${DATA.indexOf(d)}"><rect class="hl" x="0" y="${yy}" width="${w}" height="${rowH}" rx="6" fill="transparent"/>
      <text x="${L - 10}" y="${yy + 17}" text-anchor="end" class="${d.verdict ? "t-ink" : ""}" style="${d.verdict ? "font-weight:600" : ""}">${d.label}</text>
      ${rbar(x(0), yy + 5, x(d.top_share) - x(0), 15, bad ? "var(--alert)" : "url(#gt)")}
      <text x="${x(d.top_share) + 8}" y="${yy + 17}" class="t-ink" style="font-weight:600">${pct(d.top_share)}</text>
      <text x="${w}" y="${yy + 17}" text-anchor="end" class="t-dim">${d.top_company.length > 24 ? d.top_company.slice(0, 23) + "…" : d.top_company}</text></g>`; });
  s += `<line x1="${x(0.4)}" x2="${x(0.4)}" y1="${T - 12}" y2="${h - 24}" stroke="var(--alert)" stroke-width="1.5" stroke-dasharray="5 4"/>`;
  s += `<text x="${x(0.4) + 6}" y="${T - 10}" class="t-limit" style="font-weight:600">40% limit</text>`;
  s += `<text x="${w}" y="${T - 10}" text-anchor="end" class="t-dim">largest company</text>`;
  setSvg(svg, w, h, s); bindRows(svg);
}

// Agreement table
document.getElementById("agreeN").textContent = `${nAgree} of ${screened.length}`;
document.getElementById("agree").innerHTML = `<tr><th>Signal</th><th>Review</th><th>API</th><th>Result</th></tr>` +
  screened.map(d => `<tr><td><a href="#sig-${d.slug}" style="color:var(--ink);text-decoration:none;font-weight:600">${d.label}</a></td><td>${chip(d.verdict)}</td><td>${chip(d.api)}</td>
  <td>${!d.api ? "–" : d.api === d.verdict ? '<span class="agree">✓ Agree</span>' : '<span class="flag">⚑ Person decides</span>'}</td></tr>`).join("");

// Cards
function renderCards(f) {
  document.getElementById("cards").innerHTML = screened.filter(d => f === "all" || d.verdict === f).map(d => {
    const im = Math.max(...d.issues.map(x => x.n), 1);
    return `<div class="panel sig" id="sig-${d.slug}">
      <div class="ph"><div><h3>${d.label}</h3><div class="prod">${d.product}</div></div>
        <div class="verd"><div>Review ${chip(d.verdict)}</div><div>API ${chip(d.api)}</div>${d.api && d.api !== d.verdict ? '<div class="flag">⚑ screens disagree</div>' : ""}</div></div>
      <div class="mini"><div><b>${short(d.curr)}</b>complaints</div><div><b>+${Math.round((d.growth - 1) * 100)}%</b>growth</div>
        <div><b>${pct(d.top_share)}</b>top company</div><div><b>${d.n_grants}</b>grants</div></div>
      <p class="why">${d.why}</p>
      <div class="isshead">What people complain about</div>
      <div class="iss">${d.issues.map(x => `<div class="r"><div>${x.issue}<div class="bar"><span style="width:${x.n / im * 100}%"></span></div></div><div class="nn">${fmt(x.n)}</div></div>`).join("")}</div>
      ${d.grants.length ? `<div class="prod">Matching grants: ${d.grants.join(", ")}</div>` : `<div class="prod">No matching federal grant: an open market, or no buyer yet</div>`}
      <details><summary>Read the review memo (Claude Code)</summary><div class="memo">${d.memo}</div></details>
      ${d.api_memo ? `<details><summary>Read the API memo (Claude Opus 5.5)</summary><div class="memo">${d.api_memo}</div></details>` : ""}
    </div>`; }).join("");
}
document.querySelectorAll("#fSeg button").forEach(b => b.onclick = () => {
  document.querySelectorAll("#fSeg button").forEach(o => o.setAttribute("aria-pressed", o === b)); renderCards(b.dataset.f); });
renderCards("all");

// Table
document.getElementById("table").innerHTML = `<tr><th>#</th><th>Signal</th><th class="n">Last year</th><th class="n">This year</th><th class="n">Growth</th>
  <th class="n">vs market</th><th>Top company</th><th class="n">Share</th><th class="n">Grants</th><th class="n">Score</th><th>Review</th><th>API</th></tr>` +
  DATA.map(d => `<tr><td>${d.rank}</td><td>${d.label}</td><td class="n">${fmt(d.prev)}</td><td class="n">${fmt(d.curr)}</td><td class="n">${d.growth.toFixed(2)}x</td>
  <td class="n">${d.rel.toFixed(2)}x</td><td>${d.top_company}</td><td class="n">${pct(d.top_share)}</td><td class="n">${d.n_grants}</td><td class="n">${d.score.toFixed(2)}</td>
  <td>${chip(d.verdict)}</td><td>${chip(d.api)}</td></tr>`).join("");

function drawAll() { drawMap(); drawFunnel(); drawDonut(); drawGrowth(); drawPair(); drawConc(); }
addEventListener("resize", drawAll); drawAll();
if (document.fonts) document.fonts.ready.then(drawAll);
</script>
</body>
</html>
"""


if __name__ == "__main__":
    print(build())
