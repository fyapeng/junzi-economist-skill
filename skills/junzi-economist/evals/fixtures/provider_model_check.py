#!/usr/bin/env python3
"""Deterministic algebra, boundary, and benchmark-distance checks for the provider model."""
from __future__ import annotations
import math
import random

def treatment(p: float, alpha: float, v: float, q: float, c: float) -> float:
    return (p + alpha * v) / (c + alpha * q)

def bounded_treatment(p: float, alpha: float, v: float, q: float, c: float, cap: float) -> float:
    return min(cap, max(0.0, treatment(p, alpha, v, q, c)))

def benefit(t: float, v: float, q: float) -> float:
    return v * t - 0.5 * q * t * t

def cost(t: float, c: float) -> float:
    return 0.5 * c * t * t

def welfare(p: float, alpha: float, v: float, q: float, c: float, lam: float) -> float:
    t = treatment(p, alpha, v, q, c)
    return benefit(t, v, q) - cost(t, c) - lam * p * t

def close(a: float, b: float, tol: float = 1e-6) -> None:
    assert math.isclose(a, b, rel_tol=tol, abs_tol=tol), (a, b)

def main() -> int:
    rng = random.Random(20260713)
    h = 1e-6
    for _ in range(200):
        v, q, c = (rng.uniform(0.3, 3.0) for _ in range(3))
        p, alpha, lam = rng.uniform(0.1, 2.0), rng.uniform(0.1, 2.0), rng.uniform(0.0, 0.8)
        den = c + alpha * q
        t = treatment(p, alpha, v, q, c)
        close(p + alpha * (v - q * t) - c * t, 0.0)
        numeric_dp = (treatment(p + h, alpha, v, q, c) - treatment(p - h, alpha, v, q, c)) / (2 * h)
        close(numeric_dp, 1 / den)
        numeric_da = (treatment(p, alpha + h, v, q, c) - treatment(p, alpha - h, v, q, c)) / (2 * h)
        close(numeric_da, (v * c - q * p) / den**2)
        numeric_cross = ((1 / (c + (alpha + h) * q)) - (1 / (c + (alpha - h) * q))) / (2 * h)
        close(numeric_cross, -q / den**2)
        numeric_dw = (welfare(p + h, alpha, v, q, c, lam) - welfare(p - h, alpha, v, q, c, lam)) / (2 * h)
        analytic_dw = (v - (q + c) * t - lam * p) / den - lam * t
        close(numeric_dw, analytic_dw, tol=2e-5)
        p_fb = c * v * (1 - alpha) / (q + c)
        close(treatment(p_fb, alpha, v, q, c), v / (q + c))

    close(treatment(2, 0, 1, 1, 1), 2)
    close(treatment(2, 1, 1, 1, 1), 1.5)
    close(treatment(0, 1, 1, 1, 1), 0.5)
    close(welfare(0, 1, 1, 1, 1, 0), 0.25)
    close(treatment(1, 1, 1, 1, 1), 1)
    close(welfare(1, 1, 1, 1, 1, 0), 0)

    # With an upper treatment bound, payment is weakly rather than strictly increasing.
    cap = 1.0
    bounded_low = bounded_treatment(2, 0, 1, 1, 1, cap)
    bounded_high = bounded_treatment(3, 0, 1, 1, 1, cap)
    close(bounded_low, bounded_high)

    # Starting exactly at the social optimum, any nonzero movement increases distance.
    social = 1 / 2
    at_social = bounded_treatment(0, 1, 1, 1, 1, 3)
    more_altruistic = bounded_treatment(0, 2, 1, 1, 1, 3)
    close(at_social, social)
    assert abs(more_altruistic - social) > abs(at_social - social)

    # Payment can raise treatment while moving it away from the social optimum.
    paid_more = bounded_treatment(0.4, 1, 1, 1, 1, 3)
    assert paid_more > at_social
    assert abs(paid_more - social) > abs(at_social - social)
    print("provider model checks passed: formulas, boundaries, and benchmark-distance counterexamples verified")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
