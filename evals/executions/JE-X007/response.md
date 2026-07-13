Let

\[
D(\alpha)\equiv c+\alpha q>0,
\qquad
x(p,\alpha)\equiv \frac{p+\alpha v}{D(\alpha)}.
\]

Assume \(T\ge 0\), \(p\in\mathbb R\), \(v,q,c>0\), and \(\alpha\ge0\). Allowing \(p<0\) covers penalties as well as positive payments.

## 1. Provider optimum, including all boundaries

The provider solves

\[
\max_{t\in[0,T]}
U(t)
=
(p+\alpha v)t-\frac{c+\alpha q}{2}t^2.
\]

Because

\[
U''(t)=-(c+\alpha q)<0,
\]

the objective is strictly concave and the optimum is unique. The unconstrained candidate is \(x(p,\alpha)\), so the global constrained solution is

\[
\boxed{
t^*(p,\alpha)
=
\Pi_{[0,T]}
\left(
\frac{p+\alpha v}{c+\alpha q}
\right)
}
\]

where \(\Pi_{[0,T]}\) denotes projection onto \([0,T]\). Equivalently, for \(T>0\),

\[
t^*=
\begin{cases}
0,
&
p+\alpha v\le 0,\\[4pt]
\dfrac{p+\alpha v}{c+\alpha q},
&
0<p+\alpha v<(c+\alpha q)T,\\[10pt]
T,
&
p+\alpha v\ge(c+\alpha q)T.
\end{cases}
\]

At either equality the optimum remains unique: it is \(0\) at the lower threshold and \(T\) at the upper threshold. If \(T=0\), then \(t^*=0\) for every parameter value.

## 2. Social optimum

The stated welfare criterion excludes payment because it treats payment as a pure transfer:

\[
W(t)=B(t)-C(t)
=vt-\frac{q+c}{2}t^2.
\]

Since \(W''(t)=-(q+c)<0\), the unique social optimum is

\[
\boxed{
t^S
=
\Pi_{[0,T]}
\left(\frac{v}{q+c}\right)
=
\min\left\{T,\frac{v}{q+c}\right\}.
}
\]

Because \(v>0\), the lower bound is relevant only when \(T=0\).

This welfare result is conditional on excluding distortionary financing, insurer administrative costs, congestion, other patients’ displaced care, distributional weights, and any provider income effect not treated as a transfer.

## 3. Payment comparative statics

At an interior solution,

\[
\frac{\partial t^*}{\partial p}
=
\frac{1}{c+\alpha q}>0.
\]

Globally, projection implies that \(t^*\) is continuous and weakly increasing in \(p\).

For any finite increase \(p_2>p_1\), with \(T>0\),

\[
t^*(p_2,\alpha)>t^*(p_1,\alpha)
\]

if and only if

\[
\boxed{
p_2>-\alpha v
\quad\text{and}\quad
p_1<(c+\alpha q)T-\alpha v.
}
\]

Thus the statement “higher payment raises treatment” is:

- **Strictly true** for a marginal change in the interior region.
- **Weakly true globally**: higher payment never lowers treatment.
- **Not strictly true** when both payment values leave the provider at \(t=0\), when both leave the provider at \(t=T\), or when payment rises from the upper threshold.
- **False as a weak monotonicity claim only if the model’s maintained assumptions fail**; within this model, treatment cannot fall when \(p\) rises.

The interior payment response decreases with altruism:

\[
\frac{\partial^2 t^*}{\partial p\,\partial\alpha}
=
-\frac{q}{(c+\alpha q)^2}<0.
\]

## 4. Altruism comparative statics

At an interior solution,

\[
\frac{\partial t^*}{\partial\alpha}
=
\frac{vc-qp}{(c+\alpha q)^2}.
\]

Therefore, altruism raises treatment if \(p<vc/q\), has no interior effect if \(p=vc/q\), and lowers treatment if \(p>vc/q\).

Economically, increasing \(\alpha\) moves the provider’s unconstrained choice toward the patient-benefit maximizer \(v/q\), not automatically toward the social optimum \(v/(q+c)\). The two differ because the social planner also counts treatment cost.

### Exact local condition when capacity does not bind socially

First suppose

\[
T\ge \frac{v}{q+c},
\]

so \(t^S=v/(q+c)\). At an interior provider solution,

\[
t^*-t^S
=
\frac{p(q+c)+vc(\alpha-1)}
{(c+\alpha q)(q+c)}.
\]

Define

\[
N\equiv p(q+c)+vc(\alpha-1),
\qquad
A\equiv vc-qp.
\]

