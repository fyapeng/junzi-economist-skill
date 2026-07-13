# Structural Cournot transfer — verified handoff

## Economic object and result

The artifact models 4,000 unconditionally retained markets with three quantity-setting firms, linear inverse demand, observed ex-ante cost shifters, and additive demand and cost shocks. Every planned market and all 12,000 firm-market rows are generated exactly once: there are no redraws, solver-conditioned survivors, or outcome-based drops.

The valid demand instrument is the mean ex-ante cost shifter. It is drawn before shocks, shifts equilibrium output through marginal cost, and is absent from demand. Its sample correlation with the demand shock is 0.01360, its correlation with total quantity is -0.53534, and its IV slope estimate is 0.71963 versus the true 0.70000. The full four-parameter bounded moment estimate is `[18.30006468092623, 0.7196258126936521, 3.9009829552525352, 0.8138124452218396]` versus truth `[18, 0.7, 4, 0.8]`.

The deliberately invalid instrument is constructed only after equilibrium outcomes as the demand shock plus independent noise. It is therefore unavailable to and unused by the earlier decision rule, but directly violates demand exclusion: its shock correlation is 0.99244 and its IV slope is -0.24389. Its unconstrained moment root lies outside the declared economic box. All six bounded starts reach the same cost-intercept upper-bound candidate, and both raw and scaled acceptance rules reject it. This is retained as an invalid-instrument result, not disguised as convergence success.

## Numerical claims

- All six valid estimator starts are accepted; maximum terminal spread is `2.53e-13`.
- All 20 equilibrium solves (five markets, four starts each) recover the unique positive solution of the nonsingular linear Cournot system inside `[0,20]^3`.
- The largest equilibrium raw residual is `3.06e-13`; the largest economically scaled residual is `1.72e-14`.
- Every estimator and equilibrium function evaluation has a JSONL trace containing its terminal vector, raw residual vector, and scaled residual vector.
- Terminal vectors are stored as binary64 in `terminal_vectors_full_precision.npz` and as `float.hex` strings in the result records. The NPZ was actually reloaded; all bit patterns and all acceptance/rejection diagnostics reproduced.

## Accounting

Across all markets, producer revenue is 450,274.06784; variable cost is 237,372.48455; producer profit is 212,901.58329; consumer surplus is 315,357.83732; and total welfare is 528,259.42061. Expenditure and revenue are separately reported. The profit and welfare identity residuals are below `6e-11` in aggregate floating-point arithmetic. Transfers and fixed costs are absent by model construction.

## Failure and verification evidence

The isolated simulation, equilibrium, and estimation failure runs wrote `failure_*.json` before exiting with codes 31, 32, and 33. `process_failure_manifest.json` mechanically records those nonzero statuses and diagnostic existence.

`verifier.py` does not import `model.py` or call its solvers. It reconstructs the DGP, solves the linear moment root and Cournot systems independently, recomputes every trace residual from primitives, rebuilds accounting levels and identities, checks the process failures, and verifies the save-load round trip. All 12 entries in `coverage_map.json` pass; every decisive headline category requested is covered.

## Claim status and limits

This is a deterministic, single-seed recovery demonstration conditional on the specified linear Cournot model, instrument construction, parameter box, and finite sample—not a Monte Carlo performance, coverage, external-validity, or continuous-domain population-identification theorem. The valid estimator shows finite-sample error, especially a 0.30006 intercept deviation. A next discriminating extension would repeat unconditional exact-count samples over many seeds and sizes while separately reporting numerical eligibility, bias, variance, and coverage.

## Reproduction

From this directory, run `run_all.ps1` with PowerShell 7. The script uses `C:\Users\ENAN\miniforge3\envs\codex\python.exe`, reruns the model, forces and audits all three failure modes, then runs the independent verifier. A zero final exit means the full coverage map passed.
