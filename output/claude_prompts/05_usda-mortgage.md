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

# Signal pack: Mortgage / USDA mortgage

- Complaints 2024-10-01..2025-09-30: **226**
- Complaints 2025-10-01..2026-09-30: **363**
- Growth: **1.6x** (vs all non-credit-reporting complaints: **1.42x**)
- Computed scores (0-5): growth 3.1, volume 1.2, LMI 5, spread 3.8, buyer 1 → **3.22**

## Top issues (recent window)
- Struggling to pay mortgage: 203 (sub-issues: Trying to communicate with the company to fix an issue related to modification, forbearance, short sale, deed-in-lieu, bankruptcy, or foreclosure (96); Applying for or obtaining a modification, forbearance plan, short sale, or deed-in-lieu (56); An existing modification, forbearance plan, short sale, or other loss mitigation relief (27))
- Trouble during payment process: 119 (sub-issues: Escrow, taxes, or insurance (43); Trying to communicate with the company to fix an issue while managing or servicing your loan (35); Payment process (24))
- Closing on a mortgage: 18 (sub-issues: Closing disclosure or other related disclosures (6); Delays with the closing process (4); Changes in loan terms during or after closing (3))
- Applying for a mortgage or refinancing an existing mortgage: 13 (sub-issues: Application denials (6); Changes in loan terms during the application process (2); Confusing or misleading advertising or marketing (2))
- Incorrect information on your report: 8 (sub-issues: Account status incorrect (4); Account information incorrect (3); Old information reappears or never goes away (1))
- Problem with a company's investigation into an existing problem: 2 (sub-issues: Difficulty submitting a dispute or getting information about a dispute over the phone (1); Their investigation did not fix an error on your report (1))

## Companies (59 total; top company share 13%, top 5 share 49%)
- Freedom Mortgage Company: 46
- PENNYMAC LOAN SERVICES, LLC.: 43
- Rocket Mortgage, LLC: 38
- CARRINGTON MORTGAGE SERVICES, LLC: 30
- Shellpoint Partners, LLC: 22

## States (44 with complaints)
- FL 28, NC 28, LA 26, AL 21, OH 18

## Matching federal funding (Grants.gov, posted/forecasted)
- HSG-2600-DC-0033: Comprehensive Housing Counseling (CHC) and the Housing Counseling Training (HCT) NOFO (FY2026) | Department of Housing and Urban Development | closes rolling/forecast | matched "housing counseling"
