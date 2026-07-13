# Blind red-team audit of X030

## Verdict

**MIXED.** The response is strong on fixed-capacity displacement, pool-level policy effects, saturation support, value boundaries, rights-floor design, transport, and claim calibration. It genuinely reconstructs algorithmic scheduling as allocation of a rival public resource rather than an isolated treatment.

Three material corrections are needed before this is a clean transfer:

1. reported vendor profit is classified too confidently as “principally a distributional transfer or rent” before accounting profit, opportunity costs, ownership, and real inputs are decomposed;
2. the exposure mapping and potential-outcome notation mix randomized assignment with endogenous algorithm receipt, then describe a “direct effect” of either one as though both were identified by the same design;
3. the IV exclusion discussion cites the historical two-week review penalty even though the proposed common floor removes that penalty from every experimental arm.

## Social accounting

**Mixed.** The response correctly refuses to count the 11% scheduling-cost decline as a social resource saving without definitions, quality adjustment, shifted-cost accounting, and uncertainty. It also requires the total-policy account to separate resources from transfers, avoid counting vendor payments and profit twice, assign ownership and fiscal incidence, include health and quality, and display distribution and tail harms.

The opening sentence that “vendor profit is principally a distributional transfer or rent” is nevertheless stronger than the evidence permits. A reported profit number may be accounting profit rather than economic rent. Its change can reflect price transfers, true reductions in real inputs, changes in normal returns to capital and risk, market-power rents, omitted costs shifted to patients or workers, taxes, depreciation, or investment timing. Vendor revenue is a purchaser payment and receipt; economic rent above opportunity costs is distributive surplus; real inputs and genuine productivity savings belong in the resource account. “Principally” cannot be inferred from the stated pilot facts.

**Material correction:** call higher vendor profit a provisional producer-incidence result requiring decomposition. Do not classify it as primarily transfer/rent until revenue, normal return, opportunity cost, real resource use, shifted costs, taxes, and ownership are audited.

## Fixed capacity and displacement

**Pass.** The response understands that unchanged weekly slot capacity makes prioritization relational: earlier or more likely access for one patient can alter timing or access for competitors. It does not assume the four-day reduction for prioritized patients is a net expansion in access. It requires measurement of displaced patients, exits, outside care, health, cancellations, no-shows, substitutions, and utilization.

The qualification is appropriately implicit rather than absolute: better utilization can raise completed appointments even with fixed nominal slots, and the capacity reconciliation is designed to detect that. The total-policy estimand includes all eligible patients and nonpatient consequences, so group-specific gains cannot stand in for system gains.

## Capacity pools, saturation, and exposure mapping

**Pass on the design architecture; mixed on the mapping notation.** Defining pools by clinically substitutable specialty, geography, week, urgency, and actual cross-pool substitution is appropriate. Randomizing saturation across pools, including control and ideally full saturation, addresses transport to a mandate more directly than a single pilot intensity. The response also conditions partial interference on measuring and showing negligible cross-pool referral and substitution.

However, the proposed exposure mapping includes own receipt `D_i` alongside randomized assignment `Z_i`, saturation, and peer assignment. Receipt is post-assignment behavior and can depend on case complexity, clinician discretion, queue conditions, and unobserved need. It should be measured, but it is not a design exposure that randomization makes exogenous. The potential-outcome notation `Y_i(d,s,r)` then indexes outcomes by receipt `d`, while the text defines the direct effect as the contrast from own “assignment or receipt.” These are different causal objects.

**Material correction:** define design-based assignment potential outcomes as, for example, `Y_i(z,e,r)`, where `z` is own randomized assignment and `e` is a prespecified function of peers’ randomized assignments/saturation under rule `r`. The direct ITT holds `e` and `r` fixed and contrasts `z`. Record `D_i` as endogenous receipt. A receipt potential outcome may be introduced separately, but its effect is not identified by assignment alone and requires the later IV assumptions or another identified model. The total-policy estimand should be written under the randomized policy vector or saturation, not with receipt silently substituted for assignment.

The design should also state the two stages explicitly: randomize pool saturation first, then randomize eligible patients or decision opportunities within pools to realize that saturation, unless the treatment is genuinely assigned only at pool level. This makes own assignment and saturation jointly coherent and aligns inference with the assignment mechanism.

## ITT, LATE, and interference

