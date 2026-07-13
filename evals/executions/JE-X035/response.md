# Firm shutdown and the social benchmark

## 1. Environment and cost minimization

Let inputs satisfy \(K,L\ge 0\). For a required \(q>0\), the firm solves
\[
\min_{K,L\ge0}\ rK+wL+F
\quad\text{s.t.}\quad A K^\alpha L^{1-\alpha}\ge q.
\]
Because \(r,w>0\), the production constraint binds. The first-order conditions give
\[
\frac{r}{w}=\frac{\alpha}{1-\alpha}\frac{L}{K}.
\]
Define unit variable cost
\[
c\equiv \frac1A\left(\frac r\alpha\right)^\alpha
                  \left(\frac w{1-\alpha}\right)^{1-\alpha}>0.
\]
Then the unique conditional demands for every \(q>0\) are
\[
K^c(q)=\frac{\alpha cq}{r},\qquad
L^c(q)=\frac{(1-\alpha)cq}{w},
\]
and \(rK^c+wL^c=cq\). Hence
\[
C(q)=\begin{cases}
0,&q=0,\\
F+cq,&q>0.
\end{cases}
\]
At \(q=0\), positive input prices make \((K,L)=(0,0)\) the unique cost-minimizing choice and the avoidable cost is not paid. Thus \(C\) jumps at zero when \(F>0\).

The maintained regularity conditions \(A>0\), \(0<\alpha<1\), and \(r,w>0\) ensure a continuous, concave, constant-returns technology that is weakly increasing on \(\mathbb R_+^2\) and strictly increasing in either input when the other input is positive, together with finite positive unit cost and unique strictly positive conditional inputs for \(q>0\). This boundary qualification does not affect the \(q>0\) conditional demands, because positive output requires both inputs to be positive, or the unique \(q=0\) cost minimizer, which follows from \(r,w>0\). The Lagrange first-order conditions are globally sufficient: the input requirement set is convex, and the Cobb–Douglas isoquant is strictly convex. The formulas fail or require separate corner analysis if an input price is zero, \(\alpha\) is an endpoint, or productivity is nonpositive.

## 2. Global monopoly correspondence

Write \(d=a-c\). Shutdown gives profit zero. For \(q>0\),
\[
\pi(q)=(a-bq)q-cq-F=dq-bq^2-F.
\]
If \(d\le0\), every positive output yields strictly negative profit (also when \(d=0,F=0\)), so shutdown is uniquely optimal. If \(d>0\), define
\[
q_M=\frac{d}{2b},\qquad H_M=\frac{d^2}{4b}.
\]
Here \(H_M\) is the maximum operating profit before the fixed cost. The complete output correspondence is
\[
Q_M=\begin{cases}
\{0\},&d\le0,\\
\{q_M\},&d>0, F<H_M,\\
\{0,q_M\},&d>0, F=H_M,\\
\{0\},&d>0, F>H_M.
\end{cases}
\]
For an entering branch, price, factors, and economic profit are
\[
p_M=\frac{a+c}{2},\quad
K_M=\frac{\alpha c q_M}{r},\quad
L_M=\frac{(1-\alpha)cq_M}{w},\quad
\pi_M=H_M-F.
\]
For the shutdown branch they are \(q=K=L=0\), no fixed cost is paid, profit is zero, and \(P(0)=a\) is only the choke price—there is no transaction price. At \(F=H_M\), both listed allocations have profit zero.

## 3. Global social-planner correspondence

The planner uses gross willingness to pay
\[
B(q)=\int_0^q(a-bx)\,dx=aq-\frac b2q^2
\]
and subtracts real variable-input opportunity cost and the real fixed operating cost. Thus \(W(0)=0\) and, for \(q>0\),
\[
W(q)=B(q)-cq-F=dq-\frac b2q^2-F.
\]
If \(d\le0\), shutdown is uniquely optimal. If \(d>0\), define
\[
q_S=\frac{d}{b},\qquad H_S=\frac{d^2}{2b}=2H_M.
\]
The global planner correspondence is
\[
Q_S=\begin{cases}
\{0\},&d\le0,\\
\{q_S\},&d>0, F<H_S,\\
\{0,q_S\},&d>0, F=H_S,\\
\{0\},&d>0, F>H_S.
\end{cases}
\]
On the operating branch, \(p_S=P(q_S)=c\), factors are \(K_S=\alpha cq_S/r\) and \(L_S=(1-\alpha)cq_S/w\), and net surplus is \(H_S-F\). On the shutdown branch inputs and surplus are zero. At \(F=H_S\), shutdown and operation are exactly tied.

