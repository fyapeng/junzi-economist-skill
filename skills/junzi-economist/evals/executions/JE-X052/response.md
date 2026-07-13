# Dynamic household energy-resilience model

## Economic object and model

The object is a household's repeated choice among grid power, a generator, and a home retrofit. The six states combine insulation quality (`0,1,2`) and grid reliability (`0,1`). The household observes its state and one of two policy regimes, chooses an action, receives type-I extreme-value utility shocks, and transitions. Reliability transitions are action controlled; retrofit raises insulation by one step with probability 0.82. The solution concept is the unique fixed point of the discounted logit Bellman operator under the maintained finite-state specification.

The simulated population was declared before drawing: 1,200 households, 14 periods, 16,800 rows, seed 52077, with 600 households in each observed rebate regime (0 and 0.8). There was no redraw or outcome-conditioned survival.

## Estimation judgment

Controlled reliability probabilities were estimated from action-by-current-reliability transition counts. The preference/discount vector is `(insulation benefit, generator disutility, retrofit disutility, beta)`:

| object | insulation | generator | retrofit | beta |
|---|---:|---:|---:|---:|
| generating value | 1.150 | 1.350 | 2.100 | 0.910 |
| NFXP | 1.170 | 1.312 | 2.068 | 0.916 |
| two-step CCP minimum distance | 1.813 | 1.377 | 2.026 | 0.783 |

NFXP used six retained local starts; its negative log likelihood is 15,513.190 and Bellman residuals are at most `2.94e-12`. The CCP estimator is distinct: smoothed empirical conditional choice probabilities are inverted into choice-specific value differences, the action-0 value equation is solved, and structural parameters minimize those difference residuals. Its poorer recovery is reported rather than hidden.

The population mapping from four continuous primitives to exact policy log-odds plus controlled transition probabilities has numerical Jacobian rank 4 at the generating parameter. Singular values are `(21.456, 3.422, 2.001, 0.575)`. This warrants only a **continuous local population-rank result** under the maintained support, normalization, transition law, and equilibrium selection. It does not establish global point identification.

## Hard-restricted alternative

The restricted search imposed `beta <= 0.78` by the reparameterization `beta = 0.55 + 0.23 logistic(z)`, not by a penalty. The selected candidate is `(1.826, 1.294, 2.038, 0.779923)`, objective 15,515.525, a gap of 2.335 from NFXP. Realized slack is `7.7131e-05`; feasibility tolerance is `1e-12`. The candidate is feasible, but the search is numerical rather than proof of a global restricted optimum.

Audit metadata retains all 32 differential-evolution initial candidates and their objectives, 30 generation-best records, all eight polishing starts and terminals, and all six unrestricted local starts and terminals.

## Policy support and incidence

Rebates 0 and 0.8 are observed policy regimes. The 0.4 result is explicitly **model-based interpolation**, not an observed regime or reduced-form causal estimate.

| rebate | private flow payoff | public transfer | real resource cost | social-welfare flow | retrofit share |
|---:|---:|---:|---:|---:|---:|
| 0.0 | 2.394 | 0.000 | 0.278 | 2.116 | 0.084 |
| 0.4 | 2.379 | 0.048 | 0.310 | 2.021 | 0.120 |
| 0.8 | 2.382 | 0.136 | 0.354 | 1.893 | 0.170 |

The accounting criterion is `private flow payoff - public transfers - real resource costs`; transfers are displayed separately and are not treated as resources. These are stationary model-implied flow comparisons conditional on the specification, not empirically validated welfare conclusions. Omitted distributional weights, fiscal distortion, emissions, outage externalities, and liquidity constraints are failure conditions for normative use.

## Verification status

The independent verifier recomputed transition estimates from saved rows, rank arithmetic from the saved Jacobian, restricted-candidate slack, welfare identities, and search-metadata counts. Every checked object passed. Its coverage map explicitly excludes preference-estimator correctness, Bellman-solver independence, global identification, global-search optimality, normative completeness, and external validity; therefore no blanket pipeline PASS is claimed.

Claim status: simulated-data NFXP recovery is a reproducible demonstration; local population rank is supported only at the stated point and restrictions; the hard-restricted candidate is feasible; policy and welfare results are model-implied and provisional.

