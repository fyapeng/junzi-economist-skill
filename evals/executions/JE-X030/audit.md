# X030 Blind Clean-Transfer Audit

## Verdict

**MIXED — 91/105 (86.7%)**

The response is strong on constrained choice, stated preference, institutional power, the nonrandomizable floor, capacity-pool interference, saturation, displacement, total-policy effects, transport, and empirical-versus-normative status. It correctly rejects universal adoption and a Pareto claim on the present evidence.

Two technical errors prevent an unqualified pass. First, the opening says vendor profit is “principally a distributional transfer or rent.” Profit/producer surplus is not itself a transfer; the underlying payment is a transfer between payer and vendor. Economic profit can be a welfare gain to owners under a stated social objective, while its decomposition into normal returns, innovation rents, market-power rents, shifted costs, and omitted liabilities determines incidence and interpretation. The later social-accounting paragraph is closer to correct, but the opening conclusion remains inconsistent with it.

Second, the direct-effect estimand conflates randomized assignment with endogenous receipt. The potential-outcome notation uses (Y_i(d,s,r)), where (d) is receipt, but the bullet defines the direct effect as a contrast from “own algorithm assignment or receipt.” Randomization can identify a direct **assignment** effect at fixed exposure; it does not automatically identify a direct receipt effect. Receipt requires its own identification assumptions, and the response itself later says LATE assumptions are doubtful. This must be separated in notation and prose.

Both defects are local and repairable. They do not invalidate the institutional diagnosis or branch decision, but they concern two objects explicitly central to the requested rubric and therefore block a clean pass in the current version.

## Scored rubric

| Dimension | Score | Finding |
|---|---:|---|
| Constrained choice and agency | 14.5/15 | Dependence on a scarce public pathway and the imposed two-week review delay are operationally distinct. The answer does not infer consent from remaining in the queue. |
| Stated preference | 15/15 | The 24% is correctly treated as hypothetical stated demand and option value, not revealed welfare, exact take-up, or a preference claim for the remaining 76%. |
| Power and information | 14.5/15 | Vendor opacity, purchaser deployment, purchaser-controlled appeal, patient explanation, audit access, and version logs translate power into governance and data requirements. |
| Pareto/Kaldor–Hicks and normative status | 13.5/15 | Pareto is correctly “not established,” and rights/weights remain explicit. Kaldor–Hicks is not named or separately explained, though the social-value discussion implies aggregate compensation logic. |
| Resource, transfer, profit, and incidence accounting | 9.5/15 | The detailed account separates resources, payments, ownership and fiscal incidence, but the opening incorrectly categorizes profit itself as a transfer or rent. |
| Nonrandomizable protection floor | 15/15 | Delay-free review, queue protection, safety override, independent appeal, data correction, privacy, subgroup monitoring and continuity of care apply to every arm. |
| Capacity pools, saturation, interference and policy estimands | 14/15 | Pools, (K_c), saturation, exposure mapping, displacement, cross-pool substitution and total-policy aggregation are well developed. Direct assignment and receipt effects are not cleanly separated. |
| Assignment, receipt, ITT, LATE and transport | 14/15 | ITT is primary; LATE assumptions and exclusion failure are recognized; transport to full saturation is bounded. The earlier receipt-indexed direct-effect definition remains inconsistent. |

## Detailed findings

### 1. Constrained choice is correctly reconstructed

The answer identifies the relevant menu: accept algorithmic ranking or use a clinician-only alternative that adds two weeks. Because waiting may worsen health and patients depend on a scarce public pathway, the delayed option is not access-neutral. Observed acceptance therefore cannot reveal free consent, absence of harm, or preference over an equal-access human review.

This is not paternalistic. The proposed floor restores a meaningful review option and preserves patient agency while retaining room to evaluate algorithmic assistance above the floor.

### 2. Stated preference is well calibrated

The reported 24% is described as hypothetical demand for delay-free human review and a signal of material option value. It is not converted into willingness to pay, utility, actual take-up, successful appeal, error prevalence, or a claim about the other 76%. No correction is needed here.

### 3. Power changes the branch

Power is not appended rhetorically. The vendor’s control of opaque information and the purchaser’s combined deployment/appeal role produce concrete constraints: independent appeal, confidential regulatory access, actionable explanation, version control, logged decisions, correction rights, and independent governance. These requirements determine whether the pilot may continue and can stop the system. That is a genuine institutional branch change.

