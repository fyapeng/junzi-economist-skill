# Blind red-team audit of X031

## Verdict

**MIXED, with one material design defect.** The response is otherwise a genuinely strong transfer. Agency and power alter the feasible set, institution design, outcome set, safeguards, welfare criteria, research branch, and adoption rule. Social accounting, Pareto/Kaldor–Hicks distinctions, the protection floor, scarce-capacity displacement, receipt/LATE discipline, universal transport, and claim-status calibration are all materially correct.

The single material defect is internal to the two-stage saturation design: the response assigns exactly `n_g S_g` applicants in each pool, then defines a direct effect that holds peer exposure fixed across own assignment. Under exact fixed-count assignment, own assignment mechanically changes the number of treated peers, so the displayed direct effect is not identified as written.

## Material defect: fixed-count assignment and the direct-effect estimand

The design states that within each pool exactly `m_g=n_g S_g` applicants receive `Z=1`. Peer exposure is

`G_ig = sum_{j != i} Z_jg / (N_g-1)`.

Therefore, within a pool with fixed treated count `m_g`:

- if `Z_ig=1`, then `G_ig=(m_g-1)/(N_g-1)`;
- if `Z_ig=0`, then `G_ig=m_g/(N_g-1)`.

Own assignment and peer exposure cannot take both values of `Z` at the same `G` within that saturation arm. Yet the response defines

`tau_dir(s)=E[Y_ig(1,G_ig(s))-Y_ig(0,G_ig(s))]`,

describing this as a direct assignment effect at saturation `s`. That contrast requires support for both own assignments at an identical peer exposure. Exact complete randomization supplies two adjacent peer exposures instead. The difference is `1/(N_g-1)` and may be numerically small in large pools, but it is an identification mismatch, not merely a standard-error detail.

This also affects the proposed spillover comparison if `G(s)` is treated as a single exposure value independent of own assignment. Saturation-specific exposure support must be indexed jointly by own assignment and the realized treated count among peers.

### Material correction

Choose one of three coherent approaches and state its estimand explicitly:

1. **Bernoulli second-stage assignment.** Assign each applicant independently with probability `S_g`. Then both `Z=0` and `Z=1` can occur at the same realized peer count, providing support for a direct effect conditional on common `G`, subject to adequate overlap.
2. **Retain exact fixed-count assignment and use design-supported effects.** Define the own-assignment contrast under the saturation design as
   
   `E[Y(1,(m_g-1)/(N_g-1))-Y(0,m_g/(N_g-1))]`.
   
   Label it an assignment effect under fixed total saturation, not a pure direct effect holding peer exposure constant. It combines own assignment with the mechanically induced one-peer exposure change.
3. **Recover fixed-exposure direct effects across adjacent treated-count designs.** Randomize pools to adjacent counts and combine cells that provide `Z=1` and `Z=0` at the same peer exposure. This requires prespecified support and estimators across saturation arms.

Whichever approach is chosen, use the same joint support logic for spillover estimands, randomization-based estimators, and positivity statements. Do not rely on large `N` to silently equate adjacent exposures.

This correction does not require weakening the protection floor or changing the policy branch. It only aligns the estimands with the specified assignment mechanism.

## Areas that pass the red team

### Agency and power

**Pass.** Review delay, opaque scoring, fixed awards, financial dependence, deadlines, and adjudicative conflict enter the feasible set and institutional model. Observed nonreview is not treated as satisfaction. The 26% survey is hypothetical stated preference, not revealed welfare or misclassification prevalence. Procurement, adjudication, audit, and appeal are separated in the remedy.

### Social accounting

**Pass.** The 13% figure is provisional accounting rather than social surplus. Vendor profit is not called a resource saving or casually reduced to rent; it is decomposed into opportunity cost, normal return, productivity, taxes, market-power rent, and shifted costs. Payments, resources, ownership, incidence, applicant burden, employment, enrollment, and debt are not double-counted.

