# Independent endpoint audit

## Verdict

**Overall: MIXED (computational results pass; two design/accounting claims need qualification).**

The final program is deterministic and reproducible. An independent run from a copied program in `C:\Users\ENAN\AppData\Local\Temp\struct-x045-independent-reproduction` completed with exit code 0 in **37.51 seconds**. Its `raw_results.json` SHA-256 is exactly the endpoint hash, `F470593BC85D567CBE6FA9C76F20F5E380C320668E7E0F54C70E24B72CD3C855`, and its CSV hash also exactly matches (`9966DFA339D911E4D2CF0BE55D2D1FC65EC72E9EEFA7D2EF0949316AA41C4B7B`). The reproduction did not overwrite endpoint artifacts.

The reported OLS/IV estimates, first-stage statistic, moments, derivatives, multiproduct markups, recovered costs, Monte Carlo summaries, counterfactual residuals, and surplus/profit/tax/resource totals are numerically correct. The false high-price-root correction is real. The final code no longer redraws shocks until costs are positive, but it still **drops** a market conditional on realized cost; this branch did not trigger in any declared final draw. Thus the unconditional statement that no selection is conditioned on costs is not true of the implemented generator, even though it is true ex post for the reported seeds.

## Audit results by requested item

| Item | Status | Independent finding |
|---|---|---|
| Timing and DGP | **MIXED** | Markets and shocks are drawn in the stated order; firms price after `x,z,w,xi,omega,c` are realized. The main, weak, and all 30 repeated final samples contain 180 markets/540 rows and zero simulation failures. However, `simulate()` drops a market when any `c <= 0.05` (lines 95–98), so the code's population experiment can condition sample inclusion on realized costs. |
| Exclusion after transformations | **MIXED** | In the realized samples, `z` and `w` are independently drawn before equilibrium and absent from utility; the exact transformed demand error is `xi` (maximum identity error `2.22e-15`). Main-sample correlations with `xi` are `corr(z,xi)=0.0247` and `corr(w,xi)=-0.0184`, while `corr(omega,xi)=0.6325`. Equilibrium price endogeneity is therefore generated as stated. The conditional-drop branch could induce selection dependence in other seeds, so exclusion is not guaranteed over the full implemented support. |
| OLS/IV equations and signs | **PASS** | Independent construction with `X=[1,x,-p]` reproduces OLS `(-1.451277,1.238700,0.682457)`, valid IV `(-0.123540,1.274771,1.077940)`, and invalid IV `(-1.820501,1.228669,0.572480)`. Reporting the coefficient on `-p` as positive `alpha` is correct. |
| First stage, moments, rank | **PASS** | The conventional homoskedastic partial F for joint exclusion of `z,w` is independently `902.3162` with `(2,536)` degrees of freedom. Valid moments are approximately `(0,0,0.002952,-0.007065)`; invalid moments are `(0,0,-0.099847,0.248544)`. The stated rank and condition diagnostics agree with the stored matrices. The report correctly labels the F as homoskedastic; it is not a market-cluster-robust weak-IV statistic. |
| Demand derivative | **PASS** | `ds/dp=-alpha[diag(s)-ss']` is correct. The stored central-difference discrepancy, `1.94e-11`, reproduces. |
| Multiproduct markup orientation | **PASS** | For price equation `k`, the code uses row `k`, column `j` equal to `-O_kj * (partial s_j / partial p_k)`, hence `H(p-c-tax)=s`. This matches the stated FOCs. With simple logit and common `alpha`, the derivative matrix is symmetric, but the explicit transpose is nevertheless oriented consistently. |
| Marginal-cost and cost-parameter recovery | **PASS** | At true `alpha`, independent inversion recovers true marginal costs to maximum absolute error `1.05e-11`; FOC error is `1.70e-12`. At estimated valid-IV `alpha`, the reported coefficients `(2.229994,0.660755,0.274210)`, MAE `0.02145`, minimum cost `1.21391`, and condition number `47.12` reproduce. The invalid-alpha branch's one negative cost is retained. |
| Repeated-sample recovery and failures | **MIXED** | All 30 declared draws truly have 540 rows, zero simulation failures, and 30/30 numerical estimator success; the reported means, biases, RMSE, and median F reproduce. But summary `failures` counts only estimation exceptions. A market dropped by the DGP/solver would be recorded in each raw row (`simulation_solver_failures`, `n`) yet the estimation could still be labeled successful. The summary is accurate for these seeds, not a complete general failure accounting rule. |
| Weak versus invalid IV | **PASS** | Weakness is created in a separate DGP by setting the coefficient of the sole used excluded shifter `z` to `0.015`; F=`0.685`, alpha SE=`2.295`, and ill-conditioning diagnose weak relevance. The invalid design uses `qbad=xi+noise`, has F=`880.7` but alpha=`0.572` and large excluded moments, correctly separating invalidity from weakness. |
| Counterfactual FOCs and acceptance | **PASS** | Baseline, tax, and merger solve all 180 markets. Each uses five starts (900 attempts per scenario); all final attempts are accepted, economically nonnegative, and away from bounds. Acceptance checks solver success, raw residual `<1e-8`, own-share-normalized residual `<1e-8`, nonnegative net markup, and no bound contact. Stored selected-root maxima match the response (`9.51e-12`, `9.41e-12`, `6.67e-12`). |
| Root deduplication, bounds, and claims | **PASS** | Accepted roots are deduplicated at max-norm distance `<1e-7`; bounds are `[-5,25]`. One root is detected in every searched final market. The response explicitly says “detected by this search” and disclaims global uniqueness, which is the warranted language. |
| Consumer surplus and accounting | **PASS** | `CS=(1/alpha) log(1+sum exp(delta))` is correct for unit market size and normalized outside utility. Profit `sum(p-c-tax)s`, tax revenue `sum tax*s`, and real cost `sum c*s` all reproduce the table. The warning not to subtract real cost again from profit is correct. |
| Preserved failed/rejected branches | **PASS** | Full final start traces, counterfactual failures, Monte Carlo rows, and invalid cost failures are stored. Both intermediate JSON/text pairs exist and contain the rejected outcomes rather than only summaries. |
| False high-price-root correction | **PASS** | In the initial branch, accepted solutions include 170/134/194 attempts with a component above 10 in baseline/tax/merger, reaching prices near 25 while raw residuals remain below `1e-8`; 132 baseline markets are labeled multiple. The final solver minimizes share-normalized FOCs and none of these roots survive. This is a substantive correction, not just changed wording. |
| Removal of cost-conditioned redraws | **MIXED** | The final source has no redraw loop and uses bounded `z` plus a higher cost intercept (`gamma0` rises from `0.75` in both preserved intermediate JSONs to `2.25` final). Thus removal of redraw-until-positive logic from the final implementation is real. Endpoint artifacts do not preserve the intermediate source, so the exact earlier redraw algorithm cannot be independently reconstructed. More importantly, final lines 95–98 retain cost-conditioned **dropping**, contradicting the broader response sentence “No selection or redraw is conditioned on realized costs.” |

