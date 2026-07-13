# Software and computation — 驭器

## Route by task

| Task | Typical instruments | Main checks |
|---|---|---|
| Data construction and standard econometrics | Stata, R, Python | labels, joins, units, missingness, reproducible scripts |
| High-dimensional panels and fixed effects | Stata, R, Python | singleton handling, clustering, absorption, memory |
| Discrete choice and IO demand | PyBLP, Biogeme, xlogit, Julia, Matlab | shares, outside good, instruments, contraction, gradients |
| Dynamic programming and structural estimation | Julia, Python/JAX/PyTorch, Matlab | Bellman residuals, state grids, simulation, recovery |
| Bayesian estimation | Stan, PyMC, NumPyro | prior sensitivity, chains, convergence, posterior predictive checks |
| Optimization and equilibrium | JuMP, Ipopt, NLopt, Optim, SciPy | feasibility, KKT/residuals, starts, scaling, local optima |
| Agent-based and network models | Mesa, AgentPy, Julia, network libraries | calibration, stochastic variation, emergent mechanisms |
| Writing and references | LaTeX, Quarto, Zotero, BibTeX | source fidelity, reproducible tables, stable keys |

This table is a router, not a restriction. Verify current official documentation and installed versions before relying on syntax or capability.

## Reproducible workflow

- preserve immutable raw data and document provenance;
- encode transformations in scripts rather than manual edits;
- use explicit environments and dependency locks;
- record random seeds, tolerances, solver options, hardware-sensitive behavior, and versions;
- separate exploratory outputs from confirmed artifacts;
- generate tables and figures from analysis code;
- add tests for identities, invariants, toy cases, and previously observed failures;
- validate checkpoint protocol metadata, unique task keys, seeds, and expected coverage before resuming; do not reuse a partial run merely because its row count matches;
- retain portable formats and human-readable state at tool boundaries.

## Numerical discipline

Scale variables, inspect conditioning, enforce economic constraints, and distinguish solver convergence from economic validity. Save diagnostic traces when they can discriminate implementation, numerical, identification, and theoretical failures.

Make verification recompute the object from primitives in a fresh output path. Reading stored residuals or a previous result file can check a schema or snapshot, but it is not an independent solve. When searching for equilibria, retain the full scan and root-evaluation trace, reject unreliable evaluations, collect every admissible sign-change bracket, and avoid returning the first root as if uniqueness had been established. Search for a non-crossing root with a signed-residual extremum or another method that can distinguish tangency from an ordinary crossing; minimizing absolute residual around a known crossing is not a tangency test. Put every claimed diagnostic into the executed acceptance rule. Vary one numerical dimension at a time when attributing convergence, report root and residual differences, and label a joint grid change as a stress test rather than isolated evidence.

For constrained estimators, record active bounds and projected or KKT residuals for every selected solution. Preserve each start's initial point, terminal parameters, objective, raw and projected gradients, status, message, and distance from the best objective; parameter spread across starts is evidence of a ridge only among solutions with substantively equivalent objectives.

Scale equilibrium residuals by an economically meaningful quantity and reject degenerate states in which raw residuals vanish only because shares, quantities, or probabilities approach zero. Save the complete executable branch or patch that produced an important failure, not only its output. Describe a verifier that imports production solvers or reads saved summaries as a regression check; reserve “independent verification” for a separate implementation or recomputation from primitives that can detect a shared coding error.

## Toolchain exit

Do not continue using a tool because code already exists. When a package, language, data format, or pipeline blocks the real question, preserve portable inputs, specifications, tests, and learned results; then replace or retire the instrument. Never change the research target merely to fit the available tool.

## Local profiles

Machine paths, licensed software, GPU availability, cluster commands, and private databases belong in local `AGENTS.md`, environment configuration, or an untracked profile. The public skill should describe routing and verification without assuming one machine.

## Bundled manuscript checks

- Run `scripts/check_citekeys.py` to verify that Pandoc-style manuscript citations exist in a BibTeX database. Missing keys fail the command; unused entries are informational unless `--fail-on-extra` is requested.
- Run `scripts/prose_lint.py` on substantial manuscript prose when generic rhetoric or repeated contrast formulas are a concern. Treat hits as a review queue, not automatic errors or rewrite instructions.

Use Zotero, current web search, PDF, and LaTeX skills for source retrieval, library management, document reading, and compilation. Do not recreate those systems inside this skill.
