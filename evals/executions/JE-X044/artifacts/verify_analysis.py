import json
from pathlib import Path

import numpy as np
import pandas as pd

from run_analysis import TRUE, solve, trans


OUT = Path(r"C:\Users\ENAN\AppData\Local\Temp\junzi-economist-struct-x044")
pk, pr = trans(TRUE["p"])
v, q, residual, iterations = solve(TRUE["theta"], TRUE["RC"], TRUE["p"], TRUE["beta"])
recovery = pd.read_csv(OUT / "recovery_runs.csv")
sample = pd.read_csv(OUT / "sample_beta_profile.csv")
population = pd.read_csv(OUT / "population_beta_profile.csv")
counter = json.loads((OUT / "counterfactual.json").read_text(encoding="utf-8"))

checks = {
    "keep_transition_rows_sum_to_one": bool(np.allclose(pk.sum(axis=1), 1)),
    "replace_transition_rows_sum_to_one": bool(np.allclose(pr.sum(axis=1), 1)),
    "choice_probabilities_in_unit_interval": bool(np.all((q > 0) & (q < 1))),
    "truth_bellman_residual": residual,
    "truth_bellman_iterations": iterations,
    "ten_recovery_runs_present": bool(len(recovery) == 10),
    "all_best_nfxp_runs_successful": bool(recovery.nfxp_success.all()),
    "max_saved_bellman_residual": float(recovery.bellman_residual.max()),
    "sample_profile_has_50_points": bool(len(sample) == 50),
    "population_profile_has_50_points": bool(len(population) == 50),
    "population_grid_min_beta": float(population.loc[population.population_KL_per_choice.idxmin(), "beta"]),
    "sample_grid_min_beta": float(sample.loc[sample.nll.idxmin(), "beta"]),
    "subsidy_raises_replacement": bool(counter["effects"]["replacement_rate"] > 0),
    "subsidy_accounting_keeps_private_and_resource_objects_separate": bool(
        "private_inclusive_value_uniform_initial" in counter["effects"]
        and "resource_cost_per_period" in counter["effects"]
        and "fiscal_outlay_per_period" in counter["effects"]
    ),
}
assert all(v for k, v in checks.items() if isinstance(v, bool)), checks
assert checks["truth_bellman_residual"] < 1e-10
assert checks["max_saved_bellman_residual"] < 1e-10
(OUT / "verification_output.json").write_text(json.dumps(checks, indent=2), encoding="utf-8")
print(json.dumps(checks, indent=2))
