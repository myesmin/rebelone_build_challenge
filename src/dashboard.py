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
    return m.group(1) if m else "Unscreened"


def _first_sentence(memo: str) -> str:
    m = re.search(r"\*\*Verdict:[^*]*\*\*\.?\s*(.+)", memo or "")
    return m.group(1).strip().replace("*", "") if m else ""


def _grants(pack: str) -> list[str]:
    sec = pack.split("## Matching federal funding", 1)[-1]
    return [l[2:].split(":")[0] for l in sec.splitlines() if l.startswith("- ") and "none found" not in l]


def build() -> Path:
    meta = json.loads((OUT / "run_meta.json").read_text())
    rows = list(csv.DictReader(open(OUT / "signals.csv")))
    packs = {re.sub(r"^\d+_", "", p.name[:-8]): p.read_text()
             for p in (OUT / "claude_prompts").glob("*.pack.md")}
    signals = []
    for r in rows:
        s = slug(r)
        memo_path = OUT / "analyses" / f"{s}.md"
        memo = memo_path.read_text() if memo_path.exists() else ""
        api_path = OUT / "analyses_api" / f"{s}.md"
        api_memo = api_path.read_text() if api_path.exists() else ""
        pack = packs.get(s, "")
        signals.append({
            "rank": int(r["rank"]), "label": label(r), "product": r["product"], "slug": s,
            "prev": int(r["prev"]), "curr": int(r["curr"]), "growth": float(r["growth"]),
            "rel_growth": float(r["rel_growth"]), "score": float(r["score"]),
            "lmi": float(r["s_lmi"]), "spread": float(r["s_spread"] or 0),
            "top_company": r["top_company"], "top_share": float(r["top_company_share"]),
            "n_states": int(r["n_states"]), "n_grants": int(r["n_grants"]),
            "grants": _grants(pack) if pack else [],
            "verdict": _verdict(memo) if pack else "Not screened",
            "why": html.escape(_first_sentence(memo)),
            "memo_html": markdown.markdown(memo, extensions=["tables"]) if memo else "",
            "api_verdict": _verdict(api_memo) if api_memo else "",
            "api_html": markdown.markdown(api_memo, extensions=["tables"]) if api_memo else "",
        })
    screened = [s for s in signals if s["memo_html"]]
    counts = {v: sum(1 for s in screened if s["verdict"] == v) for v in ("Pursue", "Watch", "Discard")}
    both = [s for s in screened if s["api_verdict"]]
    agree = sum(1 for s in both if s["api_verdict"] == s["verdict"])
    (p0, p1), (c0, c1) = meta["windows"]

    page = TEMPLATE
    for k, v in {
        "__DATA__": json.dumps(signals),
        "__BASELINE__": f"{meta['baseline']:.2f}",
        "__WINDOWS__": f"{p0} → {p1} vs {c0} → {c1}",
        "__GENERATED__": meta.get("generated", c1),
        "__TOTAL__": f"{meta.get('curr_all', 0):,}",
        "__CANDIDATES__": str(meta["candidates"]),
        "__ENRICHED__": str(len(signals)),
        "__SCREENED__": str(len(screened)),
        "__PURSUE__": str(counts["Pursue"]),
        "__WATCH__": str(counts["Watch"]),
        "__DISCARD__": str(counts["Discard"]),
        "__AGREE__": f"{agree}/{len(both)}" if both else "n/a",
    }.items():
        page = page.replace(k, v)
    DOCS.mkdir(exist_ok=True)
    out = DOCS / "index.html"
    out.write_text(page)
    return out


TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Rebel One idea source: complaint signals</title>
<style>
.viz-root {
  color-scheme: light;
  --surface-0: #f4f3f0; --surface-1: #fcfcfb; --border: #e3e2dd; --grid: #ecebe7;
  --text-primary: #0b0b0b; --text-secondary: #52514e; --text-muted: #77766f;
  --series-1: #2a78d6; --series-1-soft: #cde2fb; --ref: #0b0b0b;
  --good: #0ca30c; --warning: #fab219; --neutral: #9b9a93;
}
@media (prefers-color-scheme: dark) {
  :root:where(:not([data-theme="light"])) .viz-root {
    color-scheme: dark;
    --surface-0: #111110; --surface-1: #1a1a19; --border: #2e2e2b; --grid: #262624;
    --text-primary: #f0efec; --text-secondary: #c3c2b7; --text-muted: #94938b;
    --series-1: #3987e5; --series-1-soft: #184f95; --ref: #f0efec;
  }
}
:root[data-theme="dark"] .viz-root {
  color-scheme: dark;
  --surface-0: #111110; --surface-1: #1a1a19; --border: #2e2e2b; --grid: #262624;
  --text-primary: #f0efec; --text-secondary: #c3c2b7; --text-muted: #94938b;
  --series-1: #3987e5; --series-1-soft: #184f95; --ref: #f0efec;
}
* { box-sizing: border-box; }
body { margin: 0; }
.viz-root { background: var(--surface-0); color: var(--text-primary); min-height: 100vh;
  font: 15px/1.5 -apple-system, BlinkMacSystemFont, "Segoe UI", Inter, sans-serif; }
.wrap { max-width: 1120px; margin: 0 auto; padding: 32px 24px 64px; }
header { display: flex; justify-content: space-between; gap: 16px; align-items: flex-start; }
h1 { font-size: 26px; margin: 0 0 4px; letter-spacing: -0.01em; }
.tagline { color: var(--text-secondary); margin: 0; max-width: 720px; }
.meta { color: var(--text-muted); font-size: 13px; margin-top: 6px; }
.toggle { background: var(--surface-1); color: var(--text-secondary); border: 1px solid var(--border);
  border-radius: 8px; padding: 6px 10px; cursor: pointer; font: inherit; font-size: 13px; white-space: nowrap; }
.card { background: var(--surface-1); border: 1px solid var(--border); border-radius: 12px; padding: 20px; }
.tiles { display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px; margin: 24px 0; }
.tile .k { color: var(--text-secondary); font-size: 13px; }
.tile .v { font-size: 26px; white-space: nowrap; font-weight: 650; font-variant-numeric: tabular-nums; letter-spacing: -0.02em; }
.tile .s { color: var(--text-muted); font-size: 12px; }
h2 { font-size: 17px; margin: 0 0 4px; }
.sub { color: var(--text-secondary); font-size: 13px; margin: 0 0 16px; }
.chart-head { display: flex; justify-content: space-between; align-items: flex-end; gap: 12px; flex-wrap: wrap; }
.seg { display: inline-flex; border: 1px solid var(--border); border-radius: 8px; overflow: hidden; }
.seg button { background: transparent; color: var(--text-secondary); border: 0; padding: 6px 12px;
  font: inherit; font-size: 13px; cursor: pointer; }
.seg button[aria-pressed="true"] { background: var(--surface-0); color: var(--text-primary); font-weight: 600; }
svg text { fill: var(--text-secondary); font-size: 12px; }
svg .lbl { fill: var(--text-primary); font-size: 13px; }
svg .val { fill: var(--text-primary); font-size: 12px; font-variant-numeric: tabular-nums; }
svg .row:hover .hit, svg .row:focus .hit { fill: var(--surface-0); }
svg .row { cursor: pointer; outline: none; }
.badge { display: inline-flex; align-items: center; gap: 6px; font-size: 12px; font-weight: 600;
  color: var(--text-primary); border: 1px solid var(--border); border-radius: 999px; padding: 2px 9px; white-space: nowrap; }
.dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; }
.tip { position: fixed; pointer-events: none; background: var(--surface-1); color: var(--text-primary);
  border: 1px solid var(--border); border-radius: 10px; padding: 10px 12px; font-size: 13px;
  box-shadow: 0 6px 24px rgba(0,0,0,.12); max-width: 300px; opacity: 0; transition: opacity .08s; z-index: 10; }
.tip b { font-weight: 650; } .tip .m { color: var(--text-secondary); }
.grid2 { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 24px; }
.sig { scroll-margin-top: 16px; }
.sig-head { display: flex; justify-content: space-between; align-items: flex-start; gap: 8px; }
.sig h3 { margin: 0; font-size: 16px; }
.sig .prod { color: var(--text-muted); font-size: 12px; }
.stats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; margin: 14px 0 10px; }
.stats div { font-size: 12px; color: var(--text-secondary); }
.stats b { display: block; font-size: 16px; color: var(--text-primary); font-variant-numeric: tabular-nums; }
.why { color: var(--text-secondary); font-size: 14px; margin: 6px 0 10px; }
details summary { cursor: pointer; color: var(--series-1); font-size: 13px; font-weight: 600; }
.memo { font-size: 14px; } .memo h3 { display: none; }
.memo table { border-collapse: collapse; margin-top: 8px; } .memo td, .memo th { border: 1px solid var(--border); padding: 4px 10px; }
table.data { width: 100%; border-collapse: collapse; font-size: 13px; font-variant-numeric: tabular-nums; }
table.data th { text-align: left; color: var(--text-secondary); font-weight: 600; border-bottom: 1px solid var(--border); padding: 8px 6px; }
table.data td { border-bottom: 1px solid var(--grid); padding: 7px 6px; } table.data td.n { text-align: right; } table.data th.n { text-align: right; }
.section { margin-top: 28px; }
.rubric { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; font-size: 14px; }
.rubric b { display: block; margin-bottom: 2px; } .rubric p { margin: 0; color: var(--text-secondary); }
footer { color: var(--text-muted); font-size: 12px; margin-top: 32px; }
a { color: var(--series-1); }
@media (max-width: 1000px) { .tiles { grid-template-columns: repeat(3, 1fr); } }
@media (max-width: 800px) { .tiles, .grid2, .rubric { grid-template-columns: 1fr 1fr; } .grid2 { grid-template-columns: 1fr; } }
</style>
</head>
<body>
<div class="viz-root"><div class="wrap">

<header>
  <div>
    <h1>Where are LMI families hurting, and who's paying to fix it?</h1>
    <p class="tagline">Bills tell you the rules changed. <b>Complaints</b> tell you who's hurting.
      <b>Grants</b> tell you who's paying to fix it. A demand-signal source for Rebel One, built from the
      CFPB Consumer Complaint Database and Grants.gov and screened by Claude.</p>
    <div class="meta">Windows __WINDOWS__ · generated __GENERATED__</div>
  </div>
  <button class="toggle" id="theme" type="button">◐ Theme</button>
</header>

<div class="tiles">
  <div class="card tile"><div class="k">Complaints analyzed</div><div class="v">__TOTAL__</div><div class="s">last 12 months, all products</div></div>
  <div class="card tile"><div class="k">Baseline growth</div><div class="v">__BASELINE__x</div><div class="s">all products except credit reporting</div></div>
  <div class="card tile"><div class="k">Funnel</div><div class="v">__CANDIDATES__ → __ENRICHED__ → __SCREENED__</div><div class="s">sub-products → enriched → Claude-screened</div></div>
  <div class="card tile"><div class="k">Two screens agree</div><div class="v">__AGREE__</div><div class="s">Claude Code review vs Claude API. Disagreements go to a human.</div></div>
  <div class="card tile"><div class="k">Verdicts (review)</div><div class="v">__PURSUE__ <span style="font-size:15px;font-weight:500;color:var(--text-secondary)">pursue</span></div><div class="s">__WATCH__ watch · __DISCARD__ discard</div></div>
</div>

