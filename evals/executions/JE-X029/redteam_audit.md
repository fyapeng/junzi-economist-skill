# Blind red-team audit of X029

## Verdict

**MIXED.** This is a strong transfer across constrained choice, coercion and dependence, survey inference, social accounting, rights-floor design, and ITT/LATE discipline. Human agency and institutional power materially change the economic object, feasible alternatives, outcomes, safeguards, estimands, and branch decision.

It is not fully clean for two material reasons. First, scarce shared housing makes interference constitutive of the intervention, but the proposed applicant-level ITT is not yet defined under a specific assignment and exposure regime. Saying to “account for” interference or cluster if contamination is likely does not by itself identify the relevant direct, spillover, or policy effect. Second, the claim ledger labels the Pareto claim “contradicted” even though the text correctly establishes only that it is unsupported or unestablished.

## Recurring-risk screen

### Constrained choice

**Pass.** The response does not interpret participation or low appeal use as free acceptance. It identifies the actual feasible set: refusal or nonparticipation threatens access to scarce housing, and nominal review costs about four weeks while delay itself is harmful. Applicant exit, digital access, record correction, and inability to inspect the score are treated as choice constraints rather than preferences.

### Coercion versus dependence

**Pass.** The institutional burden is concrete: the city controls allocation, score use, reasons, and appeal delay. Scarcity, urgent need, and weak outside options explain vulnerability but are not alone labeled coercion. The response focuses remedies on city-created process burdens—delay, opaque reasons, procurement-controlled appeal, score-only decisions—and separately calls for capacity where a delay-free review cannot otherwise be provided.

### Survey inference

**Pass.** The 31% result is correctly labeled stated demand under a hypothetical zero-delay condition. It is not treated as actual take-up, a welfare measure, error prevalence, or the share that would prevail. Sampling, wording, information, hypothetical bias, and fear of disclosure are explicitly named. The gap between stated demand and observed review is not interpreted as satisfaction because the current delay selects who can afford to appeal.

### Resource, profit, and transfer account

**Pass.** The response treats the 14% figure as provisional accounting evidence and asks whether costs were shifted to applicants or other agencies. Vendor profit is not counted as a social resource saving, and vendor rent, ownership, fiscal incidence, real administrative resources, applicant time and legal costs, and downstream housing harms are separated.

The phrase “payments are transfers” is acceptable only within the stated social-accounting frame and should continue to be read with the response’s own qualifications: transfers affect distribution, cross-boundary ownership may affect the chosen welfare population, raising funds can have fiscal costs, and vendor labor/capital/technology inputs remain real costs. The answer does not actually double-count profit and payments.

### Pareto and Kaldor–Hicks logic

**Pass in the main text; mixed in the ledger.** The decision correctly states that the mayor’s Pareto claim is not established because no-loser evidence is absent. The welfare discussion correctly separates potential compensation, actual compensation, and rights that may not be tradable. It does not infer Pareto improvement from aggregate cost or placement figures.

The ledger’s phrase “Contradicted as an established claim” is too strong and internally awkward. Missing applicant-level causal welfare evidence refutes the assertion that Pareto improvement has been demonstrated; it does not establish that the pilot is not Pareto-improving. The true state may be improvement, harm, or mixed incidence.

### Rights-floor experimental design

**Pass.** Every arm receives a substantive common floor: accountable human decisions, intelligible notice, correction, independent delay-neutral appeal, accommodation, nonretaliation, data limits, audit access, subgroup monitoring, stop rules, and remedy. The floor is explicitly not an arm. The answer refuses to purchase identification by withdrawing due process and states that capacity must be funded if delay-free review is otherwise infeasible.

### ITT, receipt, and LATE assumptions

**Pass.** Assignment, score exposure, and consequential use are separated. The primary estimand is assignment-based. Conditioning on “labeled high risk” is correctly rejected where the label is post-assignment or unavailable in control. The response names selection from actual receipt and does not compare users with nonusers as if randomized.

