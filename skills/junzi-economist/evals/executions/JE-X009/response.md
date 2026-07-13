Let

\[
B(t)=4t-t^2,\qquad C(t)=\frac{t^2}{2},
\qquad t\in[0,2].
\]

Assume \(p\ge0\) and \(\alpha\ge0\) are known when the physician chooses treatment, treatment is divisible, and the physician’s stated objective is complete.

## 1. Globally constrained choices

The physician maximizes

\[
U(t)=(p+4\alpha)t-\left(\alpha+\frac12\right)t^2.
\]

Because

\[
U''(t)=-(1+2\alpha)<0,
\]

the solution is unique. The unconstrained optimum is

\[
x(p,\alpha)=\frac{p+4\alpha}{1+2\alpha}.
\]

Since \(p,\alpha\ge0\), \(x\ge0\). Moreover,

\[
x(p,\alpha)\ge2
\iff p+4\alpha\ge2+4\alpha
\iff p\ge2.
\]

Therefore,

\[
\boxed{
t^P(p,\alpha)
=
\min\left\{2,\frac{p+4\alpha}{1+2\alpha}\right\}
=
\begin{cases}
\dfrac{p+4\alpha}{1+2\alpha},&0\le p<2,\\[8pt]
2,&p\ge2.
\end{cases}
}
\]

This includes all boundaries:

- \(p=\alpha=0\) gives \(t^P=0\);
- \(p=2\) gives \(t^P=2\) for every \(\alpha\);
- \(p>2\) remains at the capacity corner \(t^P=2\).

Social welfare is

\[
W(t)=B(t)-C(t)=4t-\frac32t^2.
\]

Because \(W''(t)=-3<0\), its unconstrained optimum is \(4/3\), which lies in \([0,2]\). Thus

\[
\boxed{t^S=\frac43.}
\]

Payment is absent from welfare because it is assumed to be a pure transfer.

## 2. General finite-change classification

For any initial and final physician choices \(t_1,t_2\), define their distances from the social optimum by

\[
d_i=\left|t_i-\frac43\right|.
\]

The finite change is:

\[
\begin{cases}
\text{strictly closer},&d_2<d_1,\\
\text{same distance},&d_2=d_1,\\
\text{farther},&d_2>d_1.
\end{cases}
\]

Both payment and altruism are weakly increasing treatment in this particular parameterization. Hence \(t_2\ge t_1\), and

\[
d_2^2-d_1^2
=
(t_2-t_1)\left(t_1+t_2-\frac83\right).
\]

Consequently:

- if \(t_2=t_1\), distance remains unchanged;
- if \(t_2>t_1\), treatment moves

\[
\boxed{
\begin{aligned}
\text{strictly closer}
&\iff t_1+t_2<\frac83,\\
\text{to the same distance}
&\iff t_1+t_2=\frac83,\\
\text{farther}
&\iff t_1+t_2>\frac83.
\end{aligned}}
\]

These conditions cover movements that cross the social optimum. Merely checking whether treatment rises is insufficient: an increase can reduce, preserve, or enlarge the distance.

## 3. Finite payment increase

Hold \(\alpha\) fixed and let \(p_2>p_1\). Define

\[
t_i=
\min\left\{2,\frac{p_i+4\alpha}{1+2\alpha}\right\}.
\]

Because \(t^P\) is strictly increasing in \(p\) below the cap and constant above it,

\[
t_2=t_1\iff p_1\ge2.
\]

Therefore the necessary and sufficient conditions are:

\[
\boxed{
\begin{array}{ll}
\text{strictly closer}
&
\iff p_1<2
\ \text{and}\ 
t_1+t_2<\dfrac83,
\\[6pt]
\text{same distance}
&
\iff
p_1\ge2
\quad\text{or}\quad
\left[p_1<2\ \text{and}\ t_1+t_2=\dfrac83\right],
\\[6pt]
\text{farther}
&
\iff p_1<2
\ \text{and}\ 
t_1+t_2>\dfrac83.
\end{array}}
\]

These remain valid when \(p_2\ge2\), because \(t_2=2\) is inserted directly into the condition.

### Initial choice exactly socially optimal

For \(p_1<2\),

\[
t_1=\frac43
\iff
\frac{p_1+4\alpha}{1+2\alpha}=\frac43
\iff
p_1=\frac{4(1-\alpha)}{3}.
\]

This is feasible with \(p_1\ge0\) exactly when \(0\le\alpha\le1\). Any strict payment increase then produces \(t_2>4/3\), so

\[
\boxed{d_1=0,\quad d_2>0: \text{ treatment moves farther}.}
\]

Calling this “weak movement toward” would be incorrect: starting at the benchmark, every nonzero movement increases distance.

## 4. Finite altruism increase

Hold \(p\) fixed and let \(\alpha_2>\alpha_1\). If \(p<2\),

\[
t^P(p,\alpha)=\frac{p+4\alpha}{1+2\alpha}
\]

and

\[
\frac{\partial t^P}{\partial\alpha}
=
\frac{4-2p}{(1+2\alpha)^2}>0.
\]