## Reproducible defects and qualifications

### D1 — Cost-conditioned market dropping contradicts the stated no-selection design

**Severity: material qualification; no effect on declared realized seeds.**

The final generator executes:

```python
if np.any(c <= 0.05):
    solver_failures.append(...)
    continue
```

This does not redraw, but it selects the estimation sample on a function of `omega`, which is correlated with `xi`. If triggered, conditioning on inclusion can invalidate `E[z xi]=E[w xi]=0` even though the primitive draws are independent. The main, weak, and 30 repeated declared samples have zero triggers, so all reported numerical results remain valid for the realized experiment. A precise response should say: “No cost-conditioned redraw or drop occurred for the declared seeds; the code retains a logged drop-on-invalid-cost safeguard.” A stronger implementation would choose bounded shock support guaranteeing admissible cost, or treat any such event as a failed whole replication rather than estimate on a shortened sample.

### D2 — Monte Carlo headline failures omit simulation/partial-sample failures

**Severity: accounting defect outside the realized zero-failure seeds.**

`monte_carlo()` stores `simulation_solver_failures` and `n`, but `valid_failed`/`invalid_failed` are set only on exceptions from `estimate()`. Therefore a 537-row partial sample can count as a successful replication. The reported 30/30 is correct because independently verified `n` is always 540 and total simulation failures are zero. For robust general accounting, a replication should be failed unless `len(df)==T*J` and `simulation_solver_failures==0`, with simulation and estimation failures summarized separately.

### D3 — Invalid-instrument observability/timing is under-described

**Severity: narrative qualification, not a numerical error.**

The economic mapping says the econometrician observes `p,s,s0,x,z,w` and excludes `xi`, but the invalid branch later uses `qbad=xi+noise`; `qbad` is generated only after equilibrium prices are solved. It is a valid deliberate *invalid-proxy experiment*, and its diagnosis is correct, but it is not included in the declared observable data mapping and is mechanically constructed from the unobservable demand shock. The response should label it an auxiliary observed proxy introduced solely for the falsification branch and state its timing.

## Bottom line

The central structural-IO exercise and all headline numbers **pass** independent numerical verification. The main correction—normalizing FOCs to eliminate vanishing-share pseudo-roots—is demonstrably real, and the response uses appropriately local/search-based equilibrium language. The endpoint should receive a **mixed rather than unqualified pass** because the final generator still has cost-conditioned sample dropping, the Monte Carlo summary would not count such partial samples as failures, and the invalid proxy's observability/timing is not declared cleanly. None of these qualifications changes the reported results for the specified seeds, because no market was dropped in any of them.
