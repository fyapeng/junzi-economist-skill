# Independent audit of `junzi-economist-struct-x054`

## Verdict: MIXED

The substantive numerical results and the restrained research judgment **PASS**. I found no incorrect objective, KKT classification, profile value, LR membership decision, count, censoring flag, policy image, or support calculation. The overall verdict is **MIXED**, rather than PASS, only because the repository's own `verify.py` is partially rather than fully independent: it imports the unrestricted reference objective from `summary.json`, reads the evaluated points and saved terminals from `profile.csv`, and uses each saved terminal as one of its three optimizer starts. Its written coverage limitation is accurate, but it does not independently establish the unrestricted reference, simulation, start/KKT records, or policy mapping.

I did not execute `study.py` or `verify.py`, did not overwrite any supplied artifact, and did not use `verification.json` as numerical evidence. I independently reconstructed the likelihood from `simulated_data.npz`, used fresh generic starts and a finite-difference bounded solve for the unrestricted problem, used derivative-free bounded solves for all 17 conditional problems, approximated gradients independently for all 108 saved terminal records, and independently rebuilt policy effects and support statistics.

## 1. Saved primitives and estimator distinctness — PASS

- The saved arrays have shape `900 x 4`; saved seed is `731904`.
- Replaying the declared RNG sequence and DGP reproduces `price`, `quality`, and `y` **exactly** (element-for-element).
- The direct estimator maximizes the six-parameter panel-mixture likelihood with L-BFGS-B and analytic scores.
- The EM implementation is algorithmically distinct: it alternates posterior responsibilities and bounded weighted component M-steps. Its 800-row trace decreases from `1320.0810416475135` to `1316.923078422088`, with zero objective increases above `1e-10`. It stops at the iteration cap and has projected-gradient maximum `0.0010601883630242455`, above the `0.0002` admission threshold, so the response correctly does not admit it as the reported optimum.
- Direct minus EM objective is `-1.7858769751910586e-7`: nearly identical likelihood, but different admission status.
- The homogeneous estimator is a genuinely different three-parameter single-logit benchmark. An independent derivative-free solve gives `1320.3516706995601`, exactly the reported objective at displayed precision.
- Recomputed comparison arithmetic: `2*(1320.3516706995601 - 1316.9230782435004) = 6.857184912119465`; AIC values are `2645.846156487001` (mixture, 6 parameters) and `2646.7033413991203` (homogeneous, 3 parameters).

Caveat: EM's internal M-step bounds are expressed on component intercepts rather than exactly the direct estimator's transformed box. Its reported terminal is nevertheless inside the direct box. The response uses EM only as a numerical comparison, not as an independently accepted estimate, so this does not overturn the PASS.

## 2. All start and KKT records — PASS

There are exactly `108` records: `6` unrestricted starts plus `17 x 6 = 102` conditional starts. All 108 report optimizer success, but the declared finite-objective/projected-gradient rule accepts only `94`; this correctly leaves `14` optimizer-success records rejected.

I recomputed the objective and a bound-aware finite-difference projected gradient at every saved terminal:

- maximum absolute objective discrepancy: `0.0`;
- acceptance decisions reproduced: `94/108` accepted, with **0 mismatches**;
- maximum absolute difference between independent and reported projected-gradient maxima: `6.303307523401611e-7`;
- largest independent projected-gradient maximum among production-accepted rows: `0.00019396679817873516`, below `0.0002`.

Accepted-start counts and selected best accepted start IDs are:

| Index | Accepted / 6 | Selected start |
|---:|---:|---:|
| unrestricted | 4 | 3 |
| 0.10 | 4 | 4 |
| 0.15 | 6 | 3 |
| 0.20 | 6 | 2 |
| 0.25 | 6 | 2 |
| 0.30 | 6 | 3 |
| 0.35 | 6 | 2 |
| 0.40 | 5 | 1 |
| 0.45 | 5 | 1 |
| 0.50 | 6 | 0 |
| 0.55 | 5 | 1 |
| 0.60 | 4 | 1 |
| 0.65 | 5 | 1 |
| 0.70 | 6 | 0 |
| 0.75 | 6 | 1 |
| 0.80 | 5 | 3 |
| 0.85 | 5 | 2 |
| 0.90 | 4 | 0 |

