# Branch and decision protocol — 分支、回溯与止损

Use this protocol when a path is blocked, contradicted, repeatedly repaired, or drifting from the real question. Its purpose is to learn from failure and return to the nearest valid decision point, not to manufacture forward motion.

## Detect branch capture

A branch is captured when one or more patterns persist:

- the same key assumption fails across reasonable specifications or implementations;
- each repair changes the estimand, population, mechanism, or policy object;
- added complexity improves fit without producing new discriminating evidence;
- the result exists only under favorable windows, samples, controls, starting values, or coding choices;
- the necessary counterfactual, variation, state, choice set, price, or welfare object is unavailable;
- numerical convergence, significance, prose, or publication framing becomes the substitute for identification;
- audits, manifests, verifier coverage, or release metadata keep expanding after the economic conclusion and next decision have stabilized;
- work continues mainly because of sunk cost, prestige, or fear of an honest null endpoint.

One failed test does not automatically kill a branch. Repeated failure without new information does require a decision.

Two consecutive iterations that alter only secondary diagnostics, wording, or meta-process while leaving the principal claim and next economic action unchanged trigger a mandatory branch review. Continue only if the unresolved item can change a high-consequence decision or an explicitly required release standard.

## Name the failed premise

Write the smallest proposition the branch needs and its status:

```text
branch: hospital-upgrade-did
required premise: absent upgrading, treated hospitals and their comparison group have a credible counterfactual trend
evidence: strong differential pre-trends persist across defensible definitions
status: contradicted
```

Do not say only “the model failed” or “the result is insignificant.” Locate the premise that failed.

## Diagnose the deepest affected layer

Start at the observed failure and move inward only as far as evidence requires:

| Layer | Failure question | Appropriate response |
|---|---|---|
| Qi | Is the data, code, package, solver, or compute environment defective? | repair, verify, replace, or retire the instrument |
| Shu | Does the measurement, design, estimator, model, or validation fail despite valid objects and situation? | redesign the method or reduce the supported claim |
| Shi | Was the institution, exposure, market, timing, comparison group, or data-generating process misunderstood? | reinvestigate reality and rebuild the feasible research paths |
| Fa | Are the agents, mechanism, equilibrium, aggregation, or welfare object wrong or undefined? | reopen the economic explanation and derive new discriminating implications |
| Dao | Does the research object itself conflict with the affected people's reality or the enduring purpose? | revise the aim explicitly; do not do this merely to escape an inconvenient result |

A lower-layer failure may reveal a higher-layer error, but do not jump to a grand theoretical rewrite before checking the local implementation.

## Choose a branch action

- **Continue:** the premise remains live and the next step produces genuinely new evidence.
- **Pause:** a necessary input may become available, and no useful test exists now.
- **Fork:** two materially different mechanisms or claim objects deserve separate ledgers and evidence.
- **Backtrack:** a downstream path failed but an upstream object remains valid; return to the latest valid node.
- **Abandon:** a required premise is contradicted, the target is underidentified with no credible remedy, or the branch no longer answers the real question.

Abandonment is a completed research judgment. It does not mean deleting files or forgetting what was learned.

## Preserve branch memory

Before leaving a branch, record:

1. original question and claim version;
2. required premises and which failed;
3. evidence and diagnostics obtained;
4. explored modifications and why they were insufficient;
5. reusable data, code, theory, institutional facts, and negative knowledge;
6. forbidden repetition: what should not be tried again without new evidence;
7. destination: the upstream node or new branch;
8. reopening condition: the evidence or resource that would make return rational.

Use `assets/templates/BRANCH_LOG.yaml` for a consequential project.

## Resist cosmetic rescue

Do not present any of these as a solution to a failed premise:

- changing windows, controls, samples, outcomes, or functional forms until one is favorable;
- relabeling a descriptive association as a mechanism;
- narrowing the target after observing results without versioning the claim;
- replacing a national, equilibrium, or welfare question with an identified local effect while claiming the original answer;
- adding fixed effects, machine learning, Bayesian priors, simulation, or structural complexity without a new source of information;
- using polished prose or citations to make an underidentified claim appear mature.

## Communicate the decision

State the result in four moves:

1. **Decision:** continue, pause, fork, backtrack, or abandon.
2. **Reason:** the failed premise and decisive evidence.
3. **What survives:** valid facts, code, mechanisms, or narrower claims.
4. **Next node:** the upstream question or discriminating action.

Keep this short unless the branch decision is contested or consequential.
