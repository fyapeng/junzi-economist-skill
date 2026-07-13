# Latent value-of-time heterogeneity in urban mode choice

## Research judgment

Continue the latent-heterogeneity branch, but treat the congestion-charge result as model-conditional and extrapolative. Repeated choices contain evidence against homogeneous preferences: normal random-coefficient simulated likelihood improves training NLL by 9.43 and AIC by 16.87 relative to homogeneous logit, while a separately parameterized two-point latent-class likelihood attains nearly the same fit. The independent diagonal-weighted SMM estimator collapses the heterogeneity standard deviation to approximately zero, showing that its eleven cross-sectional choice/attribute moments do not discriminate latent dispersion even though the panel likelihood does. The evidence supports further work on heterogeneity; it does not establish the normal mixing distribution, population injectivity, finite-sample coverage, or an equilibrium policy effect.

## Economic environment and supports (declared before estimation)

Nine hundred simulated commuters make four choices among driving, transit, and micromobility. Utility depends on alternative constants, monetary cost, travel time, reliability, and a person-specific normally distributed time coefficient. The intended and realized samples both equal 900: 700 training and 200 validation people, with no redraw or outcome-conditioned inclusion.

- Training and validation use a zero congestion charge. Cost boxes are drive $4–12, transit $1.5–5, and micromobility $0.2–2. Travel time and reliability boxes are recorded in `summary.json`.
- Interpolation is limited to new people from the same population, zero charge, and attributes within those boxes.
- Baseline-policy support is the observed $0 charge.
- Post-policy support adds $3 to driving, creating drive costs of $7–15.
- Extrapolation is explicit: the charge regime is unobserved, drive costs above $12 are outside training support, and congestion/equilibrium feedback is absent.

## Estimator comparison

| Estimator/model | Distinct criterion or distribution | Train fit | Validation NLL | Key result |
|---|---|---:|---:|---|
| Normal random-coefficient MSL | simulated integrated panel likelihood, 60 fixed antithetic draws | NLL 1739.852; AIC 3491.703 | 524.340 | sigma 0.431 |
| Diagonal-weighted SMM | 11 shares and probability-weighted attribute moments | criterion 0.061; likelihood evaluated at NLL 1749.338 | 526.084 | sigma approximately 0; selected moments do not reveal dispersion |
| Two-point latent-class MLE | exact finite-mixture panel likelihood | NLL 1740.005; AIC 3494.011 | 524.025 | two time coefficients approximately -1.263 and -0.448 |
| Homogeneous logit | misspecified sigma = 0 benchmark | NLL 1749.284; AIC 3508.569 | 525.850 | worse training fit and slightly worse validation |

All retained estimator starts, terminal parameters, objectives/criteria, raw gradients, projected gradients, active bounds, statuses, messages, and distance from the best objective are saved. Every selected estimator solution satisfies the declared projected-gradient tolerance of 0.002.

## Conditional likelihood profile and policy image

The economically justified profile domain is sigma in [0, 0.8] utility units per ten minutes, evaluated at 0.1 increments. Every one of the 9 reported indices has at least one accepted conditional optimum; there are 9 resolved points and 0 holes. At each index the likelihood profile and policy mapping use the best accepted objective, never an inferior start.

The profile minimum is at sigma = 0.4 on the reported grid. Under the 3.841459 one-parameter LR cutoff, the reported set is {0.3, 0.4, 0.5}. It is not censored at either endpoint. Mapping only those selected conditional optima gives a model-implied change in driving share from -0.07711 to -0.07605, or about -7.7 to -7.6 percentage points. This stability is conditional on the model and does not remove the support violation.

## Inference eligibility and branch decision

The profile is numerically eligible for model-conditional, one-parameter LR interpretation because the full estimator and every reported conditional problem pass the declared numerical rule. The grid and chi-square cutoff remain approximations. Population identification, finite-sample coverage, policy invariance in the unobserved charge regime, and equilibrium congestion response are not established.

Decision: **continue and fork narrowly**. Continue the panel MSL branch, retain the two-point mixture as a distributional robustness branch, and redesign the SMM branch with within-person transition/covariance moments before using it to judge heterogeneity. Pause any welfare or external-policy claim until charge variation or a defensible transport/external validation design is available. Do not abandon the descriptive result that the panel likelihood separates sigma = 0 from the profile set, but do not promote it beyond this simulated sample and maintained specification.

## Mechanical reconciliation and independent verification

The verifier passed all checks. It reconciled 900 intended = 900 realized people; 9 reported = 9 resolved + 0 holes; 3 cutoff-set rows = 3 reported set elements; and confirmed that every selected profile row is the best accepted start at its index. A separate loop-based implementation recomputed the training simulated likelihood at the profile minimum from raw attributes, choices, and draws: 1739.9734280825737 versus saved 1739.9734280825735.

Coverage map: independently recomputed—the training simulated likelihood at the selected profile minimum. Row-level reconciled—sample counts, profile resolved/hole counts, best accepted start at each index, and set count. Not covered—search completeness between starts; SMM moments/criterion; latent-class and homogeneous implementations; gradient/KKT calculations; policy arithmetic; cutoff validity; population identification; finite-sample coverage; and economic realism.

## Artifacts

- `study.py`, `smm.py`, `verify.py`: executable production, alternative-estimator, and independent-verification code.
- `artifacts/raw_simulation.npz`: compact raw attributes, choices, draws, and train/validation indices.
- `artifacts/all_starts.csv`, `smm_all_starts.csv`, `profile_all_starts.csv`: complete start-level diagnostics.
- `artifacts/profile_selected.csv`: best accepted conditional optimum and policy mapping at every index.
- `artifacts/summary.json`, `smm_summary.json`, `verification.json`, `provenance.json`: reconciled summaries, coverage map, and provenance.

Provenance: exact skill commit `77aa2f1`; simulation seed 51051; integration-draw seed 9117; Codex Python 3.11.15, NumPy 2.4.6, SciPy 1.17.1 on Windows. An initial SMM reporting attempt failed from an extra policy-array index; no partial estimate was reused, the full starts were rerun after the exact repair, and the successful artifact records the rerun.
