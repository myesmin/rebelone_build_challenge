---
name: find-signals
description: Run the Rebel One idea-source pipeline end to end. Pulls CFPB complaint growth and Grants.gov funding, ranks signals, then screens each one into a venture memo with the venture-screen skill. Use when asked to find signals, refresh the idea source, run the pipeline, or regenerate the report.
---

# Find signals

End-to-end run of the idea source. Works with or without an Anthropic API key.

## Steps

1. **Pull and rank.** From the repo root:
   ```bash
   .venv/bin/python run.py --no-llm          # or: python run.py --no-llm
   ```
   This writes `output/signals.csv` (all 16 enriched candidates), `output/report.md`, and
   for each of the top 8 signals: `output/claude_prompts/NN_<slug>.pack.md` (data only) and
   `NN_<slug>.md` (data plus full instructions, for pasting into claude.ai).
   API responses are cached in `data/raw/`. Delete that folder to force fresh data.

2. **Sanity-check the ranking** before analyzing. Read `output/signals.csv` and flag anything
   odd to the user: a catch-all bucket ranking high, a top-company share over 40%, or a
   signal with fewer than 300 complaints near the top.

3. **Screen each signal.** For each `output/claude_prompts/*.pack.md`, in rank order:
   - Apply the **venture-screen** skill (`.claude/skills/venture-screen/SKILL.md` and its
     `references/rubric.md`) to the pack.
   - Write the memo to `output/analyses/<slug>.md`. Use the slug without the `NN_` rank prefix,
     e.g. `02_installment-loan.pack.md` → `output/analyses/installment-loan.md`.
   - Skip signals that already have an analysis unless the user asks to redo them.
   If `ANTHROPIC_API_KEY` is set in `.env`, `python run.py` does this step through the
   API instead, with the same instructions.

4. **Rebuild the report** so it includes the memos:
   ```bash
   .venv/bin/python run.py --no-llm
   ```
   This is fast because data is cached.

5. **Summarize for the user**: a table of signal → verdict (Pursue / Watch / Discard) →
   best venture idea, then the 3–5 strongest picks and why the rest were cut.