Since \(\operatorname{sign}(t^*-t^S)=\operatorname{sign}(N)\) and
\(\operatorname{sign}(\partial t^*/\partial\alpha)=\operatorname{sign}(A)\), a marginal increase in altruism:

- **Strictly moves treatment toward the social optimum** iff

\[
\boxed{NA<0;}
\]

- **Weakly moves treatment toward it** iff

\[
\boxed{NA\le0;}
\]

- **Moves treatment away from it** iff

\[
\boxed{NA>0.}
\]

Equality includes either \(t^*=t^S\) or a locally zero altruism effect.

### Exact local condition when capacity binds socially

If

\[
T<\frac{v}{q+c},
\]

then \(t^S=T\). For an interior provider choice, all feasible treatment lies below the social optimum. Hence a marginal increase in altruism:

- strictly moves treatment toward \(t^S\) iff \(vc-qp>0\);
- has no local effect iff \(vc-qp=0\);
- moves treatment away from \(t^S\) iff \(vc-qp<0\).

At a strict provider corner, treatment is locally constant in \(\alpha\), so the movement is weak rather than strict. At a threshold where the projection changes regime, the ordinary two-sided derivative may not exist; the exact criterion for a finite change \(\alpha_2>\alpha_1\) is simply

\[
\left|t^*(p,\alpha_2)-t^S\right|
\begin{cases}
<\\
=\\
>
\end{cases}
\left|t^*(p,\alpha_1)-t^S\right|,
\]

corresponding respectively to strict movement toward, no change in distance, or movement away.

## 5. Numerical examples

Take \(v=q=c=1\) and \(T=3\). Then \(t^S=1/2\).

### Payment raises treatment in the interior

With \(\alpha=1\),

\[
t^*(p,1)=\frac{p+1}{2}
\]

while the solution remains interior. Raising \(p\) from \(0\) to \(0.4\) raises treatment from \(0.5\) to \(0.7\).

But the overbroad statement “every payment increase strictly raises treatment” is false. If \(T=1\), \(\alpha=0\), and \(p\) rises from \(1\) to \(2\), treatment remains at the capacity constraint:

\[
t^*(1,0)=t^*(2,0)=1.
\]

### Higher altruism can move treatment away from the social optimum

Again take \(v=q=c=1\), \(T=3\), but set \(p=0\). Then

\[
t^*(0,\alpha)=\frac{\alpha}{1+\alpha}.
\]

At \(\alpha=1\),

\[
t^*=\frac12=t^S.
\]

Raising altruism to \(\alpha=2\) gives

\[
t^*=\frac23,
\]

which is farther above the social optimum. Thus “higher altruism always moves treatment toward the social optimum” is false. Once the provider puts social weight one on patient benefit, further increasing that weight overweights benefit relative to real treatment cost.

A second useful counterexample goes in the other direction. With \(p=2\),

\[
t^*(2,\alpha)=\frac{2+\alpha}{1+\alpha},
\qquad
\frac{\partial t^*}{\partial\alpha}<0.
\]

More altruism reduces treatment because payment has already induced treatment beyond the patient-benefit maximizer \(v/q=1\).

## 6. Maintained assumptions and falsification checks

The derivation assumes:

- treatment is divisible and chosen from a fixed interval \([0,T]\);
- \(p,v,q,c,\alpha\) are known when treatment is chosen;
- the provider is a single decision-maker with a stable, quasi-linear objective;
- payment is linear and exogenous to the provider’s current treatment choice;
- patient benefit and treatment cost are correctly represented by the stated quadratics;
- there are no fixed costs, income effects, uncertainty, multitasking, capacity spillovers, strategic payer response, or dynamic effects;
- payment is a pure transfer in the stated welfare function.

Observable restrictions that could defeat the model include:

- a credibly exogenous payment increase lowers treatment away from regime or capacity changes;
- treatment responds to payment at a strict upper or lower corner;
- interior payment sensitivity rises with independently measured \(\alpha\), contrary to
  \(\partial^2t^*/(\partial p\,\partial\alpha)<0\);
- the sign change in altruism’s treatment effect does not track the predicted threshold \(p=vc/q\);
- observed treatment choices cannot be reconciled with the projected linear-index form;
- measured marginal patient benefits or real treatment costs violate the assumed linear schedules.

The welfare comparison additionally fails if payment has real financing costs, if provider income receives independent social weight, or if treatment affects other patients, quality, access, or future health. In those cases \(W=B-C\) must be replaced before drawing policy conclusions.

**Derivation status:** verified piecewise over \(t\in[0,T]\) for the stated parameter domain and welfare criterion.