### Pareto and Kaldor–Hicks

**Pass.** The Pareto claim is unsupported rather than contradicted, because joint no-loser evidence is missing. Potential compensation is distinguished from compensation actually specified, funded, received, and sufficient. Rights and due process are allowed to remain nontradeable under a stated criterion.

### Protection floor

**Pass.** Notice, correction, accountable human decision, independent no-delay review, queue and deadline protection, refusal of optional data use, accommodations, privacy, audit access, stopping rules, and institutional separation bind every arm. Historical review delay is a floor violation, not an experimental channel. Review capacity is sized ex ante and uptake is treated as an outcome rather than rationed.

### Scarce capacity and interference

**Pass apart from the fixed-count estimand mismatch.** The response correctly treats the 10,000-award cap as an allocation constraint, distinguishes identity and timing from totals, defines defensible pools and quotas, and recognizes that the state may be one interference network. Displacement, rank reversals, cross-pool effects, reviewer queues, common deadlines, vendor learning, and statewide rules enter the analysis.

### `Z/G/D`, ITT, LATE, and exclusion

**Pass apart from the direct-effect support defect.** Randomized assignment `Z`, peer exposure `G`, and endogenous receipt `D` are separated. Receipt is never substituted for assignment. The LATE conditions include relevance, exclusion, monotonicity, defined compliers, modeled interference, and handled attrition/measurement. Live direct-assignment channels above the floor are named, while review delay, missing explanations, and appeal penalties are correctly classified as floor failures rather than admissible exclusion pathways.

### Universal transport

**Pass.** The response does not extrapolate from saturation below one. It requires dose-response evidence, target-population support, equilibrium assumptions, near-universal stress tests, held-out replication, cross-pool analysis, vendor/staff adaptation, and renewal gates. It recognizes that statewide capacity interference may require cohort-level rollout, structural modeling, or partial identification rather than scaled individual ITT.

### Claim labels

**Pass.** Reported costs, timing, profit, award totals, and survey answers remain provisional. Accuracy, access, downstream outcomes, Pareto improvement, and universal effects remain underidentified or unsupported. The pause, floor, and evaluation are explicitly conditional normative/research recommendations rather than empirical findings.

## Final assessment

X031 is very close to a clean transfer, but the exact assignment mechanism and displayed direct-effect estimand are mathematically inconsistent. Because this error affects what the randomized design identifies, the final verdict is **MIXED**. Correcting the fixed-count exposure support as above would be sufficient for a pass; no other material defect was found.

---

## Retest after revision

### Final verdict

**PASS.** The initial **MIXED** verdict above is preserved as audit history. The finite-population common-`G` defect is closed, and the repair is carried consistently through the spillover, total-policy, and Wald/LATE sections. No material new contradiction was introduced.

### Finite-population support and own-assignment ITT

**Closed.** The revised response explicitly derives the exposure support under exact fixed-count assignment. With `m_g(s)=N_g s` treated applicants:

- treated applicants have `G^1_g(s)=[m_g(s)-1]/(N_g-1)`;
- control applicants have `G^0_g(s)=m_g(s)/(N_g-1)`.

It states that the design supplies no treated and control observations at a common realized peer exposure within a saturation arm and refuses to erase the difference as a large-pool approximation.

The revised estimand

`tau_FC,g(s)=N_g^{-1} sum_i [Y_i(1,(m-1)/(N-1))-Y_i(0,m/(N-1))]`

matches the assignment mechanism. Under complete randomization of exactly `m` applicants, the treated-minus-control mean difference is unbiased for this finite-population contrast, given the stated exposure mapping. The text correctly labels it a fixed-count own-assignment ITT that combines own assignment with the mechanically adjacent peer-exposure change. It no longer calls it a pure direct effect holding `G` fixed.

The response also states what would be needed for a pure common-`G` contrast: a different assignment scheme or adjacent treated-count arms providing both own-assignment states at the same peer count. This is the correct support condition.