The complier discussion is unusually disciplined: relevance, exclusion, monotonicity, well-defined receipt, attrition, and interference are stated, and exclusion is flagged as particularly doubtful because score availability may change attention, documentation, or delay without logged use. The recommendation to report ITT rather than claim LATE when exclusion fails is correct.

### Interference

**Mixed; material correction required.** The response correctly recognizes that a fixed housing stock can make one applicant’s priority affect another’s placement and that label-specific gains may be redistribution. It also mentions shared capacity, phased clusters, and saturation effects.

But the proposed primary applicant-level ITT is written as though each assigned applicant has a treatment potential outcome independent of the assignments of others. Under a scarce common queue, an applicant’s outcome can depend on the number and identities of scored applicants, caseworker behavior, office saturation, and the citywide assignment vector. Individual randomization may identify an allocation effect under the exact experimental saturation, but that effect is not automatically portable to a mandate. Office-level randomization does not solve the problem if offices draw from the same housing stock or reallocate cases.

### Empirical versus normative labels

**Pass except for the Pareto row.** Descriptive, causal, forecast, welfare, rights-floor, and policy-recommendation claims are separated. The protection floor is explicitly a conditional normative recommendation, not an empirical fact. The evaluation branch is labeled a recommendation under uncertainty and reversibility. The sole material mislabel is the Pareto “contradicted” status discussed above.

## Material corrections

### 1. Define assignment and estimands under interference

The evaluation must specify the interference structure before promising an applicant-level ITT.

At minimum:

- Define the resource pool: whether applicants compete within caseworker, office, housing program, unit type, geography, or a citywide queue.
- Define the assignment policy and saturation in each pool. Potential outcomes should be indexed by own assignment and a prespecified exposure mapping, such as the fraction or composition of other cases assigned score availability.
- If partial interference is defensible, randomize saturation across genuinely separated capacity pools and assignment within pools. Estimate direct effects at fixed saturation, spillover effects on unassigned applicants, and total pool-level effects.
- If capacity pools overlap, use a design and estimand for the allocation policy itself—such as cluster-level placement, days unhoused, exits, and distribution across all eligible applicants—rather than implying an invariant individual treatment effect.
- Report total offers and placements, displacement, queue-time distribution, and outcomes for both scored and unscored applicants. The mandate-relevant estimand is the effect of changing the allocation regime and saturation, not merely the direct effect at pilot saturation.
- Align uncertainty with the assignment level and dependence structure. Applicant-level standard errors are not valid if assignment or interference operates at caseworker, office, program, or city level.

Until this is specified, the applicant ITT should be described as design-specific and saturation-specific, not as a general score-availability effect.

### 2. Relabel the Pareto row

Change the status from **Contradicted as an established claim** to **Not established / unsupported**. The support should say that the evidence cannot verify the no-loser condition because individual causal welfare effects and relevant harms are unmeasured. If later evidence establishes at least one person is worse off under the realized allocation, then a Pareto-improvement claim would be contradicted.

## Is this a genuinely clean transfer?

**Not yet.** It is substantively cleaner than a conventional cost-saving assessment: power and agency change the choice set, housing scarcity changes the counterfactual, rights constrain experimental arms, and empirical uncertainty changes the branch from mandate to protected evaluation. The remaining interference gap is central because the policy reallocates a scarce shared good. Once the assignment regime, exposure mapping, pool-level outcomes, and saturation-specific estimands are defined—and the Pareto ledger is relabeled—the response would merit a pass.

---

## Retest after revision

### Final verdict

**PASS.** The initial **MIXED** verdict above is preserved as audit history. The revised response closes both material concerns, improves the profit account, and introduces no material contradiction in constrained choice, welfare logic, rights, causal design, or recommendation status.

### 1. Interference and mandate-relevant estimands

**Closed.** The revision no longer treats interference as a nuisance that can be handled by a generic clustering instruction. It states that interference is constitutive under shared scarce capacity and requires the researcher to recover actual offer-substitution pools across property, bedroom size, eligibility, geography, and time.

The design now includes the missing elements:

- pool-level assignment or randomized score-availability saturation;
- a prespecified exposure mapping containing own assignment, treated competitor share and composition, capacity, connected-pool treatment, and adjacent-period treatment;
- pool boundaries fixed before outcome inspection;
- assignment and design-based inference at the actual randomization level;
- direct effects at fixed exposure, displacement within offer pools, spillovers across pools and periods, and total-policy effects;
- outcomes for labeled and unlabeled applicants and all eligible applicants;
- explicit recognition that applicant ITT is capacity-, exposure-, and saturation-specific;
- full-saturation extrapolation only with randomized support near that saturation or a validated allocation model.

This repair is economically coherent. It treats the score as an allocation regime over a rival resource rather than as an isolated treatment delivered to one applicant. It also distinguishes a pilot allocation effect from a universal mandate and aligns uncertainty with the assignment level.

The LATE discussion is correspondingly repaired. Interference is not assumed away; any instrumental-variable interpretation requires it to be captured by the exposure mapping, while exclusion remains explicitly doubtful because score availability can change attention, documentation, delay, and competitors’ allocations without logged consequential use. The fallback—assignment effects by saturation—is the defensible estimand.

### 2. Pareto status

**Closed.** The claim ledger now labels the pilot Pareto conclusion **Not established / unsupported**. It says the no-loser evidence is absent and expressly adds that absence of evidence does not itself prove someone lost. This matches the opening decision and avoids confusing rejection of the mayor’s evidentiary claim with proof of the opposite welfare state.

The Kaldor–Hicks distinction remains intact: possible aggregate compensation, actual compensation, and nontradeable rights are separate questions. No individual loss is inferred merely from survey concern, appeal delay, or plausible downstream harm.

### 3. Profit and resource-account refinement

**Closed.** The revised text states that higher vendor profit is producer-side surplus/incidence rather than a separate real-resource saving, prevents the city payment and vendor receipt from being counted twice, and requires decomposition into:

- opportunity-cost compensation and normal return for vendor inputs and risk;
- economic rents arising from market power or proprietary lock-in;
- real vendor labor, technology, capital, and other inputs;
- costs shifted to applicants, workers, or other agencies;
- ownership, tax, and distributional incidence.

This is the correct accounting direction. Strictly, a reported accounting-profit figure is not automatically identical to economic producer surplus until opportunity costs and normal returns are reconstructed. The response handles that issue in substance by calling the report provisional and requiring exactly that decomposition. The shorthand “profit is producer surplus” therefore does not create a material double-counting error in context.

### New-inconsistency screen

No material new inconsistency was found.

- **Constrained choice:** appeal delay, housing urgency, exit, and information barriers remain part of the feasible set rather than being interpreted as preferences.
- **Coercion and dependence:** city-created appeal and decision rules remain distinct from background housing scarcity and vulnerability.
- **Survey evidence:** the 31% result remains hypothetical stated demand, not revealed preference, welfare loss, or error prevalence.
- **Social accounting:** costs, transfers, rents, shifted burdens, and distribution remain separate.
- **Rights floor:** no experimental arm withdraws accountable human decision, notice, correction, delay-neutral independent appeal, accommodation, data protection, monitoring, or remedy.
- **Causal claims:** descriptive pilot figures remain provisional; assignment, receipt, consequential use, exposure, and full-mandate forecasts remain distinct.
- **Interference:** direct, displacement, spillover, saturation, and total-policy effects are not collapsed into a single invariant ITT.
- **Empirical versus normative labels:** the protection floor and pause/evaluate branch remain explicitly conditional recommendations, while descriptive, causal, forecast, and welfare claims retain calibrated statuses.
- **Branch decision:** the stronger design does not quietly authorize a mandate; expansion still requires applicant-centered net benefit, no floor breach, credible scale governance, and legitimate resolution of distributional and rights choices.

### Retest conclusion

The revised X029 response is a **genuinely clean transfer** and merits **PASS**. The interference correction changes the research object and estimands in the way scarce housing allocation requires, the Pareto ledger is now logically precise, and the profit refinement avoids treating reported profit as an independent resource gain.
