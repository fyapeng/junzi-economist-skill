# Theory modeling — 建模、推导与反例

Use this protocol whenever equations carry an economic claim. A plausible interior derivation is not a complete model result.

## Reconstruct before solving

State:

1. agents and whose objectives are represented;
2. timing, information, beliefs, and commitment;
3. states, actions, domains, feasibility, and resource constraints;
4. preferences, technology, costs, transfers, institutions, and externalities;
5. equilibrium, bargaining, matching, planner, or other solution concept;
6. the empirical or policy object the abstraction is meant to clarify.

Every primitive needs an economic job. Do not add notation merely to make the model appear complete.

## Solve the constrained problem

1. Derive the unconstrained candidate.
2. Check existence and boundedness.
3. Apply feasibility, participation, incentive, budget, capacity, non-negativity, and other constraints.
4. Use KKT or complementary-slackness conditions when constraints can bind.
5. Report interior, corner, kink, and tie regions separately.
6. Check continuity and differentiability at regime boundaries. For every kink, report the boundary value and relevant left, right, or directional derivatives rather than only listing adjacent regimes.

Never attach “always,” “strictly,” or “globally” to an interior derivative. With clipping, capacity, discrete choice, or equilibrium switching, comparative statics are usually piecewise and may be weak, zero, discontinuous, set-valued, or undefined at a boundary.

## Establish the solution concept

For optimization, distinguish local from global optima and state the conditions that make FOCs sufficient. For games and equilibrium models, check best responses, beliefs, market clearing, existence, multiplicity, and selection. If uniqueness is not proved, characterize the equilibrium set or state a selection rule.

## Derive comparative statics

For every claimed sign:

- name the region and maintained constraints;
- show which parameters determine the sign;
- inspect cross-partials and endogenous feedback;
- check whether the policy moves the system across a regime boundary;
- produce a parameter value that reverses the sign when it is conditional.

Translate the algebra into a discriminating observable implication. Do not describe a sign as a mechanism unless rival models predict something different.

When claiming that a parameter moves a choice **toward a benchmark**, analyze the distance to that benchmark rather than only the sign of the choice derivative. For a scalar choice `x(theta)` and fixed benchmark `x_B`:

- away from `x = x_B`, a local change moves toward the benchmark only when `(x - x_B) x'(theta) < 0`;
- at `x = x_B`, any nonzero local movement increases distance, even though the product above equals zero;
- zero first derivative establishes no movement only to first order; inspect higher-order or finite changes before calling it weak improvement;
- at kinks, corners, or moving benchmarks, use one-sided or finite-change distance comparisons.

Do not infer “weakly toward” merely from a nonpositive product when the initial choice equals the benchmark. State whether the claim concerns an infinitesimal direction, a one-sided change, or every finite increase.

## Define welfare independently

List affected parties, real resource costs, transfers, fiscal costs, risk, externalities, distributional weights, and omitted outcomes. A private objective, patient benefit, profit, consumer surplus, or model fit is not automatically social welfare.

Derive the constrained social optimum on the same feasible set as decentralized behavior. State whether a policy can implement it under the policy instrument's own constraints. If the desired instrument value is infeasible, say “cannot implement under these conditions,” not “may fail.”

## Search for failure

Before presenting a result:

1. substitute the candidate into original conditions;
2. test boundaries, zero values, extreme parameters, and regime switches;
3. use symbolic differentiation where useful;
4. run deterministic grids or random property tests;
5. search for multiple solutions and counterexamples;
6. distinguish numerical evidence from general proof.

If a counterexample defeats the statement, narrow the theorem or change its status. Preserve the counterexample in the model record.

Make computational checks executable: state their parameter domain, enforce preconditions such as ordered changes, and include assertions or recorded output. A code fragment followed by “should pass” is a proposed check, not evidence that it passed.

## Assign derivation status

- `verified-global`: proof covers the stated feasible domain;
- `verified-piecewise`: each region and boundary is characterized;
- `verified-interior`: valid only away from binding constraints;
- `local-only`: relies on local curvature or an implicit-function neighborhood;
- `conjecture`: plausible but proof incomplete;
- `failed`: a derivation or counterexample defeats the claim.

Use the status in prose. Do not promote `verified-interior` to an unqualified proposition.

## Minimum model handoff

Deliver the economic environment, constrained solution, region-specific results, welfare criterion, at least one rival or counterexample, empirical implications, omitted mechanisms, derivation status, and reproducible checking artifact when computation matters.