The unrestricted selected terminal has transformed `log(b1)=-2`, the lower bound. Its raw derivative in that coordinate is `+0.024963831374552825`, which is the correct KKT sign for a minimizer at a lower bound; projection sets it to zero. The reported projected-gradient maximum is `1.1369414981032833e-5`.

## 3. Accepted unrestricted optimum — PASS

A fresh finite-difference bounded solve from five generic starts, without using a saved terminal or the production analytic gradient, produced objectives between `1316.9230782435025` and `1316.9230782435097`. The best fresh result is:

- objective: `1316.9230782435025`;
- discrepancy from reported objective: `2.0463630789890885e-12`;
- independent finite-difference projected-gradient maximum: `4.3058889787062064e-5`;
- structural parameters: `a1=-2.020957488336176`, `a2=1.3225335292124458`, `b1=0.1353352832366127`, `b2=1.6233226309217668`, `gamma=0.5381854919285346`, `pi=0.4800372726601422`.

These agree with the reported optimum to numerical precision. The boundary claim is exact: `b1=exp(-2)=0.1353352832366127`.

## 4. Conditional profile, LR reference, and membership — PASS

I independently solved every conditional problem from generic starts. The maximum absolute difference from the 17 reported conditional objectives is `7.889866537880152e-11`; the largest independent finite-difference projected-gradient maximum among the 17 selected solutions is `0.00018387709133094174`, below the declared `0.0002` threshold.

LR distances below use the fresh unrestricted optimum of the **same mixture likelihood**, `1316.9230782435025`. The maximum LR discrepancy from `profile.csv` is `1.5370460459962487e-10`.

| pi | Conditional NLL | LR | In evaluated-grid set | Stored policy effect |
|---:|---:|---:|:---:|---:|
| 0.10 | 1318.129218750945 | 2.412281014884 | yes | 0.050626488408 |
| 0.15 | 1317.821422628193 | 1.796688769381 | yes | 0.050686547641 |
| 0.20 | 1317.574950009962 | 1.303743532920 | yes | 0.050842556820 |
| 0.25 | 1317.374868572553 | 0.903580658101 | yes | 0.051067309046 |
| 0.30 | 1317.213354565455 | 0.580552643905 | yes | 0.051346509590 |
| 0.35 | 1317.087006718586 | 0.327856950167 | yes | 0.051668523086 |
| 0.40 | 1316.995088943696 | 0.144021400387 | yes | 0.052020746827 |
| 0.45 | 1316.938515148007 | 0.030873809010 | yes | 0.052388132808 |
| 0.50 | 1316.937509207435 | 0.028861927866 | yes | 0.052986258433 |
| 0.55 | 1317.078710068349 | 0.311263649693 | yes | 0.053536266355 |
| 0.60 | 1317.327085448133 | 0.808014409260 | yes | 0.053790277597 |
| 0.65 | 1317.643181048651 | 1.440205610298 | yes | 0.053827418517 |
| 0.70 | 1318.000115973364 | 2.154075459723 | yes | 0.053711089691 |
| 0.75 | 1318.379917849905 | 2.913679212805 | yes | 0.053490542809 |
| 0.80 | 1318.770903491612 | 3.695650496219 | yes | 0.053203218801 |
| 0.85 | 1319.165874492765 | 4.485592498524 | no | blank |
| 0.90 | 1319.560978147914 | 5.275799808823 | no | blank |

Against cutoff `3.841458820694124`, the evaluated-grid set is exactly `{0.10, 0.15, ..., 0.80}`: 15 points. Values `0.85` and `0.90` are excluded.

## 5. Holes, censoring, and count reconciliation — PASS

