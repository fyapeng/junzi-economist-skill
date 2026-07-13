# One-period debt transfer in a Diamond OLG economy

## Judgment

In this closed, non-altruistic two-period OLG economy, government debt is net
wealth to the currently young asset holders and a liability of the next young
cohort. Because date-0 log savers save a fixed share of their wage, bond supply
displaces date-1 physical capital one for one. The initial old and cohort 0 gain;
cohort 1 and the finite transition cohorts lose. The economy eventually returns
to the unique positive no-debt steady state, so the policy has a transition-level,
not permanent, effect on capital per young worker. This is a redistribution
across cohorts, not a Pareto improvement.

The 2% and 10% experiments are feasible. The requested 30% experiment has no
equilibrium with positive young consumption at repayment: the date-1 tax exceeds
the date-1 wage. Reporting a clipped or negative consumption solution would
violate the model.

## Environment and exact timing

Let `N_t=(1+n)^t`, with `N_0=1`, and `k_t=K_t/N_t`. Output at date `t` is
`Y_t=K_t^alpha N_t^(1-alpha)`. Full depreciation and competition imply

`w_t=(1-alpha)k_t^alpha`, `R_t=alpha k_t^(alpha-1)`.

At each date production occurs first. The old consume the gross return on assets
bought when young. The young receive wages, pay any contemporaneous lump-sum tax,
consume, and buy claims paying next period. At date 0, after production, the
government transfers aggregate `D_1` to the initial old and sells one-period bonds
of market value `D_1` to cohort 0. A unit purchased at date 0 pays the competitive
gross return `R_1` at date 1. At date 1, after production, cohort 1 pays aggregate
tax `R_1 D_1`; cohort 0 receives the bond payoff; the debt is extinguished. No tax
or debt exists from date 2 onward. All agents perfectly foresee this sequence.

Set `d=D_1/N_0=D_1`. For a young household born at `t`, let `s_t` denote total
saving and `tau_t` its tax:

`c^y_t+s_t=w_t-tau_t`,

`c^o_{t+1}=R_{t+1}s_t`,

where `tau_1=R_1 d/(1+n)` and all other `tau_t=0`. With
`log(c^y)+beta log(c^o)`, an interior household saves

`s_t=[beta/(1+beta)](w_t-tau_t)`.

The initial old have per-person consumption

`c^o_0=(1+n)R_0 k_0+(1+n)d`.

The government budgets are `transfer_0=D_1=bond_sales_0` and
`N_1 tau_1=R_1D_1`. Capital and bonds are perfect substitutes in cohort 0's
portfolio, so their individual composition is indeterminate, but aggregate
capital is pinned down by asset-market clearing:

`N_t s_t=K_{t+1}+D_{t+1}`.

Thus at date 0,

`s_0=(1+n)k_1+d`,

and, with no new bonds from date 1 onward, `s_t=(1+n)k_{t+1}`.

Aggregate real-resource feasibility is

`Y_t=C^y_t+C^o_t+K_{t+1}`.

Taxes, transfers, bond sales, and bond repayment do not appear as resources;
they cancel after consolidating agents and government. The numerical program
checks this identity separately at dates 0 and 1 rather than using it to infer
behavior.

## Equilibrium transition and feasibility

Let `lambda=beta/(1+beta)`. Starting from the no-debt steady state,

`k*=[lambda(1-alpha)/(1+n)]^[1/(1-alpha)]`,

the policy transition is

`k_1=[lambda w(k*)-d]/(1+n)`,

`k_2=lambda[w(k_1)-R(k_1)d/(1+n)]/(1+n)`,

and, for `t>=2`,

`k_{t+1}=lambda(1-alpha)k_t^alpha/(1+n)`.

Two different feasibility constraints matter. Positive date-1 capital requires
`d<s_0=lambda(1-alpha)Y_0`; in output shares this is `d/Y_0<0.335` under the
calibration. Positive disposable income for cohort 1 requires

`w(k_1)>R(k_1)d/(1+n)`,

which simplifies to `d<(1-alpha)s_0`, or `d/Y_0<0.22445`. The second bound is
therefore decisive. Equality gives zero young consumption, outside the log domain.

The post-debt map is increasing and concave, has a unique positive steady state,
and has local derivative `alpha=0.33` at that steady state. For each feasible
experiment here, `k_2<k*` and subsequent capital converges monotonically upward to
`k*`. Debt therefore lowers capital on impact at date 1, propagates through wages
and returns during transition, and leaves no permanent capital-per-worker effect.

