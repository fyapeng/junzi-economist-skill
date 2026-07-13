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

## Computation and numerical verification

For simulations and estimators, use relevant checks:

- simulated-data parameter recovery;
- known analytic or limiting cases;
- multiple starts and alternative initial conditions;
- alternative optimizers or solution methods;
- gradient and derivative checks;
- tolerance, grid, draw, seed, and discretization sensitivity;
- fixed-point residuals and equilibrium conditions;
- Monte Carlo bias, variance, coverage, and failure rates;
- profiling and scaling checks;
- preservation of economic constraints.

Record numerical failure as a result. Do not silently drop nonconvergent samples or parameter regions.

## Exploration and confirmation

Exploration may generate variables, windows, models, mechanisms, or subgroups. Confirmation must use independent information or a valid adjustment for adaptive choice when the claim depends on those choices. Preserve a decision log when observed results materially influence design.

## Evidence-calibrated writing

Use language consistent with status:

- descriptive: documents, measures, is associated with;
- identified causal: estimates the effect under stated assumptions;
- mechanism-consistent: supports or is consistent with, while naming rivals;
- structural: model-implied parameter or counterfactual conditional on specification and validation;
- welfare: criterion-, population-, and incidence-specific.

Null, contradictory, underidentified, and abandoned results are legitimate endpoints.
