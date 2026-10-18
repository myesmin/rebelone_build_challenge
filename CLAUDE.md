# Rebel One idea source

A demand-signal pipeline for Rebel One Venture Studios, which builds companies that expand
economic mobility for low- and middle-income families. It complements Rebel One's Reg Tracker
(bills) with **CFPB consumer complaints** (who is hurting, and growing) and **Grants.gov**
(who is paying to fix it).

## Run
```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python run.py --no-llm     # data + prompts
/find-signals                        # in Claude Code: full run including venture memos
```

## Layout
- `config.py`: windows, LMI weights, grant keywords, model
- `src/cfpb.py`, `src/grants.py`: cached API clients
- `src/score.py`: computed half of the rubric
- `src/llm.py`: Claude step. Loads `.claude/skills/venture-screen/` as its system prompt.
- `src/dashboard.py`: builds `docs/index.html` (static, GitHub Pages-ready) on every run
- `output/`: `signals.csv`, `report.md`, `claude_prompts/`, `analyses/`

## Skills
- `/find-signals`: end-to-end run
- `/venture-screen`: one signal pack → venture memo (also zipped in `dist/` for claude.ai)
- `/add-source`: how to plug in a new data source

## Conventions
- The rubric lives in one place: `.claude/skills/venture-screen/references/rubric.md`.
- CFPB no longer publishes complaint narratives. Never invent consumer quotes.
- Cache every API response in `data/raw/`. Be polite to government APIs.
- `ANTHROPIC_API_KEY` lives only in `.env` (gitignored).
