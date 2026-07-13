# Moral hazard with two efforts and limited liability

Let
\[
\Delta=p_H-p_L>0,\qquad b=\frac{k}{\Delta},
\]
and write the wage spread as \(d=w_1-w_0\). The agent's expected utility under effort \(e\) is expected wage minus effort cost. Thus high effort is incentive compatible iff \(d\ge b\), while low effort is incentive compatible iff \(d\le b\). Equalities require an effort tie-breaking rule.

## Least-cost high-effort contracts

High-effort participation and limited liability imply
\[
(1-p_H)w_0+p_Hw_1\ge u+k,\qquad w_0,w_1\ge0.
\]
Consequently the minimum expected wage is
\[
C_H=\max\{u+k,p_Hb\}.
\]
The full set of least-cost contracts is
\[
d\in[b,C_H/p_H],\qquad
w_0=C_H-p_Hd,\qquad w_1=C_H+(1-p_H)d.
\]
(Here \(p_H>0\) follows from \(0\le p_L<p_H\).) A canonical member uses \(d=b\):
\[
w_0=\max\{0,u+k-p_Hb\},\qquad w_1=w_0+b.
\]
The agent's rent above the outside option is
\[
R_H=C_H-k-u=\max\{0,p_Hb-k-u\}.
\]
Hence limited liability generates a strictly positive rent exactly when \(p_Hk/\Delta>u+k\).

For **strict** high-effort incentives, require \(d>b\). If \(u+k>p_Hb\), the same minimum \(C_H=u+k\) is attained by every \(d\in(b,(u+k)/p_H]\) with the wages above. If \(u+k\le p_Hb\), the infimum remains \(C_H=p_Hb\), but it is not attained: \((w_0,w_1)=(0,b+\varepsilon)\) approaches it as \(\varepsilon\downarrow0\). Thus the canonical \(d=b\) contract only weakly implements high effort and needs tie-breaking toward high effort.

## Least-cost low-effort contracts

Low-effort participation is \((1-p_L)w_0+p_Lw_1\ge u\). The minimum expected wage is
\[
C_L=u,
\]
and the agent gets zero rent. The full set of least-cost contracts is
\[
w_0=u-p_Ld,\qquad w_1=u+(1-p_L)d,
\]
where
\[
-\frac{u}{1-p_L}\le d\le
\begin{cases}
\min\{b,u/p_L\},&p_L>0,\\
b,&p_L=0.
\end{cases}
\]
The constant contract \((u,u)\), with \(d=0<b\), strictly induces low effort and attains \(C_L=u\), including when \(u=0\). More generally, the full least-cost **strict-low** family (weak participation, \(d<b\)) is given by the same wage formulas and
\[
d\in
\begin{cases}
[-u/(1-p_L),\,u/p_L],&p_L>0\text{ and }u/p_L<b,\\
[-u/(1-p_L),\,b),&p_L>0\text{ and }u/p_L\ge b,\\
[-u,\,b),&p_L=0.
\end{cases}
\]
Thus the limited-liability endpoint \(u/p_L\) is included when it binds strictly below \(b\), whereas the IC endpoint \(b\) is always excluded. A contract with \(d=b\), when feasible, only weakly implements low effort and needs tie-breaking toward low effort.

### Strict participation is a separate open constraint

If an indifferent agent rejects, participation must be strict. The consequences depend on effort and rent:

- For low effort, expected wage must exceed \(u\). Hence \(u\) is an unattained infimum, whether low IC is weak or strict.
- For weakly implemented high effort, if \(p_Hb>u+k\), limited liability already gives rent: the contract \((0,b)\) costs \(C_H=p_Hb\) and gives utility \(p_Hb-k>u\). Strict participation is therefore attained at the same minimum. If \(p_Hb\le u+k\), high IR binds at the weak-participation minimum, so \(C_H=u+k\) is an unattained infimum under strict participation.
- If both high IC and participation are strict, \(C_H\) is always only an unattained infimum. When \(u+k>p_Hb\), strict IC alone can attain \(u+k\), but strict participation opens the IR constraint. When \(u+k\le p_Hb\), strict IC already opens the relevant boundary; strict participation is additionally binding at equality and slack near the infimum when \(p_Hb>u+k\).

These acceptance statements do not change the weak-participation contract sets above.

## Private mode choice under weak implementation, including all ties

With optimal effort-specific contracts, define
\[
\Pi_H=p_HV-C_H,\qquad \Pi_L=p_LV-u,\qquad \Pi_S=0.
\]
The complete, necessary-and-sufficient choice correspondence is
\[
M^P(V)=\arg\max_{m\in\{H,L,S\}}\{\Pi_H,\Pi_L,0\}.
\]
Equivalently:

- \(H\in M^P\) iff \(p_HV\ge C_H\) and \(\Delta V\ge C_H-u\).
- \(L\in M^P\) iff \(p_LV\ge u\) and \(\Delta V\le C_H-u\).
- \(S\in M^P\) iff \(p_HV\le C_H\) and \(p_LV\le u\).

Every displayed equality adds the tied mode; these conditions therefore cover two-way and three-way ties without an arbitrary principal tie-break. In particular, \(H=L\) at \(V=(C_H-u)/\Delta\); \(H=S\) at \(p_HV=C_H\); and \(L=S\) at \(p_LV=u\). A triple tie satisfies both zero-profit equalities (and hence the third equality automatically). If \(p_L=0,u=0\), low effort and shutdown tie at zero for every \(V\); high effort joins or dominates according to its payoff.

### Principal mode existence under strict effort implementation

Now retain weak participation but require strict effort IC. Low effort still has an attained minimum \(u\), so let
\[
A_L=\max\{p_LV-u,0\}
\]
denote the best attained low/shutdown payoff, and let \(\overline\Pi_H=p_HV-C_H\).

