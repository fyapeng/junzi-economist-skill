from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parent
REQUIRED = ["production.py", "model_data.csv", "transition_estimates.csv", "choice_cells.csv",
            "nfxp_starts.csv", "ccp_starts.csv", "local_rank.json", "restricted_search.csv",
            "policy_results.csv", "summary.json", "response.md", "production_stdout.txt"]


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def main():
    started = datetime.now(timezone.utc)
    checks = {}
    prov = json.loads((ROOT / "provenance.json").read_text(encoding="utf-8"))
    summary = json.loads((ROOT / "summary.json").read_text(encoding="utf-8"))
    response = (ROOT / "response.md").read_text(encoding="utf-8")
    data = pd.read_csv(ROOT / "model_data.csv")
    trans = pd.read_csv(ROOT / "transition_estimates.csv")
    ns = pd.read_csv(ROOT / "nfxp_starts.csv")
    cs = pd.read_csv(ROOT / "ccp_starts.csv")
    rs = pd.read_csv(ROOT / "restricted_search.csv")
    policy = pd.read_csv(ROOT / "policy_results.csv")

    checks["production_precedes_verifier"] = datetime.fromisoformat(prov["production_completed_at_utc"]) <= started
    checks["all_hashes_match_provenance"] = all(sha256(ROOT / n) == prov["artifacts"][n]["sha256"] for n in REQUIRED)
    checks["all_mtimes_match_provenance"] = all(
        datetime.fromtimestamp((ROOT / n).stat().st_mtime, timezone.utc).isoformat() == prov["artifacts"][n]["mtime_utc"]
        for n in REQUIRED)
    checks["production_files_older_than_verifier"] = all(
        datetime.fromtimestamp((ROOT / n).stat().st_mtime, timezone.utc) <= started for n in REQUIRED)

    # Independently reconstruct transition counts and probabilities from row-level observations.
    rebuilt = data.groupby(["action", "state", "next_state"]).size().rename("count").reset_index()
    rebuilt["cell_total"] = rebuilt.groupby(["action", "state"])["count"].transform("sum")
    rebuilt["probability"] = rebuilt["count"] / rebuilt["cell_total"]
    merged = trans.merge(rebuilt, on=["action", "state", "next_state"], suffixes=("_saved", "_rebuilt"), how="outer")
    checks["transition_counts_recomputed"] = bool((merged.count_saved == merged.count_rebuilt).all())
    checks["transition_probabilities_recomputed"] = bool(np.allclose(merged.probability_saved, merged.probability_rebuilt, atol=1e-15, rtol=0))

    def start_checks(df, key):
        selected = df[df.selected]
        eligible = df[df.success]
        checks[f"{key}_one_selected"] = len(selected) == 1
        checks[f"{key}_selected_is_best_success"] = len(selected) == 1 and abs(float(selected.objective.iloc[0]) - float(eligible.objective.min())) < 1e-10
        checks[f"{key}_all_starts_retained"] = len(df) == 8 and sorted(df.start_id.tolist()) == list(range(8))
        checks[f"{key}_summary_consistent"] = (summary[key]["starts"] == len(df) and
                                               summary[key]["successful_starts"] == int(df.success.sum()) and
                                               summary[key]["selected_start_id"] == int(selected.start_id.iloc[0]))
        for n in ["state_harm", "maintenance_cost", "subsidy_loading"]:
            checks[f"{key}_{n}_consistent"] = abs(summary[key]["theta"][n] - float(selected[f"terminal_{n}"].iloc[0])) < 1e-12
    start_checks(ns, "nfxp")
    start_checks(cs, "ccp_wmd")

    delta = rs.restriction_delta.to_numpy()
    tol = rs.acceptance_tolerance.to_numpy()
    recomputed_slack = rs.linf_distance.to_numpy() - delta
    recomputed_accept = recomputed_slack >= -tol
    slab_accept = rs.slab_membership.ne("none").to_numpy()
    checks["restricted_all_rows_present"] = len(rs) == 17 ** 3 and rs.row_id.tolist() == list(range(17 ** 3))
    checks["restricted_every_slack_recomputed"] = bool(np.allclose(rs.restriction_slack, recomputed_slack, atol=2e-15, rtol=0))
    checks["restricted_every_row_acceptance_recomputed"] = bool(np.array_equal(rs.restricted_accept.to_numpy(), recomputed_accept))
    checks["restricted_every_slab_acceptance_recomputed"] = bool(np.array_equal(slab_accept, recomputed_accept))
    checks["restricted_boundaries_included"] = int(rs.is_domain_boundary.sum()) == 17 ** 3 - 15 ** 3
    accepted = rs[rs.restricted_accept]
    best = accepted.sort_values(["objective_ccp_sse", "row_id"]).iloc[0]
    checks["restricted_summary_counts_consistent"] = (summary["restricted_search"]["total_rows"] == len(rs) and
                                                       summary["restricted_search"]["accepted_rows"] == int(rs.restricted_accept.sum()) and
                                                       summary["restricted_search"]["boundary_rows"] == int(rs.is_domain_boundary.sum()))
    checks["restricted_summary_best_consistent"] = (summary["restricted_search"]["best_row_id"] == int(best.row_id) and
                                                     abs(summary["restricted_search"]["best_objective_ccp_sse"] - float(best.objective_ccp_sse)) < 1e-14)

    acct1 = policy.social_welfare - (policy.private_payoff - policy.transfer_outlay)
    acct2 = policy.social_welfare + policy.state_harm + policy.resource_cost
    checks["policy_accounting_private_transfer"] = bool(np.max(np.abs(acct1)) < 1e-12)
    checks["policy_accounting_resources"] = bool(np.max(np.abs(acct2)) < 1e-12)
    checks["policy_support_labels"] = policy.support_status.tolist() == ["observed", "model_interpolation", "observed"]
    checks["policy_summary_consistent"] = (summary["policy"]["rows"] == len(policy) and
                                           summary["policy"]["observed_regime_rows"] == int((policy.support_status == "observed").sum()) and
                                           summary["policy"]["interpolation_rows"] == int((policy.support_status == "model_interpolation").sum()))

    checks["sample_counts_recomputed"] = summary["sample"]["rows"] == len(data) and summary["sample"]["agents"] == data.agent_id.nunique()
    checks["sample_rates_recomputed"] = abs(summary["sample"]["action_rate"] - data.action.mean()) < 1e-15
    checks["response_contains_mechanical_counts"] = all(str(x) in response for x in [len(data), len(rs), int(rs.restricted_accept.sum()), int(rs.is_domain_boundary.sum())])
    checks["response_contains_estimator_start_counts"] = f"{int(ns.success.sum())}/{len(ns)}" in response and f"{int(cs.success.sum())}/{len(cs)}" in response
    checks["response_limits_claim"] = "local only" in response and "not a global population-identification claim" in response and "evaluated lattice only" in response

    checks = {k: bool(v) for k, v in checks.items()}
    passed = all(checks.values())
    report = {"verifier_started_at_utc": started.isoformat(), "verifier_completed_at_utc": datetime.now(timezone.utc).isoformat(),
              "fresh_against_production_hashes": checks["all_hashes_match_provenance"] and checks["production_files_older_than_verifier"],
              "checks": checks, "passed": passed,
              "production_hashes_verified": {n: sha256(ROOT / n) for n in REQUIRED}}
    (ROOT / "verification_report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    line = f"verification_passed={str(passed).lower()} checks={sum(checks.values())}/{len(checks)} production_hashes={len(REQUIRED)}\n"
    (ROOT / "verification_stdout.txt").write_text(line, encoding="utf-8")
    print(line, end="")
    if not passed:
        for k, v in checks.items():
            if not v:
                print(f"FAILED {k}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
