# Structural IO simulation, estimation, and counterfactuals

## Research judgment

The valid excluded-cost-shifter design recovers the demand primitives well in repeated samples, while naive OLS and the deliberately invalid design do not recover price sensitivity. In the main sample, true `(beta_x, alpha)=(1.25,1.10)`, OLS gives `(1.239,0.682)`, and valid IV gives `(1.275,1.078)`. Across 30 independently simulated samples, valid IV mean estimates are `(1.249,1.097)`; alpha RMSE is 0.065. The invalid design has a very strong first stage but estimates mean alpha 0.553, demonstrating that relevance cannot repair exclusion. These are simulated-data recovery results conditional on the stated model, not empirical claims about an actual industry.

## Economic environment and data mapping

There are 180 independent markets and three inside goods plus an outside good. Market size is normalized to one, so shares equal quantities; all aggregate monetary values below sum over 180 unit-size markets. Firm 1 owns goods 1 and 2, and firm 2 owns good 3. Each market proceeds as follows: `(x,z,w,xi,omega)` are realized; firms observe all payoff-relevant shocks and simultaneously choose prices; consumers observe products and prices and choose one option. The equilibrium concept is a static, pure-strategy, multiproduct Bertrand-Nash price equilibrium.

For product `j` in market `t`, mean utility is

`delta_jt = beta_x x_jt - alpha p_jt + xi_jt`,

and simple-logit shares are `s_jt=exp(delta_jt)/(1+sum_k exp(delta_kt))`, with outside share `s_0t=1/(1+sum_k exp(delta_kt))`. Marginal cost is linear:

`c_jt = gamma_0 + gamma_z z_jt + gamma_w w_jt + omega_jt`,

with true `(gamma_0,gamma_z,gamma_w)=(2.25,0.65,0.28)`. The common latent shock gives sample `corr(xi,omega)=0.633`; equilibrium pricing then gives `corr(p,xi)=0.335`, making price endogenous. The valid excluded shifter `z` is drawn independently of `xi`, affects cost and price, and is absent from utility. No selection or redraw is conditioned on realized costs.

The econometrician observes market/product identifiers, ownership, `p,s,s0,x,z,w`, but not `xi,omega` or true cost. The estimating equation is `log(s_jt)-log(s_0t)=beta_x x_jt-alpha p_jt+xi_jt`.

## Supply and markup recovery

Let `O_kj=1` when products `k` and `j` have the same owner. With per-unit tax `tau`, each price FOC is

`0 = s_k + sum_j O_kj (p_j-c_j-tau) (partial s_j/partial p_k)`,

where `partial s_j/partial p_k = -alpha s_j(1{j=k}-s_k)`. Defining `H_kj=-O_kj partial s_j/partial p_k`, markups solve `H(p-c-tau)=s`. Using valid-IV alpha, recovered costs yield `(gamma_0,gamma_z,gamma_w)=(2.230,0.661,0.274)`, mean absolute marginal-cost error 0.0215, mean markup 1.070, minimum recovered cost 1.214, and no nonpositive costs. The worst markup-matrix condition number is 47.1.

## Identification, estimation, and diagnostics

`beta_x` is identified by independent variation in observed demand characteristic `x` that shifts relative utility conditional on price. `alpha` is identified by `z` and `w`: they shift marginal cost, pass through equilibrium prices, and—by construction—do not enter utility or covary with `xi`. Thus price variation induced by supply conditions separates consumers' response to price from the positive demand shock embedded in observed equilibrium price. This argument, rather than the instrument label, is the identifying content.

The valid 2SLS/GMM design uses `[1,x,z,w]` as instruments for `[1,x,-p]`. Its excluded-variable first-stage F is 902.3, the moment Jacobian has full column rank, Jacobian condition number 86.6, and normal-matrix condition number 1,200. The largest sample moment is 0.0071. These are finite-sample geometry and numerical diagnostics, not a proof of population identification. Analytic share-price derivatives match central differences to `1.94e-11`.

The deliberately weak DGP reduces the sole excluded shifter's cost coefficient to 0.015. Its first-stage F is 0.685; IV gives `(beta_x,alpha)=(1.185,0.197)` with alpha SE 2.295, Jacobian condition 3,146, and normal-matrix condition 1.86 million. Near-zero moments therefore do not imply useful identification.

The invalid design includes `qbad=xi+noise`. Despite first-stage F 880.7, it estimates alpha 0.572 in the main sample and 0.553 on average across 30 samples. Its main-sample maximum moment is 0.249. Markup inversion under this invalid estimate produces one nonpositive recovered marginal cost (`-0.158` in market 172, product 2), while mean absolute cost error rises to 0.966; that branch is diagnosed and retained, not used for counterfactuals.

Across 30 pre-specified seeds, valid IV succeeds 30/30 times: beta bias -0.0005, alpha bias -0.0030, alpha RMSE 0.0653, and median first-stage F 865.7. Invalid IV also numerically “succeeds” 30/30 times but has alpha bias -0.547 and RMSE 0.551. Numerical success is therefore kept distinct from estimator recovery.

## Counterfactuals

Counterfactuals use the true primitives and costs to isolate equilibrium computation from estimation error. Every market is solved from five starts. Acceptance requires both raw and share-scaled FOC residuals below `1e-8`, economically nonnegative markups, and no bound contact. All 180 markets solve in baseline, tax, and merger cases; maximum scaled residuals are `9.51e-12`, `9.41e-12`, and `6.67e-12`. One distinct root is detected per market across the searched starts. This supports “one equilibrium detected by this search,” not global uniqueness.

| Scenario | Mean price | Consumer surplus | Producer profit net of tax | Tax revenue | Real production cost |
|---|---:|---:|---:|---:|---:|
| Baseline | 3.435 | 42.524 | 45.042 | 0.000 | 90.958 |
| Per-unit tax `tau=0.35` | 3.749 | 31.958 | 33.601 | 10.899 | 70.442 |
| Full merger, all three goods jointly owned | 3.548 | 38.962 | 45.392 | 0.000 | 84.423 |

Consumer surplus is `sum_t log(1+sum_j exp(delta_jt))/alpha`. Producer profit is `sum (p-c-tau)s`; tax revenue is `sum tau*s`; real production cost is `sum c*s`. Real cost is reported separately and is already embedded in producer profit, so it must not be subtracted again when forming a conventional total-surplus measure. No Pareto or welfare ranking is asserted: doing so would require a declared criterion, treatment of tax revenue, distributional weights, and any omitted externalities.

## Preserved failures and claim status

An initial absolute-residual solver falsely classified high-price, vanishing-share points as multiple roots (up to five detected; 132 baseline markets affected). The complete initial output is retained. Re-solving normalized FOCs removed these false roots. A second intermediate run that used cost-support redraws is also retained because conditioning on cost positivity could compromise exclusion. The final DGP uses bounded `z`, a higher intercept, and no redraw. The final equilibrium claims are `local/search-verified`: residuals and multiple starts are strong computational checks but not a global uniqueness proof. The recovery claim is supported for this declared simulated DGP and 30-seed experiment; external validity is not at issue.
