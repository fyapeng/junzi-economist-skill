# X033 Committed Release Audit

## Verdict

**PASS — 105/105 (100%)**

The commit provenance is exact and the response passes every requested Dao/economics criterion. It reconstructs constrained agency without inferring consent, makes control and information operational, calibrates stated preference, distinguishes resources/payments/producer surplus/incidence, states the Pareto boundary correctly, imposes a common nonrandomizable protection floor, defines heterogeneous-(N) support and explicit weights, separates (S/Z/G/D), restricts receipt LATE to common-(G) supported cells, centers spillover/displacement and total-policy effects, and uses correct nonoverlap outcome and treatment-effect bounds. No material or minor correction is required.

## Commit provenance

Repository checked: `C:\Users\ENAN\junzi-economist-skill`

- `git rev-parse HEAD`: `b8f461130d7968b771018eeaf1599c32b1bcf22e`
- `git show -s b8f4611`: `b8f461130d7968b771018eeaf1599c32b1bcf22e`
- Short commit: `b8f4611`
- Date: `2026-07-13 12:38:00 +0800`
- Subject: `fix: align interference support and transport bounds`

**Provenance result: exact match.** No repository evaluation records or other endpoint files were read.

## Scored rubric

| Dimension | Score | Evidence |
|---|---:|---|
| Dao object, constrained agency and branch decision | 15/15 | Public subsidy allocation is reconstructed as nonprice rationing under scarcity, care needs, income constraints and an imposed ten-day review penalty. The branch pauses, protects, audits, tests and can abandon. |
| Power, information and implementation | 15/15 | Agency, vendor, procurement, families and childcare providers have distinct controls and incentives. Opacity and conflicted appeal generate specific audit, explanation, correction, governance and stopping requirements. |
| Stated preference and claim calibration | 15/15 | The 21% is provisional hypothetical demand, not revealed welfare, exact take-up or an error rate. Descriptive, underidentified, unsupported and conditional recommendation statuses are type-consistent. |
| Resources, transfers, profit and incidence | 15/15 | Real inputs, payment flows, producer surplus, normal returns, productivity, rent, taxes, shifted costs, caregiver labor, provider response and distributional incidence are separated without double counting. |
| Pareto, Kaldor–Hicks and normative criteria | 15/15 | Pareto requires joint no-loser evidence; potential compensation differs from actual compensation; rights and weights remain explicit value choices. |
| Common nonrandomizable floor | 15/15 | Notice, correction, human decision, delay-neutral independent review, queue protection, accessibility, privacy, audits, stopping rules and institutional separation apply to every arm. |
| Heterogeneous-(N) fixed-count support and aggregation | 15/15 | Fixed-count, common-(G), spillover and total-policy contrasts have exact cell support; target family-mass weights, normalization and excluded support are explicit. |
| (S/Z/G/D), LATE and floor-consistent exclusion | 15/15 | Saturation, assignment, peer exposure and endogenous receipt are distinct; cell and aggregate LATE use correct support and complier weights; floor breaches are never identifying channels. |
| Full-adoption transport and nonoverlap bounds | 15/15 | Supported share (q) is family-weighted; outcome and effect bounds are distinct; unsupported effect range is ([L-U,U-L]); uncertainty and model dependence remain explicit. |

## Detailed audit

### 1. Economic object and agency

The answer identifies the allocation as rationing a fixed public subsidy rather than a prediction exercise. Families choose application, disclosure, review, acceptance, substitute care, work, waiting and exit, but those choices are made under scarcity, income and care constraints and a ten-day penalty imposed on review. Observed silence or compliance therefore cannot identify consent or welfare.

The policy response restores meaningful agency through notice, correction, delay-neutral review, nonretaliation, access-neutral consent where applicable, assisted channels and applicant-facing reasons. These are not decorative moral terms; they determine whether research may proceed.

### 2. Power and information are operational

The score vendor controls proprietary inputs and logic; the agency controls eligibility, queue position, records and remedies; procurement buys the system and adjudicates appeals; childcare vendors can change capacity and selection. Families bear error and delay while lacking reasons and an independent forum.

