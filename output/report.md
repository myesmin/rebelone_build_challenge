# Rebel One idea source: complaint signals
_Generated 2026-10-18 · windows 2024-10-01..2025-09-30 vs 2025-10-01..2026-09-30 · baseline growth 1.13x (all products except credit reporting)_

**Method.** Pull every CFPB consumer complaint count by product and sub-product for two 12-month windows. Rank sub-products by growth relative to the baseline, volume, and LMI relevance. Enrich the leaders with company concentration, geographic spread and matching open federal grants (Grants.gov). Then Claude screens each signal against the rubric in `.claude/skills/venture-screen/references/rubric.md`.

| # | Signal | Complaints (prev → recent) | Growth | vs baseline | LMI | Spread | Grants | Score |
|---|---|---|---|---|---|---|---|---|
| 1 | FHA mortgage <br><sub>Mortgage</sub> | 4,200 → 7,532 | 1.79x | 1.59x | 5 | 4.5 | 1 | **4.04** |
| 2 | Installment loan <br><sub>Payday loan, title loan, personal loan, or advance loan</sub> | 6,353 → 11,541 | 1.82x | 1.61x | 5 | 4.2 | 0 | **3.95** |
| 3 | VA mortgage <br><sub>Mortgage</sub> | 2,372 → 3,923 | 1.65x | 1.47x | 4 | 4.5 | 4 | **3.78** |
| 4 | Payday loan <br><sub>Payday loan, title loan, personal loan, or advance loan</sub> | 1,991 → 2,782 | 1.4x | 1.24x | 5 | 4.7 | 0 | **3.3** |
| 5 | USDA mortgage <br><sub>Mortgage</sub> | 226 → 363 | 1.6x | 1.42x | 5 | 3.8 | 1 | **3.22** |
| 6 | Vehicle loan <br><sub>Vehicle loan or lease</sub> | 16,075 → 21,911 | 1.36x | 1.21x | 4 | 4.5 | 0 | **3.22** |
| 7 | Rental debt <br><sub>Debt collection</sub> | 10,630 → 12,181 | 1.15x | 1.02x | 5 | 3.9 | 2 | **3.21** |
| 8 | Vehicle lease <br><sub>Vehicle loan or lease</sub> | 2,310 → 3,479 | 1.51x | 1.34x | 4 | 4.4 | 0 | **3.17** |

## 1. FHA mortgage (score 4.04)


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

### Claude analysis

### Government-backed homeowners falling behind (FHA)
**Verdict: Pursue.** The fastest-growing large mortgage signal, spread across 331 servicers, and the problem is *navigating* relief, which software and services can fix.

**What's happening:** FHA mortgage complaints rose from 4,200 to 7,532 (1.79x, 1.59x faster than baseline). The top issue is *struggling to pay* (3,113). Within it, the largest sub-issue is *trying to communicate with the servicer about modification, forbearance or foreclosure* (1,360). Escrow, tax and insurance problems are second (898).
**Who's hurting:** First-time and lower-down-payment buyers, FHA's core borrowers, concentrated in TX, FL, GA and CA. These are mostly families who bought in 2021–2024 at peak prices with thin savings.
**Root cause (inferred):** Rising property-insurance and tax escrow (especially FL and TX) is pushing monthly payments up after purchase. Servicer call centers can't handle the loss-mitigation volume. The FHA loss-mitigation menu is complex and changed during 2025–26.
**Today's workaround:** Repeated calls to the servicer, a HUD housing counselor with a waitlist, or a "foreclosure rescue" firm (a scam risk).

**Venture ideas**
1. **Loss-mit copilot for housing counselors:** software that turns a borrower's documents into a complete, servicer-ready FHA loss-mitigation package and tracks it to a decision. Sold to HUD-approved counseling agencies, which are funded by HUD's housing counseling NOFO. Each counselor can handle 3–5x more cases.
2. **Escrow shock shield:** monitors a homeowner's tax and insurance renewals, shops cheaper insurance and warns of escrow increases before the annual analysis. Offered through credit unions and employers; earns insurance commissions.

**Why now:** Escrow inflation in Sun Belt states. HUD's FY2026 Comprehensive Housing Counseling NOFO (HSG-2600-DC-0033) funds the buyer for idea 1.
**Noise check:**
- Single company: pass (top servicer 10%).
- Short spike: pass (structural: payment affordability and escrow).
- Policy-only: pass (fixable with navigation and tools).
- Catch-all: pass.
- Artifact: pass.