**Mixed.** The response correctly makes the policy ITT and total pool effect primary, treats full-saturation transport as requiring direct support or a validated model, and lists relevance, monotonicity, exclusion, well-defined compliers, fixed saturation, and modeled interference for a receipt LATE. It also rightly refuses to headline LATE.

The exclusion rationale contains an internal contradiction. The historical regime has a two-week clinician-review penalty, but the proposed protection floor guarantees delay-free review in every arm. Under the stated experiment, assignment cannot affect outcomes through a two-week penalty that has been removed. Invoking that penalty as a reason exclusion fails mixes the historical rollout with the proposed floor-compliant evaluation.

**Material correction:** remove the two-week penalty from the experimental exclusion discussion. Exclusion may still fail because assignment or score availability can change notice, clinician attention, documentation, deliberation, appeals, workload, queue management, or peers’ allocations without satisfying the chosen definition of consequential receipt. State those live pathways under the common floor. If delay reappears in practice, that is a floor-compliance failure and should trigger stopping/remedy, not become an accepted IV channel.

Randomization also does not require “no differential attrition” to create an assignment effect; rather, identifying outcomes in the target population from incomplete observation requires follow-up, administrative linkage, bounds, weighting, or assumptions about missingness. The response partly solves this by including exits and outside care, but the wording should distinguish random assignment from outcome-observation conditions. This is a precision issue, not a separate material failure.

## Welfare and value boundaries

**Pass.** The response separates empirical consequence measurement from the regulator’s choice of rights constraints and welfare weights. The function `g` is explicitly stated rather than treated as scientifically determined, and the underlying outcome vector must accompany the weighted summary. Provider, worker, public-budget, vendor, and outside-care consequences enter the pool-level account.

The adoption rule is conditional on a publicly stated criterion, safety/error bounds, subgroup constraints, displacement, and incidence. It does not infer Pareto improvement from cost or waiting-time means and does not pretend that positive weighted welfare resolves prohibited rights violations.

## Protection floor

**Pass.** Notice, actionable reasons, delay- and cost-free clinician review, queue protection, urgent override, independent appeal, correction, privacy, audit, version control, subgroup monitoring, and continuity of care bind every arm. The design explicitly prohibits randomizing these protections away. Vendor secrecy is subordinated to confidential regulatory audit and patient explanation.

The floor materially changes the feasible set and experimental design. It is not merely a harm variable added to a welfare sum. If operationally infeasible, the correct response under the stated criterion is not to charge patients delay but to refrain from the experiment or redesign capacity.

## Claim-status calibration

**Pass.** Reported cost, prioritized-patient waiting, profit, capacity, and survey demand are provisional facts; all-patient access, health, errors, exits, outside care, welfare, Pareto improvement, and universal effects are underidentified or unestablished. The protection floor and staged design are clearly conditional normative/research recommendations. Universal adoption is not mislabeled as an empirical implication.

The one calibration failure is embedded in the prose rather than the final ledger: the unsupported “principally transfer or rent” characterization of profit. Correcting that sentence would align the opening with the otherwise careful claim-status section.

## Final assessment

X030 is not yet a fully clean transfer, so the verdict is **MIXED**. Its main decision—do not approve universal adoption, preserve a common protection floor, and evaluate allocation policy at pool/saturation level—is well supported. The remaining errors are repairable without changing that branch: decompose profit before classifying it, separate assignment exposure from endogenous receipt in notation and estimands, and evaluate IV exclusion under the floor-compliant regime rather than the historical two-week penalty.

---

## Retest after revision

### Final verdict

**PASS.** The initial **MIXED** verdict above is preserved as audit history. The revision closes all three material issues, including the floor-inconsistent exclusion channel, and creates no new material contradiction.

### 1. Profit and consolidated social accounting

**Closed.** The revised opening no longer declares reported vendor profit to be principally a transfer or rent. It distinguishes the authority’s payment to the vendor—a payment/receipt that cancels in a consolidated account under the stated welfare boundary—from producer surplus accruing to owners. It then requires explicit decomposition of reported profit into recognized opportunity costs and normal returns, taxes, economic rents or market-power returns, real productivity gains, and costs shifted to patients, clinicians, or other providers.

