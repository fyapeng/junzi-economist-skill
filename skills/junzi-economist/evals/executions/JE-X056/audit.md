# Independent audit: `junzi-economist-struct-x056`

## Overall verdict: MIXED

The numerical/economic result is **PASS** and the currently selected branch `continue` is supported. The audit artifact as an audit implementation is **MIXED** because its coverage map contains a wrong grid count and an unsupported sample-count claim, and its implemented failure routing does not match its declared branch rule. These reporting/control-flow defects do not change the current numerical result because every current required comparison passes.

This audit did not modify or overwrite any existing repository artifact. It added only this report. A third recomputation was run from `raw_primitives.json` with a separately written grouped-binomial likelihood, fresh seeded random starts, differential evolution, explicit fresh starts on every parameter-box face, L-BFGS-B polishing, analytic gradients, and projected KKT checks. Its scratch code/result were kept outside the audited directory as `C:\Users\ENAN\AppData\Local\Temp\audit_x056_recompute.py` and `C:\Users\ENAN\AppData\Local\Temp\audit_x056_recompute.json`.

## Exact numerical evidence

### Unrestricted optimum — PASS

Third implementation:

- negative log likelihood: `1162.552165386578`
- terminal `[alpha, beta, delta, pi_high]`: `[-0.063853701613, 1.383084940989, 1.844166657667, 0.335770367911]`
- raw projected-gradient infinity norm: `4.31398e-07`
- accepted fresh-start terminals with raw projected KKT at most `1e-5`: `139`

Agreement:

- objective difference from production: `0.000000000000`
- objective difference from `independent_verify.py`: `1.13687e-12`
- maximum parameter difference from production: `1.15350e-08`
- maximum parameter difference from verifier: `9.98655e-07`

Thus the unrestricted reference used for all LR distances is independently reproduced from raw primitives.

### All 51 conditional profile optima — PASS

The audited grid is exactly `delta = 0.0, 0.1, ..., 5.0`, hence 51 values. All 51 third-implementation solutions were accepted.

- maximum absolute conditional-objective difference versus production: `2.27374e-13`
- maximum absolute conditional-objective difference versus verifier: `4.54747e-13`
- maximum absolute LR-distance difference versus production: `4.54747e-13`
- maximum absolute LR-distance difference versus verifier: `2.27374e-12`
- maximum third-implementation raw projected-gradient infinity norm: `7.43412e-06` at `delta=1.7`
- minimum number of fresh-start terminals per profile with raw projected KKT at most `1e-5`: `81`
- production's largest reported scaled KKT residual: `6.84855e-06` at `delta=1.9`, below its `2e-5` tolerance
- verifier's largest reported scaled finite-difference KKT residual: `2.04064e-05` at `delta=1.4`, below its `8e-5` tolerance

The largest conditional-terminal parameter discrepancy from production, excluding `delta=0`, is `4.56968e-07`. At `delta=0`, the mixture share is observationally irrelevant because the two component logits coincide, so terminal-share disagreement is expected and objective/policy agreement is the relevant check.

The explicit box-face starts matter: an unconstrained differential-evolution pass alone missed the narrow active `pi_high=0.08` branch at some grid points, while fresh face starts recovered it. After taking the best accepted terminal across all searches, every conditional objective agrees with both stored implementations to machine precision.

### LR set, holes, censoring, and support — PASS

Using the independently recomputed unrestricted objective and cutoff `3.841458820694124`:

- evaluated-grid LR set: all 33 points `{0.0, 0.1, ..., 3.2}`
- `LR(3.2) = 3.346525642618417`, included
- `LR(3.3) = 4.444343042110631`, excluded
- holes: none among all 51 accepted profiles
- left endpoint: `delta=0`, the declared closed label-normalization/parameter-support boundary; support-bounded, not grid-censored
- right endpoint: `delta=3.2`, strictly below the evaluated grid maximum `5.0`; not grid-censored
- parameter box: `alpha in [-3,2]`, `beta in [0.05,2.5]`, `delta in [0,5]`, `pi_high in [0.08,0.92]`
- realized sample: 1,920 rows, 796 successes, 320 rows at each of `x = {-1.4,-0.8,-0.2,0.4,1.0,1.6}`
- policy point: `x=2.1`, outside observed support above `1.6`; therefore model-based extrapolation

### Selected-only policy image — PASS