## Calibration and cohort incidence

With `alpha=0.33`, `beta=1`, and `n=0.01`:

| Debt / initial output | Status | `k_1` | `k_2` | `R_1` | cohort-1 tax | initial-old Delta log c | cohort-0 Delta U | cohort-1 Delta U |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 2% | feasible | 0.181104 | 0.182827 | 1.036818 | 0.011922 | 0.058841 | 0.041244 | -0.069274 |
| 10% | feasible | 0.135109 | 0.135426 | 1.261697 | 0.072539 | 0.264693 | 0.237545 | -0.468431 |
| 30% | infeasible at repayment | — | — | — | tax exceeds wage | — | — | — |

The baseline is `k*=0.192602`, `Y_0=0.580682`, and `s_0=0.194528`.

The initial old gain directly. Cohort 0's young consumption is unchanged because
its log-saving rule fixes total saving at `s_0`; it gains in old age because lower
`k_1` raises the common return on its fixed saving. Cohort 1 bears the repayment
tax and lower wage; its later higher return does not compensate in either feasible
calibration. Later cohorts face no tax but inherit depressed capital. Their losses
shrink toward zero as capital converges. These utility changes are cohort-specific
positive statements. Any social ranking additionally requires explicit weights
over cohorts and cannot be inferred from aggregate output or the government budget.

## Why accounting does not identify crowd-out

The identity `private saving = capital + government bonds` permits several
mechanisms. Bond issuance could raise private saving, reduce capital, draw foreign
funding, alter prices, or be offset by dynastic bequests. The one-for-one impact
crowd-out here comes from the joint assumptions of a closed economy, fixed labor,
perfect substitution and no-arbitrage between capital and bonds, log utility that
makes cohort-0 total saving a fixed share of its unaffected wage, no adjustment by
the initial old, and no altruistic link to the taxed cohort. Remove any relevant
behavioral or closure assumption and the identity remains true while the crowd-out
result can change.

## Ricardian benchmark

In an infinitely lived representative-agent benchmark, consolidate the household
and government intertemporal budgets. If the same household receives the transfer
and bears its present-value tax, has perfect foresight, can borrow and lend freely,
faces lump-sum nondistortionary taxes, has an operative infinite horizon and no
binding borrowing or bequest constraint, and government debt pays the market
return, the transfer and future tax cancel in present value. Consumption, saving,
capital, prices, and welfare are unchanged: the household saves the transfer to
meet the tax.

Those conditions fail in the stated Diamond economy. The recipient initial old,
bond-buying cohort 0, and taxed cohort 1 are distinct finite-lived agents without
operative altruistic links. Population growth also requires the per-capita transfer
and tax to be scaled across different cohort sizes. Ricardian equivalence could be
restored in an OLG setting only with operative dynastic altruism/bequests that make
the relevant families internalize the correctly scaled descendant tax, together
with the frictionless and lump-sum assumptions above. It is defeated by finite
horizons without altruism, borrowing/bequest constraints, uncertain or
distributionally mismatched taxes, distortionary taxes, incomplete markets,
different discounting/returns, myopia, or a fiscal path that is not solvent.

## Reproducible checks and falsification

`simulate_olg.py` uses only the Python standard library and writes the complete
cohort paths and summary. It asserts date-0 asset clearing, date-1 government
budget balance, date-0 and date-1 resource feasibility, impact crowd-out, and
numerical convergence. Residuals are at most `2.8e-17`. It also deliberately tests
debt just above initial saving and rejects it at issuance.

The result would be falsified or need narrowing if: a feasible run violates a
budget/resource residual beyond numerical tolerance; bond and capital returns
differ without an added friction; household saving reacts differently under the
stated log problem; `d>=s_0` yields positive capital; `d>=(1-alpha)s_0` yields
positive cohort-1 consumption; the post-debt law fails to return to `k*`; or an
explicit dynastic version satisfying all Ricardian conditions still changes the
allocation. Adding adjustment costs, partial depreciation, endogenous labor,
open-economy capital, risk, distortionary taxation, or heterogeneous constraints
defines a new branch rather than a robustness check of this closed-form result.

Derivation status: `verified-piecewise` for the stated deterministic model and
calibration; the Ricardian comparison is conditional on the assumptions listed.
