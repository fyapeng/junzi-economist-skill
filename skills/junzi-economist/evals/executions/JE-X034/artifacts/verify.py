"""Deterministic property checks for the two-effort moral-hazard solution."""
from __future__ import annotations

from itertools import product
from math import isclose

TOL = 1e-9


def analytic(p_l, p_h, k, u):
    delta = p_h - p_l
    b = k / delta
    c_h = max(u + k, p_h * b)
    return delta, b, c_h


def modes(values):
    mx = max(values.values())
    return {key for key, value in values.items() if isclose(value, mx, rel_tol=0.0, abs_tol=1e-9)}


def strict_low_spread_set(p_l, b, u):
    """Return (lower, upper, upper_closed) for least-cost strict-low contracts."""
    lower = -u / (1 - p_l)
    if p_l == 0:
        return lower, b, False
    ll_upper = u / p_l
    if ll_upper < b:
        return lower, ll_upper, True
    return lower, b, False


def strict_high_mode_status(p_l, p_h, k, u, v):
    """Global status with strict effort IC and weak participation."""
    _, b, c_h = analytic(p_l, p_h, k, u)
    sup_h = p_h * v - c_h
    alternatives = {"L": p_l * v - u, "S": 0.0}
    best_alt = max(alternatives.values())
    if u + k > p_h * b:
        vals = {"H": sup_h, **alternatives}
        return "attained", modes(vals)
    if sup_h > best_alt + 1e-9:
        return "no_maximizer", set()
    return "alternatives", modes(alternatives)


def wage_candidates(p_l, p_h, k, u):
    delta, b, c_h = analytic(p_l, p_h, k, u)
    levels = {0.0, u, b, c_h, u + k, c_h / p_h}
    # A regular grid plus all analytic wages/spreads and small boundary perturbations.
    cap = max(levels) + b + u + k + 2.0
    levels.update(i * cap / 80 for i in range(81))
    spreads = {0.0, b, c_h / p_h, -u / (1 - p_l)}
    if p_l > 0:
        spreads.add(u / p_l)
    for x in list(levels | spreads):
        if x >= 0:
            levels.add(x)
        for eps in (-1e-7, 1e-7):
            if x + eps >= 0:
                levels.add(x + eps)
    pairs = {(w0, w1) for w0 in levels for w1 in levels}
    # Explicit analytic boundaries/candidates, including negative spreads.
    for d in spreads | {b - 1e-7, b + 1e-7}:
        for c, p in ((c_h, p_h), (u, p_l)):
            w0, w1 = c - p * d, c + (1 - p) * d
            if w0 >= -TOL and w1 >= -TOL:
                pairs.add((max(0.0, w0), max(0.0, w1)))
    pairs.add((u, u))
    pairs.add((max(0.0, u + k - p_h * b), max(0.0, u + k - p_h * b) + b))
    return pairs


def check_contracts(p_l, p_h, k, u):
    delta, b, c_h = analytic(p_l, p_h, k, u)
    pairs = wage_candidates(p_l, p_h, k, u)
    feasible_h, feasible_l = [], []
    for w0, w1 in pairs:
        d = w1 - w0
        ew_h = (1 - p_h) * w0 + p_h * w1
        ew_l = (1 - p_l) * w0 + p_l * w1
        if d + TOL >= b and ew_h + TOL >= u + k:
            feasible_h.append(ew_h)
            assert ew_h + 2e-8 >= c_h
        if d <= b + TOL and ew_l + TOL >= u:
            feasible_l.append(ew_l)
            assert ew_l + 2e-8 >= u
    assert feasible_h and feasible_l
    assert isclose(min(feasible_h), c_h, abs_tol=2e-8)
    assert isclose(min(feasible_l), u, abs_tol=2e-8)

    w0 = max(0.0, u + k - p_h * b)
    w1 = w0 + b
    assert w0 >= 0 and w1 >= 0
    assert isclose((1 - p_h) * w0 + p_h * w1, c_h, abs_tol=TOL)
    assert isclose(delta * (w1 - w0), k, abs_tol=TOL)
    assert isclose(c_h - k - u, max(0.0, p_h * b - k - u), abs_tol=TOL)

    # Strict effort statements.
    strict_h_same_cost_exists = u + k > p_h * b + TOL
    if strict_h_same_cost_exists:
        d = (b + (u + k) / p_h) / 2
        assert d > b and d <= (u + k) / p_h
        assert u + k - p_h * d >= -TOL
    else:
        assert p_h * (b + 1e-7) > c_h
    assert 0 < b  # constant wage strictly favors low because k>0


