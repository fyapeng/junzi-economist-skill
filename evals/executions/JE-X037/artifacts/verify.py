from __future__ import annotations

from fractions import Fraction as F
from itertools import product


def primitives(p0: F, p1: F, k: F, U: F):
    assert F(0) <= p0 < p1 <= F(1) and k > 0 and U >= 0
    delta = p1 - p0
    a = k / delta
    L = k * p0 / delta
    A = U + k
    H = max(A, p1 * a)
    return a, L, A, H


def wages(C: F, p: F, d: F):
    return C - p * d, C + (1 - p) * d


def eu(t0: F, t1: F, p: F, cost: F = F(0)):
    return (1 - p) * t0 + p * t1 - cost


def high_exists(strict_effort: bool, accepts_indifference: bool, U: F, L: F):
    if accepts_indifference:
        return (not strict_effort) or U > L
    return (not strict_effort) and U < L


def low_exists(accepts_indifference: bool):
    return accepts_indifference


def principal_modes(P0: F, P1: F, i0: bool, i1: bool):
    M = max(F(0), P0, P1)
    modes = set()
    if M == 0:
        modes.add("D")
    if P0 == M and i0:
        modes.add("L")
    if P1 == M and i1:
        modes.add("H")
    return M, modes


def test_weak_correspondences():
    cases = [
        (F(0), F(1, 2), F(1), F(0)),
        (F(0), F(3, 4), F(2), F(3, 5)),
        (F(1, 5), F(3, 5), F(1), F(1, 10)),
        (F(1, 5), F(3, 5), F(1), F(1, 2)),
        (F(1, 5), F(3, 5), F(1), F(4, 5)),
    ]
    checked = 0
    for p0, p1, k, U in cases:
        a, L, A, H = primitives(p0, p1, k, U)

        # Weak high/accept: endpoints and midpoint of the full interval.
        for d in {a, H / p1, (a + H / p1) / 2}:
            t0, t1 = wages(H, p1, d)
            assert t0 >= 0 and t1 >= 0
            assert d >= a
            assert eu(t0, t1, p1, k) >= U
            assert eu(t0, t1, p1, k) >= eu(t0, t1, p0)
            assert (1 - p1) * t0 + p1 * t1 == H
            checked += 1

        # Weak low/accept: boundary formulas, including p0=0.
        if p0 == 0:
            ds = {-U, a, (-U + a) / 2}
        else:
            lo = -U / (1 - p0)
            hi = min(U / p0, a)
            ds = {lo, hi, (lo + hi) / 2}
        for d in ds:
            t0, t1 = wages(U, p0, d)
            assert t0 >= 0 and t1 >= 0
            assert d <= a
            assert eu(t0, t1, p0) == U
            assert eu(t0, t1, p0) >= eu(t0, t1, p1, k)
            checked += 1

        # The algebraic lower bounds: any feasible high contract costs at least H.
        # Deterministic rational grid, not an optimizer assumption.
        grid = [F(i, 10) for i in range(0, 81)]
        for t0, t1 in product(grid, repeat=2):
            d = t1 - t0
            if d >= a and eu(t0, t1, p1, k) >= U:
                assert (1 - p1) * t0 + p1 * t1 >= H
            if d <= a and eu(t0, t1, p0) >= U:
                assert (1 - p0) * t0 + p0 * t1 >= U
    return checked


