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

# Signal pack: Mortgage / FHA mortgage

- Complaints 2024-10-01..2025-09-30: **4,200**
- Complaints 2025-10-01..2026-09-30: **7,532**
- Growth: **1.79x** (vs all non-credit-reporting complaints: **1.59x**)
- Computed scores (0-5): growth 4.0, volume 3.9, LMI 5, spread 4.5, buyer 1 → **4.04**

## Top issues (recent window)
- Struggling to pay mortgage: 3,113 (sub-issues: Trying to communicate with the company to fix an issue related to modification, forbearance, short sale, deed-in-lieu, bankruptcy, or foreclosure (1,360); Applying for or obtaining a modification, forbearance plan, short sale, or deed-in-lieu (729); An existing modification, forbearance plan, short sale, or other loss mitigation relief (578))
- Trouble during payment process: 2,791 (sub-issues: Escrow, taxes, or insurance (898); Trying to communicate with the company to fix an issue while managing or servicing your loan (752); Payment process (648))
- Applying for a mortgage or refinancing an existing mortgage: 568 (sub-issues: Trying to communicate with the company to fix an issue with the application process (130); Delays in the application process (117); Application denials (88))
- Closing on a mortgage: 544 (sub-issues: Closing disclosure or other related disclosures (131); Trying to communicate with the company to fix an issue with the loan closing (129); Delays with the closing process (108))
- Incorrect information on your report: 310 (sub-issues: Account status incorrect (205); Account information incorrect (67); Information is missing that should be on the report (13))
- Problem with a company's investigation into an existing problem: 165 (sub-issues: Their investigation did not fix an error on your report (100); Problem with personal statement of dispute (33); Difficulty submitting a dispute or getting information about a dispute over the phone (18))

## Companies (331 total; top company share 10%, top 5 share 37%)
- Rocket Mortgage, LLC: 762
- Freedom Mortgage Company: 632
- Shellpoint Partners, LLC: 474
- PENNYMAC LOAN SERVICES, LLC.: 458
- LoanCare, LLC: 424

## States (54 with complaints)
- TX 803, FL 798, CA 563, GA 549, IL 350

## Matching federal funding (Grants.gov, posted/forecasted)
- HSG-2600-DC-0033: Comprehensive Housing Counseling (CHC) and the Housing Counseling Training (HCT) NOFO (FY2026) | Department of Housing and Urban Development | closes rolling/forecast | matched "housing counseling"