These are global, not merely first-order, results: on the positive-output branch each objective is a strictly concave quadratic, while comparison with the isolated shutdown payoff handles the discontinuity at zero.

## 4. Monopoly versus the benchmark

Conditional on both operating,
\[
q_M=\frac12q_S,
\]
so monopoly restricts output. Also \(H_M<H_S\) whenever \(a>c\); monopoly therefore never enters in a region where social operation is strictly undesirable.

For \(a>c\), the exact classifications are:

| Fixed cost | Monopoly | Planner |
|---|---|---|
| \(F<H_M\) | enter uniquely | enter uniquely |
| \(F=H_M\) | shutdown or enter | enter uniquely |
| \(H_M<F<H_S\) | shutdown uniquely | enter uniquely |
| \(F=H_S\) | shutdown uniquely | shutdown or enter |
| \(F>H_S\) | shutdown uniquely | shutdown uniquely |

Thus the **strict no-entry/entry wedge** is \(H_M<F<H_S\). In correspondence language, shutdown belongs to the monopoly choice and entry belongs to the planner choice on the closed interval \([H_M,H_S]\); its endpoints are set-valued for monopoly and planner, respectively. When \(a\le c\), both shut down uniquely for every \(F\ge0\), including \(a=c,F=0\).

## 5. Accounting without double counting

For any operating allocation let \(p=P(q)\), revenue \(R=pq\), consumer surplus \(CS=B(q)-R=\tfrac12bq^2\), factor payments \(V=cq=rK+wL\), operating producer surplus \(PS^{op}=R-V\), and economic profit \(\pi=R-V-F\). Then
\[
W=B(q)-V-F=CS+\pi=CS+PS^{op}-F.
\]
Revenue is a transfer from consumers to the firm. Factor payments are payments to input owners but simultaneously measure the real opportunity cost of inputs here; if factor suppliers are paid their opportunity cost, their supplier surplus is zero. Consequently one must not add \(R\) or \(V\) again to \(CS+\pi\). The fixed cost is treated as a real resource cost, not a transfer. If instead it were a pure fee paid to another domestic agent, it would enter distributional accounts as a transfer and would not be subtracted from aggregate real surplus.

## 6. Numerical examples

Take \(A=1,\alpha=1/2,r=w=1,b=1\). Then \(c=2\), and at any positive \(q\), \(K=L=q\).

1. **Both shut down:** \(a=1.5,F=0\). Since \(a<c\), both choose \(q=0\).
2. **Socially desirable entry rejected by monopoly:** \(a=6,F=6\). Here \(H_M=4\), \(H_S=8\). Monopoly shuts down; the planner chooses \(q_S=4\), with \(K=L=4\) and \(W=2\).
3. **Both enter:** \(a=6,F=2\). Monopoly chooses \(q_M=2,p_M=4,K=L=2,\pi=2\). The planner chooses \(q_S=4,p_S=2,K=L=4,W=6\).
4. **Threshold tie:** \(a=6,F=4=H_M\). Monopoly is indifferent between shutdown and \((q,p,K,L)=(2,4,2,2)\), each yielding zero profit. The planner enters uniquely at \(q=4\), with \(W=4\).

## 7. What changes in richer models

- A capacity bound clips the positive-output candidates and requires recomputing the gross gains at the capacity-constrained maximizers; it can create an additional kink and shadow value.
- Increasing returns generally destroy linear variable cost and may make cost minimization nonconvex; the fixed-cost comparison must then use the global cost envelope, not these quadratic thresholds.
- Endogenous quality makes demand and cost depend jointly on \((q,z)\); “output restriction” is no longer a sufficient welfare comparison because monopoly may alter quality too.
- Endogenous entry changes the object from one firm's shutdown decision to an equilibrium in firm counts, business stealing, strategic interaction, and possibly duplicated fixed costs. A planner must compare market-level surplus across entry configurations.

**Derivation status:** verified-global under the stated primitives. The accompanying deterministic program is a finite regression check, not a substitute for the analytic proof.

## 8. Finite verification

`verify.py` checks unit-cost/factor-demand duality, production feasibility, analytic versus boundary-enriched grid maxima, every regime in the table (plus \(a<c\) and \(a=c\)), the four numerical examples, and the accounting identities. Its actually observed output is recorded in `verification_output.txt`.