Mapping only the best accepted conditional terminal at each included grid value gives:

- third implementation: `[0.7716340453664032, 0.8453102552398015]`
- production: `[0.7716340454355755, 0.8453102550897541]`
- verifier: `[0.7716340476781150, 0.8453102556679246]`
- maximum endpoint difference from production: `1.50047e-10`
- maximum endpoint difference from verifier: `2.31171e-09`

Inferior local terminals do not enter this image.

## Independence of `independent_verify.py` — PASS

Static AST inspection and direct source inspection establish:

- imports are only `json`, `math`, `platform`, `pathlib`, `numpy`, `scipy`, and `scipy.optimize`; there is no production-module import
- the only input read before solving is `raw_primitives.json` at line 12
- grouped sufficient counts are reconstructed from raw observation rows at lines 13–20
- likelihood evaluation is separately coded as a scalar grouped Bernoulli mixture loop
- starts are generated solely from declared bounds, count, offset, and a cosine lattice at lines 67–76
- no production result, stored terminal, or stored objective is read or supplied as a start/input
- `independent_results.json` appears only as the output written at line 142
- SHA-256 of the inspected verifier is `a82a489ec84fabaf37db937b9591736013b4737b436eb070683f5fa5b6e4830a`, matching `provenance.json`

The verifier does write its own output, but it does not consume that output or any production output during reconstruction.

## Audit-artifact defects — MIXED

1. `audit.py` line 29 and `audit.json` say every conditional optimum is covered at "27 values". The executable check at line 16 correctly requires 51, and the actual result has 51; the coverage prose is wrong.
2. `audit.py` line 33 says sample construction covers the expected-versus-realized row count, but `raw_sample_complete` at line 25 checks only the six stored `training_x` values. It neither reads raw primitives nor asserts `expected_n == realized_n == 1920`. The raw file does satisfy that condition, as independently checked above, but `audit.py` does not establish it.
3. The declared rule says failures in unrestricted reconstruction, KKT, likelihood agreement, or membership comparison require `backtrack`. The implementation at line 44 instead sends every failed audit with `conditional_objectives_agree == true` to `refine`. For example, a failed unrestricted KKT check with agreeing conditional objectives would be misrouted. This defect is dormant in the current run because `passed == true`.

## Coverage map

| Object or claim | Status | Evidence / limit |
|---|---|---|
| Raw-primitives-only verifier | PASS | Static imports/file reads and start construction inspected; no production input or stored seed |
| Unrestricted optimum on declared box | PASS | Third objective exact to production and within `1.14e-12` of verifier; fresh global, random, and box-face searches |
| 51 conditional optima | PASS | All accepted; maximum objective disagreement `4.55e-13` |
| KKT/acceptance | PASS | Third max raw projected norm `7.44e-06`; production/verifier below their declared tolerances |
| LR reference and distances | PASS | Recomputed from third unrestricted optimum; maximum LR disagreement `2.28e-12` |
| Evaluated-grid set | PASS | Exactly 33 points, `0.0` through `3.2` |
| Holes and censoring | PASS | No holes; lower endpoint support-bounded; upper endpoint interior to evaluated support |
| Selected-only policy image | PASS | `[0.7716340454, 0.8453102552]`, agreeing within `2.32e-09` |
| Observed and policy support | PASS | observed `x` from `-1.4` to `1.6`; policy `2.1` explicitly extrapolative |
| Existing audit coverage prose | MIXED | wrong "27" count and row-count coverage overstatement |
| Existing failure branch implementation | MIXED | current `continue` correct; counterfactual failure routing can contradict declared rule |
| Continuous-domain population identification | UNVERIFIED | finite-grid sample likelihood does not prove it |
| External validity at `x=2.1` | UNVERIFIED | policy point lies outside observed support |
| Finite-sample chi-square LR coverage | UNVERIFIED | no Monte Carlo calibration |
| Welfare | NOT CLAIMED | adoption probability is not a welfare measure |

## Branch decision — PASS for the current run

The evidence supports **`continue`**: unrestricted and all 51 conditional reconstructions agree, all selected solutions satisfy their acceptance rules, there are no holes, and neither reported-set endpoint is a numerical grid-censoring failure. `refine` and `backtrack` are not triggered by the current data/results. The implementation of how future failed cases are routed should nevertheless be corrected as described above.
