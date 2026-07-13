# Structural differentiated-products simulation: executed result

## Research judgment

The artifact is a successful, equation-verified recovery demonstration for one deliberately designed finite population. It is **not** a broad estimator-performance result. Forty markets with five products each were declared before simulation, and all 200 rows were retained: there are no redraws, no market survival rule, and no inclusion decision based on latent shocks, equilibrium success, or outcomes.

Consumers choose one inside product or an outside good under

\[
u_{jm}=1.1x_{jm}-1.6p_{jm}+\xi_{jm}+\epsilon_{jm}.
\]

Each single-product firm solves the logit Bertrand condition under per-unit subsidy \(\tau\):

\[
p_{jm}-(mc_{jm}-\tau)-\frac{1}{1.6(1-s_{jm})}=0.
\]

The bounded solver searches only \([mc-\tau+10^{-8},mc-\tau+4]\), keeps every start, and accepts a market only when the raw maximum FOC residual is below \(10^{-10}\). Roots were found for all markets and all three starts. Maximum raw residuals were \(3.33\times10^{-16}\) at baseline and \(4.44\times10^{-16}\) under the subsidy; economically scaled maxima were \(1.94\times10^{-16}\) and \(2.39\times10^{-16}\). This establishes roots found in the declared box, not global uniqueness or the absence of roots outside it.

## Instrument timing and recovery

The valid cost instrument `z_cost` is observed before pricing, enters marginal cost, and is included in the equilibrium input. The finite-population demand shock is constructed to be exactly orthogonal to `[1, x, z_cost]`. The valid-IV estimates recover \(\alpha=1.6000\) and \(\beta_x=1.1000\).

The deliberately invalid instrument is not merely described after the fact. Only after demand shocks, prices, shares, and outcomes exist does the executable code construct `z_invalid = xi + noise`, then merge it one-to-one into the estimation table. It was unavailable to and unused by the pricing solver, but it directly contains the demand error and therefore violates exclusion. Its estimates are economically nonsensical here (\(\alpha=-15.5517\), \(\beta_x=-5.5567\)); this is an implementation check and counterexample, not a general statement about invalid-IV bias.

## Payments, resources, and welfare

All amounts are totals over the same 40-market finite population. Consumer payment, government subsidy payment, producer receipts, real resource cost, profit, consumer surplus, and welfare are separately recorded. With the logit Euler-constant normalization set to zero,

\[
W=CS+\Pi-\text{fiscal payment}=CS+\text{consumer payment}-\text{resource cost}.
\]

At baseline, consumer payments are 2543.5532, real resource cost is 1772.1500, producer profit is 771.4031, and welfare is 1579.3701. Under a 0.12 per-unit subsidy, consumer payments are 2809.0335, fiscal payments are 166.9758, real resource cost is 2069.7059, producer profit is 906.3033, and welfare is 1696.9811. The payment/resource identities pass to floating-point precision. These are model-conditional finite-population accounting results, not empirical policy estimates.

## Failure and independent verification evidence

`equilibrium_starts.jsonl` preserves all 240 start records (2 policies × 40 markets × 3 starts), including initial and terminal vectors, status, message, evaluations, objective, raw and scaled residuals, and active bounds. Three isolated forced-failure executions cover simulation count mismatch, equilibrium failure, and rank-deficient estimation. Each writes its diagnostic first, rejects the whole replication, and exits with code 2; the compact consolidated record is `process_failure_tests.json`.

The independent verifier does not import the production solver or trust stored summaries. From saved CSV primitives it separately recomputes logit shares, both equilibrium equations, the just-identified IV system, and both welfare identities. All checks pass; its report is `results/verification/verification.json`.

## Reproduction

Use `C:\Users\ENAN\miniforge3\envs\codex\python.exe`:

```powershell
& 'C:\Users\ENAN\miniforge3\envs\codex\python.exe' .\run_simulation.py --output .\results\success
& 'C:\Users\ENAN\miniforge3\envs\codex\python.exe' .\verify_independent.py --run .\results\success --output .\results\verification
& 'C:\Users\ENAN\miniforge3\envs\codex\python.exe' .\test_process_failures.py --root .
```

Exact source-instruction provenance and claim limits are in `provenance.md`.