<div class="card">
  <div class="chart-head">
    <div>
      <h2>Complaint growth, year over year</h2>
      <p class="sub">Each bar is a sub-product's growth. The line marks baseline growth across all complaints (__BASELINE__x).
        Bars to the right of the line are growing faster than complaints overall. Hover for details; click to jump to the memo.</p>
    </div>
    <div class="seg" role="group" aria-label="Sort">
      <button type="button" data-sort="score" aria-pressed="true">By score</button>
      <button type="button" data-sort="growth" aria-pressed="false">By growth</button>
      <button type="button" data-sort="curr" aria-pressed="false">By volume</button>
    </div>
  </div>
  <svg id="chart" width="100%" role="img" aria-label="Year-over-year complaint growth by sub-product"></svg>
</div>

<div class="section chart-head">
  <div><h2>Screened signals</h2><p class="sub" style="margin:0">Each memo follows the venture-screen skill and the shared rubric.</p></div>
  <div class="seg" role="group" aria-label="Filter verdict">
    <button type="button" data-f="all" aria-pressed="true">All</button>
    <button type="button" data-f="Pursue" aria-pressed="false">Pursue</button>
    <button type="button" data-f="Watch" aria-pressed="false">Watch</button>
    <button type="button" data-f="Discard" aria-pressed="false">Discard</button>
  </div>
</div>
<div class="grid2" id="cards"></div>

<div class="section card">
  <h2>How we separate signal from noise</h2>
  <p class="sub">Computed by the pipeline, judged by Claude, defined once in <code>rubric.md</code>.</p>
  <div class="rubric">
    <div><b>Growth vs baseline</b><p>Raw growth misleads. We compare against all complaints and exclude credit reporting (~6M/yr).</p></div>
    <div><b>Spread</b><p>If one company is more than 40% of complaints, it's an enforcement story, not a market.</p></div>
    <div><b>Structural issue mix</b><p>"Fees I didn't expect" counts more than one-off operational spikes.</p></div>
    <div><b>LMI relevance</b><p>Payday, benefit cards, FHA/USDA, remittances and medical or rental debt score highest.</p></div>
    <div><b>A buyer exists</b><p>A matching open grant, employer, lender or agency. No grant can also mean white space.</p></div>
    <div><b>Verdict</b><p>Pursue / Watch / Discard. A clear Discard is a useful output.</p></div>
  </div>
</div>

<div class="section card">
  <h2>All enriched candidates</h2>
  <p class="sub">Table view of the chart above.</p>
  <table class="data" id="table"></table>
</div>

<footer>Sources: <a href="https://www.consumerfinance.gov/data-research/consumer-complaints/">CFPB Consumer Complaint Database</a>
  (public API) · <a href="https://www.grants.gov/">Grants.gov</a> (search2 API). Complaint counts aren't verified by CFPB and
  aren't a measure of total harm. CFPB stopped publishing narratives in 2026, so memos are based on structured fields only. Built with Claude Code.</footer>
</div></div>
<div class="tip" id="tip" role="tooltip"></div>

<script>
const DATA = __DATA__;
const BASE = __BASELINE__;
const VCOL = {Pursue: "var(--good)", Watch: "var(--warning)", Discard: "var(--neutral)", "Not screened": "transparent"};
const VICON = {Pursue: "✓", Watch: "◐", Discard: "✕", "Not screened": ""};
const fmt = n => n.toLocaleString("en-US");
const badge = v => v === "Not screened" ? `<span class="badge" style="color:var(--text-muted)">Not screened</span>`
  : `<span class="badge"><span class="dot" style="background:${VCOL[v]}"></span>${VICON[v]} ${v}</span>`;

// Theme toggle: wins over the OS setting in both directions.
document.getElementById("theme").onclick = () => {
  const r = document.documentElement, dark = r.dataset.theme ? r.dataset.theme === "dark"
    : matchMedia("(prefers-color-scheme: dark)").matches;
  r.dataset.theme = dark ? "light" : "dark";
};

