"""High-precision deterministic checks for the two-period SOE model.

The analytic proof is in response.md. These are finite regression/property checks.
"""
from decimal import Decimal as D, getcontext

getcontext().prec = 60
ZERO, ONE = D(0), D(1)


def dec(x):
    return x if isinstance(x, D) else D(str(x))


def solve(beta, R, y1, b0, Bbar, ys, qs):
    beta, R, y1, b0, Bbar = map(dec, (beta, R, y1, b0, Bbar))
    ys = [dec(y) for y in ys]
    qs = [dec(q) for q in qs]
    assert beta > 0 and R > 0 and y1 > 0 and Bbar >= 0
    assert all(y > 0 for y in ys) and sum(qs) == ONE and all(q > 0 for q in qs)
    X, ell = y1 + R * b0, -Bbar
    # Maintained common feasible set: the institutional floor gives positive consumption.
    assert X - ell > 0 and all(y + R * ell > 0 for y in ys)

    def g(b):
        c1 = X - b
        return -ONE / c1 + beta * R * sum(q / (y + R * b) for y, q in zip(ys, qs))

    if g(ell) <= 0:
        b, mu, regime = ell, -g(ell), "binding"
    else:
        lo, hi = ell, (ell + X) / 2
        while g(hi) > 0:
            hi = (hi + X) / 2
        for _ in range(260):
            mid = (lo + hi) / 2
            if g(mid) > 0:
                lo = mid
            else:
                hi = mid
        b, mu, regime = (lo + hi) / 2, ZERO, "interior"
    c1 = X - b
    c2 = [y + R * b for y in ys]
    return {
        "beta": beta, "R": R, "y1": y1, "b0": b0, "Bbar": Bbar,
        "ys": ys, "qs": qs, "X": X, "ell": ell, "b": b,
        "c1": c1, "c2": c2, "mu": mu, "regime": regime, "g": g,
    }


def utility(sol, b):
    c1 = sol["X"] - b
    return c1.ln() + sol["beta"] * sum(
        q * (y + sol["R"] * b).ln() for y, q in zip(sol["ys"], sol["qs"])
    )


def check_solution(sol):
    b, R, b0 = sol["b"], sol["R"], sol["b0"]
    c1, mu, ell = sol["c1"], sol["mu"], sol["ell"]
    assert b >= ell and c1 > 0 and all(c > 0 for c in sol["c2"])
    # KKT: 1/c1 = beta R E(1/c2) + mu; mu(b-ell)=0.
    lhs = ONE / c1
    rhs = sol["beta"] * R * sum(q / c for q, c in zip(sol["qs"], sol["c2"])) + mu
    assert abs(lhs - rhs) < D("1e-50")
    assert mu >= 0 and abs(mu * (b - ell)) < D("1e-50")
    if sol["regime"] == "interior":
        assert b > ell and abs(sol["g"](b)) < D("1e-50")
    else:
        assert b == ell and sol["g"](ell) <= 0

    # Strict concavity and a boundary-enriched finite global check.
    fpp = -ONE / c1**2 - sol["beta"] * R**2 * sum(
        q / c**2 for q, c in zip(sol["qs"], sol["c2"])
    )
    assert fpp < 0
    ub = sol["X"] - D("1e-18")
    grid = [ell + (ub - ell) * D(i) / D(3000) for i in range(3001)] + [b]
    ustar = utility(sol, b)
    assert all(ustar >= utility(sol, z) - D("1e-45") for z in grid)

    # Period budgets and external accounts, state by state.
    assert c1 + b == sol["y1"] + R * b0
    ca1, tb1 = b - b0, b - R * b0
    assert ca1 == tb1 + (R - ONE) * b0
    for y, c2 in zip(sol["ys"], sol["c2"]):
        assert c2 == y + R * b
        ca2, tb2 = -b, -R * b
        assert ca2 == tb2 + (R - ONE) * b
        assert ca1 + ca2 == -b0  # change in NFA from b0 to terminal zero


