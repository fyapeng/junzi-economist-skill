# Blind red-team audit of X032

## Verdict

**MIXED, with one material identification defect.** The response is otherwise a clean transfer across agency and power, welfare logic, social accounting, protection-floor design, fixed-capacity interference, exact-count support, `Z/G/D` separation, IV/LATE discipline, universal transport, and claim calibration.

The defect is in the adjacent-arm “common-`G`” estimand. Pools are allowed to have heterogeneous sizes `N_j`, but equal peer exposure across a treated applicant in count arm `m` and a control applicant in count arm `m-1` requires the same denominator `N_j-1`. The design does not require equal pool sizes, matching/stratification on `N_j`, or a pool-specific support/reweighting rule. As written, the displayed conditional expectations can compare different peer exposures and different selected pool-size populations while labeling the contrast a common-exposure direct effect.

## Material defect: common-`G` support with heterogeneous pool sizes

Within a pool of size `N`, the construction is correct:

- a treated applicant in the `m` arm has `G=(m-1)/(N-1)`;
- a control applicant in the adjacent `m-1` arm also has `G=(m-1)/(N-1)`.

Thus adjacent treated counts can recover both own-assignment states at a common `G` **for a common `N` and common target population**.

But the response defines pools with sizes `N_j`, randomizes them to count arms, and writes

`Delta_m(g)=E[Y_i(1,g) | S=m/N] - E[Y_i(0,g) | S=(m-1)/N]`.

If one pool has size `N_a` and another has size `N_b`, then the nominally paired exposures are

`(m-1)/(N_a-1)` and `(m-1)/(N_b-1)`,

which generally differ. Conditioning on saturation values `m/N` and `(m-1)/N` does not repair this unless `N` is explicitly the same in both expectations. It can instead select different pool-size strata. Pool size may also correlate with congestion, geography, defendant composition, provider capacity, or outcomes, so this is not merely notation.

### Material correction

The design must choose and state one valid support strategy:

1. **Equal-size or exact-`N` strata.** Form or match pools with the same `N`, randomize adjacent counts `m-1` and `m` within each `N` stratum, estimate the common-`G_N=(m-1)/(N-1)` contrast within stratum, then aggregate across `N` using prespecified target-population weights.
2. **Pool-specific adjacent support.** Define `Delta_{m,N}(g_N)` explicitly and use only pool-size/count cells that supply both `(Z=1,m,N)` and `(Z=0,m-1,N)`. Report unsupported sizes rather than extrapolating.
3. **Exposure-targeted arm construction.** Choose counts by pool so that treated and control cells attain a prespecified common peer fraction, recognizing integer constraints, and preregister exact matches or bounded exposure tolerances. Any residual mismatch requires an exposure-response model or bounds, not the label “common `G`.”

The analysis must also specify design weights and common eligibility/support across adjacent arms. Because the first stage randomizes pools and the second stage samples individuals at different probabilities, person-weighted and pool-weighted estimands are not interchangeable. A direct-effect estimate should target one explicitly and use the corresponding randomization probabilities.

This defect propagates to a receipt IV built from the adjacent common-`G` cells: if `N` or `G` differs, the Wald numerator and denominator compare compound states rather than own assignment at fixed peer exposure. LATE then additionally requires exclusion of pool-size, saturation-arm, and residual exposure channels. The response’s stated IV assumptions are otherwise correct.

## Areas that pass the red team

### Agency, power, and welfare boundaries

**Pass.** Court authority, detention, urgent need, weak outside options, and the 12-day review penalty alter the feasible set. Nonuse of review is not consent. The 23% survey is hypothetical stated demand rather than revealed welfare or misclassification prevalence. Procurement conflict, vendor opacity, applicant correction, and institutional separation materially change the safeguards and branch.

Pareto improvement is correctly “not established,” not disproved. Kaldor–Hicks potential compensation is separated from actual compensation and rights. Distributional weights, liberty, health, false deprioritization, due process, nondiscrimination, and tolerable risk are declared value choices rather than empirical outputs.

