# Latent-heterogeneity profile study

## Economic object and judgment

This simulated study asks how a subsidy index changes adoption when eligible households have one of two latent intercept types. The observed choice probability is

\[
q(x)=(1-\pi)\Lambda(\alpha+\beta x-\delta)+\pi\Lambda(\alpha+\beta x+\delta),\qquad \delta\ge 0,
\]

where the closed restriction \(\delta\ge0\) labels the high-intercept type. The target is the latent separation \(\delta\); the policy object is adoption at \(x=2.10\). This policy point is beyond the observed maximum \(x=1.60\), so its image is explicitly a model-based extrapolation, not an externally validated effect or welfare statement.

The accepted unrestricted optimum is

| parameter | estimate |
|---|---:|
| \(\alpha\) | -0.063854 |
| \(\beta\) | 1.383085 |
| \(\delta\) | 1.844167 |
| \(\pi\) | 0.335770 |

Its negative log likelihood is 1162.552165. The largest scaled projected-gradient/KKT residual among the unrestricted and 51 selected conditional solutions is \(6.85\times10^{-6}\), below the declared \(2\times10^{-5}\) acceptance tolerance.

Using the accepted unrestricted optimum of the same individual Bernoulli mixture likelihood as the LR reference, the 95% chi-square(1) evaluated-grid LR set is

\[
\delta\in\{0.0,0.1,\ldots,3.2\}.
\]

This is an evaluated-grid set, not a continuous confidence interval or a population-identification result. There are no unresolved profile holes. The upper endpoint is not grid-censored because all values from 3.3 through the evaluated upper bound 5.0 are accepted conditional optima and fall outside the cutoff. The lower endpoint \(\delta=0\) is the model's closed label-normalization boundary: it is support-bounded, not a numerical grid-censoring failure.

Mapping only the best accepted conditional optimum at each included grid point gives the selected-only policy-adoption image

\[
[0.771634,\ 0.845310].
\]

Inferior local terminals never enter either the LR set or this policy image.

## Independent verification

The verifier reads `raw_primitives.json` only. It reconstructs sufficient counts from the 1,920 raw household records, implements the mixture likelihood as an independent scalar grouped calculation, chooses a cosine-lattice start design, solves with Powell followed by SLSQP, and computes finite-difference KKT residuals. It does not import production code or functions and does not read or use stored selected terminals or objectives as starts or inputs. Only after both solve paths finish does `audit.py` compare their outputs.

The independent unrestricted objective differs by \(1.1\times10^{-12}\); the largest unrestricted parameter difference is below \(10^{-6}\). Every one of the 51 conditional optima is independently reconstructed. Conditional objectives, evaluated-grid membership, and the selected-only policy image all meet the audit tolerances. The executed audit exits successfully and selects the declared `continue` branch.

## Explicit coverage map

| Claim or pipeline object | Coverage |
|---|---|
| Unrestricted optimum on the declared parameter box | Covered by independent raw-primitive reconstruction plus objective and parameter agreement |
| Every conditional optimum on \(\delta=0,0.1,\ldots,5.0\) | Covered independently at all 51 values; objectives and membership compared |
| Start and constrained-optimum acceptance | Covered by saved starts/terminals, production analytic projected gradients, and verifier finite-difference KKT checks |
| LR reference and reported evaluated-grid set | Covered; both implementations use their own accepted unrestricted optimum of the identical likelihood |
| Holes, grid censoring, and the closed lower support boundary | Covered and mechanically reconciled; no holes or grid-censored endpoints |
| Selected-only policy image | Covered by independent remapping of each independently selected conditional optimum |
| Expected versus realized sample and observed \(x\) support | Covered; 1,920 expected and realized rows, with all six declared regimes present |
| Continuous-domain population identification | **Unverified**; finite-grid separation and sample geometry cannot establish it |
| External validity at policy \(x=2.10\) | **Unverified**; the policy value is extrapolated beyond observed support |
| Finite-sample LR coverage | **Unverified**; the chi-square cutoff was not Monte Carlo validated here |
| Social welfare | **Not claimed**; adoption is not a welfare criterion |

## Branch and artifacts

The executed rule was: `continue` only if all required comparisons pass, no profile holes remain, and no endpoint is grid-censored; `refine` for a hole or grid-censored endpoint; `backtrack` for failed unrestricted/conditional reconstruction, KKT, likelihood, or membership agreement. The final decision is `continue`. This does not upgrade the extrapolation, continuous identification, or LR-coverage claims.

Compact audit artifacts are `profile_selected.csv`, `audit.json`, and `provenance.json`. Full start-level diagnostics are retained in `production_results.json` and `independent_results.json`; raw simulated inputs are in `raw_primitives.json`. `run.ps1` reproduces the complete workflow and returns nonzero if a required unit fails.
