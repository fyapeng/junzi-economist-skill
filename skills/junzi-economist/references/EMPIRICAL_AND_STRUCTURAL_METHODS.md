# Empirical and structural methods — 成事之术

## Start from the target

Classify the target as a descriptive object, causal effect, mechanism, behavioral primitive, equilibrium relationship, forecast, policy counterfactual, or welfare comparison. Different targets require different evidence.

## Descriptive economic facts

Build economically meaningful measurements before causal work. Examine levels, distributions, transitions, concentration, decomposition, heterogeneity, market boundaries, balance identities, and institutional timing. Validate definitions and denominators. A carefully established fact can be a complete contribution.

## Causal identification

Write before estimation:

```text
estimand:
assignment or variation:
identifying assumptions:
observable implications:
main threats:
population and margin:
```

Then choose among experiments, differences-in-differences, event studies, instrumental variables, regression discontinuity, synthetic controls, panel methods, matching/weighting, or other designs. The design name never substitutes for the assumption.

Distinguish treatment timing, anticipation, composition, spillovers, interference, heterogeneous effects, attrition, measurement change, and equilibrium responses. Use robustness analysis to probe specific threats, not to accumulate favorable specifications.

When every arm preserves an access, safety, consent, or due-process floor, define assignment and estimand relative to that floor. If people can choose whether to receive the intervention, randomizing its offer, default, information, or availability identifies an intention-to-treat policy effect, not the effect of intervention receipt without additional assumptions. Name take-up, noncompliance, selection, and any complier or structural target before interpreting the comparison.

When units compete for a fixed or congestible capacity, interference is constitutive rather than a robustness footnote. Define capacity pools and the exposure mapping; if feasible randomize saturation or policy at the pool level; distinguish direct, displacement, spillover, and total policy effects; align inference with the assignment level; and report the saturation and allocation rule to which each ITT belongs. A unit-level effect under one treatment share is not automatically the effect of a universal mandate.

Keep randomized assignment and endogenous receipt separate in notation and potential outcomes. In a two-stage saturation design, first randomize a pool's saturation or policy package, then randomize individual offers or eligibility within the pool where applicable. Define direct assignment ITTs with own assignment and randomized peer exposure; define receipt effects only through an IV, principal-strata, or structural estimand with its additional assumptions. Do not write one “direct effect” that alternates between assignment and receipt.

Match the direct-effect estimand to the second-stage assignment scheme. With exactly `m` of `N` units assigned, a treated unit has assigned-peer exposure `(m-1)/(N-1)` and a control has `m/(N-1)`; their observed contrast does not hold realized peer exposure fixed. Use the design-supported fixed-count contrast and label its adjacent exposure difference, randomize independently when a common-exposure contrast is required and feasible, or add adjacent treated-count arms that create common support. Do not display an equal-peer-exposure direct effect that the design cannot identify.

Adjacent treated-count arms create common assigned-peer exposure only at the same pool size `N`, or when counts are chosen to solve the same exposure target across pool sizes. For heterogeneous pools, stratify or match on exact `N`, define pool-size-specific supported contrasts and aggregation weights, or construct exposure-targeted count arms. Carry the same common-support restriction into any Wald ratio or LATE; never compare different pool-size populations as though equal counts implied equal exposure.

Keep outcome-level bounds distinct from effect bounds. If both potential outcomes lie in `[L,U]`, an unsupported unit-level treatment effect lies in `[L-U,U-L]`, not `[L,U]`. Weight that effect interval by the target population's unsupported share, and combine it with supported-sample estimates only under explicit sampling and transport assumptions.

Evaluate exclusion and other identifying assumptions under the intervention actually being tested. Do not cite a delay, penalty, missing safeguard, or institutional channel that the common protection floor has removed; its recurrence is noncompliance or floor failure. Look instead for live channels such as notice, attention, documentation, provider behavior, queue spillovers, or peer exposure that assignment can change without the defined receipt.

For difference-in-difference-in-differences designs, include all constituent lower-order interactions unless fixed effects demonstrably absorb them. State the assignment and clustering level, verify support in every comparison cell, inspect the relevant pretrends, and distinguish a proposed source of variation from one whose timing and assignment have been established.

A mechanism signature is usually diagnostic rather than identifying. Label a pattern “consistent with” a mechanism unless rival mechanisms make different predictions or an additional intervention, measurement, timing restriction, or exclusion separates them.

## Structural modeling and estimation

Use a structural model when the question requires latent preferences or technology, strategic or dynamic responses, equilibrium feedback, or policy counterfactuals outside observed variation.

Document:

1. economic environment, timing, state, information, actions, and equilibrium;
2. mapping from model objects to observed data;
3. sources of identification for each important parameter or parameter combination;
4. normalization and functional-form contribution;
5. estimator and computational approximation;
6. targeted moments or likelihood components;
7. fit to targeted and untargeted facts;
8. external or out-of-sample validation;
9. counterfactual support and extrapolation;
10. welfare criterion and incidence.