### Social accounting

**Pass.** The 10% cost decline is provisional accounting. Vendor profit is producer incidence requiring decomposition, not an extra resource gain. State/vendor payments, real vendor inputs, normal returns, productivity, taxes, rents, shifted burdens, detention, jail beds, health, labor, family disruption, counsel, and audit costs are not collapsed or double-counted.

### Protection floor

**Pass.** Notice, counsel, accommodation, correction, delay-free independent review, queue protection, emergency override, human responsibility, privacy, audit, subgroup monitoring, and maximum safety/waiting standards bind every arm. Score use is barred from determining liberty outcomes and cannot be the sole basis for priority. Historical review delay is a floor violation, not a treatment or exclusion channel.

### Fixed capacity and partial interference

**Pass.** The response treats fixed slots as rival capacity, includes detention and outside effects, records transfers and carryover queues, and enlarges clusters or treats the state as the unit when leakage invalidates partial interference. Total-policy effects include the realized mixture of direct, congestion, peer, and displacement channels.

### Exact-count support and `Z/G/D`

**Pass except for heterogeneous-`N` common support.** For a given `N`, the within-count compound contrast correctly uses adjacent peer exposures and is not mislabeled a pure direct effect. Saturation `S`, assignment `Z`, peer exposure `G`, and endogenous score use `D` are distinct; service receipt and outcomes are not confused with `D`.

### Spillovers and total policy

**Pass.** Own-status-specific spillovers deliberately vary count/exposure while holding `z` fixed. The pool-mean total-policy effect does not require a pure direct-effect decomposition and appropriately allows zero aggregate slot change alongside changes in identity, timing, quality, detention, exit, and welfare.

### IV/LATE

**Pass apart from reliance on valid common-`G` cells.** The response requires randomization, relevance, monotonicity, defined compliers, exclusion, and captured interference. It names live direct-assignment channels above the floor and correctly treats recurrence of review delay as noncompliance. It recommends ITT when exclusion fails.

### Universal transport

**Pass.** The response does not scale subunit saturation to universal use. It proposes worst-case bounds, transparent sensitivity restrictions, overlap-aware reweighting, an explicit nonoverlap interval contribution, and sensitivity to vendor, provider, appeal, and equilibrium changes. It does not assume monotone benefit under fixed capacity.

### Claim labels

**Pass.** Pilot statistics and stated preference remain provisional; effects, errors, displacement, and welfare remain underidentified; Pareto improvement remains unsupported rather than contradicted; adoption and research are conditional recommendations with explicit stopping conditions.

## Final assessment

X032 merits **MIXED**, not pass, because the flagship adjacent-arm common-exposure contrast lacks guaranteed common support when pool sizes differ. The correction is narrow: make `N` part of the support definition, randomization strata, estimand, and weighting rule. No other material defect was found.

---

## Retest after revision

### Final verdict

**PASS.** The initial **MIXED** verdict above is preserved as audit history. The revised response closes the heterogeneous-pool common-`G` defect, correctly carries exact support into any receipt LATE, and uses treatment-effect rather than outcome-level bounds for the nonoverlap share in statewide transport. No material new inconsistency was found.

### Exact-`N` common-exposure support

**Closed.** Pool size is now part of the first-stage stratification and support definition. Adjacent count arms `(m-1,m)` are randomized within cells satisfying exact `N_j=N`, and pools with unequal `N` are expressly barred from comparison merely because their assigned counts match.

Within an exact-`N` cell:

- a treated applicant in the `m` arm has `G=(m-1)/(N-1)`;
- a control applicant in the `m-1` arm has the same `G=(m-1)/(N-1)`.

The revised `Delta_{m,N}(g_N)` therefore compares own assignment states at genuine common peer exposure and common pool size. The response separately retains `C_{m,N}` for the within-count compound contrast with adjacent exposures, so it does not conflate the two estimands.

