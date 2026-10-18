"""Claude step. Same instructions as the venture-screen skill, so the API path and the
skill path (Claude Code / claude.ai, no key) produce the same memo."""
import os
import re
from pathlib import Path

from config import MODEL

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / ".claude" / "skills" / "venture-screen"


def system_prompt() -> str:
    skill = (SKILL / "SKILL.md").read_text()
    skill = re.sub(r"^---.*?---\s*", "", skill, flags=re.S)  # drop frontmatter
    rubric = (SKILL / "references" / "rubric.md").read_text()
    return f"{skill}\n\n<rubric>\n{rubric}\n</rubric>"


def signal_pack(sig: dict, det: dict, grants: list[dict], windows) -> str:
    (p0, p1), (c0, c1) = windows
    lines = [
        f"# Signal pack: {sig['product']} / {sig['sub_product']}",
        "",
        f"- Complaints {p0}..{p1}: **{sig['prev']:,}**",
        f"- Complaints {c0}..{c1}: **{sig['curr']:,}**",
        f"- Growth: **{sig['growth']}x** (vs all non-credit-reporting complaints: **{sig['rel_growth']}x**)",
        f"- Computed scores (0-5): growth {sig['s_growth']}, volume {sig['s_volume']}, "
        f"LMI {sig['s_lmi']}, spread {sig['s_spread']}, buyer {sig['s_buyer']} → **{sig['score']}**",
        "",
        "## Top issues (recent window)",
    ]
    for i in det["issues"]:
        subs = "; ".join(f"{s} ({n:,})" for s, n in i["sub_issues"] if s)
        lines.append(f"- {i['issue']}: {i['count']:,}" + (f" (sub-issues: {subs})" if subs else ""))
    lines += ["", f"## Companies ({det['n_companies']} total; top company share "
                  f"{det['top_company_share']:.0%}, top 5 share {det['top5_company_share']:.0%})"]
    lines += [f"- {c}: {n:,}" for c, n in det["top_companies"]]
    lines += ["", f"## States ({det['n_states']} with complaints)",
              "- " + ", ".join(f"{s} {n:,}" for s, n in det["top_states"])]
    lines += ["", "## Matching federal funding (Grants.gov, posted/forecasted)"]
    if grants:
        lines += [f"- {g['number']}: {g['title']} | {g['agency']} | closes {g['close']} | "
                  f"matched {g['keyword']}" for g in grants]
    else:
        lines.append("- none found")
    return "\n".join(lines)


def has_key() -> bool:
    try:
        from dotenv import dotenv_values
        # Fill from .env when the variable is unset *or empty* (load_dotenv won't
        # replace an empty one, which some shells export).
        for k, v in dotenv_values(ROOT / ".env").items():
            if v and not os.environ.get(k, "").strip():
                os.environ[k] = v
    except ImportError:
        pass
    return bool(os.environ.get("ANTHROPIC_API_KEY", "").strip())


def analyze(pack: str) -> str:
    import anthropic

    client = anthropic.Anthropic()
    response = client.beta.messages.create(
        model=MODEL,
        max_tokens=16000,
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
        output_config={"effort": "high"},
        cache_control={"type": "ephemeral"},  # system prompt is identical for every signal
        system=system_prompt(),
        messages=[{"role": "user", "content": pack}],
    )
    if response.stop_reason == "refusal":
        return "_Claude declined to analyze this signal._"
    return "\n".join(b.text for b in response.content if b.type == "text").strip()


def prompt_file(pack: str) -> str:
    """Self-contained prompt for pasting into claude.ai (no skill upload needed)."""
    return (f"{system_prompt()}\n\n---\n\nScreen this signal pack using the instructions "
            f"and rubric above.\n\n{pack}\n")