def check_strict_participation_and_low_family(p_l, p_h, k, u):
    _, b, c_h = analytic(p_l, p_h, k, u)
    rent = p_h * b - u - k

    # Weak high IC plus strict participation: attained exactly with LL rent.
    if rent > TOL:
        w0, w1 = 0.0, b
        assert isclose((1 - p_h) * w0 + p_h * w1, c_h, abs_tol=TOL)
        assert p_h * w1 + (1 - p_h) * w0 - k > u
    else:
        # Every cost-C_H contract has binding high IR; adding epsilon is feasible.
        assert isclose(c_h, u + k, abs_tol=TOL)
        for d in (b, c_h / p_h):
            w0, w1 = c_h - p_h * d, c_h + (1 - p_h) * d
            if w0 >= -TOL:
                assert isclose((1 - p_h) * w0 + p_h * w1 - k, u, abs_tol=2e-8)
        eps = 1e-6
        d = b
        c = c_h + eps
        w0, w1 = c - p_h * d, c + (1 - p_h) * d
        assert min(w0, w1) >= -TOL and c - k > u

    # Low strict participation always opens IR at cost u.
    assert isclose((1 - p_l) * u + p_l * u, u, abs_tol=TOL)
    assert (1 - p_l) * (u + 1e-6) + p_l * (u + 1e-6) > u

    # Full least-cost strict-low family and its open/closed upper endpoint.
    lo, hi, hi_closed = strict_low_spread_set(p_l, b, u)
    probes = {lo, (lo + hi) / 2}
    if hi_closed:
        probes.add(hi)
    else:
        probes.add(hi - min(1e-6, (hi - lo) / 2 if hi > lo else 1e-6))
    for d in probes:
        w0, w1 = u - p_l * d, u + (1 - p_l) * d
        assert w0 >= -2e-8 and w1 >= -2e-8
        assert d < b
        assert isclose((1 - p_l) * w0 + p_l * w1, u, abs_tol=2e-8)
    # Lower endpoint is closed; moving below violates success-wage LL.
    d = lo - 1e-6
    assert u + (1 - p_l) * d < 0
    if hi_closed:
        assert p_l > 0 and hi < b
        assert isclose(u - p_l * hi, 0.0, abs_tol=TOL)
        assert u - p_l * (hi + 1e-6) < 0
    else:
        assert isclose(hi, b, abs_tol=TOL)
        # The endpoint can satisfy LL but fails strict low IC.
        w0, w1 = u - p_l * hi, u + (1 - p_l) * hi
        assert min(w0, w1) >= -2e-8 and not (hi < b)

    # With both high IC and participation strict, C_H is never attained.
    if u + k > p_h * b:
        # Cost C_H can satisfy strict IC, but high IR binds.
        d = (b + c_h / p_h) / 2
        assert d > b
        assert isclose(c_h - k, u, abs_tol=TOL)
    else:
        # Any strict spread forces expected cost strictly above p_H b = C_H.
        assert p_h * (b + 1e-6) > c_h


def check_strict_mode_existence():
    # Nonattainment because LL/strict-IC boundary binds: below, at, above limit comparison.
    pars = (0.2, 0.6, 2.0, 0.0)
    assert strict_high_mode_status(*pars, 6.0) == ("alternatives", {"L"})
    assert strict_high_mode_status(*pars, 7.5) == ("alternatives", {"L"})
    assert strict_high_mode_status(*pars, 8.0) == ("no_maximizer", set())

    # Exact boundary u+k=p_H b also has no strict-high minimizer.
    pars_equal = (0.2, 0.6, 2.0, 1.0)
    _, _, c_h = analytic(*pars_equal)
    v_equal = (c_h - pars_equal[3]) / (pars_equal[1] - pars_equal[0])
    status, chosen = strict_high_mode_status(*pars_equal, v_equal)
    assert status == "alternatives" and "H" not in chosen
    assert strict_high_mode_status(*pars_equal, v_equal + 1.0)[0] == "no_maximizer"

    # When u+k>p_H b, strict high is attained and ordinary ties include H.
    pars_attained = (0.2, 0.6, 2.0, 2.0)
    _, _, c_h = analytic(*pars_attained)
    v_tie = c_h / pars_attained[1]
    status, chosen = strict_high_mode_status(*pars_attained, v_tie)
    assert status == "attained" and {"H", "S"}.issubset(chosen)

    # If both IC and participation are strict, only shutdown can be attained at the suprema.
    for pars, v, expected in [
        ((0.2, 0.6, 2.0, 0.0), 0.0, "shutdown"),
        ((0.2, 0.6, 2.0, 0.0), 6.0, "no_maximizer"),
        ((0.2, 0.6, 2.0, 2.0), 8.0, "no_maximizer"),
    ]:
        p_l, p_h, k, u = pars
        _, _, c_h = analytic(*pars)
        sup_h, sup_l = p_h * v - c_h, p_l * v - u
        result = "shutdown" if max(sup_h, sup_l) <= 0 else "no_maximizer"
        assert result == expected


