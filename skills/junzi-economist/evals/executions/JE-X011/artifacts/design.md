# Pre-estimation design

## Economic target

Estimate two behavioral primitives in a stationary infinite-horizon equipment-replacement problem: the marginal operating disutility from equipment condition, `theta`, and the replacement cost, `RC`. The policy exercise asks how choices and the stationary state distribution change when `RC` falls by 25%; it is not a welfare claim because the model contains provider utility, not patient benefit or social resource incidence.

## Mapping to observables

Observed physician-period states `x` and binary choices `a` enter a dynamic logit likelihood. For any candidate `(theta, RC)`, nested value-function iteration solves the integrated Bellman equation, produces choice-specific value indices, and maps them to conditional choice probabilities. Known action-specific transition matrices connect current choices to continuation values. The conditional likelihood of observed choices given states identifies the parameters within the maintained model.

## Identification burden

- The type-I extreme-value shock scale is normalized to one; otherwise utility scale is not identified.
- The discount factor is fixed at 0.9 and transition probabilities are treated as known.
- `theta` is identified from how replacement probabilities vary with condition; `RC` is identified primarily from the replacement intercept. Separating them requires state support and both actions occurring over relevant states.
- State and choice measurement, stationarity, conditional independence of action shocks, and the transition law must be correct.
- A well-conditioned likelihood near its optimum and successful parameter recovery in this controlled simulation are diagnostics, not general proofs of structural identification.
- The final 100 of 400 physicians are held out before simulation output is inspected; only the first 300 enter estimation.

## Fixed analysis choices

- Seed: `20260713`.
- Physicians and periods: 400 by 30.
- Training/held-out split: physicians 0--299 / 300--399.
- Baseline Bellman tolerance: `1e-11`; estimation bounds: `[1e-6, 5]` for `theta`, `[1e-6, 8]` for `RC`.
- Optimizer: bounded L-BFGS-B from five dispersed starts.
- Sensitivity tolerances: `1e-8`, `1e-10`, and `1e-12`.

