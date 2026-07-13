# Minimal dynamic DDC artifact

This compact artifact estimates a two-state, two-action infinite-horizon dynamic logit model. Controlled transition probabilities are estimated from raw state-action transition counts. Choice parameters are estimated separately by (i) NFXP full-solution likelihood and (ii) a distinct CCP/Hotz–Miller policy-evaluation minimum-distance criterion.

`production.py` creates `raw_primitives.json` and `production_output.json`. It retains every declared optimizer start and accepts a start only using a fresh finite-difference projected-gradient/KKT check. The reported singular values support only a local numerical-rank statement.

The exact restricted search is the declared closed 3-by-3 finite parameter grid. Every grid row is saved, including its unique key, domain label, boundary flags, restriction slack, feasibility flag, and NFXP objective. No continuous identification claim is made.

Policy levels 0 and 1 are observed regimes. Levels 0.25, 0.5, and 0.75 are explicitly labeled model-based interior interpolation. Accounting separately records deterministic action components, policy cost, logit entropy, and their identity against the initial Bellman value.

After production is finalized and run, `verifier.py` is authored last. It is the sole independent verifier, reimplements the model from raw primitives, and writes `verification.json` plus `final_manifest.json`, whose hashes include the verifier source itself.

Run with the dedicated environment:

```powershell
& 'C:\Users\ENAN\miniforge3\envs\codex\python.exe' .\production.py
& 'C:\Users\ENAN\miniforge3\envs\codex\python.exe' .\verifier.py
```