**Biggest risk:** Servicer portals and data access vary, and counseling agencies have small budgets.
**Next validation step:** Interview 5 HUD-approved counseling agencies in TX and FL about case volume and their time per loss-mitigation package. Ask whether they'd pilot a tool for free.

| Venture fit | Who pays | Why now | Mobility impact |
|---|---|---|---|
| 4/5 | 4/5 | 4/5 | 5/5 |


## 2. Installment loan (score 3.95)


- Complaints 2024-10-01..2025-09-30: **6,353**
- Complaints 2025-10-01..2026-09-30: **11,541**
- Growth: **1.82x** (vs all non-credit-reporting complaints: **1.61x**)
- Computed scores (0-5): growth 4.1, volume 4.2, LMI 5, spread 4.2, buyer 0.0 → **3.95**

## Top issues (recent window)
- Problem when making payments: 2,787
- Charged fees or interest you didn't expect: 2,562
- Getting the loan: 1,835
- Problem with additional add-on products or services: 1,206
- Struggling to pay your loan: 959
- Problem with the payoff process at the end of the loan: 853

## Companies (558 total; top company share 17%, top 5 share 34%)
- Affirm Holdings, Inc: 1,924
- Paramount GR Holdings, LLC: 771
- Klarna AB: 559
- OneMain Finance Corporation: 388
- Block, Inc.: 273

## States (56 with complaints)
- CA 1,444, TX 1,437, FL 1,286, NY 555, GA 545

## Matching federal funding (Grants.gov, posted/forecasted)
- none found

### Claude analysis

### Buy now, pay later stacking
**Verdict: Pursue.** The fastest-growing signal in the dataset (1.82x). The company list shows this is mostly BNPL, not classic installment lending, and there is no federal money aimed at it: a market gap rather than a grant program.

**What's happening:** "Installment loan" complaints rose from 6,353 to 11,541. Top companies are Affirm (1,924), Paramount (771), Klarna (559), OneMain and Block (Afterpay). Top issues are *problems when making payments* (2,787), *unexpected fees or interest* (2,562) and *getting the loan* (1,835). Complaints are spread across 558 companies; the top company has 17%.
**Who's hurting:** Hourly and gig workers who use BNPL for groceries, bills and emergencies, not just big purchases. They are concentrated in CA, TX and FL. (Inferred from the issue mix and BNPL usage patterns; no narratives are available.)
**Root cause (inferred):** BNPL moved from occasional checkout to an everyday cash-flow tool. Families now juggle several BNPL plans across apps, each with different autopay dates, so they miss payments, pay late fees and overdraw. BNPL loans mostly don't show up on credit reports, so no one sees the full picture, including the borrower.
**Today's workaround:** Spreadsheets, calendar reminders, or skipping a bill to cover an autopay.

**Venture ideas**
1. **One view of every BNPL plan:** links Affirm, Klarna, Afterpay and others into one calendar, moves due dates to match payday where providers allow it, and warns before an autopay would overdraw. Free for consumers; paid by credit unions and earned-wage-access providers as a member benefit and for retention.
2. **BNPL-to-credit-builder refinance:** consolidates several BNPL plans into one low-cost credit-union installment loan that is reported to the bureaus. Turns invisible debt into a credit history. Earns lending margin with CDFI or credit-union partners.

**Why now:** Usage has outgrown oversight. The federal BNPL rule was withdrawn in 2025, and states such as New York are adding their own licensing (inferred; verify). Volume nearly doubled in a year.
**Noise check:**
- Single company: pass (Affirm 17%).
- Short spike: pass (growth across many providers).
- Policy-only: pass.
- Catch-all: pass.
- Artifact: possible. Some growth may be BNPL complaints moving into this category. Check whether Affirm and Klarna complaints also grew under other products.

**Biggest risk:** BNPL providers can block account linking.
**Next validation step:** Survey 100 BNPL users (r/povertyfinance, a credit-union partner) on how many active plans they hold and how many fees they paid in the last 90 days.

| Venture fit | Who pays | Why now | Mobility impact |
|---|---|---|---|
| 5/5 | 3/5 | 5/5 | 4/5 |


## 3. VA mortgage (score 3.78)


- Complaints 2024-10-01..2025-09-30: **2,372**
- Complaints 2025-10-01..2026-09-30: **3,923**
- Growth: **1.65x** (vs all non-credit-reporting complaints: **1.47x**)
- Computed scores (0-5): growth 3.3, volume 3.3, LMI 4, spread 4.5, buyer 4 → **3.78**