If \(p\ge2\), treatment is always capped at \(2\). Hence

\[
t_2=t_1\iff p\ge2.
\]

Let

\[
t_i=
\min\left\{2,\frac{p+4\alpha_i}{1+2\alpha_i}\right\}.
\]

The necessary and sufficient conditions are:

\[
\boxed{
\begin{array}{ll}
\text{strictly closer}
&
\iff p<2
\ \text{and}\ 
t_1+t_2<\dfrac83,
\\[6pt]
\text{same distance}
&
\iff
p\ge2
\quad\text{or}\quad
\left[p<2\ \text{and}\ t_1+t_2=\dfrac83\right],
\\[6pt]
\text{farther}
&
\iff p<2
\ \text{and}\ 
t_1+t_2>\dfrac83.
\end{array}}
\]

Again, these are finite-change results, not local derivative claims.

### Initial choice exactly socially optimal

For \(p<2\),

\[
t^P(p,\alpha_1)=\frac43
\iff
p=\frac{4(1-\alpha_1)}{3}.
\]

Since treatment strictly increases with \(\alpha\) when \(p<2\), every \(\alpha_2>\alpha_1\) produces

\[
t_2>\frac43.
\]

Thus an altruism increase from a socially optimal initial choice necessarily moves treatment farther away. In particular, at \(p=0,\alpha_1=1\), the physician already implements the social optimum; increasing altruism induces overtreatment.

## 5. Parameter examples

### Payment changes

Set \(\alpha=0\), so \(t^P=\min\{2,p\}\).

- **Strictly closer:** \(p_1=0.5\), \(p_2=1\).  
  Then \(t_1=0.5\), \(t_2=1\), and \(t_1+t_2=1.5<8/3\).

- **Same distance by crossing the optimum:** \(p_1=1\), \(p_2=5/3\).  
  Then \(t_1+t_2=8/3\); both choices lie \(1/3\) from \(4/3\).

- **Same distance at the capacity corner:** \(p_1=2\), \(p_2=3\).  
  Both choices equal \(2\).

- **Farther, starting exactly at the optimum:** \(p_1=4/3\), \(p_2=3/2\).  
  The initial distance is zero and the final distance is \(1/6\).

### Altruism changes

Set \(p=0\), so \(t^P=4\alpha/(1+2\alpha)\).

- **Strictly closer:** \(\alpha_1=0\), \(\alpha_2=1/2\).  
  Treatment rises from \(0\) to \(1\).

- **Same distance by crossing the optimum:** \(\alpha_1=1/2\), \(\alpha_2=5/2\).  
  Treatment rises from \(1\) to \(5/3\), and both are \(1/3\) from \(4/3\).

- **Farther, starting exactly at the optimum:** \(\alpha_1=1\), \(\alpha_2=2\).  
  Treatment rises from \(4/3\) to \(8/5\).

For a same-distance altruism example at a corner, set \(p=2\) and take any \(\alpha_2>\alpha_1\); both choices equal \(2\).

## 6. Reproducible falsification check

The model produces sharp restrictions:

1. For every \(p<2\),

\[
\frac{\partial t^P}{\partial p}
=
\frac{1}{1+2\alpha}>0.
\]

2. For every \(p<2\),

\[
\frac{\partial t^P}{\partial\alpha}
=
\frac{4-2p}{(1+2\alpha)^2}>0.
\]

3. Treatment reaches \(2\) exactly when \(p\ge2\), independently of \(\alpha\).

A preregistered experiment or credible quasi-experiment that varies \(p\) while holding the treatment technology and capacity fixed can therefore falsify the model. In observations known to satisfy \(p<2\), a statistically and economically meaningful treatment decrease after an exogenous payment increase contradicts the model. Likewise, systematic treatment below \(2\) when \(p\ge2\), absent implementation failure or a changed capacity constraint, contradicts its corner prediction.

The algebra and all finite classifications can be reproduced with:

```python
def treatment(p, alpha):
    return min(2.0, (p + 4.0 * alpha) / (1.0 + 2.0 * alpha))

SOCIAL = 4.0 / 3.0

def classify(t1, t2, tol=1e-12):
    d1 = abs(t1 - SOCIAL)
    d2 = abs(t2 - SOCIAL)
    if d2 < d1 - tol:
        return "closer"
    if d2 > d1 + tol:
        return "farther"
    return "same"

def algebraic_classification(t1, t2, tol=1e-12):
    if abs(t2 - t1) <= tol:
        return "same"
    s = t1 + t2
    if s < 8.0 / 3.0 - tol:
        return "closer"
    if s > 8.0 / 3.0 + tol:
        return "farther"
    return "same"
```

A deterministic grid over \(p,\alpha\ge0\) should return identical labels from `classify` and `algebraic_classification`. Any disagreement away from numerical tolerance would falsify the stated finite-change characterization.

**Derivation status:** verified globally and piecewise for the stated feasible set, parameter restrictions, and welfare criterion.