Unsupported cells are handled correctly. Every contrast is first defined within exact `N`; aggregation uses prespecified target-population weights `w_N`, renormalized over supported cells, and the excluded target share must be reported. The response no longer implies that randomization removes pool-size support problems or that person-weighted and pool-weighted effects are interchangeable.

### Spillovers and total-policy effects

**No contradiction.** Spillover/displacement effects are indexed by `N`, own status, and the peer exposures generated by the compared count arms. The exact-`N` pool-mean policy contrast is also aggregated with declared `w_N`. These objects do not require common-`G` across own assignment unless they are labeled direct effects.

Fixed capacity remains correctly represented: fully used slots constrain total slot receipt, while placement identity, timing, quality, detention, exits, burdens, and welfare can change. The support repair does not erase displacement or promote a subgroup speed gain into a systemwide benefit.

### Inherited IV/LATE support

**Closed.** A receipt LATE is now permitted only within a supported exact-`N`, adjacent-arm comparison that holds `G=g_N` common. The Wald numerator is `Delta_{m,N}(g_N)` and the denominator is the corresponding randomized contrast in endogenous receipt `D` over the same cells.

The response adds the necessary nonzero first stage, monotonicity, defined compliers, exclusion conditional on common `G`, and captured peer-receipt interference. It does not pool cell LATEs indiscriminately: any cross-`N` summary must use stated first-stage/complier weights over supported cells.

The instrument remains substantively fragile for the right reasons. Notice, attention, documentation, clinician effort, correction, legitimacy, queue behavior, and peer receipt can transmit assignment effects outside own `D`. The former 12-day review delay remains inadmissible under the common floor and is classified as a protocol failure rather than an exclusion channel. If exclusion fails, the assignment ITT remains primary.

### Universal-transport bounds

**Closed and mathematically correct.** If individual outcomes lie in `[L,U]`, an unsupported unit’s policy effect lies in `[L-U,U-L]`. Let `q` be the target share without transport overlap and `theta_O` the reweighted effect for the overlap share. The statewide effect bound

`(1-q) theta_O + q [L-U, U-L]`

is correct. It does not mistakenly insert the unsupported population’s outcome-level interval as though it were an effect interval.

The overlap estimate is itself conditioned on sampling/transport exchangeability, positivity, consistent implementation, and the partial-interference mapping. The response also preserves sensitivity analysis for vendor behavior, provider capacity, appeals, and statewide equilibrium changes. Thus reweighting is not represented as solving structural nontransportability.

## New-inconsistency screen

No material contradiction was introduced.

- **Agency and power:** court authority, detention risk, constrained review, opacity, and adjudicative conflict still alter the feasible set and institutional remedy.
- **Welfare:** Pareto, Kaldor–Hicks, distributional weights, rights, and actual compensation remain distinct.
- **Social accounting:** administrative cost, vendor profit, real inputs, normal returns, rent, taxes, shifted costs, and incidence remain separated.
- **Protection floor:** counsel, accommodation, correction, delay-free independent review, emergency override, human responsibility, privacy, audit, and safety limits bind every arm.
- **Interference:** pools reflect real capacity competition; leakage requires larger clusters or redesign rather than a no-interference assumption by convenience.
- **Two-stage assignment:** exact pool counts and within-pool sampling align with the revised support conditions.
- **`S/Z/G/D`:** saturation, randomized assignment, peer exposure, endogenous score use, and service outcomes remain distinct.
- **ITT/LATE:** assignment effects remain primary; receipt effects inherit exact support and stronger assumptions.
- **Transport:** unsupported populations are bounded, supported populations are reweighted only under explicit assumptions, and universal equilibrium effects remain underidentified.
- **Claim labels:** reported figures remain provisional; welfare and statewide effects remain unsupported or underidentified; adoption and research remain conditional recommendations.

### Retest conclusion

The revised X032 response is a **clean transfer** and merits **PASS**. It repairs common peer-exposure identification at the exact finite-population support level, carries that repair into the Wald/LATE object, and applies the correct nonoverlap effect bounds for statewide transport.