// Chart
const svg = document.getElementById("chart"), tip = document.getElementById("tip");
let sortKey = "score";
function draw() {
  const rows = [...DATA].sort((a, b) => b[sortKey] - a[sortKey]);
  const W = svg.clientWidth || 1000, L = 230, R = 150, rowH = 30, top = 24, bot = 28;
  const H = top + rows.length * rowH + bot, plotW = W - L - R;
  const max = Math.max(2, Math.ceil(Math.max(...rows.map(r => r.growth)) * 4) / 4);
  const x = v => L + (v / max) * plotW;
  svg.setAttribute("height", H); svg.setAttribute("viewBox", `0 0 ${W} ${H}`);
  let s = "";
  for (let t = 0; t <= max + 1e-9; t += 0.5) {
    s += `<line x1="${x(t)}" x2="${x(t)}" y1="${top - 6}" y2="${H - bot}" stroke="var(--grid)" />`;
    s += `<text x="${x(t)}" y="${H - bot + 16}" text-anchor="middle">${t.toFixed(1)}x</text>`;
  }
  rows.forEach((r, i) => {
    const y = top + i * rowH, bh = 14, by = y + (rowH - bh) / 2, x0 = x(0), x1 = x(r.growth);
    const w = Math.max(1, x1 - x0);
    s += `<g class="row" tabindex="0" data-slug="${r.slug}" data-i="${DATA.indexOf(r)}">
      <rect class="hit" x="0" y="${y}" width="${W}" height="${rowH}" fill="transparent" rx="6"/>
      <text class="lbl" x="${L - 12}" y="${y + rowH / 2 + 4}" text-anchor="end">${r.label}</text>
      <path d="M${x0},${by} h${w - 4} a4,4 0 0 1 4,4 v${bh - 8} a4,4 0 0 1 -4,4 h-${w - 4} z" fill="var(--series-1)"/>
      <text class="val" x="${x1 + 8}" y="${y + rowH / 2 + 4}">${r.growth.toFixed(2)}x · ${fmt(r.curr)}</text>
      ${r.verdict !== "Not screened" ? `<circle cx="${W - 16}" cy="${y + rowH / 2}" r="5" fill="${VCOL[r.verdict]}"/>
      <text x="${W - 28}" y="${y + rowH / 2 + 4}" text-anchor="end">${r.verdict}</text>` : ""}
    </g>`;
  });
  s += `<line x1="${x(BASE)}" x2="${x(BASE)}" y1="${top - 10}" y2="${H - bot}" stroke="var(--ref)" stroke-width="1.5" stroke-dasharray="4 3"/>`;
  s += `<text x="${x(BASE) + 4}" y="${top - 12}" style="fill:var(--text-primary)">baseline ${BASE}x</text>`;
  svg.innerHTML = s;
  svg.querySelectorAll(".row").forEach(g => {
    const r = DATA[+g.dataset.i];
    const show = e => {
      tip.innerHTML = `<b>${r.label}</b> <span class="m">· ${r.product}</span><br>
        ${fmt(r.prev)} → <b>${fmt(r.curr)}</b> complaints (${r.growth.toFixed(2)}x, ${r.rel_growth.toFixed(2)}x vs baseline)<br>
        <span class="m">Top company:</span> ${r.top_company} (${Math.round(r.top_share * 100)}%)<br>
        <span class="m">States:</span> ${r.n_states} · <span class="m">Matching grants:</span> ${r.n_grants}<br>
        <span class="m">Score:</span> <b>${r.score.toFixed(2)}</b> · ${r.verdict}`;
      const bx = e.clientX ?? g.getBoundingClientRect().left + 240, byy = e.clientY ?? g.getBoundingClientRect().top;
      tip.style.left = Math.min(bx + 14, innerWidth - 320) + "px"; tip.style.top = (byy + 14) + "px"; tip.style.opacity = 1;
    };
    g.addEventListener("mousemove", show); g.addEventListener("focus", show);
    g.addEventListener("mouseleave", () => tip.style.opacity = 0); g.addEventListener("blur", () => tip.style.opacity = 0);
    const go = () => { const el = document.getElementById("sig-" + r.slug); if (el) { el.scrollIntoView({behavior: "smooth"}); el.querySelector("details")?.setAttribute("open", ""); } };
    g.addEventListener("click", go); g.addEventListener("keydown", e => { if (e.key === "Enter") go(); });
  });
}
document.querySelectorAll("[data-sort]").forEach(b => b.onclick = () => {
  sortKey = b.dataset.sort; document.querySelectorAll("[data-sort]").forEach(o => o.setAttribute("aria-pressed", o === b)); draw();
});
addEventListener("resize", draw); draw();

