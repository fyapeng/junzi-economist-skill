"""Deterministic finite regression checks for the shutdown model.

These tests support implementation and boundary checking; the global result is
proved analytically in response.md.
"""
from __future__ import annotations

import math
import platform


TOL = 1e-10


def unit_cost(A: float, alpha: float, r: float, w: float) -> float:
    return ((r / alpha) ** alpha * (w / (1 - alpha)) ** (1 - alpha)) / A


def factors(q: float, A: float, alpha: float, r: float, w: float):
    if q == 0:
        return 0.0, 0.0
    c = unit_cost(A, alpha, r, w)
    return alpha * c * q / r, (1 - alpha) * c * q / w


def objective(q: float, a: float, b: float, c: float, F: float, planner: bool):
    if q == 0:
        return 0.0
    curvature = b / 2 if planner else b
    return (a - c) * q - curvature * q * q - F


def candidates(a: float, b: float, c: float, planner: bool):
    d = a - c
    return 0.0 if d <= 0 else d / (b if planner else 2 * b)


def gross_gain(a: float, b: float, c: float, planner: bool):
    d = a - c
    if d <= 0:
        return 0.0
    return d * d / (2 * b if planner else 4 * b)


def predicted_mode(a: float, b: float, c: float, F: float, planner: bool):
    qstar = candidates(a, b, c, planner)
    if qstar == 0:
        return "shutdown", {0.0}
    H = gross_gain(a, b, c, planner)
    if math.isclose(F, H, rel_tol=0.0, abs_tol=TOL):
        return "tie", {0.0, qstar}
    if F < H:
        return "entry", {qstar}
    return "shutdown", {0.0}


def enriched_grid(a: float, b: float, c: float, planner: bool):
    qstar = candidates(a, b, c, planner)
    choke = a / b
    upper = max(1.0, 1.5 * choke, 2.0 * qstar)
    grid = [upper * i / 20000 for i in range(20001)]
    extras = [0.0, qstar, choke]
    if qstar > 0:
        extras += [qstar * (1 - 1e-7), qstar * (1 + 1e-7)]
    return sorted(set(x for x in grid + extras if x >= 0))


def check_duality():
    parameter_sets = [
        (1.0, 0.5, 1.0, 1.0),
        (2.3, 0.2, 0.7, 4.1),
        (0.8, 0.73, 3.2, 0.4),
    ]
    for A, alpha, r, w in parameter_sets:
        c = unit_cost(A, alpha, r, w)
        for q in (0.0, 0.01, 1.0, 7.3):
            K, L = factors(q, A, alpha, r, w)
            if q == 0:
                assert (K, L) == (0.0, 0.0)
                continue
            produced = A * K**alpha * L ** (1 - alpha)
            assert math.isclose(produced, q, rel_tol=2e-12)
            assert math.isclose(r * K + w * L, c * q, rel_tol=2e-12)
            # Search the entire isoquant through K=t*K*, with L implied.
            best = r * K + w * L
            for j in range(-400, 401):
                t = math.exp(j / 40)
                K_alt = K * t
                L_alt = (q / (A * K_alt**alpha)) ** (1 / (1 - alpha))
                assert r * K_alt + w * L_alt >= best - 2e-10


def check_case(name, a, b, c, F, expected_m, expected_s):
    observed = []
    for planner, expected in ((False, expected_m), (True, expected_s)):
        mode, argset = predicted_mode(a, b, c, F, planner)
        assert mode == expected, (name, planner, mode, expected)
        grid = enriched_grid(a, b, c, planner)
        vals = [(objective(q, a, b, c, F, planner), q) for q in grid]
        grid_max = max(v for v, _ in vals)
        analytic_max = max(objective(q, a, b, c, F, planner) for q in argset)
        assert math.isclose(grid_max, analytic_max, rel_tol=0.0, abs_tol=2e-10)
        for q in argset:
            assert math.isclose(objective(q, a, b, c, F, planner), grid_max,
                                rel_tol=0.0, abs_tol=2e-10)
            if q > 0:
                assert 0 < q <= a / b + TOL  # nonnegative price at every candidate
        observed.append(mode)
    return f"{name}: monopoly={observed[0]}, planner={observed[1]}"


def check_accounting(a, b, c, F, q):
    B = a * q - b * q * q / 2
    p = a - b * q
    revenue = p * q
    cs = B - revenue
    factor_payments = c * q
    op_ps = revenue - factor_payments
    profit = op_ps - F
    welfare_resources = B - factor_payments - F
    assert math.isclose(cs, b * q * q / 2, abs_tol=TOL)
    assert math.isclose(welfare_resources, cs + profit, abs_tol=TOL)
    assert math.isclose(welfare_resources, cs + op_ps - F, abs_tol=TOL)
    assert math.isclose(B, cs + revenue, abs_tol=TOL)


def main():
    check_duality()
    # c=2, b=1. Above-cost thresholds for a=6 are HM=4 and HS=8.
    cases = [
        ("below-unit-cost", 1.5, 1.0, 2.0, 0.0, "shutdown", "shutdown"),
        ("equal-unit-cost", 2.0, 1.0, 2.0, 0.0, "shutdown", "shutdown"),
        ("above-cost-below-HM", 6.0, 1.0, 2.0, 2.0, "entry", "entry"),
        ("at-HM", 6.0, 1.0, 2.0, 4.0, "tie", "entry"),
        ("strict-wedge", 6.0, 1.0, 2.0, 6.0, "shutdown", "entry"),
        ("at-HS", 6.0, 1.0, 2.0, 8.0, "shutdown", "tie"),
        ("above-HS", 6.0, 1.0, 2.0, 9.0, "shutdown", "shutdown"),
    ]
    lines = [check_case(*case) for case in cases]

    # Accounting identities at both analytic positive-output candidates.
    for F in (2.0, 4.0, 6.0, 8.0):
        check_accounting(6.0, 1.0, 2.0, F, 2.0)
        check_accounting(6.0, 1.0, 2.0, F, 4.0)

    # Explicit numerical-example assertions.
    assert predicted_mode(1.5, 1, 2, 0, False)[0] == "shutdown"
    assert predicted_mode(1.5, 1, 2, 0, True)[0] == "shutdown"
    assert predicted_mode(6, 1, 2, 6, False)[0] == "shutdown"
    assert predicted_mode(6, 1, 2, 6, True)[0] == "entry"
    assert predicted_mode(6, 1, 2, 2, False)[0] == "entry"
    assert predicted_mode(6, 1, 2, 2, True)[0] == "entry"
    assert predicted_mode(6, 1, 2, 4, False)[0] == "tie"

    print("Deterministic verification: PASS")
    print(f"Python: {platform.python_version()}")
    print("Duality/feasibility parameter sets: 3; quantities each: 4")
    print("Boundary-enriched objective grids: 14 (20,001 base points each)")
    for line in lines:
        print(line)
    print("Accounting identities: PASS (8 positive allocations)")


if __name__ == "__main__":
    main()
