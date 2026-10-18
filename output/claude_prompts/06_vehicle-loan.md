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

# Signal pack: Vehicle loan or lease / Loan

- Complaints 2024-10-01..2025-09-30: **16,075**
- Complaints 2025-10-01..2026-09-30: **21,911**
- Growth: **1.36x** (vs all non-credit-reporting complaints: **1.21x**)
- Computed scores (0-5): growth 2.0, volume 4.8, LMI 4, spread 4.5, buyer 0.0 → **3.22**

## Top issues (recent window)
- Managing the loan or lease: 6,619 (sub-issues: Billing problem (3,250); Problem with additional products or services purchased with the loan (1,479); Problem with fees charged (933))
- Repossession: 6,005 (sub-issues: Loan balance remaining after the vehicle is repossessed and sold (1,165); Account reinstatement or redemption after repossession (932); Deficiency balance after repossession (913))
- Problems at the end of the loan or lease: 2,989 (sub-issues: Unable to receive car title or other problem after the loan is paid off (1,682); Problem with paying off the loan (717); Problem related to refinancing (325))
- Getting a loan or lease: 2,328 (sub-issues: Loan opened without my consent or knowledge (730); Confusing or misleading advertising or marketing (436); Changes in terms mid-deal or after closing (315))
- Incorrect information on your report: 1,918 (sub-issues: Account status incorrect (786); Account information incorrect (760); Information belongs to someone else (225))
- Struggling to pay your loan: 1,086 (sub-issues: Denied request to lower payments (998); Problem after you declared or threatened to declare bankruptcy (88))

## Companies (539 total; top company share 10%, top 5 share 36%)
- SANTANDER HOLDINGS USA, INC.: 2,115
- Westlake Services, LLC: 1,742
- ALLY FINANCIAL INC.: 1,662
- CAPITAL ONE FINANCIAL CORPORATION: 1,253
- CREDIT ACCEPTANCE CORPORATION: 1,118

## States (57 with complaints)
- FL 2,790, TX 2,340, CA 2,207, GA 1,479, NY 932

## Matching federal funding (Grants.gov, posted/forecasted)
- none found