// Cards
const cards = document.getElementById("cards");
function renderCards(f) {
  cards.innerHTML = DATA.filter(r => r.memo_html && (f === "all" || r.verdict === f)).map(r => `
    <div class="card sig" id="sig-${r.slug}">
      <div class="sig-head"><div><h3>${r.label}</h3><div class="prod">${r.product}</div></div>
        <div style="text-align:right;display:grid;gap:4px;justify-items:end">
          <div><span class="prod">Review </span>${badge(r.verdict)}</div>
          ${r.api_verdict ? `<div><span class="prod">API </span>${badge(r.api_verdict)}</div>` : ""}
          ${r.api_verdict && r.api_verdict !== r.verdict ? `<div class="prod" style="color:var(--text-primary)">⚑ screens disagree</div>` : ""}
        </div></div>
      <div class="stats">
        <div><b>${fmt(r.curr)}</b>complaints</div><div><b>${r.growth.toFixed(2)}x</b>growth</div>
        <div><b>${Math.round(r.top_share * 100)}%</b>top company</div><div><b>${r.n_grants}</b>grants</div>
      </div>
      <p class="why">${r.why}</p>
      ${r.grants.length ? `<div class="prod" style="margin-bottom:8px">Grants: ${r.grants.join(", ")}</div>` : ""}
      <details><summary>Read review memo (Claude Code)</summary><div class="memo">${r.memo_html}</div></details>
      ${r.api_html ? `<details style="margin-top:6px"><summary>Read API memo (Claude Opus 5.5)</summary><div class="memo">${r.api_html}</div></details>` : ""}
    </div>`).join("");
}
document.querySelectorAll("[data-f]").forEach(b => b.onclick = () => {
  document.querySelectorAll("[data-f]").forEach(o => o.setAttribute("aria-pressed", o === b)); renderCards(b.dataset.f);
});
renderCards("all");

// Table
document.getElementById("table").innerHTML = `<tr><th>#</th><th>Signal</th><th class="n">Prev 12 mo</th><th class="n">Last 12 mo</th>
  <th class="n">Growth</th><th class="n">vs baseline</th><th>Top company</th><th class="n">Share</th><th class="n">Grants</th><th class="n">Score</th><th>Review</th><th>API</th></tr>` +
  DATA.map(r => `<tr><td>${r.rank}</td><td>${r.label}</td><td class="n">${fmt(r.prev)}</td><td class="n">${fmt(r.curr)}</td>
  <td class="n">${r.growth.toFixed(2)}x</td><td class="n">${r.rel_growth.toFixed(2)}x</td><td>${r.top_company}</td>
  <td class="n">${Math.round(r.top_share * 100)}%</td><td class="n">${r.n_grants}</td><td class="n">${r.score.toFixed(2)}</td><td>${r.verdict}</td><td>${r.api_verdict || "–"}</td></tr>`).join("");
</script>
</body>
</html>
"""


if __name__ == "__main__":
    print(build())