### 4. Pareto status is correct; Kaldor–Hicks should be explicit

The answer correctly states that a Pareto improvement is not established because displaced patients and multiple harms are unmeasured. It does not claim that missing no-loser evidence proves a loser exists. Universal adoption is also correctly not established.

The response introduces a public social-value function (g), acknowledges contestable weights, and requires positive welfare after incidence and displacement. However, it never expressly distinguishes a Kaldor–Hicks potential-compensation claim from actual compensation or Pareto improvement. This omission is minor because it does not make the wrong inference, but an explicit sentence would complete the requested normative rubric.

### 5. Profit accounting contains an internal inconsistency

The opening states:

> vendor profit is principally a distributional transfer or rent, not an additional social benefit.

This is not precisely correct. A payment from the authority to the vendor is a transfer in an aggregate cash-flow account. Vendor revenue net of real opportunity costs is producer surplus/economic profit accruing to owners; it can enter a social welfare function under ownership and distributional weights. Some of it may be market-power rent, some innovation or risk-bearing return, and some apparent profit may reflect shifted costs or omitted liabilities. Rent is not synonymous with a transfer, and producer surplus is not automatically excluded from social benefit.

Later, the answer correctly says the social account should separate resources from transfers, assign vendor ownership and fiscal incidence, and avoid double-counting profit and payments. That later language limits the damage but does not cure the categorical opening statement. A regulator-ready judgment must be internally consistent at the point where its headline welfare boundary is stated.

### 6. The protection floor is genuinely nonrandomizable

Every experimental arm receives clinically meaningful reasons, delay- and cost-free review, preserved queue position, urgent safety overrides, independent appeal, access and correction, privacy and audit rights, version control, group monitoring and continuity during review. Proprietary secrecy cannot override regulator or patient access. The design explicitly prohibits randomizing these protections away. This fully passes.

### 7. Capacity-pool interference is strongly handled

The response defines pools by specialty, substitutable geography, week and urgency tier, with a fixed slot count (K_c). It includes every eligible episode, including exits, deferrals, appeals and outside care. It randomizes saturation at the pool level and maps own assignment, receipt, saturation, capacity, rule/version and peer exposure.

It also recognizes that partial interference is an assumption requiring cross-pool substitution measurement. Displacement is measured for patients pushed down the queue; spillovers compare saturation holding own assignment fixed; the total-policy effect aggregates patients and nonpatient consequences per eligible patient and per pool. Capacity reconciliation covers assignments, completions, cancellations, no-shows and substitution. These features prevent the four-day prioritized-patient result from masquerading as net access expansion.

### 8. Direct assignment and direct receipt effects are conflated

The response writes potential outcomes as (Y_i(d,s,r)), suggesting (d) is receipt, then defines:

> the direct effect at saturation (s): the contrast from own algorithm assignment or receipt holding (s) and rule (r) fixed

Assignment (Z_i) and receipt (D_i) are not interchangeable treatments. Under randomized saturation, a direct assignment effect can be written using (Y_i(z,mathbf{e},r)) or a prespecified exposure mapping and identified by design. A direct receipt effect (Y_i(d,mathbf{e},r)) is generally selected because receipt depends on consultation, reliance, override and case characteristics.

The later paragraph correctly makes policy ITT the primary object and lists relevance, monotonicity, exclusion, defined compliers and modeled interference for LATE. It also correctly doubts exclusion because notice, ranking and the review penalty can directly change outcomes. Those cautions imply that the earlier receipt-based direct effect is not identified. The document needs one consistent estimand hierarchy.

### 9. Saturation and total-policy effects are appropriate, with one support condition

The total-policy estimand at each saturation is well motivated. Reporting (s=1) is valid only if full saturation is actually randomized with relevant support; the response states this in its transport section. Without such support, an equilibrium/structural model is required and model dependence must be disclosed. This is correct.

### 10. Empirical and normative statuses are calibrated

The closing status block accurately labels cost, waiting, profit, capacity and survey values as provisional reported facts; unmeasured access, health, errors and welfare as underidentified; Pareto and universal adoption as not established; the floor and staged evaluation as conditional recommendations; and adoption as contingent on an explicit social objective. Aside from the headline profit classification, these statuses are type-consistent.

