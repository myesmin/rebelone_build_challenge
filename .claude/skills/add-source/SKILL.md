---
name: add-source
description: Add a new data source to the Rebel One idea-source pipeline (e.g. Regulations.gov public comments, 311 service requests, IRS 990 nonprofit filings, BLS/Census data, state labor complaints). Use when asked to add, plug in, or prototype another signal source.
---

# Add a source

Every source plugs into the same shape: **pull → normalize to a signal → enrich → screen**.

## Checklist

1. **Test the API first** with `curl`, read-only. Record what works, rate limits, auth, and
   any surprises in the module docstring (see `src/cfpb.py` for the pattern). Most US
   government APIs work keyless or with `DEMO_KEY` (api.data.gov).

2. **Create `src/<source>.py`** following `src/cfpb.py` / `src/grants.py`:
   - `_get()` / `_search()`: cache every response in `data/raw/<source>_<hash>.json`, retry
     with backoff, sleep between calls.
   - Return plain dicts. No pandas.

3. **Decide its role.** Either:
   - **Demand source** (like CFPB): emits candidate rows with `prev`, `curr`, `growth`. Add
     them in `score.candidates()` or a sibling, and add LMI weights to `config.py`.
   - **Enrichment source** (like Grants.gov): attaches evidence to existing signals. Add a
     `match(product, sub_product)` and a keyword map in `config.py`, then add a section to
     `llm.signal_pack()`.

4. **Update the rubric** in `.claude/skills/venture-screen/references/rubric.md` if the source
   adds a new dimension. `src/score.py` and the venture-screen skill both read from it,
   so keep them in sync.

5. **Wire it into `run.py`**, run `python run.py --no-llm`, and check that the new data
   appears in `output/claude_prompts/*.pack.md`.

## Good next sources (from the original pitch)
- **Regulations.gov comments** (`api.regulations.gov`, DEMO_KEY): replaces the complaint
  narratives CFPB stopped publishing. Families and advocates describe problems in their own words.
- **Census ACS by ZCTA**: join complaint ZIP codes to median income, to check LMI concentration
  directly instead of using product weights.
- **Rebel One Reg Tracker**: link each signal to bills touching the same product. A spike plus
  a new law is the strongest "why now".
