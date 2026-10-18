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
