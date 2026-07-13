from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from mpmath import mp

mp.dps = 100


class Region(Enum):
    NEGATIVE = "D<0"
    ZERO = "D=0"
    BELOW_PEAK = "0<D<Smax"
    TANGENCY = "D=Smax"
    ABOVE_PEAK = "D>Smax"


@dataclass(frozen=True)
class Primitives:
    A: mp.mpf
    alpha: mp.mpf

    @property
    def peak_pi(self):
        return 1 / self.alpha

    @property
    def peak_S(self):
        return self.A / (4 * self.alpha)


def S(pi, p: Primitives):
    return p.A * pi / (1 + p.alpha * pi) ** 2


def classify(D, p: Primitives) -> Region:
    # Strict high-precision comparisons classify economics. No residual tolerance
    # is allowed to turn a positive number into zero or a near-peak value into a tangency.
    if D < 0:
        return Region.NEGATIVE
    if D == 0:
        return Region.ZERO
    if D < p.peak_S:
        return Region.BELOW_PEAK
    if D == p.peak_S:
        return Region.TANGENCY
    return Region.ABOVE_PEAK


def roots_from_primitives(D, p: Primitives, declared: Region):
    # The caller supplies a deliberately constructed economic label; we verify it
    # by exact high-precision comparison before using the corresponding formula.
    assert classify(D, p) is declared
    if declared in (Region.NEGATIVE, Region.ABOVE_PEAK):
        return ()
    if declared is Region.ZERO:
        return (mp.mpf("0"),)
    if declared is Region.TANGENCY:
        return (p.peak_pi,)
    disc = p.A * (p.A - 4 * p.alpha * D)
    assert disc > 0
    sq = mp.sqrt(disc)
    # Rationalized low root prevents cancellation as D -> 0+.
    low = 2 * D / (p.A - 2 * p.alpha * D + sq)
    high = (p.A - 2 * p.alpha * D + sq) / (2 * p.alpha**2 * D)
    return low, high


def fmt(x, n=70):
    return mp.nstr(x, n)


def residual_ok(x, scale=1):
    # Used only after the economic branch/root count has been fixed.
    return abs(x) <= mp.mpf("1e-90") * max(mp.mpf("1"), abs(scale))


