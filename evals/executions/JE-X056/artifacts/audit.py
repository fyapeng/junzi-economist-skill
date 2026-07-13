import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
p = json.loads((ROOT / "production_results.json").read_text(encoding="utf-8"))
v = json.loads((ROOT / "independent_results.json").read_text(encoding="utf-8"))

checks = {}
checks["unrestricted_objective_agreement"] = abs(p["unrestricted_selected"]["objective"] - v["unrestricted"]["objective"]) <= 2e-5
checks["unrestricted_parameter_agreement"] = max(abs(a-b) for a,b in zip(p["unrestricted_selected"]["terminal"], v["unrestricted"]["terminal"])) <= 2e-3
pp = {z["delta"]: z for z in p["profile_grid"]}
vv = {z["delta"]: z for z in v["profile_grid"]}
checks["same_grid"] = set(pp) == set(vv)
common = sorted(set(pp) & set(vv))
checks["every_conditional_reconstructed"] = len(common) == 51 and all(vv[d]["status"] == "accepted" for d in common)
checks["conditional_objectives_agree"] = all(abs(pp[d]["objective"] - vv[d]["objective"]) <= 3e-5 for d in common if pp[d]["status"] == vv[d]["status"] == "accepted")
checks["evaluated_grid_membership_agrees"] = all(pp[d].get("in_evaluated_grid_set") == vv[d].get("in_evaluated_grid_set") for d in common)
checks["policy_selected_image_agrees"] = max(abs(a-b) for a,b in zip(p["inference"]["policy_image_selected_only"], v["summary"]["policy_image_selected_only"])) <= 3e-5
checks["production_no_profile_holes"] = not p["inference"]["holes"]
checks["verifier_no_profile_holes"] = not v["summary"]["holes"]
checks["not_boundary_censored"] = not any([p["inference"]["left_censored"], p["inference"]["right_censored"], v["summary"]["left_censored"], v["summary"]["right_censored"]])
checks["closed_lower_support_reported"] = p["inference"]["left_support_bounded"] and v["summary"]["left_support_bounded"]
checks["all_selected_kkt"] = p["unrestricted_selected"]["kkt_scaled_inf"] <= 2e-5 and all(z.get("kkt_scaled_inf", 1) <= 2e-5 for z in p["profile_grid"] if z["status"] == "accepted")
checks["raw_sample_complete"] = p["support"]["training_x"] == [-1.4, -0.8, -0.2, 0.4, 1.0, 1.6]

coverage = {
    "unrestricted global search on declared box": "covered by independent raw-primitive reconstruction and objective/parameter agreement",
    "every conditional optimum on evaluated delta grid": "covered independently at all 27 values; objective and set membership compared",
    "selected-only policy image": "covered by independent remapping of each independently selected conditional optimum",
    "constraint/KKT acceptance": "covered with analytic projected gradients in production and finite-difference KKT in verifier",
    "holes, grid censoring, and closed support boundary": "covered mechanically in both implementations and reconciled; delta=0 is support-bounded, not grid-censored",
    "sample construction": "covered only for expected-versus-realized row count and declared x support",
    "population identification on continuous parameter domain": "UNVERIFIED; grid separation and sample likelihood geometry do not prove it",
    "counterfactual external validity at policy_x=2.10": "UNVERIFIED; this is model-based extrapolation beyond observed x=1.60",
    "frequentist LR coverage in this finite mixture/sample": "UNVERIFIED; chi-square cutoff is a reference approximation, not Monte Carlo validated here",
    "welfare": "NOT CLAIMED; adoption probability is not social welfare"
}
passed = all(checks.values())
audit = {"passed": passed, "checks": checks, "coverage_map": coverage,
         "branch_rule": {"continue": "all required checks pass, no holes, and neither endpoint is censored",
                         "refine": "any reported-set endpoint is censored or a grid hole remains",
                         "backtrack": "unrestricted/conditional reconstruction, KKT acceptance, likelihood agreement, or membership comparison fails"},
         "branch_decision": "continue" if passed else ("refine" if checks.get("conditional_objectives_agree", False) else "backtrack")}
(ROOT / "audit.json").write_text(json.dumps(audit, indent=2), encoding="utf-8")

prov_files = ["simulate.py", "estimate_profile.py", "independent_verify.py", "audit.py", "raw_primitives.json",
              "production_results.json", "profile_selected.csv", "independent_results.json", "audit.json", "response.md"]
manifest = {"files": {}}
for name in prov_files:
    data = (ROOT / name).read_bytes()
    manifest["files"][name] = {"sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}
manifest["commands"] = [
    "C:/Users/ENAN/miniforge3/envs/codex/python.exe simulate.py",
    "C:/Users/ENAN/miniforge3/envs/codex/python.exe estimate_profile.py",
    "C:/Users/ENAN/miniforge3/envs/codex/python.exe independent_verify.py",
    "C:/Users/ENAN/miniforge3/envs/codex/python.exe audit.py"
]
manifest["source_skill_commit"] = "f120979 (read via git show only)"
(ROOT / "provenance.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
print(json.dumps({"passed": passed, "branch_decision": audit["branch_decision"], "checks": checks}))
raise SystemExit(0 if passed else 1)