These asymmetries generate observable and enforceable requirements: decision logs, model versions, input access, correction records, independent appeal, subgroup reference processes, audit access, separation of functions and stopping rules. The institutional diagnosis changes implementation and the branch decision.

### 3. Stated preference is calibrated

The 21% response is explicitly provisional stated preference subject to sampling, wording, information, nonresponse and fear of disclosure. It establishes that human review cannot be presumed valueless, but it is not used as revealed welfare, actual review take-up, exact suppressed demand or an error rate. This is correctly bounded.

### 4. Scarce-capacity displacement

With fully used quota (K_j), aggregate slot receipt is fixed. The response correctly states that gains in award probability or timing for some families have counterparts in probability, delay or option value for others, unless only processing speed changes without rank or receipt. Exits remain outcomes rather than attrition to discard.

The evaluation therefore measures displaced identity, substitute care, work, children, provider responses, timing and distribution rather than treating unchanged slots as welfare neutrality.

### 5. Social accounting

The answer keeps one internally coherent account:

- real agency, vendor, review, appeal and compliance resources;
- subsidy payments and fees by payer and recipient;
- vendor producer surplus and its decomposition;
- caregiver work, earnings, taxes and substitute care;
- provider capacity, wages, staffing and quality;
- child/family outcomes and nonmarket harms;
- distribution across economically and legally relevant groups.

The 9% administration figure remains accounting until denominators, quality, shifted costs and uncertainty are audited. Vendor profit is not equated with social welfare or excluded as a mere transfer; it is assigned to owners and decomposed under explicit weights. No duplicate counting is present.

### 6. Pareto and Kaldor–Hicks

Pareto improvement is correctly underidentified/not established because no joint individual no-loser comparison exists. The answer does not infer that the claim is false merely from missing evidence. Kaldor–Hicks potential compensation is explicitly distinguished from actual documented compensation and from rights that may be nontradeable.

Population, horizon, family/child/owner weights, public funds, risk, inequality aversion and rights boundaries must be declared. Evidence is not presented as selecting those values.

### 7. Common protection floor

Every arm has unchanged eligibility/quota rules, no sole-score denial, notice, data inspection/correction, intelligible reasons, accountable human decision, delay-neutral independent review, queue and deadline protection, refusal/nonretaliation, accessibility, privacy/security, full logs, independent audits and harm stopping rules.

The response also recognizes a transport consequence: removing the old delay changes the policy, so unprotected pilot results do not automatically apply. Recurrence of delay is floor noncompliance, not an exclusion channel or experimental treatment.

### 8. (S/Z/G/D) separation

The response cleanly defines:

- (M_j): exact assigned count;
- (S_j=M_j/N_j): first-stage saturation label;
- (Z_{ij}): randomized own assignment;
- (G_{ij}=(M_j-Z_{ij})/(N_j-1)): assignment-induced peer exposure;
- (D_{ij}): endogenous actual material score use.

Slot receipt, timing and downstream outcomes are not mislabeled as (D). Peer receipts may refine the exposure mapping but remain endogenous. Assignment analysis remains primary.

### 9. Fixed-count support

Within exact ((n,k,m)), the fixed-count assignment contrast identifies

\[
\mu_1\!\left(n,k,\frac{m-1}{n-1}\right)
-\mu_0\!\left(n,k,\frac{m}{n-1}\right).
\]

The response correctly labels this as a compound own-assignment/one-peer-exposure contrast, not a controlled direct effect.

For common (G=m/(n-1)), it compares treated applicants in count arm (m+1) with control applicants in count arm (m), within the same exact (N=n), matched quota and implementation stratum. It explicitly states that equal counts across unequal (N) do not create equal exposure.

The additional condition that the saturation label be irrelevant after ((Z,G,n,k)) is fixed is stated rather than assumed silently. If arm-level policy features remain, the contrast must be interpreted as the joint supported policy contrast rather than a pure own-assignment effect.

### 10. Spillovers and total-policy effects