def main():
    p = Primitives(A=mp.mpf("7.3"), alpha=mp.mpf("2.1"))
    print(f"mp.dps={mp.dps}")
    print(f"peak_pi={fmt(p.peak_pi)}")
    print(f"peak_S={fmt(p.peak_S)}")

    # Exactly constructed cases: their labels determine root multiplicity without tolerance.
    tiny_D = mp.mpf(10) ** -70
    eps = mp.mpf(10) ** -80
    cases = [
        ("negative", -tiny_D, Region.NEGATIVE),
        ("zero", mp.mpf("0"), Region.ZERO),
        ("d_to_zero_plus", tiny_D, Region.BELOW_PEAK),
        ("peak_minus_eps", p.peak_S - eps, Region.BELOW_PEAK),
        ("tangency", p.peak_S, Region.TANGENCY),
        ("peak_plus_eps", p.peak_S + eps, Region.ABOVE_PEAK),
    ]
    for name, D, label in cases:
        roots = roots_from_primitives(D, p, label)
        print(f"case={name}; label={label.value}; root_count={len(roots)}")
        for index, pi in enumerate(roots):
            res = S(pi, p) - D
            assert residual_ok(res, D)
            print(f"  root[{index}]={fmt(pi)}; residual={fmt(res, 12)}")

    # D -> 0+ asymptotics and the fact that the high finite root escapes to infinity.
    low0, high0 = roots_from_primitives(tiny_D, p, Region.BELOW_PEAK)
    low_ratio = low0 / (tiny_D / p.A)
    high_ratio = high0 / (p.A / (p.alpha**2 * tiny_D))
    assert abs(low_ratio - 1) < mp.mpf("1e-60")
    assert abs(high_ratio - 1) < mp.mpf("1e-60")
    print(f"d_to_zero low/(D/A)={fmt(low_ratio)}")
    print(f"d_to_zero high/(A/(alpha^2 D))={fmt(high_ratio)}")

    # Interior two-branch residuals and product identity.
    Dbar = mp.mpf("0.37") * p.peak_S
    low, high = roots_from_primitives(Dbar, p, Region.BELOW_PEAK)
    assert low < p.peak_pi < high
    assert residual_ok(S(low, p) - Dbar, Dbar)
    assert residual_ok(S(high, p) - Dbar, Dbar)
    assert residual_ok(low * high - 1 / p.alpha**2, 1 / p.alpha**2)
    print(f"interior_D={fmt(Dbar)}")
    print(f"low_root={fmt(low)}; low_residual={fmt(S(low,p)-Dbar, 12)}")
    print(f"high_root={fmt(high)}; high_residual={fmt(S(high,p)-Dbar, 12)}")
    print(f"root_product_residual={fmt(low*high-1/p.alpha**2, 12)}")

    # Tangency checked independently from its analytic primitive, not by near-zero discriminant.
    tangent_residual = S(p.peak_pi, p) - p.peak_S
    assert tangent_residual == 0
    print(f"tangency_residual={fmt(tangent_residual)}")

    # Dynamic rules recomputed from primitives.
    r = mp.mpf("0.04")
    k = mp.mpf("0.15")
    bbar = mp.mpf("2.0")
    dpbar = Dbar - r * bbar
    print(f"dynamic_primitives r={r}; k={k}; bbar={bbar}; dpbar={fmt(dpbar)}")
    for x in (mp.mpf("0.031"), mp.mpf("-0.027")):
        # Target-only plus constant inflation: divergence.
        dot_const = r * x
        assert dot_const * x > 0
        # An alternative extra closure that exactly persists.
        q_persist = Dbar + r * x
        dot_persist = r * x + Dbar - q_persist
        assert dot_persist == 0
        # Monetary dominance: fiscal feedback, fixed inflation.
        dp = dpbar - (r + k) * x
        dot_md = r * (bbar + x) + dp - S(low, p)
        assert residual_ok(dot_md + k * x, k * x)
        # Fiscal dominance: fixed fiscal deficit, monetary seigniorage feedback, both branches.
        q = Dbar + (r + k) * x
        q_label = classify(q, p)
        assert q_label is Region.BELOW_PEAK
        pi_l, pi_h = roots_from_primitives(q, p, q_label)
        dot_fd_l = r * (bbar + x) + dpbar - S(pi_l, p)
        dot_fd_h = r * (bbar + x) + dpbar - S(pi_h, p)
        assert residual_ok(dot_fd_l + k * x, k * x)
        assert residual_ok(dot_fd_h + k * x, k * x)
        print(
            f"x={x}; constant_dot={fmt(dot_const)}; persistent_dot={fmt(dot_persist)}; "
            f"MD_dot={fmt(dot_md)}; FD_low_dot={fmt(dot_fd_l)}; FD_high_dot={fmt(dot_fd_h)}"
        )

    # Exact fiscal-dominance feasibility endpoints and deliberately infeasible points.
    x_lo = -Dbar / (r + k)
    x_hi = (p.peak_S - Dbar) / (r + k)
    # Label the analytically constructed endpoint values themselves. Re-forming
    # them via divide-then-multiply may lose a last digit even at high precision;
    # a tolerance must not be used to relabel that rounded value as equality.
    q_lo_endpoint = mp.mpf("0")
    q_hi_endpoint = p.peak_S
    assert classify(q_lo_endpoint, p) is Region.ZERO
    assert classify(q_hi_endpoint, p) is Region.TANGENCY
    assert residual_ok(Dbar + (r + k) * x_lo - q_lo_endpoint, p.peak_S)
    assert residual_ok(Dbar + (r + k) * x_hi - q_hi_endpoint, p.peak_S)
    outside = mp.mpf("1e-60")
    q_below = q_lo_endpoint - (r + k) * outside
    q_above = q_hi_endpoint + (r + k) * outside
    assert classify(q_below, p) is Region.NEGATIVE
    assert classify(q_above, p) is Region.ABOVE_PEAK
    assert roots_from_primitives(q_below, p, Region.NEGATIVE) == ()
    assert roots_from_primitives(q_above, p, Region.ABOVE_PEAK) == ()
    print(f"FD_low_branch_interval=[{fmt(x_lo)}, {fmt(x_hi)}]")
    print(f"FD_high_branch_interval=({fmt(x_lo)}, {fmt(x_hi)}]")
    print(f"below_interval_label={classify(q_below,p).value}; q={fmt(q_below)}")
    print(f"above_interval_label={classify(q_above,p).value}; q={fmt(q_above)}")

    print("ALL ASSERTIONS PASSED")
    print("Finite numerical checks corroborate selected cases; they do not replace the analytic derivative, discriminant, and boundary proof.")


if __name__ == "__main__":
    main()