def test_strictness_and_existence():
    # U<L, U=L, U>L, including p0=0 equality and p0=0 strict-above.
    cases = [
        (F(1, 5), F(3, 5), F(1), F(1, 10), "below"),
        (F(1, 5), F(3, 5), F(1), F(1, 2), "equal"),
        (F(1, 5), F(3, 5), F(1), F(4, 5), "above"),
        (F(0), F(1, 2), F(1), F(0), "equal"),
        (F(0), F(1, 2), F(1), F(1, 3), "above"),
    ]
    checked = 0
    for p0, p1, k, U, relation in cases:
        a, L, A, H = primitives(p0, p1, k, U)
        assert {"below": U < L, "equal": U == L, "above": U > L}[relation]
        expected = {
            (False, True): True,
            (True, True): U > L,
            (False, False): U < L,
            (True, False): False,
        }
        for key, value in expected.items():
            assert high_exists(*key, U, L) is value
            checked += 1

        # Strict-effort/accept witness when it exists; otherwise an approaching
        # sequence is feasible but its endpoint violates strict IC.
        if U > L:
            d = (a + A / p1) / 2
            t0, t1 = wages(A, p1, d)
            assert d > a and eu(t0, t1, p1, k) == U
        else:
            for n in (2, 10, 1000):
                d = a + F(1, n)
                C = max(A, p1 * d)
                t0, t1 = wages(C, p1, d)
                assert d > a and eu(t0, t1, p1, k) >= U
                assert C > H
            t0, t1 = wages(H, p1, a)
            assert t1 - t0 == a  # endpoint fails strict IC

        # Weak-effort/reject witness iff LL rent is strictly positive.
        if U < L:
            t0, t1 = F(0), a
            assert eu(t0, t1, p1, k) == L > U
        else:
            for n in (2, 10, 1000):
                C = H + F(1, n)
                d = a
                t0, t1 = wages(C, p1, d)
                assert eu(t0, t1, p1, k) > U
                assert C > H

        # With both constraints strict, feasible contracts approach H, but H
        # itself always violates at least one open constraint.
        for n in (2, 10, 1000):
            d = a + F(1, n)
            C = max(A, p1 * d) + F(1, n)
            t0, t1 = wages(C, p1, d)
            assert d > a
            assert eu(t0, t1, p1, k) > U
            assert C > H
        if H == A:
            assert H - k == U  # strict PC fails at the infimum
        if H == p1 * a:
            endpoint_t0, endpoint_t1 = wages(H, p1, a)
            assert endpoint_t1 - endpoint_t0 == a  # strict IC fails

        # Strict participation always prevents low-cost attainment but admits
        # a decreasing feasible sequence under both weak and strict low IC.
        for n in (2, 10, 1000):
            C = U + F(1, n)
            t0 = t1 = C
            assert eu(t0, t1, p0) > U
            assert (t1 - t0) < a
        assert low_exists(False) is False
    return checked


def test_principal_nonattainment_and_ties():
    # Strict/accept, U<L: high uniquely tops but is unattained -> empty.
    p0, p1, k, U, R = F(1, 5), F(3, 5), F(1), F(1, 10), F(5)
    a, L, A, H = primitives(p0, p1, k, U)
    P0, P1 = p0 * R - U, p1 * R - H
    M, modes = principal_modes(P0, P1, True, high_exists(True, True, U, L))
    assert M == F(3, 2) and modes == set()

    # Weak/reject, U<L: low uniquely tops but is unattained -> empty.
    R = F(3)
    P0, P1 = p0 * R - U, p1 * R - H
    M, modes = principal_modes(P0, P1, False, high_exists(False, False, U, L))
    assert (P0, P1) == (F(1, 2), F(3, 10)) and modes == set()

    # A tied unattained high supremum does not kill an attained low maximum.
    # Choose R from P0=P1: Delta*R=H-U.
    R = (H - U) / (p1 - p0)
    P0, P1 = p0 * R - U, p1 * R - H
    assert P0 == P1 > 0
    M, modes = principal_modes(P0, P1, True, False)
    assert modes == {"L"}

    # If all active suprema are nonpositive, shutdown exists even when neither
    # active cost infimum is attained.
    M, modes = principal_modes(F(-1), F(0), False, False)
    assert M == 0 and modes == {"D"}
    return 4


def test_wedge_and_social_correspondence():
    checked = 0
    for p0, p1, k, U in [
        (F(0), F(1, 2), F(1), F(0)),
        (F(1, 5), F(3, 5), F(1), F(1, 10)),
        (F(1, 5), F(3, 5), F(1), F(4, 5)),
    ]:
        a, L, A, H = primitives(p0, p1, k, U)
        assert H - (U + k) == max(F(0), L - U)
        assert (H - U) == k + max(F(0), L - U)
        checked += 1

    # Numerical inefficient-choice example.
    p0, p1, k, U, R = F(1, 5), F(3, 5), F(1), F(1, 10), F(3)
    a, L, A, H = primitives(p0, p1, k, U)
    S0, S1 = p0 * R - U, p1 * R - k - U
    P0, P1 = p0 * R - U, p1 * R - H
    assert (S0, S1) == (F(1, 2), F(7, 10))
    assert (P0, P1) == (F(1, 2), F(3, 10))
    return checked + 1


if __name__ == "__main__":
    counts = {
        "weak_contract_checks": test_weak_correspondences(),
        "strict_existence_cells": test_strictness_and_existence(),
        "principal_existence_cases": test_principal_nonattainment_and_ties(),
        "wedge_social_checks": test_wedge_and_social_correspondence(),
    }
    print("ALL ASSERTIONS PASSED")
    for key, value in counts.items():
        print(f"{key}: {value}")
    print("Covered p0=0; U<L, U=L, U>L; weak/strict IC; weak/strict PC; ties.")
