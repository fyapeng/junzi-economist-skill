from __future__ import annotations

import math

import numpy as np
from scipy.optimize import brentq
from scipy.special import lambertw


TOL = 2e-10


def S(pi: float, A: float, alpha: float) -> float:
    return A * pi * math.exp(-alpha * pi)


def Sp(pi: float, A: float, alpha: float) -> float:
    return A * math.exp(-alpha * pi) * (1.0 - alpha * pi)


def Spp(pi: float, A: float, alpha: float) -> float:
    return A * math.exp(-alpha * pi) * (alpha * alpha * pi - 2.0 * alpha)


def analytic_roots(d: float, A: float, alpha: float) -> list[float]:
    peak = A / (alpha * math.e)
    if d < -TOL:
        raise ValueError("d must be nonnegative")
    if abs(d) <= TOL:
        return [0.0]
    if d > peak + TOL:
        return []
    if abs(d - peak) <= TOL:
        return [1.0 / alpha]
    z = -alpha * d / A
    low = -float(lambertw(z, 0).real) / alpha
    high = -float(lambertw(z, -1).real) / alpha
    return [low, high]


def bracket_roots(d: float, A: float, alpha: float) -> list[float]:
    """Independent monotone-interval root check, not using Lambert W."""
    peak_pi = 1.0 / alpha
    peak = S(peak_pi, A, alpha)
    if d == 0.0:
        return [0.0]
    if d > peak * (1.0 + 1e-12):
        return []
    if abs(d - peak) <= 1e-12 * max(1.0, peak):
        return [peak_pi]
    low = brentq(lambda x: S(x, A, alpha) - d, 0.0, peak_pi)
    upper = 2.0 * peak_pi
    while S(upper, A, alpha) > d:
        upper *= 2.0
    high = brentq(lambda x: S(x, A, alpha) - d, peak_pi, upper)
    return [low, high]


def check_peak_and_counts() -> int:
    count = 0
    for A in (0.7, 1.0, 3.5, 10.0):
        for alpha in (0.2, 1.0, 2.0, 5.0):
            ppi = 1.0 / alpha
            pval = A / (alpha * math.e)
            assert abs(S(ppi, A, alpha) - pval) < TOL
            assert abs(Sp(ppi, A, alpha)) < TOL
            assert Spp(ppi, A, alpha) < 0.0
            # Dense deterministic scan: the analytical peak dominates all nodes.
            grid = np.linspace(0.0, 8.0 / alpha, 4001)
            assert max(S(float(x), A, alpha) for x in grid) <= pval + TOL

            for ratio, expected in (
                (0.0, 1), (0.001, 2), (0.1, 2), (0.5, 2),
                (0.999, 2), (1.0, 1), (1.001, 0), (2.0, 0),
            ):
                d = ratio * pval
                ar = analytic_roots(d, A, alpha)
                br = bracket_roots(d, A, alpha)
                assert len(ar) == expected == len(br)
                for x, y in zip(ar, br):
                    assert x >= 0.0
                    assert abs(S(x, A, alpha) - d) < 2e-9
                    assert abs(x - y) < 2e-8
                if expected == 2:
                    assert 0.0 < ar[0] < ppi < ar[1]
                count += 1
    return count


def check_lambert_and_comparative_counterexample() -> int:
    A, alpha = 10.0, 2.0
    pval = A / (alpha * math.e)
    # Includes points very near zero and the branch point.
    for ratio in np.linspace(0.002, 0.998, 250):
        d = float(ratio * pval)
        roots = analytic_roots(d, A, alpha)
        assert len(roots) == 2
        for pi in roots:
            assert abs(S(pi, A, alpha) - d) < 3e-10
    r1 = analytic_roots(0.5, A, alpha)
    r2 = analytic_roots(1.0, A, alpha)
    assert r1[0] < r2[0] < 1.0 / alpha < r2[1] < r1[1]
    assert all(abs(S(x, A, alpha) - d) < TOL for d, roots in ((0.5, r1), (1.0, r2)) for x in roots)
    return 250 * 2 + 2


def check_stability_signs() -> int:
    kappa = 0.7
    count = 0
    for A, alpha in ((1.0, 0.5), (3.0, 2.0), (10.0, 2.0)):
        pval = A / (alpha * math.e)
        for ratio in (0.05, 0.3, 0.8, 0.99):
            low, high = analytic_roots(ratio * pval, A, alpha)
            fprime_low = -kappa * Sp(low, A, alpha)
            fprime_high = -kappa * Sp(high, A, alpha)
            assert fprime_low < 0.0 < fprime_high
            # Reversing the law reverses both signs.
            assert -fprime_low > 0.0 > -fprime_high
            count += 1
        ppi = 1.0 / alpha
        assert abs(-kappa * Sp(ppi, A, alpha)) < TOL
        tangent_quadratic = -0.5 * kappa * Spp(ppi, A, alpha)
        assert tangent_quadratic > 0.0
        assert -kappa * Sp(0.0, A, alpha) < 0.0
    return count + 6


def check_debt_closure() -> int:
    A, alpha = 10.0, 2.0
    r, b = 0.05, 2.0

    # Fiscal-dominant constant-debt example: both roots exactly close debt flow.
    dp = 0.9
    D = dp + r * b
    roots = analytic_roots(D, A, alpha)
    assert len(roots) == 2
    for pi in roots:
        bdot = r * b + dp - S(pi, A, alpha)
        assert abs(bdot) < TOL

    # Monetary-dominant example with stabilizing fiscal feedback.
    pibar, bbar, phi = 0.1, 2.0, 0.2
    dpbar = S(pibar, A, alpha) - r * bbar
    assert abs(r * bbar + dpbar - S(pibar, A, alpha)) < TOL
    assert r - phi < 0.0
    for deviation in (-1.0, -0.25, 0.25, 1.0):
        current_b = bbar + deviation
        current_dp = dpbar - phi * deviation
        bdot = r * current_b + current_dp - S(pibar, A, alpha)
        assert abs(bdot - (r - phi) * deviation) < TOL

    # Closure failure: even peak seigniorage leaves debt growing.
    dp_bad = 1.8
    D_bad = dp_bad + r * b
    peak = A / (alpha * math.e)
    assert D_bad > peak
    assert analytic_roots(D_bad, A, alpha) == []
    assert r * b + dp_bad - peak > 0.0
    return 2 + 1 + 4 + 3


def numeric_report() -> None:
    A, alpha = 10.0, 2.0
    peak = A / (alpha * math.e)
    for d in (0.0, 0.5, 1.0, peak, 2.0):
        roots = analytic_roots(d, A, alpha)
        print(f"d={d:.9f} roots=" + ", ".join(f"{x:.9f}" for x in roots))
    print(f"peak_pi={1/alpha:.9f} peak_S={peak:.9f}")
    print(f"monetary_dp={S(0.1, A, alpha)-0.05*2:.9f}")
    print(f"bad_closure_bdot_at_peak={1.8+0.05*2-peak:.9f}")


if __name__ == "__main__":
    counts = {
        "root_regime_cases": check_peak_and_counts(),
        "lambert_residual_and_counterexample_checks": check_lambert_and_comparative_counterexample(),
        "stability_sign_checks": check_stability_signs(),
        "debt_closure_checks": check_debt_closure(),
    }
    print("ALL ASSERTIONS PASSED")
    for name, count in counts.items():
        print(f"{name}: {count}")
    numeric_report()