## Top issues (recent window)
- Trouble during payment process: 1,820 (sub-issues: Escrow, taxes, or insurance (728); Trying to communicate with the company to fix an issue while managing or servicing your loan (448); Payment process (386))
- Struggling to pay mortgage: 1,025 (sub-issues: Trying to communicate with the company to fix an issue related to modification, forbearance, short sale, deed-in-lieu, bankruptcy, or foreclosure (487); Applying for or obtaining a modification, forbearance plan, short sale, or deed-in-lieu (249); An existing modification, forbearance plan, short sale, or other loss mitigation relief (178))
- Applying for a mortgage or refinancing an existing mortgage: 489 (sub-issues: Trying to communicate with the company to fix an issue with the application process (113); Confusing or misleading advertising or marketing (97); Delays in the application process (89))
- Closing on a mortgage: 390 (sub-issues: Closing disclosure or other related disclosures (106); Delays with the closing process (104); Trying to communicate with the company to fix an issue with the loan closing (82))
- Incorrect information on your report: 124 (sub-issues: Account status incorrect (76); Account information incorrect (33); Information is missing that should be on the report (8))
- Problem with a company's investigation into an existing problem: 57 (sub-issues: Their investigation did not fix an error on your report (26); Problem with personal statement of dispute (20); Was not notified of investigation status or results (6))

## Companies (210 total; top company share 10%, top 5 share 40%)
- Freedom Mortgage Company: 409
- Ocwen Financial Corporation: 363
- Rocket Mortgage, LLC: 319
- Shellpoint Partners, LLC: 283
- PENNYMAC LOAN SERVICES, LLC.: 203

## States (56 with complaints)
- TX 519, FL 375, CA 357, VA 231, GA 215

## Matching federal funding (Grants.gov, posted/forecasted)
- FOA-VETS-27-01: Homeless Veterans’ Reintegration Program (HVRP), Incarcerated Veterans’ Transition Program (IVTP), and the Homeless Women Veterans' and Homeless Veterans' with Children Reintegration Grant Program (HWVHVWC) (referred to collectively as HVRP) | Veterans Employment and Training Service | closes rolling/forecast | matched veteran
- O-BJA-2026-172760: BJA FY 2026 National Center for Veterans Justice | Bureau of Justice Assistance | closes 10/30/2026 | matched veteran
- O-BJA-2026-172714: BJA FY 2026 Veterans Treatment Court Program | Bureau of Justice Assistance | closes 10/29/2026 | matched veteran
- HSG-2600-DC-0033: Comprehensive Housing Counseling (CHC) and the Housing Counseling Training (HCT) NOFO (FY2026) | Department of Housing and Urban Development | closes rolling/forecast | matched "housing counseling"

### Claude analysis

### Veteran homeowners: escrow and loss-mitigation trouble (VA)
**Verdict: Watch.** A real and growing signal, but its issue mix matches FHA, so treat it as one "government-backed mortgage distress" opportunity rather than a separate company.

**What's happening:** VA mortgage complaints rose from 2,372 to 3,923 (1.65x). Unlike FHA, the top issue is the *payment process* (1,820), led by **escrow, taxes or insurance** (728). *Struggling to pay* is second (1,025), mostly loss-mitigation communication (487). Top servicers: Freedom, Ocwen, Rocket, Shellpoint, PennyMac. Top states: TX, FL, CA, VA.
**Who's hurting:** Veterans and military families with VA loans, many with no down payment, near bases in TX, VA and FL.
**Root cause (inferred):** The same escrow shock as FHA, plus a gap in VA's loss-mitigation options after VA ended its servicing purchase program in 2025 (inferred; verify the current status of VA partial-claim legislation).
**Today's workaround:** Calling the servicer, VA regional loan technicians, veteran service organizations.

**Venture ideas**
1. **Add a VA module to the FHA loss-mit copilot:** same product, VA-specific workflow, distributed through veteran service organizations and HUD counselors (HSG-2600-DC-0033).
2. **Escrow shock shield for military families:** distributed through military credit unions (Navy Federal, PenFed, USAA-style channels).

**Why now:** VA loss-mitigation policy is changing. DOL-VETS HVRP (FOA-VETS-27-01) and other veterans' programs show funders active in veteran housing stability. These are adjacent buyers; the matches are weak.
**Noise check:**
- Single company: pass (10%).
- Short spike: pass.
- Policy-only: **partial fail** (part of the gap is a VA policy gap).
- Catch-all: pass.
- Artifact: pass.

