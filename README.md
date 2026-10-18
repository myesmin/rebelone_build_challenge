# Rebel One idea source: consumer complaints × federal funding

**Bills tell you the rules changed. Complaints tell you who's hurting. Grants tell you who's paying to fix it.**

Rebel One's Reg Tracker watches legislation. This adds two demand signals it can't see:

| Source | Signal | Why |
|---|---|---|
| **CFPB Consumer Complaint Database** (≈7M complaints/yr, public API, no key) | A **problem worth solving** that is growing | Structured, national, updated daily, tagged by product, issue, company, state and ZIP. The closest thing to a live record of financial pain for LMI families. |
| **Grants.gov** (public API, no key) | **Someone is paying** for a solution | Open and forecasted federal funding = ready buyers, distribution partners or non-dilutive funding for a venture. |

**Live dashboard:** https://myesmin.github.io/rebelone_build_challenge/ (built from `docs/index.html`)

## What it does
```
CFPB API ──► complaint counts by product/sub-product, two 12-month windows
          ──► growth vs baseline · volume · LMI relevance          (src/score.py)
          ──► leaders enriched: issues, companies, states           (src/cfpb.py)
Grants.gov ─► matching open/forecasted funding                     (src/grants.py)
          ──► signal pack → Claude venture memo + verdict           (src/llm.py / skills)
          ──► output/report.md, output/signals.csv, docs/index.html (dashboard)
```

## Run it
```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python run.py --no-llm        # ~1 min first run; cached after
```
Then do the Claude step in one of three ways:
1. **Claude Code:** open this folder and run `/find-signals`.
2. **claude.ai:** upload `dist/venture-screen.zip` as a skill, or paste any `output/claude_prompts/NN_*.md`. Save the answer to `output/analyses/<slug>.md` and rerun.
3. **Claude API:** `cp .env.example .env`, add `ANTHROPIC_API_KEY`, then `python run.py`. This uses `claude-opus-5-5`, about $0.10 per signal.

All three use the same instructions and rubric (`.claude/skills/venture-screen/`).

## What it found (Oct 2025–Sep 2026 vs prior year; baseline growth 1.13x)
| Signal | Complaints | Growth | Verdict | Venture idea |
|---|---|---|---|---|
| **FHA mortgage distress** | 4.2k → 7.5k | 1.79x | **Pursue** | Loss-mitigation copilot for HUD housing counselors (funded by HUD's CHC NOFO) |
| **BNPL stacking** (installment loans: Affirm, Klarna, Afterpay) | 6.4k → 11.5k | 1.82x | **Pursue** | One view of every BNPL plan, with due dates moved to match payday; BNPL-to-credit-builder refinance |
| **Auto repossession and missing titles** | 16.1k → 21.9k | 1.36x | **Pursue** | Repo-prevention refinance through CDFI credit unions; title and add-on refund recovery |
| VA mortgage | 2.4k → 3.9k | 1.65x | Watch | Merge with FHA (escrow-led) |
| Payday / online small-dollar | 2.0k → 2.8k | 1.40x | Watch | "Stop the debit" ACH revocation tool, sold to credit unions |
| Rental debt collection | 10.6k → 12.2k | 1.15x | Watch | Move-out evidence and dispute kit (HUD Eviction Protection Grant) |
| USDA mortgage / vehicle lease | small / weak LMI | | Discard | Folded into FHA / auto |

Full memos: `output/report.md` · all candidates: `output/signals.csv`

## Separating signal from noise
Computed in `src/score.py`, judged by Claude, defined once in
[`rubric.md`](.claude/skills/venture-screen/references/rubric.md):
- **Growth relative to baseline**, not raw growth. Excludes credit reporting (≈6M/yr, driven by templates and the three bureaus).
- **Spread:** if one company is more than 40% of complaints, it's an enforcement story, not a market.
- **Issue mix:** *structural* ("fees I didn't expect") vs *one-off* ("account frozen during migration").
- **LMI weight** by product (payday, benefit cards, FHA/USDA, remittances score high).
- **Buyer:** a relevant grant, employer, lender or agency. Grants.gov matches must have the phrase in the title, because full-text search hits applicant boilerplate.
- **Verdict:** Pursue / Watch / Discard. A clear Discard is a useful output.

## What I learned
- **CFPB stopped publishing complaint narratives** in 2026 (API and bulk CSV). Structured fields still carry real signal: the company list alone revealed that the "installment loan" spike is BNPL.
- **Grants.gov search is noisy.** Unfiltered phrase searches returned nuclear-energy and national-park grants. It took category filters plus title matching to get useful results.
- **Missing grants is itself a signal.** BNPL and auto repossession have no federal funding: a gap a venture would have to fill on its own, with no grant buyer.

## With more time
- Join complaint ZIP codes to Census ACS income data, to measure LMI concentration directly.
- Monthly series and alerts: a weekly scheduled run that posts new spikes to Slack.
- Link each signal to Reg Tracker bills (spike plus new law = strongest "why now").
- Replace the lost narratives with Regulations.gov public comments (see `/add-source`).
- Validate the top 3 with 5 interviews each (next steps are in each memo).

## Built with Claude
- **Claude Code (Opus 5.5):** tested the APIs, discovered the narrative removal, wrote the pipeline, and ran the venture screen.
- **Project skills** (`.claude/skills/`): `find-signals` (end-to-end run), `venture-screen` (memo plus rubric, also packaged for claude.ai), `add-source` (extension guide). `CLAUDE.md` holds the project brief.
- **Claude API** (`src/llm.py`, `claude-opus-5-5`): the same skill as its system prompt. I ran it as a **second, independent screen** (`output/analyses_api/`). The two screens agreed on 3 of 8 verdicts (both say **Pursue** on FHA). The API was stricter on "named buyer" (BNPL and auto: Pursue → Watch) and never chose Discard. Disagreements are flagged on the dashboard for human review.