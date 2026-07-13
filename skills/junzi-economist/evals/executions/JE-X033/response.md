# Regulator-ready economic judgment

## Decision

The governor's Pareto-improvement claim is **not established**. The evidence is unaudited, no joint individual-welfare comparison has been made, and fixed county-year slot capacity makes displacement intrinsic. If all `K_j` slots are used, a higher probability or earlier offer for one family must be offset by a lower probability, later offer, or changed option value for another family unless the reported gain is only faster processing with no change in rank or receipt. The missing loser evidence makes the Pareto claim underidentified; it does not yet prove that the claim is false.

Do **not** authorize universal adoption now. Freeze expansion, preserve current records, and require an independent input/output and process audit. A bounded evaluation may continue only after the common protection floor below is operational in every arm. If the agency cannot make human review delay-free and independent, or cannot observe all eligible families rather than only respondents and recipients, the correct research decision is to pause rather than randomize weaker rights.

## Economic object, agency, and power

The allocation is not “prediction” in isolation. It is nonprice rationing of a fixed public subsidy. Relevant agents are eligible families and children, caregivers, county staff, childcare vendors and workers, the score vendor, procurement and appeals staff, taxpayers, and elected officials. Families choose whether to apply, disclose information, contest a score, accept an offered vendor, shift to paid or informal care, work, wait, or exit—but scarcity, care needs, income, and the ten-day review penalty sharply constrain those choices. Observed compliance or silence is therefore not consent or revealed welfare.

Power and information are asymmetric. The score owner controls proprietary inputs and logic; the agency controls eligibility, queue position, records, and remedies; vendors can gain profit and may adapt capacity or selection; procurement both buys the system and hears appeals, creating an institutional conflict between contract defense and impartial adjudication. Families bear error and delay while lacking reasons or an independent forum. The 21% survey response favoring delay-free human review is, at most, provisional stated-preference evidence with unknown sampling, wording, information, nonresponse, and fear-of-disclosure properties. It nevertheless shows that human review cannot be treated as valueless.

## Scarce-capacity displacement and social accounting

For county-year pool `j`, let `N_j` be eligible families and `K_j` the fully used slot quota. Then

`sum_i Slot_ij = K_j`.

Consequently, the sum of treatment effects on eventual slot receipt is zero within a pool when eligibility, quota, utilization, and horizon are fixed. The score can redistribute who receives a slot and when; it cannot create slots. A faster offer to a high-score family may be a benefit, but its counterpart—later service, lost receipt, increased uncertainty, or costly substitute care—must be measured for lower-ranked families. Exits are outcomes, not harmless attrition.

Use one social account. Report separately:

- real agency labor, computing, vendor production, review, appeal, and compliance resources;
- subsidy payments and fees by payer and recipient, without counting transfers twice;
- vendor producer surplus accruing to identified owners, decomposed where possible into normal return, productivity gain, market-power rent, taxes, and costs shifted to workers, families, or the public;
- caregiver employment, earnings, taxes, paid and unpaid substitute care, travel and waiting time;
- provider entry, exit, staffing, wages, quality, and capacity responses;
- child development, safety, continuity, and family stress;
- privacy, autonomy, dignitary loss, reason-giving, option value, and due process; and
- incidence by income, race/ethnicity, disability, language, family structure, geography, and other legally or substantively protected groups.

Thus the reported 9% administration-cost reduction is not yet a 9% social-resource gain, higher vendor profit is not itself social welfare, and unchanged slots is not evidence of unchanged welfare. A defensible welfare statement must specify the population and horizon, family/child and owner weights, treatment of taxpayers and public funds, risk and inequality aversion, and which rights are nontradeable. Report both unweighted physical/resource quantities and results under preregistered distributional weights. Do not collapse rights into dollars unless the regulator explicitly adopts that value boundary. Pareto improvement requires credible evidence that every affected person's welfare is weakly higher and at least one is strictly higher; Kaldor-Hicks potential compensation is different, and actual compensation must be documented rather than imagined.

## Common nonrandomizable protection floor

Every experimental and comparison arm must receive the same floor:

1. unchanged statutory eligibility and quota rules; no denial based solely on the proprietary score;
2. timely notice that a score is used, the operative reasons and data sources, and a usable route to inspect and correct data;
3. meaningful human review completed within the ordinary offer clock, with no ten-day penalty, no loss of queue position, and an urgent override for imminent harm;
4. an appeal decided by a function institutionally separate from procurement, the vendor, and the original decision-maker, with a reasoned record;
5. refusal, correction, appeal, and exit without retaliation or reduced access; access-neutral consent where consent is legally and operationally appropriate;
6. complete decision logs, model/version records, access controls, retention limits, incident reporting, and independent audit access;
7. monitoring of false deprioritization and subgroup error against an independently defined reference process, plus preregistered harm stopping rules; and
8. a staffed human pathway throughout the study and after it; no arm may withdraw basic due process, privacy, accessibility, or safety.

