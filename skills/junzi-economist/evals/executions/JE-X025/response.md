# Constrained abatement model — complete result

## Environment and global choices

The firm chooses `a in [0,E]` after observing `s>=0`. Its payoff is
`pi(a;s)=sa-ca^2/2`. Because `pi` is strictly concave (`-c<0`), its unique global constrained choice is

`a_p(s)=min{s/c,E}`.

Equivalently, `a_p=s/c` for `0<=s<cE` and `a_p=E` for `s>=cE`; the formulas agree at `s=cE`.

Social welfare (the subsidy is a transfer) is
`W(a)=-ca^2/2-d(E-a)^2/2`. It is strictly concave (`-(c+d)<0`). Its unconstrained FOC gives

`a*=dE/(c+d)`.

Since `c,d,E>0`, `0<a*<E`; hence this is also the unique global constrained social optimum.

## Exact finite-increase classification

For any finite `0<=s1<s2`, define `x_i=a_p(s_i)`, `A=a*`, and `D_i=|x_i-A|`. Monotonicity gives `x2>=x1`. If `x2>x1`,

`D2^2-D1^2=(x2-x1)(x1+x2-2A)`.

Consequently, the following conditions are necessary and sufficient:

1. **Strictly closer:** `x2>x1` and `x1+x2<2A`.
2. **Same distance:** either `x2=x1` (equivalently, given `s1<s2`, `s1>=cE`, so both choices are saturated) or `x2>x1` and `x1+x2=2A`.
3. **Farther:** `x2>x1` and `x1+x2>2A`.

These exhaustive conditions cover every boundary. In particular, if `x1=A`, any nonsaturated increase has `x2>x1` and is strictly farther. If the increase crosses `A`, it is closer only when the endpoint overshoot is smaller than the initial shortfall, unchanged only under exact symmetry, and farther when the overshoot is larger. If `x2=E>x1`, the same sum test applies. If `x1=E`, both are saturated and distance is unchanged.

In subsidy notation, substitute `x_i=min{s_i/c,E}` and `A=dE/(c+d)` in the three conditions above.

## Continuity and all kink derivatives

The choice is continuous:

`a_p(s)=s/c` on `[0,cE]`, and `E` on `[cE,infinity)`.

Its right derivative at the domain boundary `s=0` is `1/c`; at the saturation kink `cE`, its left and right derivatives are `1/c` and `0`.

Distance from the social optimum is the continuous function

`D(s)=A-s/c` for `0<=s<=cA`;
`D(s)=s/c-A` for `cA<=s<=cE`;
`D(s)=E-A` for `s>=cE`.

Thus `D'_+(0)=-1/c`. At the equality kink `s=cA`, `D'_-= -1/c` and `D'_+=1/c`. At the saturation kink `s=cE`, `D'_-=1/c` and `D'_+=0`. The boundary values coincide at both kinks. These directional derivatives also show why a nonpositive product test at initial equality is insufficient.

## Implementation and examples

The unique subsidy inducing `a*` is

`s_impl=c a*=cdE/(c+d)`.

It is feasible because it is positive and strictly below `cE`; hence it respects `s>=0` and induces an interior choice. (If an additional subsidy cap existed, implementation would require that cap to be at least `s_impl`.)

With `(c,d,E)=(2,2,10)`, `A=5`:

- closer: `(s1,s2)=(2,6)` induces `(1,3)`, distances `(4,2)`;
- same by symmetric crossing: `(4,16)` induces `(2,8)`, distances `(3,3)`;
- farther from initial equality: `(10,12)` induces `(5,6)`, distances `(0,1)`;
- farther after overshooting: `(12,18)` induces `(6,9)`, distances `(1,4)`;
- same by saturation: `(20,24)` induces `(10,10)`, distances `(5,5)`.

## Marginal resource cost of public funds

If financing each subsidy dollar has additional marginal resource cost `lambda>0`, welfare for a policy-induced allocation becomes

`W_lambda(s)=-C(a_p(s))-d(E-a_p(s))^2/2-lambda*s*a_p(s)`.

The firm choice and all distance classifications relative to the original `A` are unchanged, because the firm still receives `s`. The old implementing subsidy `s_impl` remains technologically feasible and still induces `A`, but it is no longer policy-optimal under `W_lambda`.

For an unsaturated policy, `s=ca`, so maximizing policy welfare over implementable `a` is equivalent to maximizing
`-ca^2/2-d(E-a)^2/2-lambda*c*a^2`. The unique optimum is

`a_lambda=dE/[d+c(1+2lambda)] < A`,
`s_lambda=c a_lambda=cdE/[d+c(1+2lambda)]`.

It is positive and strictly below `cE`, hence feasible and unsaturated. The factor `2` arises because raising `s` increases both the payment per unit and induced units. This conclusion uses the explicit convention that `lambda` is an extra resource cost per subsidy dollar; alternative fiscal-cost conventions must be stated separately.

## Status and verification

**Analytic status.** The constrained private and social optima are globally proved by strict concavity plus feasibility. The finite-change classification is globally proved for every `c,d,E>0`, `s>=0`, and finite ordered increase `0<=s1<s2` by the displayed algebraic identity and the monotonic clipped choice. Continuity and directional derivatives follow from the explicit piecewise formulas. With `lambda>0`, strict concavity of the implementable policy objective, its zero first-order condition, and feasibility prove the stated fiscal-cost optimum globally.

**Computational status.** `verify.py` is a deterministic implementation-regression check, not a proof over the continuous parameter domain. It uses exact rational arithmetic on finite boundary-enriched grids, enforces all preconditions, checks candidate objective values against grid points, verifies the classification, continuity and directional slopes, checks the fiscal-cost FOC and negative curvature, and preserves counterexamples to overbroad monotonicity claims.
