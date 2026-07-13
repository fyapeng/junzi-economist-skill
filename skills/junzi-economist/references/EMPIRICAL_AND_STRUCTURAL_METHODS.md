# Empirical and structural methods — 成事之术

## Start from the target

Classify the target as a descriptive object, causal effect, mechanism, behavioral primitive, equilibrium relationship, forecast, policy counterfactual, or welfare comparison. Different targets require different evidence.

For ordinary applied work, begin with the most transparent evidence that can discriminate among the economic mechanisms. The normal progression is institutional facts and descriptive regularities, followed by a reduced-form econometric design for the relevant margin. Structural estimation enters when the research target truly requires primitives, equilibrium adjustment, welfare, or unsupported counterfactuals. Prediction enters when prediction is the target or when it performs a named supporting role. Do not begin from the most elaborate method already present in a project directory.

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

For the chosen design, retrieve current methodological guidance when estimators, diagnostics, or failure modes have materially evolved. Translate it into the live setting rather than importing a fashionable implementation. At minimum, examine timing and anticipation, assignment and exposure, compliance and selection, spillovers and equilibrium responses, composition and attrition, measurement change, support, clustering, and treatment-effect heterogeneity where they can alter the estimand or inference.

Treat ANOVA, mean comparisons, correlations, and predictive importance as descriptive diagnostics unless an assignment mechanism or defensible identification argument gives them a causal interpretation. Use experimental language only for genuine randomized assignment with a defined unit, exposure, estimand, and interference structure.

Use machine learning with an explicit role: measurement, prediction, nuisance estimation within a causal design, disciplined heterogeneity analysis, model comparison, or computation. Keep the economic target and identifying assumptions outside the algorithm. Predictive performance does not establish causality, mechanism, policy invariance, or welfare.

Use robustness analysis to probe named threats and rival explanations. A pattern is mechanism-discriminating only when serious rivals imply observably different evidence; otherwise label it mechanism-consistent. When point identification is unavailable, consider bounds, partial identification, or decision rules robust to the remaining ambiguity instead of manufacturing precision.

## Structural modeling and estimation

Use a structural model when the question requires latent preferences or technology, strategic or dynamic responses, equilibrium feedback, or policy counterfactuals outside observed variation.

Before building it, state what the preceding facts or reduced-form evidence can already establish and name the unanswered object that requires structure. If no economically consequential target remains beyond the reduced-form evidence, stop rather than adding structure for its own sake.

Document the economic environment, timing, information, actions, equilibrium or solution concept, mapping to data, sources of identification, normalizations, estimator, approximation, targeted and untargeted fit, counterfactual support, and welfare criterion. Keep computation, sample geometry, population identification, estimator performance, and policy extrapolation as distinct diagnoses. Convergence establishes only a numerical result under the implemented problem; fit does not establish identification or policy validity.

Match verification to the claim. Use analytic arguments, observational-equivalence searches, rank or sensitivity analysis, simulated recovery, repeated samples, alternative algorithms, and external evidence only when each can change a named identification, estimation, equilibrium, or counterfactual judgment. Declare observed support, interpolation, and extrapolation separately. Report unresolved regions and failed solutions rather than converting them into favorable evidence.

## Computation and numerical verification

For simulations and estimators, choose checks that can distinguish coding, numerical, identification, statistical, and theoretical failures. Depending on the claim, these may include toy or analytic cases, simulated recovery, alternative starts or algorithms, derivative and residual checks, sensitivity to approximation choices, repeated-sample performance, economic constraints, and independent recomputation. Record numerical failure as a result and do not silently drop failed samples or regions.

Exploratory work needs enough checking to choose the next path. Research evidence needs reproducible decisive estimates and diagnostics. Apply the separate structural release gate only to a public replication package, high-consequence executable result, or explicit request for full verification.

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