If this floor changes current delays or implementation, old pilot results do not automatically transport to the protected policy. A delay removed by the floor also cannot later be invoked as an exclusion violation; its recurrence is floor noncompliance.

## Protected evaluation under partial interference

### Pools and variables

Define a pool `j` as a county-year allocation queue with a predeclared closure time, a fixed eligible roster `N_j`, quota `K_j`, common implementation regime, and outcome horizon. Assume partial interference only after checking that families cannot cross county pools, providers do not reallocate capacity across pools, staff do not learn across simultaneously randomized pools in outcome-relevant ways, and the same household is not counted in overlapping cohorts. Provider and queue responses within a pool are part of the policy effect, not nuisances. If cross-pool links remain, enlarge or cluster pools and redefine exposure before estimation.

Let:

- `M_j` be the exact number assigned to algorithmic prioritization in pool `j`;
- `S_j = M_j/N_j` be the randomized saturation label;
- `Z_ij in {0,1}` be family `i`'s randomized assignment above the common floor;
- `G_ij = sum_(l != i) Z_lj/(N_j-1) = (M_j-Z_ij)/(N_j-1)` be assigned-peer exposure; and
- `D_ij in {0,1}` be endogenous receipt—whether the score actually enters family `i`'s operative priority decision—after opt-out, technical failure, override, appeal, or staff noncompliance.

`S`, `Z`, `G`, and `D` are not interchangeable. In particular, under exact-count assignment a treated family in an `M=m` pool has `G=(m-1)/(N-1)`, while a control family has `G=m/(N-1)`.

### Two-stage exact-count saturation design

Before assignment, enumerate all eligible families and record baseline covariates. Form randomization strata by exact `N_j=n`, exact `K_j=k` where replication permits (otherwise a prespecified quota stratum with exact `k` retained in estimation), calendar, and implementation regime. Within strata, stage 1 randomly assigns pools to a menu of feasible integer counts `M_j=m`; counts should include adjacent arms `m` and `m+1`. Stage 2 uses simple random sampling without replacement to assign exactly `m` of the `n` families to `Z=1`. No count arm may weaken the floor. The menu must leave a genuine human pathway and be chosen for overlap, not convenience.

Preregister primary outcomes for every eligible family: application/exit, offer timing and rank, receipt, false deprioritization, correction and appeal, substitute care, caregiver employment and earnings, child outcomes, provider outcomes, administrative resources, and subgroup errors. Audit assignment and receipt, analyze by assignment, keep exits in denominators, and use randomization-based inference respecting both stages and pool-level assignment. Survey outcomes remain secondary unless nonresponse is corrected under stated assumptions.

### Design-supported estimands

Write mean potential outcomes under the assigned-exposure mapping as `mu_z(n,k,g)`. This mapping is itself testable and fails if identities, network position, or peer receipt matter beyond assigned peer share.

**Fixed-count assignment contrast.** Within the same exact `(n,k,m)` cell,

`Delta_FC(n,k,m) = E[Y | N=n,K=k,M=m,Z=1] - E[Y | N=n,K=k,M=m,Z=0]`

identifies

`mu_1(n,k,(m-1)/(n-1)) - mu_0(n,k,m/(n-1))`.

This is supported by stage-2 randomization, but it is not a direct effect at fixed peer exposure: own assignment changes while assigned-peer exposure differs by `1/(n-1)`.

**Common-`G` assignment contrast.** Let `g=m/(n-1)` with integer `m`, and require randomized support for both total-count arms `M=m` and `M=m+1` at the same exact `N=n` (and matched `K=k` and implementation stratum). Then

`Delta_CG(n,k,g) = E[Y | N=n,K=k,M=m+1,Z=1] - E[Y | N=n,K=k,M=m,Z=0]`

compares two families each facing `G=g`. It identifies `mu_1(n,k,g)-mu_0(n,k,g)` only if the exposure mapping makes the saturation label irrelevant once `(Z,G,n,k)` is fixed. Equal counts across different `N` do not imply equal exposure. Across sizes, use only counts satisfying `m_n=g(n-1)` as integers, estimate within exact `n`, then aggregate.

**Spillover contrasts.** For fixed `z` and peer counts `q_r=g_r(n-1)` that are integers with supported arms `M=q_r+z`, define

`Psi_z(n,k;g_1,g_0) = E[Y | N=n,K=k,M=q_1+z,Z=z] - E[Y | N=n,K=k,M=q_0+z,Z=z]`.

This changes assigned-peer exposure while holding own assignment fixed. It is a spillover of assignment, not receipt.

**Total policy contrasts.** For two randomized exact-count policies `a` and `b`,

`TP(n,k;a,b) = E[bar(Y)_j | N=n,K=k,M=a] - E[bar(Y)_j | N=n,K=k,M=b]`.