def fmt(x):
    return f"{float(x):.9f}"


def main():
    cases = {}
    cases["interior"] = solve("0.95", "1", "2", "0", "0.8", ["1"], ["1"])
    cases["binding"] = solve("0.9", "1", "1", "0", "0.5", ["4"], ["1"])
    cases["boundary_equality"] = solve("0.9", "1", "3", "0", "0.5", ["3.65"], ["1"])
    cases["det_mean"] = solve("0.95", "1", "2", "0", "0.4", ["2"], ["1"])
    cases["risky"] = solve("0.95", "1", "2", "0", "0.4", ["1", "3"], ["0.5", "0.5"])
    cases["narrow_mps"] = solve("0.95", "1", "2", "0", "0.4", ["1.5", "2.5"], ["0.5", "0.5"])
    cases["wide_mps"] = solve("0.95", "1", "2", "0", "0.4", ["1", "3"], ["0.5", "0.5"])
    cases["future_up"] = solve("0.95", "1", "2", "0", "0.4", ["2.5"], ["1"])
    cases["higher_mean_risky"] = solve("0.95", "1", "2", "0", "0.4", ["0.5", "3.9"], ["0.5", "0.5"])
    cases["stop_old"] = solve("0.9", "1", "2", "-0.5", "2", ["4"], ["1"])
    cases["stop_new"] = solve("0.9", "1", "2", "-0.5", "0", ["4"], ["1"])
    cases["R_pos"] = solve("0.9", "1", "5", "0", "1", ["2"], ["1"])
    cases["R_neg"] = solve("0.9", "1", "5", "-3", "1", ["2"], ["1"])

    for sol in cases.values():
        check_solution(sol)

    assert cases["interior"]["regime"] == "interior"
    assert cases["binding"]["regime"] == "binding"
    assert cases["boundary_equality"]["b"] == cases["boundary_equality"]["ell"]
    assert abs(cases["boundary_equality"]["mu"]) < D("1e-50")
    assert cases["risky"]["b"] > cases["det_mean"]["b"]
    assert cases["wide_mps"]["b"] > cases["narrow_mps"]["b"]
    assert cases["future_up"]["b"] < cases["det_mean"]["b"]
    # A higher mean need not lower saving if downside risk rises enough.
    assert sum(q*y for q, y in zip(cases["higher_mean_risky"]["qs"], cases["higher_mean_risky"]["ys"])) > D(2)
    assert cases["higher_mean_risky"]["b"] > cases["det_mean"]["b"]

    old, new = cases["stop_old"], cases["stop_new"]
    assert old["b"] < old["b0"] and new["b"] > new["b0"]
    assert new["b"] > old["b"] and new["c1"] < old["c1"]
    assert new["b"] - new["b0"] > 0 > old["b"] - old["b0"]

    # Deterministic interior derivative db/dR=[beta*b0+y2/R^2]/(1+beta).
    for key, expected_sign in (("R_pos", 1), ("R_neg", -1)):
        sol = cases[key]
        deriv = (sol["beta"] * sol["b0"] + sol["ys"][0] / sol["R"]**2) / (ONE + sol["beta"])
        assert deriv * D(expected_sign) > 0

    print("HIGH-PRECISION CHECKS: PASS")
    print("cases checked: 13; decimal precision: 60 digits")
    for key in ("interior", "binding", "boundary_equality", "det_mean", "risky", "narrow_mps", "wide_mps",
                "future_up", "higher_mean_risky", "stop_old", "stop_new"):
        sol = cases[key]
        print(f"{key}: b1={fmt(sol['b'])}, c1={fmt(sol['c1'])}, regime={sol['regime']}")
    print("risk saving, mean-preserving spread, future-income ambiguity: PASS")
    print("sudden-stop CA sign reversal: PASS")
    print("R comparative-static sign reversal: PASS")
    print("budgets, CA/TB identities, KKT, strict concavity, finite global grids: PASS")


if __name__ == "__main__":
    main()
