"""Diamond OLG debt-transfer experiment; Python 3 + standard library only."""
from __future__ import annotations

import csv
import math
from pathlib import Path

ALPHA = 0.33
BETA = 1.0
N_GROWTH = 0.01
HORIZON = 80
SHARES = (0.02, 0.10, 0.30)


def wage(k: float) -> float:
    return (1.0 - ALPHA) * k**ALPHA


def gross_return(k: float) -> float:
    return ALPHA * k ** (ALPHA - 1.0)


def utility(cy: float, co: float) -> float:
    if cy <= 0.0 or co <= 0.0:
        return float("-inf")
    return math.log(cy) + BETA * math.log(co)


def steady_state() -> float:
    saving_share = BETA / (1.0 + BETA)
    return (saving_share * (1.0 - ALPHA) / (1.0 + N_GROWTH)) ** (1.0 / (1.0 - ALPHA))


def simulate(share: float) -> tuple[list[dict[str, float | int | str]], dict[str, float | str]]:
    kstar = steady_state()
    y0 = kstar**ALPHA
    d = share * y0  # aggregate debt because N_0=1; also debt per initial young
    s0 = BETA / (1.0 + BETA) * wage(kstar)
    k1_numerator = s0 - d
    if k1_numerator <= 0.0:
        return [], {"share": share, "status": "infeasible-at-issue", "s0_minus_d": k1_numerator}
    k = [kstar, k1_numerator / (1.0 + N_GROWTH)]
    r1 = gross_return(k[1])
    tau1 = r1 * d / (1.0 + N_GROWTH)
    disposable1 = wage(k[1]) - tau1
    if disposable1 <= 0.0:
        return [], {"share": share, "status": "infeasible-at-repayment", "w1_minus_tau1": disposable1}
    k.append((BETA / (1.0 + BETA) * disposable1) / (1.0 + N_GROWTH))
    for _t in range(2, HORIZON):
        nxt = (BETA / (1.0 + BETA) * wage(k[-1])) / (1.0 + N_GROWTH)
        if not math.isfinite(nxt) or nxt <= 0.0:
            raise RuntimeError("post-debt capital transition left the positive domain")
        k.append(nxt)

    rows: list[dict[str, float | int | str]] = []
    baseline_s = s0
    baseline_u = utility(wage(kstar) - baseline_s, gross_return(kstar) * baseline_s)
    for t in range(0, HORIZON):
        kt = k[t]
        wt = wage(kt)
        rt = gross_return(kt)
        tax = tau1 if t == 1 else 0.0
        sav = BETA / (1.0 + BETA) * (wt - tax)
        cy = wt - tax - sav
        co_next = gross_return(k[t + 1]) * sav if t + 1 < len(k) else float("nan")
        du = utility(cy, co_next) - baseline_u if math.isfinite(co_next) else float("nan")
        rows.append({"share": share, "cohort": t, "k_t": kt, "w_t": wt, "R_t": rt,
                     "tax_young": tax, "saving": sav, "c_y": cy,
                     "c_o_next": co_next, "welfare_change": du})

    # Initial old: pre-transfer consumption per initial-old person; N_-1=1/(1+n).
    co_old_base = (1.0 + N_GROWTH) * gross_return(kstar) * kstar
    co_old_policy = co_old_base + (1.0 + N_GROWTH) * d
    old_gain = math.log(co_old_policy) - math.log(co_old_base)

    # Exact accounting checks for t=0 and t=1 in aggregates.
    cy0 = rows[0]["c_y"]
    co0_aggregate = gross_return(kstar) * kstar + d
    resource0 = y0 - float(cy0) - co0_aggregate - (1.0 + N_GROWTH) * k[1]
    y1_aggregate = (1.0 + N_GROWTH) * k[1] ** ALPHA
    cy1_aggregate = (1.0 + N_GROWTH) * float(rows[1]["c_y"])
    co1_aggregate = gross_return(k[1]) * s0
    investment2 = (1.0 + N_GROWTH) ** 2 * k[2]
    resource1 = y1_aggregate - cy1_aggregate - co1_aggregate - investment2
    gov1 = (1.0 + N_GROWTH) * tau1 - r1 * d
    asset0 = s0 - ((1.0 + N_GROWTH) * k[1] + d)
    max_tail_gap = max(abs(x - kstar) for x in k[-10:])
    summary: dict[str, float | str] = {
        "share": share, "status": "feasible", "k_star": kstar, "y0": y0, "debt_d": d,
        "saving0": s0, "k1": k[1], "k2": k[2], "R1": r1, "tau1": tau1,
        "disposable_wage1": disposable1, "initial_old_log_gain": old_gain,
        "cohort0_welfare_change": float(rows[0]["welfare_change"]),
        "cohort1_welfare_change": float(rows[1]["welfare_change"]),
        "minimum_cohort_welfare_change": min(float(x["welfare_change"]) for x in rows[:-1]),
        "maximum_cohort_welfare_change": max(float(x["welfare_change"]) for x in rows[:-1]),
        "resource_residual_t0": resource0, "resource_residual_t1": resource1,
        "government_residual_t1": gov1, "asset_residual_t0": asset0,
        "tail_max_k_gap": max_tail_gap,
    }
    return rows, summary


def main() -> None:
    out = Path(__file__).resolve().parent
    all_rows: list[dict[str, float | int | str]] = []
    summaries = []
    for share in SHARES:
        rows, summary = simulate(share)
        summaries.append(summary)
        all_rows.extend(rows)
    summary_fields = sorted({key for row in summaries for key in row})
    with (out / "simulation_summary.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=summary_fields)
        writer.writeheader()
        writer.writerows(summaries)
    with (out / "cohort_paths.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(all_rows[0].keys()))
        writer.writeheader()
        writer.writerows(all_rows)

    tol = 1e-11
    feasible = [summary for summary in summaries if summary["status"] == "feasible"]
    assert [summary["status"] for summary in summaries] == ["feasible", "feasible", "infeasible-at-repayment"]
    for summary in feasible:
        assert abs(float(summary["asset_residual_t0"])) < tol
        assert abs(float(summary["government_residual_t1"])) < tol
        assert abs(float(summary["resource_residual_t0"])) < tol
        assert abs(float(summary["resource_residual_t1"])) < tol
        assert float(summary["k1"]) < float(summary["k_star"])
        assert float(summary["tail_max_k_gap"]) < 1e-10
    infeasible_share = (BETA / (1.0 + BETA)) * (1.0 - ALPHA) + 1e-6
    _, bad = simulate(infeasible_share)
    assert bad["status"] == "infeasible-at-issue"
    print("All accounting, feasibility, direction, and convergence checks passed.")
    for s in summaries:
        print(s)
    print("Deliberate infeasibility test:", bad)


if __name__ == "__main__":
    main()