**Biggest risk:** Fixing it may depend on VA policy rather than on a product.
**Next validation step:** Pull VA and FHA complaints by month to see whether the VA jump lines up with mid-2025 policy changes.

| Venture fit | Who pays | Why now | Mobility impact |
|---|---|---|---|
| 3/5 | 3/5 | 4/5 | 4/5 |


## 4. Payday loan (score 3.3)


- Complaints 2024-10-01..2025-09-30: **1,991**
- Complaints 2025-10-01..2026-09-30: **2,782**
- Growth: **1.4x** (vs all non-credit-reporting complaints: **1.24x**)
- Computed scores (0-5): growth 2.2, volume 3.0, LMI 5, spread 4.7, buyer 0.0 → **3.3**

## Top issues (recent window)
- Charged fees or interest you didn't expect: 904
- Struggling to pay your loan: 500
- Can't stop withdrawals from your bank account: 337
- Received a loan you didn't apply for: 204
- Can't contact lender or servicer: 174
- Money was taken from your bank account on the wrong day or for the wrong amount: 155

## Companies (330 total; top company share 6%, top 5 share 22%)
- Dave Operating, LLC: 156
- Rosebud Economic Development Corporation: 137
- WLCC: 107
- Uprova Credit, LLC: 105
- CCF Intermediate Holdings LLC: 101

## States (52 with complaints)
- CA 335, TX 322, FL 268, OH 129, GA 106

## Matching federal funding (Grants.gov, posted/forecasted)
- none found

### Claude analysis

### Payday and online small-dollar loans: losing control of the bank account
**Verdict: Watch.** Growing and very low-income, but several top issues point to bad actors (tribal online lenders, loans the person never applied for). Much of the fix is enforcement.

**What's happening:** Payday complaints rose from 1,991 to 2,782 (1.40x). Top issues are *unexpected fees* (904), *struggling to pay* (500), **can't stop withdrawals from bank account** (337), *loan not applied for* (204) and *can't contact lender* (174). The company mix is very fragmented (330 companies, top one 6%). It includes earned-wage-access/cash-advance apps (Dave) and tribal-affiliated online lenders (Rosebud Economic Development Corp, WLCC).
**Who's hurting:** Very low-income workers with checking accounts and no credit cushion. The withdrawal problems show the harm is in their bank account, not just the loan.
**Root cause (inferred):** Online lenders based outside state rate caps, combined with repeated ACH debits that borrowers don't know how to stop.
**Today's workaround:** Closing the bank account (and losing direct deposit), stop-payment fees, or ignoring it until it goes to collections.

**Venture ideas**
1. **"Stop the debit" tool:** guides a borrower through revoking ACH authorization, files the bank's stop-payment and Reg E dispute, and keeps a record. Sold to banks and credit unions as a cheaper alternative to account churn and call-center handling.
2. **Payday payoff swap:** a credit-union small-dollar loan (like the NCUA PAL program) offered at the moment someone revokes a lender's debit, so they aren't left short of cash.

**Why now:** Cash-advance apps are growing, and states are enforcing against tribal lenders.
**Noise check:**
- Single company: pass.
- Short spike: pass.
- Policy-only: **partial fail** (unauthorized loans are an enforcement problem).
- Catch-all: pass.
- Artifact: pass.

**Biggest risk:** Volume is small (2.8k), and the people affected are hard to reach profitably.
**Next validation step:** Ask 3 credit unions how many members a month request stop-payments on payday lenders, and what that costs them.

| Venture fit | Who pays | Why now | Mobility impact |
|---|---|---|---|
| 3/5 | 3/5 | 3/5 | 4/5 |


## 5. USDA mortgage (score 3.22)


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

### Claude analysis

### Rural homeowners with USDA loans
**Verdict: Discard as a standalone.** Same pattern as FHA and VA, but only 363 complaints. Treat it as a rural channel for the FHA idea, not its own company.

**What's happening:** USDA mortgage complaints rose from 226 to 363 (1.60x). Issues match FHA: *struggling to pay* (203, mostly loss-mitigation communication) and *payment process and escrow* (119). The state mix is notably Southern and rural: FL, NC, LA, AL, OH.
**Who's hurting:** Rural low- and moderate-income buyers who used USDA's no-down-payment program, in areas with fewer housing counselors.
**Root cause (inferred):** The same escrow and affordability pressure, plus thin local counseling capacity.
**Today's workaround:** Remote HUD counselors, servicer phone lines.

