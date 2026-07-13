# Bounded differentiated-products structural simulation

Run with the `codex` environment. The success run generates a finite-population logit Bertrand dataset, estimates demand with valid and deliberately invalid instruments, solves a per-unit subsidy counterfactual, and separates consumer payments, fiscal payments, real resource costs, profit, consumer surplus, and welfare.

The three forced-failure modes are process tests: each must write `failure_diagnostic.json` and exit nonzero. No partial replication is admitted to estimation.
