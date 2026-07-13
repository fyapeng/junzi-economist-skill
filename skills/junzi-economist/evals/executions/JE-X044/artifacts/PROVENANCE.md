# Provenance

## Scope and source discipline

The requested skill repository was not modified. Skill guidance was read only from Git commit `d9e1673` in `C:\Users\ENAN\junzi-economist-skill`, using `git show` for exactly these committed objects:

- `skills/junzi-economist/SKILL.md`
- `skills/junzi-economist/references/EMPIRICAL_AND_STRUCTURAL_METHODS.md`
- `skills/junzi-economist/references/THEORY_MODELING.md`
- `skills/junzi-economist/references/SOFTWARE_AND_COMPUTATION.md`

`git ls-tree -r --name-only d9e1673` was used only to locate those four committed paths after root-level paths failed. No eval, temporary endpoint, other reference, or uncommitted repository file was opened.

## Runtime

- Working directory: `C:\Users\ENAN\AppData\Local\Temp\junzi-economist-struct-x044`
- Interpreter: `C:\Users\ENAN\miniforge3\envs\codex\python.exe`
- Random seeds: 1103, 2207, 3313, 4421, 5531 for recovery; 98761 for local counterfactual uncertainty draws
- Recorded package and platform versions: `run_metadata.json`
- Bellman stopping tolerance: 1e-12; maximum iterations: 20,000
- NFXP bounds: theta in [0.02,2.0], RC in [0.2,8.0]
- NFXP starts: (0.25,1.5), (0.65,3.2), (1.2,5.5), (1.8,7.5)
- Beta profile: 50 points from 0.50 through 0.99

## Artifact map

- `run_analysis.py`: complete simulation, estimation, profiling, prediction, and counterfactual pipeline
- `verify_analysis.py`: independent artifact and invariant checks rerun from primitives
- `response.md`: economic report
- `recovery_runs.csv`: seed-level estimates and held-out metrics
- `recovery_summary.csv`: sample-size aggregates
- `optimizer_starts.json`: every NFXP start, convergence status, objective, and gradient norm
- `gradient_checks.json`: finite-difference step comparisons
- `sample_beta_profile.csv`: finite-sample profile likelihood
- `population_beta_profile.csv`: exact-CCP population KL profile
- `counterfactual.json`: baseline/subsidy results and conditional uncertainty
- `counterfactual_sensitivity.csv`: beta and transition sensitivity
- `run_metadata.json`: DGP, timing, seeds, and versions
- `raw_console_output.txt`, `raw_console_error.txt`: final raw process streams
- `verification_output.json`, `verification_console.txt`: fresh verification results
- `failed_branch_parameter_name.txt`: preserved initial interface failure

CSV files use UTF-8 with BOM for Excel compatibility; JSON and Markdown use UTF-8.