**Venture ideas**
1. **Rural channel for the FHA loss-mit copilot:** a remote-first version for rural counseling agencies and USDA Rural Development partners.
2. **Hurricane-season escrow plan:** LA, FL and NC carry storm-insurance shocks. Partner with state housing finance agencies.

**Why now:** Insurance costs in Gulf states. HUD housing counseling NOFO (HSG-2600-DC-0033).
**Noise check:**
- Single company: pass.
- Short spike: pass.
- Policy-only: pass.
- Catch-all: pass.
- Volume: **fail** (363 is too small to support its own company).

**Biggest risk:** Too small on its own.
**Next validation step:** None separately. Include rural agencies in the FHA interviews.

| Venture fit | Who pays | Why now | Mobility impact |
|---|---|---|---|
| 2/5 | 3/5 | 3/5 | 4/5 |


## 6. Vehicle loan (score 3.22)


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

### Claude analysis

### Auto loans: repossession, deficiency balances and missing titles
**Verdict: Pursue.** The largest-volume signal here (21.9k), growing faster than baseline. A car is often what gets someone to work, and several pain points have clear B2B buyers.

**What's happening:** Vehicle loan complaints rose from 16,075 to 21,911 (1.36x). Top issues: *managing the loan* (6,619, mostly billing and add-on products), **repossession** (6,005, including balances left after the car is sold and trouble reinstating the loan), and *end of loan* (2,989), where **1,682 people paid off the loan but can't get their title**. There are also 730 complaints about loans opened without consent. Subprime lenders dominate the top five (Santander, Westlake, Credit Acceptance) alongside Ally and Capital One.
**Who's hurting:** Subprime borrowers who need a car for hourly jobs, concentrated in FL, TX, CA and GA.
**Root cause (inferred):** Loans made at 2021–23 peak car prices with high subprime rates, sold with expensive add-ons (GAP insurance, warranties). Repossession leaves a family with no car and a debt.
**Today's workaround:** Buy-here-pay-here dealers, borrowing from family, or losing the job.

**Venture ideas**
1. **Repo-prevention refinance:** spots borrowers 30–60 days late (opt-in through employer or credit-union apps) and refinances them into a credit-union or CDFI auto loan before repossession, refunding unused add-ons. Earns a referral fee from lenders. Employers pay to reduce turnover.
2. **Title and add-on recovery:** a service that chases lien releases and title delivery after payoff, and files for refunds on cancelled GAP and warranty products. Takes a fee on recovered refunds.

**Why now:** Subprime auto delinquencies are elevated (inferred from the repossession volume; verify with NY Fed data). Credit unions are looking for auto-loan growth.
**Noise check:**
- Single company: pass (Santander 10%).
- Short spike: pass (structural).
- Policy-only: pass.
- Catch-all: pass.
- Artifact: pass.

**Biggest risk:** Refinancing late subprime borrowers is real credit risk for the partner lender.
**Next validation step:** Ask 2 CDFI credit unions whether they would fund refinances for borrowers 30–60 days late at a given loss rate. In parallel, measure demand from title-recovery requests by sampling 50 complaints by complaint ID.

| Venture fit | Who pays | Why now | Mobility impact |
|---|---|---|---|
| 4/5 | 4/5 | 3/5 | 5/5 |


## 7. Rental debt (score 3.21)


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

### Claude analysis

### Disputed rental debt from former landlords
**Verdict: Watch.** Large and squarely low-income, with a matching HUD grant. But it is barely growing (1.02x baseline) and the top five collectors hold 58%, so it looks more like an enforcement target than a new market.

**What's happening:** Rental debt collection complaints rose from 10,630 to 12,181 (1.15x, about baseline). The dominant issue is **debt not owed** (5,437): *not mine* (3,492), *already paid* (993), *identity theft* (818). Next is *wrong amount* (2,855). National Credit Systems, a collector for apartment landlords, has 23% on its own.
**Who's hurting:** Renters who moved out and were later charged damage or early-termination fees. That debt then blocks their next apartment through tenant screening. Concentrated in TX, FL and GA.
**Root cause (inferred):** Move-out charges are disputed, often undocumented, and sent quickly to collections. Tenant-screening reports then pass the debt on to the next landlord.
**Today's workaround:** Paying debts they don't owe in order to get approved for a new lease, or legal aid (where available).

**Venture ideas**
1. **Move-out evidence and dispute kit:** a timestamped move-out inspection app plus automated debt-validation and dispute letters. Distributed through HUD-funded eviction-protection providers (PDR-2600-DC-0079) and legal aid organizations.
2. **Tenant-screening repair:** finds disputed rental debts on screening reports and runs the dispute process across screening companies. Paid by housing nonprofits or as a renter subscription.