def check_modes_and_welfare(p_l, p_h, k, u):
    delta, b, c_h = analytic(p_l, p_h, k, u)
    boundaries = {
        0.0,
        k / delta,
        (u + k) / p_h,
        (c_h - u) / delta,
        c_h / p_h,
    }
    if p_l > 0:
        boundaries.add(u / p_l)
    vmax = max(boundaries) + 3.0
    values = {i * vmax / 100 for i in range(101)} | boundaries
    for x in list(boundaries):
        values |= {max(0.0, x - 1e-5), x + 1e-5}

    rent = c_h - u - k
    for v in sorted(values):
        private = {"H": p_h * v - c_h, "L": p_l * v - u, "S": 0.0}
        social = {"H": p_h * v - k - u, "L": p_l * v - u, "S": 0.0}
        mp, ms = modes(private), modes(social)
        # Classification equivalences.
        h_test = p_h * v + 1e-9 >= c_h and delta * v + 1e-9 >= c_h - u
        assert ("H" in mp) == h_test, (p_l, p_h, k, u, v, private, mp, h_test)
        assert ("L" in mp) == (p_l * v + 1e-9 >= u and delta * v <= c_h - u + 1e-9)
        assert ("S" in mp) == (p_h * v <= c_h + 1e-9 and p_l * v <= u + 1e-9)
        assert isclose(private["H"], social["H"] - rent, abs_tol=TOL)
        if rent <= TOL:
            assert mp == ms

    if rent > TOL:
        a = max(k / delta, (u + k) / p_h)
        b_private = max((c_h - u) / delta, c_h / p_h)
        assert b_private > a
        probes = [max(0.0, a - 1e-6), a, (a + b_private) / 2, b_private, b_private + 1e-6]
        for v in probes:
            mp = modes({"H": p_h * v - c_h, "L": p_l * v - u, "S": 0.0})
            ms = modes({"H": p_h * v - k - u, "L": p_l * v - u, "S": 0.0})
            if v < a - 1e-8 or v > b_private + 1e-8:
                assert mp == ms
            else:
                assert mp != ms


def main():
    p_pairs = [(0.0, 0.2), (0.0, 1.0), (0.2, 0.6), (0.4, 1.0), (0.9, 1.0)]
    ks = [0.05, 0.5, 2.0]
    us = [0.0, 0.1, 2.0, 10.0]
    count = 0
    for (p_l, p_h), k, u in product(p_pairs, ks, us):
        check_contracts(p_l, p_h, k, u)
        check_strict_participation_and_low_family(p_l, p_h, k, u)
        check_modes_and_welfare(p_l, p_h, k, u)
        count += 1
    # Named examples and exact equality p_H b = u+k.
    check_contracts(0.2, 0.6, 2.0, 2.0)
    check_contracts(0.2, 0.6, 2.0, 0.0)
    p_l, p_h, k = 0.2, 0.6, 2.0
    delta = p_h - p_l
    u_equal = p_h * k / delta - k
    assert u_equal >= 0
    check_contracts(p_l, p_h, k, u_equal)
    check_modes_and_welfare(p_l, p_h, k, u_equal)
    check_strict_participation_and_low_family(p_l, p_h, k, u_equal)
    check_strict_mode_existence()
    print(f"PASS: {count + 3} deterministic parameter cases")
    print("PASS: grid-plus-boundary feasibility and cost optimality")
    print("PASS: weak/strict implementation properties")
    print("PASS: strict participation below, at, and above the LL-rent boundary")
    print("PASS: complete strict-low family with open/closed upper boundaries")
    print("PASS: strict-high principal maximizer existence and nonexistence")
    print("PASS: private mode classifications and all argmax ties")
    print("PASS: social/private equivalence without rent and exact wedge interval with rent")


if __name__ == "__main__":
    main()