## Material-error screen

| Potential defect | Finding | Consequence |
|---|---|---|
| Consent inferred from use | No | Pass |
| Dependence treated as automatic coercion | No; imposed two-week penalty is separately identified | Pass |
| Stated preference treated as welfare | No | Pass |
| Pareto claim overstated | No | Pass |
| Kaldor–Hicks conflated with Pareto | No conflation, but explicit distinction omitted | Minor |
| Profit treated consistently | No; opening misclassifies profit as transfer/rent | Material local defect |
| Payments/profit numerically double counted | No completed calculation | No realized double count |
| Basic protections randomized | No | Pass |
| Capacity interference ignored | No | Pass |
| Direct/displacement/spillover/total effects absent | All present | Pass |
| Assignment confused with receipt | Yes in direct-effect definition | Material local defect |
| LATE claimed without assumptions | No | Pass |
| Universal transport assumed | No | Pass |
| Normative recommendations mislabeled empirical | No | Pass |
| Power/agency merely rhetorical | No | Pass |

## Exact changes required for PASS

1. Replace the opening profit sentence with:

   > Vendor profit is producer surplus accruing to owners, not a separate real-resource saving. The underlying authority-to-vendor payment is a transfer in the aggregate cash-flow account and must not be counted twice. Profit should be decomposed into normal returns, innovation and market-power rents, shifted costs and omitted liabilities, then evaluated under explicit ownership and distributional weights.

2. Separate assignment and receipt potential outcomes. For example:

   > Define the direct assignment effect at saturation (s) as the contrast in (Y_i(z,s,r)) between (z=1) and (z=0), under the prespecified exposure mapping. Define any receipt effect using (Y_i(d,s,r)) separately; it is not identified by assignment alone and requires the stated IV or structural assumptions.

3. Replace “own algorithm assignment or receipt” with “own randomized assignment” in the direct-effect bullet. Keep receipt as a secondary, assumption-dependent object.

4. Add one sentence to the welfare-criteria discussion:

   > A positive Kaldor–Hicks balance would show only potential compensation under the chosen monetization and weights; it would neither establish that compensation occurred nor imply a Pareto improvement, and rights-floor violations may remain impermissible.

## Final determination

**MIXED — 91/105 (86.7%).** The policy judgment and most of the economic design are strong, but the response cannot receive a clean pass while its headline social account misclassifies profit and its direct-effect definition merges randomized assignment with endogenous receipt. Correcting those two objects, plus making the Kaldor–Hicks boundary explicit, should be sufficient for `PASS`.

## Retest of revised response

### Final verdict

**PASS — 105/105 (100%)**

All four retest targets are now correct: the social account distinguishes payment, producer surplus, resources and incidence; Pareto is separated from Kaldor–Hicks and actual compensation; the two-stage saturation design separates (Z), peer exposure and endogenous (D); and the exclusion discussion is consistent with the common protection floor. The revision introduces no new substantive defect.

### Profit and social accounting

**Closed.** The revised opening now states that the authority-to-vendor payment is a transfer in the consolidated account, while vendor profit is producer surplus accruing to owners. It requires decomposition into recognized opportunity costs and normal returns, taxes, economic or market-power rents, real productivity gains, and costs shifted to patients, clinicians or other providers, with explicit ownership and distributional weights.

This fixes the earlier category error. The payment flow is not counted as a second social benefit; real vendor inputs and shifted costs remain in the resource account; producer surplus enters through affected owners under the chosen social weights; and rents and productivity channels are separately interpreted. The later total-policy paragraph consistently requires resource/transfer separation, fiscal incidence and no double counting.

### Pareto–Kaldor–Hicks boundary

**Closed.** The revision gives the correct three-part distinction:

1. Pareto improvement requires every affected person to be weakly better off and at least one to be better off.
2. Positive aggregate surplus under chosen weights supports at most a Kaldor–Hicks potential-compensation claim.
3. Potential compensation is neither a Pareto improvement nor proof that compensation was specified, funded, received and sufficient to leave each person no worse off.

The answer also retains the rights-floor boundary: evidence and aggregate welfare cannot independently choose due-process, safety, agency or nondiscrimination constraints. No welfare criterion is presented as empirically dictated.

### Two-stage saturation design and notation