**Why now:** HUD Eviction Protection Grant Program (PDR-2600-DC-0079) and growing attention to tenant-screening accuracy.
**Noise check:**
- Single company: borderline (23%; top five 58%).
- Short spike: pass.
- Policy-only: **partial fail** (collector conduct is an enforcement issue).
- Growth: **fail** (flat compared with baseline).

**Biggest risk:** Renters don't pay for this, so it depends on grant funding.
**Next validation step:** Ask 2 legal aid organizations how many rental-debt cases a month they turn away.

| Venture fit | Who pays | Why now | Mobility impact |
|---|---|---|---|
| 3/5 | 3/5 | 3/5 | 4/5 |


## 8. Vehicle lease (score 3.17)


- Complaints 2024-10-01..2025-09-30: **2,310**
- Complaints 2025-10-01..2026-09-30: **3,479**
- Growth: **1.51x** (vs all non-credit-reporting complaints: **1.34x**)
- Computed scores (0-5): growth 2.7, volume 3.2, LMI 4, spread 4.4, buyer 0.0 → **3.17**

## Top issues (recent window)
- Managing the loan or lease: 892 (sub-issues: Billing problem (442); Problem with fees charged (198); Problem with additional products or services purchased with the loan (167))
- Problems at the end of the loan or lease: 875 (sub-issues: Excess mileage, damage, or wear fees, or other problem after the lease is finished (217); Unable to receive car title or other problem after the loan is paid off (217); Termination fees or other problem when ending the lease early (175))
- Repossession: 779 (sub-issues: Loan balance remaining after the vehicle is repossessed and sold (145); Account reinstatement or redemption after repossession (134); Deficiency balance after repossession (95))
- Getting a loan or lease: 334 (sub-issues: Loan opened without my consent or knowledge (153); Confusing or misleading advertising or marketing (51); Credit denial (41))
- Incorrect information on your report: 310 (sub-issues: Account status incorrect (148); Account information incorrect (105); Information belongs to someone else (29))
- Problem with a company's investigation into an existing problem: 154 (sub-issues: Their investigation did not fix an error on your report (104); Problem with personal statement of dispute (19); Difficulty submitting a dispute or getting information about a dispute over the phone (18))

## Companies (211 total; top company share 11%, top 5 share 40%)
- HYUNDAI CAPITAL AMERICA: 391
- SANTANDER HOLDINGS USA, INC.: 328
- TOYOTA MOTOR CREDIT CORPORATION: 233
- AMERICAN HONDA FINANCE CORP: 222
- ALLY FINANCIAL INC.: 218

## States (53 with complaints)
- CA 634, FL 426, TX 281, NY 257, GA 160

## Matching federal funding (Grants.gov, posted/forecasted)
- none found

### Claude analysis

### Car leases: end-of-lease fees
**Verdict: Discard.** Growing (1.51x), but driven by automakers' own finance arms (Hyundai, Toyota, Honda) and end-of-lease fees. That's a less clearly low-income customer, and it overlaps with the stronger auto loan signal.

**What's happening:** Vehicle lease complaints rose from 2,310 to 3,479. Top issues are *billing* (442) and **end-of-lease charges** (875): excess mileage and damage fees (217), title problems (217), early-termination fees (175). There are also 153 complaints about leases opened without consent.
**Who's hurting:** A mix of middle-income lessees, plus subprime lessees through Santander. Concentrated in CA.
**Root cause (inferred):** Leases signed in 2022–23 are ending with high used-car values and disputed damage assessments.
**Today's workaround:** Paying the fees, or a third-party lease buyout.

**Venture ideas**
1. **Lease-end inspection evidence:** a pre-return photo and inspection app that the lessee can use to dispute damage charges.
2. **Lease-equity buyout:** helps lessees buy out leases worth more than the payoff and refinance with a credit union.

**Why now:** A wave of leases ending.
**Noise check:**
- Single company: pass.
- Short spike: **likely fail** (a wave of lease endings rather than a trend).
- LMI relevance: weak.
- Catch-all: pass.

**Biggest risk:** Not an economic-mobility customer.
**Next validation step:** None. Fold the useful parts (title and add-on recovery) into the auto loan opportunity.

| Venture fit | Who pays | Why now | Mobility impact |
|---|---|---|---|
| 2/5 | 2/5 | 2/5 | 2/5 |