- Expected evaluated indices: `17`.
- Profile rows / selected accepted conditional solutions: `17`.
- Indices with at least one accepted start: `17`.
- Holes: `0`.
- In-set rows: `15`; out-of-set rows: `2`; `15 + 2 = 17`.
- Accepted conditional start records: `90`; accepted unrestricted records: `4`; `90 + 4 = 94` accepted records overall.
- The lowest evaluated point, `0.10`, is in the set, so the left endpoint is correctly labeled censored.
- The highest evaluated point, `0.90`, is outside the set, and `0.85` is also outside, so the right endpoint is correctly labeled not censored.

The response correctly calls this an evaluated-grid set rather than a continuous confidence interval and makes no interpolation or coverage claim.

## 6. Selected-only policy image — PASS

I independently evaluated the subsidy mapping from each selected profile terminal:

- all 15 in-set rows have a stored policy value;
- both out-of-set rows (`0.85`, `0.90`) are blank;
- no policy value differs from the independent calculation at machine-readable precision;
- selected in-set range: `[0.05062648840805483, 0.053827418517399084]`;
- unrestricted policy effect: `0.05266331782071512`, exactly the reported value.

Thus the response's 5.06–5.38 percentage-point range and its statement that only selected, accepted, in-set solutions enter the policy image are correct. The range width is about `0.003201` in probability, or `0.3201` percentage point.

## 7. Support and branch claims — PASS, with appropriately limited status

Independent support calculations reproduce:

- baseline observed price support: `[0.35, 3.8]`;
- post-subsidy support: `[-0.10000000000000003, 3.3499999999999996]`;
- share of post-policy prices below the observed baseline minimum: `0.03277777777777778` (`3.28%`).

The code holds quality, preference parameters, and the mixing share fixed while reducing every price by `0.45`. The response correctly calls the result model-implied rather than causal or welfare evidence, explicitly lists omitted fiscal, producer, quality, congestion, distributional, and equilibrium channels, and identifies the lower-tail extrapolation.

The branch judgment is supported by the evidence: the unrestricted low-type price coefficient is at the lower box bound; the true `b1=0.72` is not recovered; the `pi` grid set reaches the lowest evaluated value; and no repeated-seed or sample-size experiment exists. Retaining the work as a numerical/profile demonstration while declining latent-parameter recovery, population-identification, coverage, and estimator-performance claims is the strongest defensible conclusion. Extending the profile below `0.10`, testing a substantively defensible lower bound for `b1`, and running repeated seeds/larger samples are discriminating next steps. A denser interior grid would not resolve the active coefficient-bound issue.

## 8. Repository verifier independence and coverage — MIXED

What `verify.py` independently does:

- restates the conditional mixture negative log likelihood rather than importing `study.py`;
- uses derivative-free Powell rather than production L-BFGS-B/analytic gradients;
- recomputes a conditional objective at all 17 rows;
- rebuilds LR arithmetic, membership, set values/count, holes relative to the summary grid, and endpoint flags;
- obtains maximum conditional-objective disagreement `2.7284841053187847e-11` in the supplied `verification.json`.

What prevents full independence:

- it imports `uobj` from `summary.json` instead of independently solving the unrestricted likelihood;
- it reads the evaluated points and terminals from `profile.csv`;
- the first Powell start at each index is the saved production terminal, so the verification is not a from-scratch basin search;
- it does not recompute simulation generation, direct-start acceptance, projected gradients/KKT conditions, EM, homogeneous estimation, or policy effects.

The `coverage_map` in `verification.json` explicitly discloses that simulation, EM, and policy mapping are not covered, and accurately describes the positive checks it performs. Therefore the **coverage disclosure passes**, while **verifier independence is mixed**. This limitation does not contaminate the reported numerical conclusions because the present audit independently supplied the missing unrestricted, KKT, DGP, homogeneous, and policy checks.

## Final disposition

- Numerical artifacts and reconciliation: **PASS**.
- Economic/support/branch claims: **PASS** at the stated exploratory, model-implied status.
- Original verifier coverage statement: **PASS**.
- Original verifier independence: **MIXED**.
- Overall: **MIXED**, with no substantive numerical failure found.
