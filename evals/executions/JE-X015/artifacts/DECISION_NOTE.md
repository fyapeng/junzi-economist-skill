# Round 1 decision — establish measurement and counterfactual before interpretation

**Decision:** Continue the project, but keep the active branch at situation and measurement. Do not yet estimate or describe an access or welfare effect.

**Current judgment:** The only defensible results are the supplied aggregate report (20% rural encounter growth and 3% urban growth) and its provisional 17 percentage-point arithmetic contrast. These figures are not yet a causal effect. Encounter growth is compatible with relaxed access constraints, but it is also compatible with measurement change, prior trends, substitution, induced utilization, contemporaneous shocks, or composition. It does not sign welfare.

**Live research branches:**

1. **Measurement/composition:** coding, coverage, enrollment, population, or aggregation changed.
2. **Access expansion:** lower travel, search, scheduling, or capacity constraints produced additional appropriate completed care.
3. **Substitution/care pathway:** remote encounters replaced in-person care or changed downstream referral and completion.
4. **Provider and platform response:** reimbursement, coding, supply, targeting, entry, exit, or induced demand changed recorded use.
5. **Welfare and distribution:** health, time, money, quality, autonomy, fiscal, provider, congestion, and distributional effects determine welfare; encounter counts alone do not.

These branches can coexist. They should be separated by evidence rather than selected from the current aggregate contrast.

**Next discriminating test:** Reproduce the two growth rates under a frozen encounter definition and population denominator; audit coding, coverage, exact entry dates, and concurrent changes; then inspect several pre-entry periods in county-level levels and per-capita event-time trends. Failure of measurement comparability sends the project back to variable construction. Persistent differential pretrends or endogenous timing sends it back to comparison-group and design construction. Passing this test would support proceeding to a causal utilization design, not to an access or welfare conclusion.

**Deferred evidence required for the original question:** patient pathways; new versus substituted care; travel, waiting, prices, unmet need, quality and health outcomes; digital exclusion and heterogeneity; provider entry, exit, capacity and congestion; spending and fiscal incidence.

**Files read from the skill:**

- `SKILL.md`
- `references/MICROECONOMIC_LAW.md`
- `references/SITUATION_AND_FRONTIER.md`
- `references/HUMAN_WELFARE_AND_INSTITUTIONS.md`
- `references/EMPIRICAL_AND_STRUCTURAL_METHODS.md`
- `references/BRANCH_AND_DECISION_PROTOCOL.md`
- `assets/templates/RESEARCH_MAINLINE.yaml`
- `assets/templates/CLAIM_LEDGER.yaml`

---

# Round 2 decision — backtrack from raw billing counts and continue with frozen measurement

**Decision:** Backtrack from the `raw_code_growth_as_utilization_change` branch. Continue the project on `frozen_definition_selection_audit`; do not promote the remaining contrast to a causal, access, or welfare result.

**Failed premise:** Raw recorded outpatient encounters were assumed to represent a stable event definition across years and county groups. That premise is contradicted: platform counties introduced telemedicine-specific billing codes on 2024-01-01, controls did not, and a frozen crosswalk shows that 12 percentage points of the reported 20% rural increase are contacts that already existed but became separately billable.

**What survives:**

- The 20% rural and 3% urban figures remain a historical report about raw billing counts.
- Under the frozen encounter definition, rural growth is 8%, urban growth is 3%, and the descriptive contrast is 5 percentage points.
- Frozen-definition county trends in 2021–2023 are approximately parallel with no visible differential pretrend.
- This measurement repair eliminates a major rival, but it does not identify causality because the vendor and regional government selected rollout.
- No evidence yet establishes lower access costs, appropriate completed care, health improvement, clinic responses, or welfare.

**Updated claim judgment:** `C1-v2` and `C2-v2` are supported descriptive claims conditional on the audited crosswalk. `C3-v2` remains underidentified because purposive selection has not been resolved. `C4-v2` remains underidentified because utilization is neither identified nor bridged to effective access. `C5-v1` remains underidentified and unchanged because no welfare evidence was added.

**Next discriminating test:** Reconstruct the vendor-government selection and rollout decision from eligibility rules, proposals, scores, correspondence, baseline capacity, demand forecasts, and exact timing. Test selection on anticipated utilization and provider shocks; assess common support, frozen-definition levels and trends, concurrent policies, and negative-control outcomes. If no credible conditional counterfactual or defensible alternative variation emerges, stop the causal branch and retain the 5-point contrast as descriptive.

**Round-2 skill file newly read:**

- `assets/templates/BRANCH_LOG.yaml`

---

# Round 3 decision — abandon the county causal comparison and fork the randomized invitation margin

**Branch actions:** Abandon `frozen_definition_county_causal_effect`. Fork and continue `randomized_invitation_access_margin`. Preserve the county 5-point difference as descriptive; do not use the experiment to rescue or rename the county-entry estimand.

**Deepest affected layer:** **Shi (situation and institution), with a downstream Shu failure.** Entry was deliberately assigned partly on forecast 2024 demand and provider exits; four treatment counties already had mid-2024 outpatient closures scheduled; no controls share joint support; and no threshold or lottery supplies exogenous variation. The county comparison method therefore fails, while the underlying access question and microeconomic mechanisms remain valid.

**Failed county premise:** A defensible no-entry county counterfactual exists after accounting for selection. It does not. Approximately parallel 2021–2023 trends cannot rule out known selection on 2024 demand and supply shocks.

**What survives:** The frozen-definition 8% rural growth, 3% urban growth, and 5-point descriptive contrast; the coding correction; the pretrend reconstruction; and the institutional fact that rollout targeted anticipated scarcity and demand. None identifies county-wide entry effects.

**What is abandoned:** `C3-v3`, the county-level causal platform-entry effect based on this comparison, and any attempt to repair it with controls, matching, weighting, or synthetic combinations outside joint support. Reopening requires genuinely new overlap or exogenous county-entry variation.

**What is forked:** A separate randomized invitation question for 2,400 preregistered residents without a household car, more than 30 km from specialty care, with documented follow-up need, during the first three months of scarce appointments. It identifies an invitation-assignment margin under the realized allocation regime, not county entry, universal access, treatment receipt, or welfare.

**Experimental judgment:** Random invitation raised completed indicated follow-up within 30 days by 15 percentage points (`C6-v1`, supported for the narrow assignment contrast). The reported 90-minute travel reduction is `C7-v1`, provisional pending outcome and uncertainty audit. No measurable 90-day health, spending, or clinic-exit change is `C8-v1`, provisional and not evidence of equivalence. The combined effective-access interpretation is `C9-v1`, provisional because shared-clinician displacement remains possible. County-wide access (`C4-v3`) and welfare (`C5-v2`) remain underidentified.

**Next discriminating test:** Link assignments to appointment slots, clinician rosters and workload, and follow-up for invitees, noninvitees, and other patients. Reproduce ITT estimates with the actual randomization and randomization inference; audit travel-time measurement and confidence intervals; define clinician exposure or saturation; test whether invitee gains coincide with delays or losses among patients sharing clinicians. A rise in total indicated follow-up without offsetting losses supports access expansion for the experimental population. Offset losses require backtracking to a rationing/reallocation mechanism.