This is the preferred policy estimand because it includes direct effects, queue displacement, provider responses, and within-pool spillovers. Report both per-eligible-family outcomes and pool totals. Slot-receipt totals should satisfy the `K_j` accounting identity; deviations diagnose vacancies, horizon changes, or data error.

Aggregate only supported cells. For a family-average target, use prespecified target family-mass weights

`w_h = (sum_(j in target cell h) N_j)/(sum_(j in supported target cells) N_j)`,

where `h` contains exact `N`, exact exposure, quota/implementation stratum, and the required count arms. Normalize weights over supported cells. Use pool weights for a pool-average administrative estimand and fiscal weights for a budget total; do not switch denominators. Same `m`, same `S`, or similar `N` is not exact exposure matching.

### Receipt effects and LATE

`D` is not randomized. A receipt effect may be estimated only on a common-`G`, exact-`N` supported contrast via the Wald ratio

`LATE(n,k,g) = Delta_CG^Y(n,k,g) / Delta_CG^D(n,k,g)`,

provided the first stage is nonzero. Interpretation as a complier LATE requires: two-stage randomization and no differential attrition; consistency; partial interference and a correct assigned-exposure mapping; monotonicity `D_i(1,g) >= D_i(0,g)`; and exclusion at the protection floor, `Y_i(z,g,d)=Y_i(d,g)`. Exclusion requires that `Z` affect the outcome only through own receipt `D` at common `G`: no independent effect through notice, attention, documentation, staff behavior, appeal salience, provider response, queue signaling, or peer receipt composition not captured by `G`. These are demanding, auditable conditions. If peer endogenous receipt matters, the simple Wald estimand is not a receipt LATE even though assignment ITTs and total-policy ITTs remain valid.

An aggregate LATE must use complier-share weights: equivalently, take a target-weighted sum of common-`G` outcome ITTs divided by the same target-weighted sum of first stages. Do not average cell Wald ratios with ordinary family weights, and do not carry a numerator or denominator across unmatched `N`, `G`, or populations.

## Full-adoption transport and bounds

Universal adoption is a policy counterfactual, not the unit-level ITT at one observed saturation. It requires the full-adoption exposure and provider/queue equilibrium, compliance with the floor, and target support across county sizes and quotas. Define `q` as the **eligible-family-weighted** share of the target population whose exact `(N,K,G,implementation)` cells and required count arms are supported:

`q = sum_j N_j 1{target cell j supported} / sum_j N_j`.

Do not use the share of counties unless the target is explicitly the average county. Let all relevant potential outcomes lie in `[L,U]`. For a supported treated-policy mean `mu_1,S`, the target treated outcome is bounded by

`[q*mu_1,S + (1-q)*L, q*mu_1,S + (1-q)*U]`.

Outcome bounds are not treatment-effect bounds. An unsupported unit's effect lies in `[L-U,U-L]`, so if the supported average effect is `tau_S`, the target effect is bounded by

`[q*tau_S + (1-q)*(L-U), q*tau_S + (1-q)*(U-L)]`.

Sampling uncertainty around supported quantities must be added to these identification bounds. Tighter transport requires preregistered effect-homogeneity, reweighting/selection-exchangeability and positivity assumptions, plus validation in held-out pool sizes; otherwise report the bounds. With no randomized full-adoption or adjacent exposure support, the unsupported share receives weight `1-q`, not `q`, and a structural extrapolation must be labeled model-dependent rather than causal evidence.

## Calibrated statuses and recommendations

- **9% lower administration cost:** provisional accounting fact; baseline, denominator, quality, shifted costs, and uncertainty unaudited.
- **Faster offers for high-score families:** provisional descriptive fact; causal source and counterpart delays/displacement unaudited.
- **Higher vendor profit:** provisional accounting fact; ownership, opportunity cost, rent, productivity, and shifted-cost incidence unknown.
- **Unchanged total slots:** provisional balance fact; consistent with fixed capacity and therefore informative about redistribution, not welfare neutrality.
- **21% favor delay-free human review:** provisional stated preference; representativeness and interpretation unaudited.
- **Effects on false deprioritization, exit, employment, children, substitute care, and subgroup error:** underidentified because the necessary outcomes and processes are unaudited.
- **Pareto improvement and universal-adoption welfare gain:** underidentified/not established; no-loser, equilibrium, distributional, rights, and transport evidence is missing.

The normative recommendation is conditional: under a criterion that gives positive weight to affected families and children, treats due process and meaningful review as a floor, and counts displaced and shifted costs, universal adoption should be withheld. The research recommendation is also conditional: continue only a protected, independently governed, two-stage exact-count evaluation with audited full-roster outcomes and harm stopping rules. Adopt more broadly only if total-policy effects—not merely high-score-family ITTs—show acceptable child and family outcomes, no unacceptable subgroup or rights violations, transparent social-resource gains, and transport support or honestly narrow bounds. Otherwise retain or redesign human allocation; if the floor repeatedly fails, abandon the algorithmic expansion branch.