Do not claim that convergence identifies a parameter or that in-sample fit validates a counterfactual.

Keep four diagnoses separate:

- **computation:** solver convergence, residuals, gradients, starts, and numerical sensitivity;
- **sample likelihood geometry:** local curvature, profile shape, and finite-sample parameter correlation;
- **population identification:** whether the distribution of observables uniquely determines the target under stated normalizations, support, exclusions, and equilibrium assumptions;
- **estimator performance:** bias, variance, recovery, coverage, and failure rates across repeated samples.

A positive-definite sample Hessian and one successful simulated recovery establish neither local nor global population identification. Use wording such as “well-curved sample likelihood” unless an injectivity, rank, observational-equivalence, or other population identification argument is supplied. Use repeated seeds and sample sizes to assess recovery rather than promoting one favorable draw.

A unique minimum on a finite parameter grid establishes separation only on that grid. Do not call it point identification on a continuous domain without an analytic argument, a valid local rank result plus its maintained restrictions, or a refinement and bounding exercise that excludes between-grid equivalence. A small collection of successful replications is a recovery demonstration, not general estimator-performance support.

For bound-constrained estimation, judge first-order convergence with projected gradients or KKT/complementarity residuals. Raw gradients need not vanish at a valid boundary optimum. Make numerical convergence part of inferential eligibility; report coverage conditional on admissible geometry separately from success-and-coverage over all replications, and never let a failed optimum enter a Wald calculation unnoticed.

Declare training, interpolation, extrapolation, baseline-policy, and post-policy supports separately. An optimizer box is not an economically justified identification set, and a proposed profile or partial-identification exercise is not evidence until the criterion set, bounds, and inferential interpretation are actually computed. A profile requires at least one accepted conditional optimum at every reported index value: unresolved points remain explicit holes, never likelihood rejections. Form the profile from the best accepted conditional objective at each index value before applying a cutoff or mapping the set into a counterfactual; do not pool inferior local starts into the reported set image. Compute likelihood-ratio distances from the accepted unrestricted optimum of the same likelihood, not from the best evaluated profile-grid point when the unrestricted optimum lies between grid points. Call a discrete result an evaluated-grid set; a continuous confidence set requires refinement or justified interpolation plus endpoint checks.

Distinguish observed policy support from model-based interpolation between observed regimes. For restricted alternative searches, identified-set calculations, or exclusion regions, enforce the declared restriction with a hard constraint, valid reparameterization, or explicit feasibility rejection. A soft penalty does not establish feasibility; report the realized constraint slack and acceptance tolerance for every selected candidate. Ensure the computational parameterization covers the declared restricted set, including relevant closed boundaries; finite bounds on a transformed coordinate must be translated into and disclosed as the actual economic domain.

In simulated structural work, declare the intended population and expected sample size before drawing data. Do not condition inclusion, redraw, or market survival on latent shocks, endogenous costs, solver success, or outcomes unless that selection is itself the modeled target. Treat an incomplete simulated sample as a replication failure or redesign primitives so the stated domain holds. For deliberately invalid instruments, state what is observed, when it is realized, and exactly which exclusion it violates. Make that timing executable: construct or merge the variable at the stated stage, or use the narrower claim that it is unavailable to and unused by the earlier decision rule.

When additive shock normalizations shift the level of an integrated or expected value, report the normalization. Policy differences may be invariant even when absolute value levels are not.

## Computation and numerical verification

For simulations and estimators, use relevant checks:

- simulated-data parameter recovery;
- known analytic or limiting cases;
- multiple starts and alternative initial conditions;
- alternative optimizers or solution methods;
- gradient and derivative checks;
- finite-difference step sensitivity before attributing Hessian or coverage failures to statistical rather than numerical causes;
- tolerance, grid, draw, seed, and discretization sensitivity;
- fixed-point residuals and equilibrium conditions;
- Monte Carlo bias, variance, coverage, and failure rates;
- profiling and scaling checks;
- preservation of economic constraints.

Record numerical failure as a result. Do not silently drop nonconvergent samples or parameter regions.

## Exploration and confirmation

Exploration may generate variables, windows, models, mechanisms, or subgroups. Confirmation must use independent information or a valid adjustment for adaptive choice when the claim depends on those choices. Preserve a decision log when observed results materially influence design.

## Evidence-calibrated writing

Random assignment can make a causal estimand identifiable, but a reported point estimate remains provisional until the assignment and outcome data are audited, the estimate is reproduced, and design-consistent uncertainty is available. Do not upgrade a claim to `supported` merely because the assignment mechanism sounds credible.

Use language consistent with status:

- descriptive: documents, measures, is associated with;
- identified causal: estimates the effect under stated assumptions;
- mechanism-consistent: supports or is consistent with, while naming rivals;
- structural: model-implied parameter or counterfactual conditional on specification and validation;
- welfare: criterion-, population-, and incidence-specific.

Null, contradictory, underidentified, and abandoned results are legitimate endpoints.