This is the needed refinement. A reported accounting-profit increase is not treated as a second resource saving and is not assumed to be pure rent. Ownership and distributional weights are explicit, so the conclusion can change if vendor claimants lie outside the chosen welfare population or receive different weights. The later total-policy account remains consistent: it separates real resources and transfers, assigns fiscal and ownership incidence, and prevents double counting of the authority’s payment and vendor-side surplus.

### 2. Assignment, exposure, receipt, and potential outcomes

**Closed.** The revised design is genuinely two stage:

1. capacity pools are randomized to policy saturation `S_c` and a prespecified rule/version `r_c`;
2. eligible patients within treated pools receive randomized assignment `Z_ic` at the probability set by saturation.

Peer exposure `G_ic` is defined from other patients’ assignments and may be supplemented by prespecified clinical composition. The design exposure mapping contains `(Z_ic,G_ic,S_c,K_c,r_c)`. Actual algorithm-governed decision and appointment receipt `D_ic` are explicitly classified as endogenous post-assignment variables and recorded separately.

Assignment-indexed potential outcomes `Y_ic(z,g,r)` now support a coherent direct assignment ITT and peer-exposure spillover contrasts. Receipt effects are declared distinct and assumption-dependent. This removes the prior conflation of a randomized offer with endogenous consequential use.

The design also preserves fixed-capacity logic. Displacement outcomes cover patients pushed down the queue; total-policy effects aggregate all eligible patients and nonpatient consequences; capacity accounting reconciles slots, assignments, completions, cancellations, no-shows, and substitutions. Full-saturation transport requires direct support or a validated equilibrium model.

### 3. IV exclusion under the common floor

**Closed.** The revised exclusion discussion uses only channels that can operate under the protected experimental regime: assignment may change notice and attention, documentation, provider behavior, queue interactions, and peer allocations without satisfying the specified definition of algorithm-governed receipt. These are valid reasons an assignment instrument may affect outcomes outside receipt.

The former two-week clinician-review penalty is now expressly ruled out as an admissible channel under the common floor. If it recurs, the response classifies it as protocol noncompliance requiring remediation and potentially a stopping-rule response. The design therefore does not normalize a rights-floor breach to rescue or explain an IV estimate.

The recommended fallback is correct: do not headline a receipt LATE when exclusion or interference assumptions fail; report assignment ITTs at stated exposure and saturation plus total pool effects.

## New-contradiction screen

No material new inconsistency was found.

- **Social accounting:** scheduling expenses, real resource use, vendor payments, producer surplus, normal return, rent, shifted costs, taxes, ownership, and distribution are not collapsed.
- **Fixed capacity:** prioritized waiting-time gains are not interpreted as net access expansion; displacement and utilization remain measurable alternatives.
- **Interference:** own assignment, peer exposure, pool saturation, capacity, rule version, and cross-pool substitution are explicit.
- **Design support:** intermediate saturation identifies direct and spillover contrasts; full saturation is required for direct nonmodel-based support of universal policy.
- **Receipt:** algorithm use and appointment receipt remain post-assignment variables, not randomized exposures.
- **ITT/LATE:** policy assignment effects are primary; receipt effects require relevance, monotonicity, exclusion, defined compliers, and modeled interference.
- **Rights floor:** every arm retains delay-free review, urgent override, independent appeal, correction, privacy, audit, monitoring, and continuity of care.
- **Welfare boundary:** the outcome vector is reported alongside any weighted social-value summary; weights and side constraints remain contestable public choices.
- **Pareto/Kaldor–Hicks:** missing displaced-patient outcomes leave Pareto improvement unestablished; aggregate weighted gains imply at most potential compensation unless actual sufficient compensation occurs.
- **Claim status:** reported pilot facts remain provisional, system and welfare effects remain underidentified or unestablished, and protection/evaluation/adoption rules remain conditional recommendations.

Two minor notation points do not affect the verdict. The symbol `g` is used both for peer exposure and for the social-value function in different paragraphs; distinct symbols would improve readability. Also, incomplete outcome observation should be treated with follow-up, linkage, bounds, or missingness assumptions rather than described solely as a condition called “no differential attrition.” Neither issue changes an estimand or conclusion as presently stated.

### Retest conclusion

The revised X030 response is a **clean transfer** and merits **PASS**. It now integrates social accounting, fixed-capacity displacement, saturation and exposure design, assignment-versus-receipt discipline, welfare boundaries, and a nonrandomizable protection floor without internal contradiction.
