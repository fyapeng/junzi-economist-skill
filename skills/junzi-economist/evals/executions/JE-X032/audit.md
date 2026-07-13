# X032 Committed Clean-Transfer Audit

## Verdict

**MIXED — 92/105 (87.6%)**

The commit provenance is exactly verified, and the response passes nearly all substantive Dao and economics criteria. It correctly reconstructs constrained agency, makes institutional power operational, distinguishes stated preference from revealed welfare, separates producer surplus from resources and transfers, calibrates Pareto status, imposes a common nonrandomizable floor, separates (S/Z/G) from endogenous (D), defines fixed-count and interference-aware estimands, limits LATE by exclusion, and refuses to transport pilot saturation mechanically to statewide adoption.

Two design/bounding errors prevent a clean pass.

1. The adjacent-arm common-(G) contrast (Delta_m(g)) is common support only when compared pools have the same (N), or when treated counts are selected pool by pool so that the realized peer fraction is exactly matched. The design begins with heterogeneous (N_j) but later suppresses the (j) subscript and uses the same (m). If (N_j) differs, ((m-1)/(N_j-1)) differs, so the displayed contrast is not at common (G). This also affects the proposed common-(G) IV/LATE.
2. The transport section says that if outcomes lie in ([L,U]), a nonoverlap share (q) contributes (q[L,U]) to an effect estimate. For an average treatment effect with both potential outcomes bounded in ([L,U]), the worst-case effect interval is ([L-U,U-L]), so the nonoverlap contribution is (q[L-U,U-L]), unless one potential outcome is observed and a sharper explicitly derived bound is used. The current formula mixes outcome-level and effect-level bounds.

Both errors are local and repairable, but both concern explicitly requested release criteria—common-(G) support and full-adoption transport bounds—so the current result is `MIXED`, not `PASS`.

## Commit provenance

Repository checked: `C:\Users\ENAN\junzi-economist-skill`

- `git rev-parse HEAD` returned `2e2c603a7af8390fa37ee1f49a9786f0a5563b5e`.
- `git show -s 2e2c603` resolved to the same full object ID.
- Short ID: `2e2c603`.
- Commit date: `2026-07-13 12:31:06 +0800`.
- Subject: `fix: operationalize agency and protected allocation`.

**Provenance result: exact match.** This audit did not inspect repository evaluation records or other endpoint files.

## Scored rubric

| Dimension | Score | Judgment |
|---|---:|---|
| Dao object, constrained agency and institutional branch | 14.5/15 | Court authority, detention risk, urgent health/family needs, weak options and the imposed 12-day review penalty define the menu. The branch changes to pause, floor, audit and possible termination. |
| Power, information and implementation | 15/15 | Court, clinicians, vendor, procurement and defendants have distinct control and information. Conflict, secrecy, correction, audit, appeal and stopping are operational. |
| Stated preference and claim status | 15/15 | The 23% is hypothetical demand, not revealed welfare or exact error. Descriptive, underidentified, unsupported and conditional recommendation statuses are type-consistent. |
| Profit, resources, transfers and incidence | 15/15 | Vendor profit is producer surplus, not a resource saving; payments, real inputs, normal returns, productivity, rents, taxes and shifted costs are separated without double counting. |
| Pareto, Kaldor–Hicks and normative constraints | 15/15 | Pareto is not established but not contradicted; potential compensation is distinct from paid compensation and rights. Weights and nontradeable constraints remain public choices. |
| Common nonrandomizable floor | 15/15 | Delay-free independent review, counsel, correction, explanation, safety, human responsibility, privacy, subgroup monitoring and appeal apply to every arm; breach is noncompliance. |
| Fixed-count (C_m), common-(G) (Delta), spillovers and totals | 11/15 | (C_m), own-status spillovers and pool total effects are conceptually strong. (Delta_m(g)) lacks an equal-(N) or exact-(g)-matching condition when (N_j) varies. |
| (Z/G/D), LATE, transport and bounds | 11.5/15 | Receipt is endogenous and exclusion threats are clear. Common-(G) LATE inherits the support issue, and the nonoverlap worst-case effect bound is incorrectly written. |

## Detailed findings

### 1. Constrained agency and stated preference

The response does not infer consent from remaining in the score-assisted process or failing to request review. The nominal clinician-only alternative imposes a 12-day cost under possible detention and urgent health/family need. That imposed penalty is analytically distinct from background dependence on a scarce public pathway.

The 23% survey response is correctly limited to stated demand for a hypothetical delay-free review. It is not used as a revealed welfare measure, an error rate, exact take-up or proof of preference among the remaining 77%.