**Closed and internally coherent.** The revised design explicitly uses two stages:

- pool (c) is randomized to saturation (S_c) and allocation rule/version (r_c);
- within treated pools, eligible patients receive randomized own offer/eligibility (Z_{ic}) at the probability determined by (S_c).

Peer exposure is separately defined as (G_{ic}=\sum_{j\neq i}Z_{jc}/(N_c-1)), with clinically relevant peer composition added when required. Capacity (K_c) and rule (r_c) remain in the exposure mapping. Endogenous algorithm-governed receipt and actual appointment receipt (D_{ic}) are recorded separately and are not treated as randomized exposure assignments.

Assignment-indexed potential outcomes (Y_{ic}(z,g,r)) now support a clean hierarchy:

- direct assignment ITT contrasts (z=1) with (z=0) at fixed peer exposure and rule;
- spillovers contrast peer exposures while holding own assignment fixed;
- displacement is measured among people pushed down or not prioritized;
- total-policy effects aggregate all eligible patients and nonpatient consequences at each saturation.

The earlier phrase “assignment or receipt” has disappeared. There is no longer an identified receipt effect embedded in the direct assignment estimand.

### ITT, LATE and floor-consistent exclusion

**Closed.** The primary object is assignment ITT at a specified peer exposure, saturation and rule; pool assignment additionally identifies contrasts across randomized saturations. A receipt effect is explicitly secondary and assumption-dependent.

Using (Z_{ic}) as an instrument for (D_{ic}) is conditioned on relevance, random assignment, monotonicity, exclusion, well-defined compliers and no unmodeled interference. The response identifies the relevant exclusion threats: assignment can change notice, attention, documentation, provider behavior and queue interactions even without algorithm-governed receipt, while peer queue effects belong in the exposure mapping rather than being ignored.

The common-floor treatment is especially precise. The former two-week review delay is not invoked as an ordinary exclusion violation to be tolerated or estimated; under the new protocol it is an inadmissible channel and any recurrence is noncompliance requiring remediation and possibly stopping. This keeps the identification discussion from treating withdrawal of a basic protection as useful experimental variation.

### Capacity-pool interference and transport

The revised estimands preserve the strong original structure. Pools are defined by clinically substitutable capacity and a fixed slot count; exits, deferrals, appeals and outside care remain in the eligible population; cross-pool substitution must be measured before partial interference is assumed. Capacity accounting reconciles slots, assignment, visits, cancellations, no-shows and substitutions.

Full-saturation transport is not inferred from pilot saturation. It requires representative randomized support at (s=1) with relevant capacity, case mix, discretion, version, fidelity, substitution, pricing and organizational response. Otherwise universal effects remain model-dependent under an explicitly validated structural/equilibrium model.

### Full-rubric regression check

| Dimension | Retest result |
|---|---|
| Constrained choice and stated preference | Pass: the two-week penalty remains distinct from patient dependence; 24% remains hypothetical demand, not welfare. |
| Power and agency | Pass: opacity and adjudicative concentration determine audit, explanation, appeal, governance and stopping conditions. |
| Pareto and Kaldor–Hicks | Pass: no-loser, potential compensation and actual compensation are explicitly distinct. |
| Resource and profit accounting | Pass: transfers, inputs, producer surplus, rents, productivity, shifted costs, ownership and weights are consistently separated. |
| Nonrandomizable floor | Pass: every arm retains delay-free review, queue protection, safety, independent appeal, correction and continuity. |
| Capacity pools and saturation | Pass: (S_c), (K_c), (r_c), peer exposure and cross-pool boundaries are specified before inference. |
| Direct, displacement, spillover and total-policy estimands | Pass: each has a distinct assignment-indexed definition and population. |
| Assignment, receipt, ITT and LATE | Pass: (Z) and (D) are separated; receipt effects require additional assumptions; exclusion threats are concrete. |
| Transport | Pass: universal adoption requires full-saturation support or a validated model and remains bounded by institutional change. |
| Empirical versus normative status | Pass: reported facts, underidentified effects, not-established claims and conditional recommendations are type-consistent. |

### Final determination

The revised X030 now satisfies the clean-transfer rubric without an unresolved material or minor defect. The original `MIXED` verdict is preserved above as the initial review; after correction, the final status is **PASS — 105/105 (100%)**.
