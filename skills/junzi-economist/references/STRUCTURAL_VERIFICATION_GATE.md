# Structural verification gate — 结构估计发布门槛

Use this gate for an executed structural estimate, profile, equilibrium, restricted search, policy counterfactual, or welfare result. Apply it before describing the endpoint as reproducible or independently verified.

## 1. Declare the production contract

Before execution, record:

- intended population, expected row and cell keys, support, timing, and selection rule;
- estimator objectives, parameter domains, normalizations, starts, tolerances, and the projected-gradient or KKT acceptance predicate;
- equilibrium or Bellman residual predicates and economically scaled counterparts;
- profile, restricted-search, and policy domains, including closed boundaries and feasibility slack;
- accounting objects and the exact welfare criterion.

Every estimator start receives a row-level acceptance decision from the declared predicate. Solver status, `ftol`, or a finite objective does not substitute for KKT acceptance. Select only among accepted starts and reconcile the selected row, accepted count, and headline count mechanically.

Instantiate `assets/templates/STRUCTURAL_RELEASE_MATRIX.yaml` before running production. Give every required claim or artifact family a stable `check_id`, its composite row key, every field that must be recomputed or reconciled, its verification mode, tolerance, and permitted scope language. A prose checklist does not substitute for this matrix.

Keep the release lifecycle explicit and acyclic:

1. freeze the contract, with requirements but no runtime pass or closure values;
2. freeze a manifest of production inputs that already exist;
3. run the verifier and write its emitted checks and closure result;
4. generate the report from that result;
5. write a final handoff receipt that reopens and hashes the contract, input manifest, verification result, and report.

The handoff receipt is last and is not self-verifying. Do not put future files in an earlier manifest, and do not let the frozen contract double as the later pass certificate.

## 2. Freeze a complete production record

Retain enough precision to recompute after serialization:

- raw primitives or sufficient immutable counts;
- every start, terminal vector, objective, raw and projected gradient, active bound, status, and message;
- every profile or finite restricted-domain key, coordinate, boundary flag, feasibility flag, slack, objective, and selected status;
- every policy tuple `(key, numeric value, support label, scenario flags)` and all accounting levels;
- production code, configuration, versions, seeds, stdout or failure record, and hashes.

An exhaustive finite-domain claim requires every declared row, including infeasible and failed rows. A profile requires the best accepted conditional solution at each reported index.

## 3. Reconstruct independently from primitives

Write the verifier after production artifacts are frozen. It must not import the production solver or take stored selected parameters, objectives, gradients, roots, or terminals as inputs to the claimed independent solve.

For every headline object, do one of the following from raw primitives:

- re-estimate from independent starts with separately coded equations;
- solve analytically or with a materially different algorithm;
- exhaustively recompute every finite-domain row;
- recompute every saved policy level and accounting component.

Evaluating a likelihood, residual, or Bellman equation only at a stored estimate is a regression check, not independent estimation. Checking only the best restricted row does not verify an exhaustive grid.

## 4. Test interfaces beyond saved examples

Bind composite policy records as tuples, not separate sets. For an arbitrary-input or functional-interface claim:

1. generate at least two valid off-grid inputs absent from production artifacts;
2. invoke the production interface on those inputs;
3. solve the same objects independently without importing production code;
4. compare full vectors, residuals, and accounting levels, not identities alone.

If only saved policies were checked, say “verified on the declared finite policy set.”

## 5. Make coverage executable and literal

The verifier's coverage map names one predicate per claim and records pass, failure, tolerance, and evidence. It must cover:

- key uniqueness, completeness, and key-to-value-to-label binding;
- transition and choice cells;
- estimator parameters, objectives, gradients, and every start's acceptance;
- Bellman, equilibrium, or FOC residuals;
- identification diagnostic and its claim boundary;
- every profile or restricted-domain row;
- saved and generated policy inputs;
- accounting levels and identities;
- headline reconciliation and artifact hashes.

Leave unexecuted predicates explicitly unverified. A verifier failure writes its record and exits nonzero.

Exercise the failure path before release. Save the exact command or injected failing condition, numeric process exit code, and resulting failure record. A nonempty status string is not evidence of nonzero exit behavior.

Close the release matrix mechanically:

- the set of required `check_id` values in the frozen contract must equal the set emitted by the verifier;
- each emitted result records the exact `fields_checked`, and those fields must equal the contract fields for that `check_id`;
- row-family checks bind every declared composite key to every required saved field, not merely to the row count or objective;
- interface checks cover every estimator or solver family for which the public interface claim is made and compare the exact returned schema;
- headline and hash checks are ordinary required matrix rows, not informal post-processing.

An input-hash predicate covers only files frozen before verification. Claims that the final verification result and report were reopened belong to the later handoff receipt; they cannot be marked passed in the verifier before those files exist in final form.

The report may say “all,” “complete,” “every,” “full output,” or “independently verified” only at the scope for which matrix closure passes. Otherwise name the narrower executed scope. A truthful predicate is still insufficient when its label implies fields that its code did not check.

## 6. Bound provenance and the final claim

Hashes establish byte identity. Modification times establish filesystem chronology. Neither proves authorship, exclusive access, or causal execution order. State provenance at the level actually evidenced.

Before handoff, reopen the frozen production files, verifier output, report, and manifest. Reconcile all numbers and hashes read-only. Preserve every failed endpoint and the rule it generated; do not overwrite it with a repaired run.
