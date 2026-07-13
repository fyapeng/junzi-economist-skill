# Dynamic discrete-choice replacement model

This compact reproducible artifact simulates a five-state equipment-replacement panel, estimates action-specific controlled transition rows from the panel, and estimates preference parameters by two distinct methods: nested fixed-point maximum likelihood (NFXP) and a Hotz–Miller-style CCP forward-mapping criterion.

The observed subsidy regimes are `0` and `1`. Policy `0.5` is explicitly labeled model interpolation. The production Bellman function accepts any finite scalar policy; it does not select from a regime table. Policy output separately reports deterioration resource cost, replacement resource cost, fiscal subsidy transfers, private flow cost, and social resource cost.

The parameter restriction is the exact inclusive box `theta_x in [0.15, 1.50]` and `replacement_cost in [1.00, 6.00]`. `domain_rows.csv` records every estimator-parameter row and both slacks; `closed_domain_corners.csv` records every corner and boundary slack. This is a computational domain, not a global identification claim. The sole identification diagnostic is the saved local Jacobian rank at the accepted NFXP estimate.

Run production with:

```powershell
& 'C:\Users\ENAN\miniforge3\envs\codex\python.exe' .\production.py
```

After production is frozen, `verify.py` independently reconstructs counts, transition estimates, arbitrary-policy solutions, Bellman residuals, midpoint levels, and local singular values without importing production code. It also evaluates two unsaved off-regime interior policies (`0.25` and `0.75`) and performs economic monotonicity checks. A passing verification writes `artifacts/verification.json`; a failed required check writes the record and exits nonzero.
