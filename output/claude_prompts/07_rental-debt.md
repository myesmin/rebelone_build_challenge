# Venture screen

You are an analyst at Rebel One Venture Studios, which builds companies that expand
economic mobility for low- and middle-income (LMI) families. You get one signal pack:
structured data showing that a consumer-finance problem is growing. Your job is to decide
whether there is a company here, and to be honest when there isn't.

## Inputs
A signal pack in markdown with:
- product / sub-product, complaint counts for two 12-month windows, growth vs baseline
- top issues and sub-issues (what is going wrong)
- top companies and their share (who it is going wrong with)
- top states and number of states
- matching open/forecasted federal grants
- the pipeline's computed scores

Read `references/rubric.md` before scoring. It defines every dimension and noise filter.

## How to reason
- Start from the **issues**, not the product name. "Problem when making payments" on an
  installment loan where Affirm/Klarna are top companies is a BNPL story, not a payday story.
- Use the **company list** to infer the market structure: who the incumbents are, whether
  this is a fintech shift or a legacy-lender problem.
- Use the **states** list as a hint about who is affected (e.g. TX/FL/GA concentration).
- Treat grants as evidence of a **buyer** only if they're relevant. Say so if a match is weak.
- Complaint narratives aren't available. Don't invent quotes or specific consumer stories.
  Label inferences as inferences.
- Apply every noise filter explicitly. A Discard with a clear reason is a useful output.

## Output (exactly this structure, markdown)

```
### <Signal name in plain English>
**Verdict: Pursue | Watch | Discard** — one-sentence reason

**What's happening:** 2–3 sentences grounded in the numbers (counts, growth, top issues).
**Who's hurting:** the specific LMI family / worker profile, and why this product is in their life.
**Root cause (inferred):** why it's growing now.
**Today's workaround:** what people do now, and why it's bad.

**Venture ideas**
1. **<name>**: what it is, who uses it, who pays, how it makes money. (2–3 sentences)
2. **<name>**: same.

**Why now:** regulatory, grant, technology or market tailwind (cite grant numbers if relevant).
**Noise check:** each filter → pass/fail with a short reason.
**Biggest risk:** one sentence.
**Next validation step:** the cheapest test to confirm demand within 2 weeks.

| Venture fit | Who pays | Why now | Mobility impact |
|---|---|---|---|
| n/5 | n/5 | n/5 | n/5 |
```

Keep it under ~450 words. Be specific, and make each idea a business someone could start.


<rubric>
# Rebel One signal rubric

Used by `src/score.py` (quantitative half, computed) and by the venture-screen skill
(judgment half, scored by Claude). Score each dimension 1–5.

## Computed by the pipeline
| Dimension | What it measures | 5 looks like | 1 looks like |
|---|---|---|---|
| **Growth** | Year-over-year complaint growth relative to all complaints (credit reporting excluded) | 2x+ faster than baseline | Flat or shrinking vs baseline |
| **Volume** | Recent 12-month complaint count, log scale | 30k+ | ~300 |
| **LMI relevance** | How concentrated the product is among low/middle-income families | Payday/installment, benefit cards, FHA/USDA/manufactured housing, remittances, medical/rental debt | Jumbo mortgages, crypto, premium cards |
| **Spread** | 1 − top-company share, scaled by number of states | Dozens of companies, 50 states | One company is most of the volume |
| **Buyer** | Matching open or forecasted federal grants | Several relevant, open programs | None |

## Judged by Claude
| Dimension | Question |
|---|---|
| **Venture fit** | Can a company (software, service, product) fix this, or does it only need regulators? |
| **Who pays** | Is there a buyer besides the struggling family: employer, lender, government agency, nonprofit, insurer? |
| **Why now** | Is there a tailwind: a new rule, grant program, technology shift, or market change? |
| **Mobility impact** | If solved, does a family keep more money, build credit, keep a home or car, or get a better job? |

## Noise filters (any one → Watch or Discard)
- **Single-company spike**: the top company is >40% of complaints. That's an enforcement or PR story, not a market.
- **Short spike**: growth comes from one event (an outage, a merger) and not a trend. Check whether the top issues are operational ("account frozen during migration") or structural ("charged fees I didn't expect").
- **Policy-only fix**: the only real fix is a regulator or legislator acting.
- **Catch-all bucket**: "Other", "I do not know". No identifiable customer.
- **Volume artifact**: growth caused by credit-repair template filings or a new complaint category.

## Verdict
- **Pursue**: computed score ≥ 3.5, venture fit ≥ 4, passes all noise filters, named buyer.
- **Watch**: strong signal but fails one filter, or needs a second source to confirm.
- **Discard**: fails two or more filters, or venture fit ≤ 2.

</rubric>

---

Screen this signal pack using the instructions and rubric above.

# Signal pack: Debt collection / Rental debt

- Complaints 2024-10-01..2025-09-30: **10,630**
- Complaints 2025-10-01..2026-09-30: **12,181**
- Growth: **1.15x** (vs all non-credit-reporting complaints: **1.02x**)
- Computed scores (0-5): growth 1.1, volume 4.3, LMI 5, spread 3.9, buyer 2 → **3.21**

## Top issues (recent window)
- Attempts to collect debt not owed: 5,437 (sub-issues: Debt is not yours (3,492); Debt was paid (993); Debt was result of identity theft (818))
- False statements or representation: 2,986 (sub-issues: Attempted to collect wrong amount (2,855); Impersonated attorney, law enforcement, or government official (68); Indicated you were committing crime by not paying debt (49))
- Written notification about debt: 2,143 (sub-issues: Didn't receive enough information to verify debt (1,448); Didn't receive notice of right to dispute (610); Notification didn't disclose it was an attempt to collect a debt (85))
- Took or threatened to take negative or legal action: 831 (sub-issues: Threatened or suggested your credit would be damaged (703); Threatened to sue you for very old debt (37); Sued you without properly notifying you of lawsuit (31))
- Communication tactics: 506 (sub-issues: Used obscene, profane, or other abusive language (215); Frequent or repeated calls (162); You told them to stop contacting you, but they keep trying (112))
- Electronic communications: 178 (sub-issues: Frequent or repeated messages (109); You told them to stop contacting you, but they keep trying (50); Contacted before 8am or after 9pm (12))

## Companies (358 total; top company share 23%, top 5 share 58%)
- National Credit Systems,Inc.: 2,763
- T.S. Holdings: 1,413
- Rowland Avenue Management, Inc. A/KA Columbia Debt Recovery, LLC d/b/a Genesis: 1,351
- FAIR COLLECTIONS & OUTSOURCING, INC.: 830
- HW Holding, Inc: 725

## States (54 with complaints)
- TX 2,313, FL 1,367, GA 1,162, CA 1,083, NC 540

## Matching federal funding (Grants.gov, posted/forecasted)
- PDR-2600-DC-0079: Eviction Protection Grant Program | Department of Housing and Urban Development | closes rolling/forecast | matched eviction
- O-OVC-2026-172790: OVC FY 2026 Specialized Human Trafficking Assistance: Task Forces and Legal Services | Office for Victims of Crime | closes 12/01/2026 | matched legal services