### Spillover/displacement estimand

**No contradiction.** The revised control spillover contrast compares

`Y_i(0,m(s)/(N-1))` with `Y_i(0,m(s')/(N-1))`

across first-stage randomized saturation arms. Unlike the original direct-effect formula, this comparison holds own assignment at zero and deliberately changes peer exposure. The response conditions interpretation on common eligibility/support across saturation arms and places the expectation over pools randomized at the first stage.

This design can recover a control spillover effect because control applicants occur at each nonfull saturation and are random subsets within pools. The response appropriately treats award displacement, queue changes, reviewer attention, winner identity, need, rank reversals, and transition matrices as outcomes. At full saturation there are no controls, so this particular control-spillover estimand lacks support; the transport section correctly recognizes that fact rather than extrapolating it mechanically.

### Total-policy effect

**No contradiction.** The pool-average total-policy contrast explicitly averages the realized mixture of `m(s)` assigned and `N-m(s)` unassigned applicants at their respective adjacent exposures. It incorporates own-assignment and within-pool spillover channels without claiming a direct/spillover decomposition that the fixed-count design cannot identify.

The quota identity is also handled correctly: when pools fill, total awards cannot change, but award composition, timing, review, burden, enrollment, debt, administrative resources, and welfare can. Comparing pool averages across randomized saturation arms is therefore mandate-relevant at supported saturations, while universal transport remains a separate problem.

### Wald/LATE under compound states

**No contradiction.** The revised Wald discussion uses the same compound assignment states as the reduced-form ITT:

- `(Z=1,G=(m-1)/(N-1))`;
- `(Z=0,G=m/(N-1))`.

It does not present the ratio as a pure receipt effect by default. A saturation-specific complier interpretation is conditioned on random and relevant assignment, well-defined receipt and outcome potential states, monotonicity across the compound states, exclusion of both direct assignment and adjacent peer-exposure channels, a captured interference structure, handled attrition/measurement, and a described complier population.

The response correctly identifies why exclusion is implausible in a fixed scholarship pool: the one-peer exposure change is part of the instrument contrast and can affect competition even apart from own receipt. Notice, documentation, reviewer attention, legitimacy, effort, queue position, and staff/vendor behavior provide additional live direct channels. Historical delay, missing explanation, and appeal penalties remain prohibited floor failures rather than accepted exclusion pathways. The recommended headline remains ITT, not Wald/LATE.

## New-contradiction screen

No material inconsistency was found.

- **Two-stage design:** first-stage pool saturation and second-stage exact-count assignment now align with the estimands.
- **`Z/G/D`:** assignment, peer exposure, and endogenous receipt remain separate throughout.
- **Finite-population inference:** exact support, pool weights, randomization-based estimators, cluster uncertainty, unequal probabilities, and multiple outcomes are acknowledged.
- **Partial interference:** pool validity is conditional on real scholarship competition and reviewer queues; statewide dependence remains a stopping or redesign condition.
- **Protection floor:** score assistance varies only above common notice, correction, human decision, no-delay independent review, privacy, audit, and stopping protections.
- **Social accounting:** administrative costs, vendor profit, real inputs, normal returns, rents, shifted costs, taxes, ownership, enrollment, and debt remain distinct.
- **Pareto/Kaldor–Hicks:** no-loser evidence remains absent; potential compensation is not actual compensation or a rights override.
- **Universal transport:** saturation below one is not scaled mechanically; full policy requires support, replication, invariance assumptions, equilibrium analysis, or partial identification.
- **Claim labels:** empirical reports, causal unknowns, welfare conclusions, and conditional recommendations retain calibrated statuses.

### Retest conclusion

The revised X031 response is a **clean transfer** and merits **PASS**. It resolves the exact finite-population identification problem rather than approximating it away, and the correction remains coherent across all downstream estimands and policy conclusions.