### 2. Power and agency change the action set

The court controls liberty-relevant procedure and the queue; clinicians control access and judgment; the vendor controls proprietary information; procurement both contracts and hears appeals. These facts generate independent appeal, counsel, correction, audit access, logged versions, human responsibility, subgroup monitoring and termination conditions.

The answer does not merely append fairness language. Current consequential use pauses, the floor precedes research, and inability to secure protection or audit access ends the pilot. This is a genuine Dao conflict among liberty, health, due process, scarcity, efficiency and distribution.

### 3. Resource and profit accounting

The reported 10% cost change remains unaudited accounting until labor, treatment capacity, court/clinician time, jail use, detention, health, earnings, caregiving, data/audit costs and vendor inputs are reconciled. Payments are mapped to payer and recipient rather than counted as multiple resource changes.

Vendor profit is accurately treated as producer surplus accruing to owners, not itself a real-resource saving. Decomposition includes normal return, productivity, rent, taxes and costs shifted to defendants, workers, families or agencies. Distributional weights and incidence remain explicit. No double count is present.

### 4. Pareto and Kaldor–Hicks status

The response says the Pareto claim is unsupported because no evidence shows every affected person weakly benefits. It also says this does not prove the claim false. That is the correct evidentiary status.

Kaldor–Hicks is separately identified as monetized gains sufficient for potential compensation, not actual compensation or resolution of rights. Distributional weights on liberty, health, waiting, error, public cost and vendor surplus are explicit. Evidence is not presented as choosing due process or nondiscrimination constraints.

### 5. The common protection floor is nonrandomizable

Every arm receives notice, counsel, interpretation/accommodation, data correction, delay-free independent clinician review, preserved queue position, safety override, accountable human decisions, logs, privacy, subgroup monitoring and independent appeal. The score cannot control detention, guilt, sentence or eligibility and cannot be the sole priority basis. The prior 12-day delay is removed; recurrence is floor failure, not experimental variation or a useful exclusion channel.

### 6. Fixed-count assignment and (C_m)

For a pool of size (N) assigned exactly (m) treated applicants, the response correctly defines

\[
G_i=\frac{m-Z_i}{N-1}
\]

and the design-supported compound assignment contrast

\[
C_m=E\left[Y_i\left(1,\frac{m-1}{N-1}\right)-Y_i\left(0,\frac{m}{N-1}\right)\right].
\]

It correctly states that (C_m) changes own assignment and peer exposure by one peer and is not a controlled direct effect at equal (G). This part passes.

### 7. Adjacent-arm common-(G) contrast needs an equal-size or matching condition

The response defines capacity pools with heterogeneous sizes (N_j), then writes adjacent count arms (m-1) and (m) using an unsubscripted (N). Common exposure follows only when denominators match:

- treated in an (m)-count pool: (G=(m-1)/(N_j-1));
- control in an ((m-1))-count pool: (G=(m-1)/(N_{j'}-1)).

These are equal only if (N_j=N_{j'}), or if pool-specific treated counts (m_j,m_{j'}) are chosen to solve an exact common-(g) condition. Merely assigning adjacent counts does not create common support across unequal pool sizes.

The design must therefore do one of the following:

1. restrict each adjacent-arm comparison to strata with identical (N);
2. construct pool-specific count pairs that yield exactly the same peer fraction and preregister the matched-support set;
3. redefine exposure as a coarser category and accept the corresponding estimand, with approximation error/bounds; or
4. omit the pure direct common-(G) claim and retain (C_m), saturation spillovers and total-policy effects.

Until one is stated, (Delta_m(g)) is not generally identified as displayed.

### 8. Spillover and displacement estimands

The own-status spillover contrasts across randomized counts are appropriate conditional on comparable pools and first-stage randomization. For (z=0), they measure how control outcomes change as more peers receive assignment; for (z=1), the corresponding peer counts are adjusted by one. Placement, detention and untreated time make these central displacement estimands.

The answer also requires cross-pool transfer, shared clinicians, repeated appearances and carryover measurement before assuming partial interference. If leakage is material, clusters expand or the policy unit becomes the state. This is correct.

### 9. Pool total-policy effects

The randomized pool-mean contrast (T(m_b,m_a)) appropriately aggregates assignment, peer, congestion and displacement effects under the fixed capacity/allocation rule. It does not require decomposition into a pure direct effect. Under fully used fixed slots, aggregate receipt is mechanically limited, while identity, timing, quality, detention, exit and welfare remain consequential. This passes.

### 10. (Z/G/D) and LATE

The response cleanly separates saturation (S), randomized own assignment (Z), assignment-based peer exposure (G), and endogenous actual score use (D). Appointment receipt and outcomes are not mislabeled as (D). Assignment ITTs remain primary.

The proposed receipt LATE is limited by relevance, monotonicity, defined compliers, exclusion and modeled interference. Direct assignment channels—notice, documentation, clinician attention, data correction, legitimacy and queue behavior—are explicitly named. Peer receipt beyond assigned-peer exposure is also an exclusion/interference threat.

However, “valid only at common (G)” inherits the unequal-(N) issue. If the instrument compares treated observations in an (m) arm with control observations in an (m-1) arm, exact peer exposure must be proven equal. Without the support restriction, the Wald ratio mixes receipt with different peer exposure. Even with exact common (G), the listed direct (Z) channels make exclusion demanding. The answer correctly says floor violations cannot supply exclusion variation.

### 11. Full-adoption transport bounds contain an effect-scale error

The response correctly refuses to infer (S=1) from sub-universal saturation and requests overlap, reweighting, equilibrium sensitivity and structural/bounding analysis.

The numerical bounding statement is not correct as written. If both potential outcomes are bounded by

\[
Y(1),Y(0)\in[L,U],
\]

then the individual treatment effect lies in

\[
Y(1)-Y(0)\in[L-U,U-L].
\]

Therefore, for a nonoverlap target share (q), its worst-case contribution to an average treatment effect is

\[
q[L-U,U-L],
\]

not (q[L,U]). If one potential outcome or target baseline mean is observed, the response may derive sharper bounds, but it must state the observed object and formula. Outcome bounds cannot be inserted directly into an effect aggregation.

### 12. Transport and status otherwise remain calibrated

The response appropriately rejects monotonic benefit under fixed capacity, allows only prespecified sensitivity tightening, requires overlap for reweighting and includes vendor/provider/equilibrium responses. Its status section correctly labels reported facts provisional, causal and welfare claims underidentified, Pareto unsupported, and action/research recommendations conditional.

## Material-error screen

| Criterion | Finding | Consequence |
|---|---|---|
| Commit provenance | Exact `2e2c603a7af8390fa37ee1f49a9786f0a5563b5e` | Pass |
| Constrained choice/stated preference | Correct | Pass |
| Power/agency changes branch | Yes | Pass |
| Profit/resources/transfers | Correct | Pass |
| Pareto status | Correct | Pass |
| Common floor | Correct and nonrandomizable | Pass |
| (C_m) fixed-count support | Correct | Pass |
| Adjacent-arm (Delta_m(g)) | Missing equal-(N)/exact-(g) support condition | Material local defect |
| Spillover/displacement | Correct conditional on comparable pools | Pass |
| Pool total effects | Correct | Pass |
| (Z/G/D) separation | Correct | Pass |
| Receipt LATE | Assumptions calibrated, but common-(G) comparison inherits support defect | Material local defect |
| Floor-consistent exclusion | Correct | Pass |
| Full-adoption transport logic | Correct in direction | Pass |
| Nonoverlap bound | Uses outcome bounds as effect bounds | Material local defect |
| Empirical/normative statuses | Correct | Pass |

## Exact changes required for PASS

1. Add an explicit support condition to (Delta_m(g)): restrict comparisons to pools with identical (N), or define pool-specific adjacent/matched counts that produce an exactly equal (g). State how pools are weighted and how eligibility/support is maintained.
2. Apply the same exact common-(G) restriction to any Wald/LATE comparison. If exact support is unavailable, do not label the ratio a receipt LATE; report (C_m), spillovers and pool total-policy effects.
3. Replace the nonoverlap effect contribution (q[L,U]) with (q[L-U,U-L]) when ([L,U]) bounds both potential outcomes. If sharper bounds use an observed potential outcome, derive and label them explicitly.

## Final determination

**MIXED — 92/105 (87.6%).** X032 has excellent economic and normative architecture and exact commit provenance, but the adjacent-arm common-support claim and the full-adoption nonoverlap bound are not correct for the stated heterogeneous pools and outcome limits. These are precise, repairable design errors; correcting them should be sufficient for `PASS`.

## Retest of revised response

### Final verdict

**PASS — 105/105 (100%)**

The revised response fully corrects heterogeneous-(N) common support, supported-cell aggregation, the corresponding receipt LATE, and the nonoverlap transport bound. The initial `MIXED` review remains preserved above; no downstream inconsistency remains.

### Heterogeneous-(N) common-(G) support

**Closed.** The design now stratifies the first-stage randomization by exact pool size (N_j=N) and restricts adjacent-arm comparisons to exact-(N) cells containing both (m-1) and (m) arms. It explicitly prohibits comparing unequal-(N) pools merely because their assigned counts match.

Within an exact-(N) cell:

- treated applicants in the (m) arm have (G=(m-1)/(N-1));
- control applicants in the (m-1) arm have the same (G=(m-1)/(N-1)).

Thus (Delta_{m,N}(g_N)) is now genuinely evaluated at common peer exposure (g_N). The within-arm contrast (C_{m,N}) remains correctly labeled as a compound assignment/adjacent-peer-exposure contrast rather than an equal-peer direct effect.

### Aggregation across supported cells

**Closed.** Every contrast is first defined within an exact-(N) cell. Aggregation uses prespecified target-population weights (w_N), renormalized over cells with the required randomized arms, and the excluded share must be reported. The aggregate

\[
\sum_N w_N\Delta_{m,N}
\]

is explicitly a weighted collection of supported cell effects, not a comparison of different-(N) populations masquerading as common exposure.

The same rule applies to displacement/spillover effects (Gamma_{z,N}) and total-policy effects (T_N). Because (g_N) and saturation can differ with (N), the weighted aggregate should be interpreted as a declared target mixture of cell-specific policy contrasts; the response’s cell-first definition and weight disclosure provide that interpretation.

### Receipt LATE

**Closed.** A Wald receipt effect is now permitted only within a supported exact-(N), adjacent-arm comparison that holds (G=g_N) common. Its numerator is (Delta_{m,N}(g_N)); its denominator is the corresponding randomized contrast in (D).

The response additionally requires:

- a nonzero first stage;
- monotonicity across the supported assignment states;
- well-defined compliers;
- exclusion conditional on common (G);
- no omitted peer-receipt channel beyond the exposure mapping.

Cross-(N) LATE is correctly described as a stated first-stage/complier-weighted aggregation of supported cell LATEs, not an unweighted pooled ratio. Direct assignment channels—notice, attention, documentation, effort, correction, legitimacy and queue behavior—remain explicit exclusion threats. The eliminated 12-day penalty remains floor noncompliance rather than usable variation.

### Full-adoption nonoverlap bounds

**Closed.** The revised response now distinguishes outcome bounds from effect bounds. If

\[
Y(1),Y(0)\in[L,U],
\]

then each unsupported unit effect lies in

\[
[L-U,U-L].
\]

For target nonoverlap share (q) and reweighted overlap effect (	heta_O), the statewide effect is correctly bounded by

\[
(1-q)\theta_O+q[L-U,U-L].
\]

The response also states the necessary transport conditions for the overlap component: conditional sampling/transport exchangeability, positivity, consistent policy implementation and the declared partial-interference mapping. Sensitivity analysis covers violations, vendor response, capacity, appeals and statewide equilibrium changes.

### Regression check

| Criterion | Retest result |
|---|---|
| Commit provenance | Pass; exact commit verification remains unchanged. |
| Profit/resources/transfers | Pass; producer surplus, real inputs, payments, rents and incidence remain distinct. |
| Pareto/Kaldor–Hicks | Pass; unsupported Pareto, potential compensation and rights remain separate. |
| Common floor | Pass; delay-free review and other protections remain nonrandomizable. |
| (C_{m,N}) | Pass; compound fixed-count contrast correctly labeled. |
| (Delta_{m,N}(g_N)) | Pass; exact-(N) adjacent arms provide common (G). |
| Cross-cell aggregation | Pass; supported cells, prespecified (w_N), renormalization and excluded share are disclosed. |
| Spillover/displacement | Pass; cell-specific randomized count contrasts are aligned with peer exposure. |
| Pool total effects | Pass; cell-specific pool means aggregate assignment, congestion and displacement. |
| (Z/G/D) separation | Pass; assignment, peer exposure and endogenous receipt remain distinct. |
| LATE | Pass; exact common support, first-stage/complier weighting and exclusion threats are explicit. |
| Floor-consistent exclusion | Pass; protection breaches cannot become identifying channels. |
| Nonoverlap transport bounds | Pass; effect interval is ([L-U,U-L]), not ([L,U]). |
| Empirical/normative statuses | Pass; no type drift introduced. |

### Final determination

The revision resolves every issue from the initial audit and makes the fixed-count support and transport logic exact for heterogeneous pool sizes. **Final status: PASS — 105/105 (100%).**