For a fixed own status (z), spillover contrasts use supported count arms (M=q+z), where peer counts (q=g(n-1)) are integers. Thus own assignment is held fixed while randomized peer exposure changes. These are assignment spillovers, not receipt effects.

The pool-mean total-policy contrast across exact-count policies aggregates direct, peer, congestion, provider and displacement channels. It reports both per-family and pool totals and retains the quota identity as a diagnostic rather than a welfare result. This is the preferred policy estimand and is correctly prioritized.

### 11. Explicit aggregation weights

Cell (h) includes exact (N), exact exposure, quota/implementation stratum and required count arms. For a family-average target, weights are proportional to target family mass:

\[
w_h=\frac{\sum_{j\in h}N_j}{\sum_{j\in\text{supported target cells}}N_j}.
\]

Weights are normalized only over supported cells, and support exclusions must be reported. Pool-average and fiscal targets use different declared denominators. The answer explicitly prohibits switching denominators or treating similar (N), identical (m) or identical saturation as exact exposure matching.

### 12. Receipt LATE

A cell LATE uses the common-(G), exact-(N) outcome contrast divided by the corresponding receipt first stage. Required conditions include randomization, nonzero first stage, no differential attrition, consistency, correct partial interference/exposure mapping, monotonicity and floor-consistent exclusion.

The exclusion threats are substantive and correctly named: notice, attention, documentation, staff behavior, appeal salience, provider response, queue signaling and endogenous peer receipt composition. If these remain, assignment and total-policy ITTs survive but the Wald ratio is not a receipt LATE.

Cross-cell aggregation is also correct: use complier/first-stage weights, equivalently a target-weighted sum of ITT numerators divided by the same target-weighted sum of first stages. Ordinary family-weighted averages of cell Wald ratios are explicitly rejected.

### 13. Transport and bounds

The supported share (q) is the eligible-family-weighted share of target exact cells with required arms, not the county share. The response correctly gives:

- treated outcome bound:
  \[
  [q\mu_{1,S}+(1-q)L,\ q\mu_{1,S}+(1-q)U];
  \]
- target treatment-effect bound:
  \[
  [q\tau_S+(1-q)(L-U),\ q\tau_S+(1-q)(U-L)].
  \]

This correctly uses ([L-U,U-L]) for unsupported unit effects and assigns weight (1-q) to nonoverlap. Sampling uncertainty is added to identification bounds. Tighter claims require explicit exchangeability, positivity, homogeneity and held-out validation; structural extrapolation remains model-dependent.

### 14. Status and branch calibration

Cost, speed, profit, slots and the survey remain provisional. Errors, exits, employment, child outcomes and mechanisms are underidentified. Pareto and universal welfare are not established. Withholding adoption and running a protected evaluation are conditional normative/research recommendations under declared criteria.

If the floor or measurement fails, the response abandons consequential experimentation and returns to human allocation/offline evaluation. This is a genuine backtrack and stop condition, not continued optimization of an invalid branch.

## Release checklist

| Criterion | Result |
|---|---|
| Commit `b8f4611` exact provenance | Pass |
| Constrained choice and stated preference | Pass |
| Power and agency operational | Pass |
| Resource/transfer/profit accounting | Pass |
| Pareto/Kaldor–Hicks | Pass |
| Common nonrandomizable floor | Pass |
| Heterogeneous-(N) fixed-count support | Pass |
| Common-(G) adjacent arms | Pass |
| Explicit family/pool/fiscal weights | Pass |
| Spillover/displacement | Pass |
| Pool total-policy effects | Pass |
| (S/Z/G/D) separation | Pass |
| Cell and aggregate LATE | Pass |
| Floor-consistent exclusion | Pass |
| Supported-share definition | Pass |
| ([L-U,U-L]) nonoverlap bounds | Pass |
| Transport assumptions and model dependence | Pass |
| Empirical/normative status calibration | Pass |

## Final determination

**PASS — 105/105 (100%).** X033 is internally coherent, design-supported and release-ready. No corrective edit is required.
