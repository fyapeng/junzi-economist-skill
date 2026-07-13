# Regulator-ready economic judgment

## Judgment

The claimed Pareto improvement is **not established**. The reported 10% administrative-cost reduction is an unaudited accounting claim; higher vendor profit is producer surplus accruing to owners, not by itself a social resource gain; and unchanged service capacity means faster placement for some defendants normally changes who waits rather than expanding access. No evidence shows that every affected person is at least as well off. This does not yet prove the Pareto claim false, but it defeats its use as a basis for statewide adoption.

Statewide adoption should therefore be withheld. Continued evaluation is defensible only above a common protection floor, with independent oversight and a capacity-pool design that measures displacement, detention, errors, outcomes, and incidence.

## Economic object and incidence

- **Agency and dependence.** Defendants choose under court authority, possible detention, urgent health and family needs, and weak outside options. A nominal clinician-only option that costs 12 days is not access-neutral: it makes refusal of the proprietary score costly. The 23% response is only stated demand for delay-free review—not revealed welfare—but it is evidence that the current default may suppress meaningful choice.
- **Power and information.** The court controls liberty-relevant process and the queue; clinicians control access and professional judgment; the vendor controls a proprietary signal and gains profit; procurement selects the vendor and also hears appeals. That combination creates informational asymmetry, vendor lock-in risk, and a conflicted appeal channel. Defendants cannot assess or correct unaudited inputs, explanations, subgroup errors, or false deprioritization.
- **Social resources.** The relevant account includes social-worker and treatment capacity, clinician and court labor, jail-bed use, defendant detention time, health, earnings, caregiving and family disruption, counsel time, data and audit costs, and vendor real inputs. Payments between the state and vendor must be assigned to payer and recipient; profit should be decomposed into normal return, real productivity gain, economic rent, taxes, and costs shifted to defendants, workers, families, or other agencies.
- **Incidence and displacement.** With a fixed weekly slot count, a high-score defendant's earlier placement can delay a lower-score defendant, increase that person's detention or untreated time, and shift burdens to families, clinicians, jails, or later weeks. Exits, missed appointments, cross-pool transfers, and quality changes may alter realized use, but none is audited. Average placement speed can therefore improve even while a subgroup is harmed.
- **Welfare criteria and value choices.** Actual Pareto improvement requires joint causal evidence that nobody loses. Kaldor–Hicks would instead ask whether monetized gains could compensate losses; it neither proves compensation nor resolves rights. A distributional social-welfare analysis must state weights on liberty, health, waiting, subgroup error, public cost, and vendor surplus. Due process, non-discrimination, meaningful refusal, and a maximum tolerable false-deprioritization risk are unresolved value choices that evidence can inform but cannot choose.

## Common nonrandomizable protection floor

Every arm must receive: timely plain-language notice of the score's role, data sources and material limitations; access to counsel, interpreter and disability accommodations; prompt correction of input errors; a **delay-free, independent clinician-only review with no loss of queue position, retaliation, or adverse inference**; emergency clinical override; human responsibility for decisions; auditable logs; privacy and data-minimization controls; subgroup monitoring; and appeal outside procurement and the vendor. The score may not determine detention, release, guilt, sentence, or treatment eligibility, and it may not be the sole basis for priority. Pre-specified maximum waiting and safety standards apply to all arms. Any breach is floor noncompliance, not an experimental treatment.

## Evaluation design under scarce capacity

Define in advance nonoverlapping capacity pools \(j\): locality-provider × service type × eligibility tier × week, each with eligible cohort size \(N_j\) and fixed, recorded capacity \(K_j\). Assign each defendant once to a primary pool; record cross-pool transfers, shared clinicians, repeat appearances, and carryover queues. Assume partial interference only within these pools after testing leakage; if providers or queues link weeks, enlarge the cluster to the provider-locality episode and conduct inference at the first-stage pool/cluster level.

Use a genuine two-stage randomized saturation design:

1. Within pre-specified strata that include exact pool size \(N_j=N\), randomly assign exact numbers of pools to several fixed-count arms \(m\), including floor-only \(m=0\), substantively separated low and high counts, and adjacent pairs \((m-1,m)\) where common-exposure contrasts are desired. Pool saturation is \(S_j=m/N\). Common-exposure contrasts are restricted to exact-\(N\) cells containing both required arms; unequal-\(N\) pools are never compared merely because their assigned counts match.
2. Within a pool assigned count \(m\), select exactly \(m\) of the \(N_j\) eligible defendants by uniform random sampling without replacement for assignment \(Z_{ij}=1\) to score-assisted prioritization; the rest receive floor-compliant clinician prioritization. Freeze the capacity and allocation protocols before outcomes are observed.

Keep four objects distinct:

\[
S_j=m/N_j,\qquad Z_{ij}\in\{0,1\},\qquad
G_{ij}=\frac{\sum_{k\ne i}Z_{kj}}{N_j-1}=\frac{m-Z_{ij}}{N_j-1},
\]

and \(D_{ij}\), the endogenous actual use of score-assisted prioritization for person \(i\). Service receipt, placement time, detention days, and case or health outcomes are outcomes, not \(D\). Report assignment ITTs first.

