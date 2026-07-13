from fractions import Fraction as Q
from itertools import product


def payoff_adopt(x, g, opponent_action):
    return x + g * opponent_action


def pure_ne_bruteforce(x, g):
    out = set()
    for a1, a2 in product((0, 1), repeat=2):
        u1 = payoff_adopt(x, g, a2)
        u2 = payoff_adopt(x, g, a1)
        ok1 = (a1 == 1 and u1 >= 0) or (a1 == 0 and u1 <= 0)
        ok2 = (a2 == 1 and u2 >= 0) or (a2 == 0 and u2 <= 0)
        if ok1 and ok2:
            out.add((a1, a2))
    return out


def pure_ne_formula(x, g):
    if g == 0 and x == 0:
        return {(0, 0), (0, 1), (1, 0), (1, 1)}
    out = set()
    if x <= 0:
        out.add((0, 0))
    if x + g >= 0:
        out.add((1, 1))
    return out


def welfare_values(b, g, s=Q(0), lam=Q(0)):
    c = b - lam * s
    return {0: Q(0), 1: c, 2: 2 * (c + g)}


def welfare_argmax_bruteforce(b, g, s=Q(0), lam=Q(0)):
    vals = welfare_values(b, g, s, lam)
    best = max(vals.values())
    return {n for n, value in vals.items() if value == best}


def welfare_argmax_formula(b, g, s=Q(0), lam=Q(0)):
    c = b - lam * s
    if c + g < 0:
        return {0}
    if c + g > 0:
        return {2}
    if g > 0:
        return {0, 2}
    return {0, 1, 2}


grid = [Q(n, 4) for n in range(-8, 9)]
nonnegative = [Q(n, 4) for n in range(0, 9)]
positive_lambda = [Q(1, 4), Q(1, 2), Q(1), Q(2)]

pure_checks = 0
mixed_checks = 0
welfare_checks = 0
policy_checks = 0
coordination_failures = 0
excess_adoption_cases = 0

for b, s, g in product(grid, nonnegative, nonnegative):
    x = b + s
    assert pure_ne_bruteforce(x, g) == pure_ne_formula(x, g)
    pure_checks += 1

    # Interior mixing, indifference, basin direction, and risk dominance.
    if g > 0 and -g < x < 0:
        p = -x / g
        assert 0 < p < 1
        assert x + g * p == 0
        eps = min(p, 1 - p) / 2
        assert x + g * (p - eps) < 0
        assert x + g * (p + eps) > 0
        loss_both = x + g
        loss_none = -x
        assert (loss_both > loss_none) == (p < Q(1, 2))
        assert (loss_both == loss_none) == (p == Q(1, 2))
        assert (loss_both < loss_none) == (p > Q(1, 2))
        mixed_checks += 1

    # Transfer-free welfare formula and all ties.
    assert welfare_argmax_bruteforce(b, g) == welfare_argmax_formula(b, g)
    welfare_checks += 1

    # Exhaustive policy-inefficiency classifications.
    ne = pure_ne_bruteforce(x, g)
    coordination_failure = (b + g > 0) and ((0, 0) in ne)
    assert coordination_failure == ((b + g > 0) and (x <= 0))
    coordination_failures += int(coordination_failure)
    excess_adoption = (b + g < 0) and ((1, 1) in ne)
    assert excess_adoption == ((b + g < 0) and (x + g >= 0))
    excess_adoption_cases += int(excess_adoption)

    # Boundary equilibrium cases.
    if g > 0 and x in (-g, Q(0)):
        assert pure_ne_bruteforce(x, g) == {(0, 0), (1, 1)}
    if g == 0 and x == 0:
        assert pure_ne_bruteforce(x, g) == set(product((0, 1), repeat=2))

    for lam in positive_lambda:
        assert welfare_argmax_bruteforce(b, g, s, lam) == welfare_argmax_formula(
            b, g, s, lam
        )
        # Both-adoption fiscal test is exactly the sign of b+g-lambda*s.
        w = welfare_values(b, g, s, lam)
        assert (w[2] > w[0]) == (b + g - lam * s > 0)
        assert (w[2] == w[0]) == (b + g - lam * s == 0)
        # Unique-both classification, including failure at the infimum x=0.
        unique_both = pure_ne_bruteforce(x, g) == {(1, 1)}
        assert unique_both == (x > 0)
        if b <= 0 and s == -b:
            assert not unique_both
        policy_checks += 1

# Equality/tie witnesses.
assert pure_ne_bruteforce(Q(-1), Q(1)) == {(0, 0), (1, 1)}  # x=-g
assert pure_ne_bruteforce(Q(0), Q(1)) == {(0, 0), (1, 1)}   # x=0
assert welfare_argmax_bruteforce(Q(-1), Q(1)) == {0, 2}
assert welfare_argmax_bruteforce(Q(0), Q(0)) == {0, 1, 2}

# Preserved counterexample 1: welfare dominance does not select equilibrium.
b, s, g = Q(-1, 4), Q(0), Q(1)
assert pure_ne_bruteforce(b + s, g) == {(0, 0), (1, 1)}
assert welfare_argmax_bruteforce(b, g) == {2}

# Preserved counterexample 2: equilibrium-changing subsidy can fail welfare.
b, g, lam = Q(-3, 5), Q(1), Q(1)
s0, s1 = Q(0), Q(7, 10)
assert pure_ne_bruteforce(b + s0, g) == {(0, 0), (1, 1)}
assert pure_ne_bruteforce(b + s1, g) == {(1, 1)}
assert welfare_values(b, g, s1, lam)[2] == Q(-3, 5)
assert welfare_values(b, g, s1, lam)[2] < welfare_values(b, g, s1, lam)[0]

print("ALL CHECKS PASSED")
print(f"pure best-response cases: {pure_checks}")
print(f"strict mixed/risk cases: {mixed_checks}")
print(f"transfer-free welfare cases: {welfare_checks}")
print(f"financing-cost policy cases: {policy_checks}")
print(f"coordination-failure witnesses: {coordination_failures}")
print(f"excess-adoption witnesses: {excess_adoption_cases}")
print("boundary cases: x=-gamma, x=0, gamma=x=0 verified")
print("counterexample retained: welfare dominance does not select equilibrium")
print("counterexample retained: equilibrium-changing subsidy can reduce fiscal welfare")
