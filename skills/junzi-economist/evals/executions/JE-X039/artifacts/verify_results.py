import json
from pathlib import Path


root = Path(__file__).resolve().parent
data = json.loads((root / "results.json").read_text(encoding="utf-8"))
runs = {x["config"]["name"]: x for x in data["runs"]}
assert set(runs) == {"baseline", "finer_wider_grid", "smaller_grid",
                     "relaxed_borrowing", "lower_persistence"}

for name, x in runs.items():
    eq, cv, op, ds = x["equilibrium"], x["convergence"], x["optimality"], x["distribution"]
    assert abs(eq["asset_market_residual"]) < 2e-8
    assert abs(eq["resource_residual_C_plus_deltaK_minus_Y"]) < 1e-8
    assert cv["distribution_invariance_residual"] < 3e-13
    assert cv["distribution_mass_error"] < 1e-12
    assert cv["egm_policy_sup_diff"] < 3e-9
    assert cv["value_policy_sup_diff"] < 3e-10
    assert cv["continuous_bellman_residual_sup"] < 3e-5
    assert op["nonbinding_euler_relative_max"] < 1e-4
    assert op["borrowing_constraint_kkt_violation_max"] < 1e-10
    assert abs(sum(ds["efficiency_state_mass"]) - 1.0) < 1e-12
    assert abs(x["prices_identity"]["mean_efficiency"] - 1.0) < 1e-12

b = runs["baseline"]
fine = runs["finer_wider_grid"]
assert b["distribution"]["top_grid_mass"] < 1e-10
assert fine["distribution"]["top_grid_mass"] < 1e-10
assert abs(b["equilibrium"]["K"] - fine["equilibrium"]["K"]) / b["equilibrium"]["K"] < 2e-4
assert b["equilibrium"]["K"] > data["representative_agent"]["K"]
assert b["equilibrium"]["r"] < data["representative_agent"]["r"]
assert runs["relaxed_borrowing"]["equilibrium"]["K"] < b["equilibrium"]["K"]
assert runs["lower_persistence"]["equilibrium"]["K"] < b["equilibrium"]["K"]

print("ALL RESULT CHECKS PASSED")
print("market clearing, invariant distribution, resources, Bellman, Euler/KKT: PASS")
print("fine/wide grid stability and top-grid checks: PASS")
print("representative-agent and sensitivity comparisons: PASS")
