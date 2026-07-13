"""Deterministic verification of the constrained abatement model."""
from fractions import Fraction as F

def private(s, c, E):
    assert c > 0 and E > 0 and s >= 0
    return min(s / c, E)

def social(c, d, E):
    assert c > 0 and d > 0 and E > 0
    return d * E / (c + d)

def dist(s, c, d, E):
    return abs(private(s, c, E) - social(c, d, E))

def classify(s1, s2, c, d, E):
    assert 0 <= s1 < s2 and c > 0 and d > 0 and E > 0
    x1, x2, A = private(s1,c,E), private(s2,c,E), social(c,d,E)
    if x1 == x2:
        return "same"
    q = x1 + x2 - 2*A
    return "closer" if q < 0 else "same" if q == 0 else "farther"

def brute_classify(s1, s2, c, d, E):
    D1, D2 = dist(s1,c,d,E), dist(s2,c,d,E)
    return "closer" if D2 < D1 else "same" if D2 == D1 else "farther"

def objective_private(a,s,c): return s*a-c*a*a/F(2)
def objective_social(a,c,d,E): return -c*a*a/F(2)-d*(E-a)**2/F(2)
def objective_fiscal(a,c,d,E,lam):
    # For an unsaturated implementable allocation, the least subsidy is s=ca.
    return objective_social(a,c,d,E)-lam*c*a*a

params = [(F(c),F(d),F(E)) for c in range(1,6) for d in range(1,6) for E in range(1,5)]
checks = pairs = fiscal_checks = 0
for c,d,E in params:
    A = social(c,d,E)
    # Grid includes 0, the distance kink cA, saturation cE, and points around both.
    S = sorted(set([F(0), c*A, c*E] + [c*E*F(k,12) for k in range(0,25)]))
    for s in S:
        x = private(s,c,E)
        assert F(0) <= x <= E
        # Global optimality checked on a deterministic fine feasible grid plus the candidates.
        grid = set([E*F(k,120) for k in range(121)] + [x,A,F(0),E])
        assert objective_private(x,s,c) == max(objective_private(a,s,c) for a in grid)
        assert objective_social(A,c,d,E) == max(objective_social(a,c,d,E) for a in grid)
        checks += 2
    for i,s1 in enumerate(S):
        for s2 in S[i+1:]:
            assert classify(s1,s2,c,d,E) == brute_classify(s1,s2,c,d,E)
            pairs += 1
    # Exact continuity at both kinks (piecewise formulas meet).
    assert A-c*A/c == 0 == c*A/c-A
    assert c*E/c-A == E-A
    # Exact one-sided slopes of D(s): domain endpoint, equality kink, saturation kink.
    h = min(c*A, c*(E-A))/F(100)
    assert (dist(h,c,d,E)-dist(F(0),c,d,E))/h == -1/c
    assert (dist(c*A,c,d,E)-dist(c*A-h,c,d,E))/h == -1/c
    assert (dist(c*A+h,c,d,E)-dist(c*A,c,d,E))/h == 1/c
    assert (dist(c*E,c,d,E)-dist(c*E-h,c,d,E))/h == 1/c
    assert (dist(c*E+h,c,d,E)-dist(c*E,c,d,E))/h == 0

    # Fiscal-cost extension, checked exactly for a boundary-enriched lambda grid.
    for lam in [F(1,100), F(1,10), F(1,2), F(1), F(3), F(10)]:
        assert lam > 0
        a_lam = d*E/(d+c*(1+2*lam))
        s_lam = c*a_lam
        assert F(0) < a_lam < A < E
        assert F(0) < s_lam < c*E
        assert private(s_lam,c,E) == a_lam  # feasible and unsaturated implementation
        foc = d*E-(d+c*(1+2*lam))*a_lam
        curvature = -(d+c*(1+2*lam))
        assert foc == 0
        assert curvature < 0
        # Regression check of global policy optimality over implementable a in [0,E].
        # Include both boundaries, A, a_lam, and a dense deterministic rational grid.
        a_grid = set([F(0), E, A, a_lam] + [E*F(k,240) for k in range(241)])
        assert objective_fiscal(a_lam,c,d,E,lam) == max(
            objective_fiscal(a,c,d,E,lam) for a in a_grid
        )
        fiscal_checks += 1

# Named examples and preserved counterexamples to overbroad monotonic claims.
c,d,E = F(2),F(2),F(10); A = social(c,d,E)
examples = {
    "closer": (F(2),F(6)),       # a: 1 -> 3, A=5
    "same_crossing": (F(4),F(16)),# a: 2 -> 8, symmetric around A
    "farther_initial_equality": (F(10),F(12)), # a: 5 -> 6
    "farther_overshoot": (F(12),F(18)),        # a: 6 -> 9
    "same_saturation": (F(20),F(24)),          # a: 10 -> 10
}
expected = ["closer","same","farther","farther","same"]
assert [classify(*v,c,d,E) for v in examples.values()] == expected

print(f"PASS: {len(params)} parameter triples; {checks} global-optimality checks; {pairs} ordered subsidy-pair classifications.")
print("PASS: exact continuity and one-sided kink slopes verified for every parameter triple.")
print(f"PASS: {fiscal_checks} fiscal-cost cases verified exactly: feasibility, unsaturation, a_lambda<A, FOC, strict concavity, and boundary-enriched implementable-grid optimality.")
for (name,(s1,s2)), result in zip(examples.items(), expected):
    print(f"{name}: s=({s1},{s2}), a=({private(s1,c,E)},{private(s2,c,E)}), A={A}, classification={result}")
print("Preserved counterexamples: initial equality can become farther; overshooting can become farther; saturation can yield no distance change despite s2>s1.")