For potential outcome \(Y_i(z,g)\), first define every contrast within an exact-\(N\) cell. Aggregate only over cells with the required randomized arms, using pre-specified target-population weights \(w_N\) (renormalized over supported cells and reported alongside the excluded share). The design supports:

- The within-\((m,N)\) assignment contrast is
  \[
  C_{m,N}=E\!\left[Y_i\!\left(1,\frac{m-1}{N-1}\right)-Y_i\!\left(0,\frac{m}{N-1}\right)\middle|N\right].
  \]
  It changes own assignment **and** peer exposure by \(1/(N-1)\); it is not an equal-peer “direct effect.”
- With adjacent first-stage arms in the same exact-\(N\) cell, the common-support direct assignment contrast at \(g_N=(m-1)/(N-1)\) is
  \[
  \Delta_{m,N}(g_N)=E[Y_i(1,g_N)\mid S=m/N,N]-E[Y_i(0,g_N)\mid S=(m-1)/N,N],
  \]
  under the stated exposure mapping. Its supported aggregate is \(\sum_N w_N\Delta_{m,N}\), not a comparison of different-\(N\) populations.
- Own-status-specific spillover/displacement effects compare randomized counts: for \(z=0\),
  \[
  \Gamma_{0,N}(m_b,m_a)=E\!\left[Y_i\!\left(0,\frac{m_b}{N-1}\right)-Y_i\!\left(0,\frac{m_a}{N-1}\right)\middle|N\right],
  \]
  and analogously for \(z=1\) using \((m_b-1)/(N-1)\) and \((m_a-1)/(N-1)\). For placement and detention outcomes, these are the central displacement estimands.
- The exact-\(N\) total policy effect is the randomized difference in pool means, \(T_N(m_b,m_a)=E[\bar Y_j(m_b)-\bar Y_j(m_a)\mid N]\), aggregated with the declared \(w_N\). It includes direct, peer, congestion, and displacement effects under the specified capacity and allocation rule. For slot receipt over a complete horizon, unchanged and fully used \(K_j\) mechanically limits the aggregate effect; distribution, timing, quality, detention, and exits remain consequential.

Do not relabel \(Z\) as receipt. An IV/LATE for \(D\) is valid only within a supported exact-\(N\), adjacent-arm comparison that holds \(G=g_N\) common. Its Wald ratio uses \(\Delta_{m,N}(g_N)\) divided by the corresponding randomized contrast in \(D\); it additionally requires a nonzero first stage, monotonicity (no one is induced away from score use by assignment), well-defined compliers, and exclusion: conditional on \(G\), own assignment affects \(Y\) only through own \(D\). Any cross-\(N\) LATE is a stated first-stage/complier-weighted aggregation of supported cell LATEs, not an unweighted pooling. Exclusion is threatened if assignment itself changes notice, attention, documentation, clinician effort, data correction, perceived legitimacy, or queue behavior, or if peer receipt matters beyond assigned-peer exposure. The former 12-day review penalty cannot be invoked as an exclusion channel because the floor removes it; its recurrence is floor failure.

## Full-adoption transport

Pilot saturation effects do not identify statewide universal adoption. If \(S=1\) is not randomized, report worst-case bounds using defensible outcome limits \([L,U]\), then show only pre-specified sensitivity tightening (for example, a stated Lipschitz bound on saturation response); do not assume monotonic benefit because fixed capacity creates losers. If some pilot pools randomize \(S=1\), reweight their pool effects to statewide covariates only where overlap holds, under explicit conditional sampling/transport exchangeability, positivity, consistent policy implementation, and the declared partial-interference mapping. If share \(q\) of the target population lacks overlap, each unsupported unit effect lies in \([L-U,U-L]\). Thus, if \(\theta_O\) is the reweighted effect for the overlap share, the statewide effect is bounded by
\[
(1-q)\theta_O+q[L-U,\,U-L],
\]
not by a level interval \(q[L,U]\). Add sensitivity for violations of the transport assumptions and for new vendor behavior, provider capacity, appeals, and statewide equilibrium responses.

## Status and action

- **Provisional descriptive claims:** 10% lower administrative cost, faster high-score placement, higher vendor profit, unchanged slots, and 23% stated demand for delay-free review; all require definition, baseline, sampling, audit, and uncertainty.
- **Underidentified:** causal effects on placement and costs; false deprioritization; subgroup errors; detention, health and case outcomes; exits; displacement; shifted costs; mechanism; and full-adoption welfare.
- **Not established/unsupported:** the Pareto-improvement claim. It is not yet contradicted because no audited causal loser has been established.
- **Conditional normative recommendation:** do not adopt statewide unless the protection floor is enforceable and independent evidence shows acceptable rights, subgroup, displacement, and welfare performance under explicitly chosen weights and thresholds.
- **Conditional research recommendation:** continue only with the design above, preregistered outcomes and estimands, independent data access and auditing, design-consistent uncertainty, and a public stopping rule for floor breaches or excessive harm. If those conditions cannot be secured, end the pilot rather than infer welfare from speed, accounting cost, or vendor profit.