- If \(u+k>p_Hb\), strict high effort has an attained minimum. The ordinary argmax comparison applies with \(\Pi_H=\overline\Pi_H\), \(\Pi_L=p_LV-u\), and shutdown zero; all equality ties are attained.
- If \(u+k\le p_Hb\), \(\overline\Pi_H\) is only a supremum. If \(\overline\Pi_H>A_L\), the principal's contracting problem has **no maximizer**: strict-high contracts approach the superior payoff, every such contract can be improved, and the attained alternatives are inferior. If \(\overline\Pi_H\le A_L\), the maximizing modes are exactly the attained members of \(\arg\max\{p_LV-u,0\}\); high effort is absent. In particular, when \(\overline\Pi_H=A_L\), high effort is not an attained tied mode.

If both effort IC and participation are strict, both operating-mode cost bounds are open and neither mode has a least-cost contract. Writing the same suprema \(\overline\Pi_H=p_HV-C_H\) and \(\overline\Pi_L=p_LV-u\), shutdown is the unique maximizer if both are nonpositive; if either supremum is positive, the overall problem has no maximizer. This is an open-set existence result, not a tie-breaking convention.

## Social benchmark and the exact wedge

Treat \(u\) as the real value of the outside opportunity forgone when the agent takes the project. Transfers are socially neutral. Relative social surpluses are
\[
W_H=p_HV-k-u,\qquad W_L=p_LV-u,\qquad W_S=0,
\]
so \(M^S(V)=\arg\max\{W_H,W_L,0\}\). In particular,
\[
H\in M^S\iff \Delta V\ge k\quad\text{and}\quad p_HV\ge u+k.
\]
The private and social payoffs for low effort and shutdown coincide, whereas
\[
\Pi_H=W_H-R_H.
\]
Therefore:

- If \(p_Hb\le u+k\), then \(R_H=0\) and the private and social mode correspondences coincide for every \(V\), including all boundaries. Equality may make limited liability bind, but it creates neither rent nor an allocative wedge.
- If \(p_Hb>u+k\), limited liability creates the exact wedge \(R_H=p_Hb-u-k>0\): high effort is privately underselected, never overselected.

For a precise value-by-value statement in the binding region, put
\[
A=\max\left\{\frac{k}{\Delta},\frac{u+k}{p_H}\right\},\qquad
B=\max\left\{\frac{C_H-u}{\Delta},\frac{C_H}{p_H}\right\}.
\]
Then \(B>A\). The social and private choice correspondences differ exactly for \(V\in[A,B]\): at \(A\), society includes high effort while the principal does not; for \(A<V<B\), society uniquely wants high effort while the principal chooses low effort or shutdown; at \(B\), the principal is just indifferent between high effort and at least one non-high mode while society uniquely wants high effort. Below \(A\) both choose from the same low/shutdown set, and above \(B\) both uniquely choose high effort.

## Numerical examples

1. **No liability wedge.** Let \((p_L,p_H,k,u)=(0.2,0.6,2,2)\). Then \(\Delta=0.4\), \(b=5\), \(C_H=4\), and \((w_0,w_1)=(1,6)\) is least-cost. Rent is zero and private choices equal social choices. Strict high IC is also attained at cost \(4\), for example with any \(d\in(5,20/3]\). At \(V=8\), high profit/surplus is \(0.8\), low is \(-0.4\), so high is uniquely chosen.
2. **Positive rent, underprovision, and strict-IC nonexistence.** Let \((p_L,p_H,k,u)=(0.2,0.6,2,0)\). Then \(b=5\), \(C_H=3\), the least-cost canonical contract is \((0,5)\), and rent is \(1\). Here \(A=5\), \(B=7.5\). At \(V=6\), society prefers high (\(1.6\) versus \(1.2\)), but the principal prefers low (\(1.2\) versus \(0.6\)). At \(V=7.5\), weak implementation ties high and low at \(1.5\); under strict high IC, high only approaches \(1.5\), so low is the sole attained maximizing mode. At \(V=8\), the strict-high profit supremum \(1.8\) exceeds low profit \(1.6\), so no strict-IC maximizing contract exists.
3. **Degenerate low/shutdown tie.** If \(p_L=0,u=0\), the least-cost low contract is \((0,0)\); low effort and shutdown both yield zero privately and socially for every \(V\). Other ties are determined by the high-effort payoff as above.

## What the maintained assumptions are doing

- **Negative wages:** without limited liability (and assuming transfers are enforceable and the agent can pay), high effort can always be delivered at expected wage \(u+k\); the liability rent and wedge disappear. Wage spreads and levels can be adjusted using negative failure payments. Strict high incentives can also be attained at that expected cost. Wealth or bankruptcy constraints would reintroduce bounds.
- **Risk-averse agent:** expected wage no longer summarizes utility. Incentives require a utility spread, while insurance favors smoother consumption; the least-cost contract solves a nonlinear insurance-incentive problem. The formulas above generally do not survive and depend on utility and reservation consumption/wealth.
- **Limited principal commitment:** a promised success wage may not be credible ex post. One must specify enforcement, renegotiation, repeated interaction, bonding, or relational-contract constraints. Feasible incentives can shrink or disappear; the commitment solution above is not valid merely with a modified threshold.

The derivation is **verified-piecewise**: the analytic argument covers the corners, weak/strict inequalities, participation ties, open-set existence cases, and mode-choice boundaries. The accompanying deterministic program is a finite regression/property check—using selected parameter cases and a wage grid augmented with analytic candidates and boundaries—not a proof over the continuous parameter or contract spaces.
