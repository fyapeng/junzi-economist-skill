# Complete equilibrium and welfare analysis

Let
\[
b\equiv \theta-F,\qquad x\equiv b+s=\theta+s-F.
\]
An adopter's payoff is (x+\gamma a_j), whereas nonadoption pays zero. Thus, against an opponent who adopts with probability (q), adoption is optimal iff
\[
x+\gamma q\ge 0.
\]
All statements below allow (F>0, s\ge0, \gamma\ge0), and unrestricted \(\theta\).

## 1. Complete Nash-equilibrium correspondence

Write (N=(0,0)), (B=(1,1)), and describe a mixed strategy by its adoption probability.

### If \(\gamma>0\)

| Parameter region | Nash equilibria |
|---|---|
| (x<-gamma) | (N) only |
| (x=-\gamma) | (N) and (B); (B) is weak |
| (-\gamma<x<0) | (N), (B), and one symmetric completely mixed equilibrium (p_1=p_2=p^*=-x/\gamma\in(0,1)) |
| (x=0) | (N) and (B); (N) is weak |
| (x>0) | (B) only |

There are no asymmetric pure equilibria and no other mixed equilibria. Indeed, an asymmetric pure profile would require simultaneously (x\ge0) for its adopter and (x+\gamma\le0) for its nonadopter, which is impossible for \(\gamma>0\). At either boundary (x=-\gamma) or (x=0), the interior mixed equilibrium collapses to a pure profile; it does not generate a continuum of equilibria.

### If \(\gamma=0\)

The decisions are independent: (N) is unique if (x<0), (B) is unique if (x>0), and if (x=0) **every** strategy pair ((p_1,p_2)\in[0,1]^2) is a Nash equilibrium. Hence all four pure profiles, including the one-adopter profiles, are equilibria only in this fully indifferent degenerate case.

## 2. Strict coordination, basins, and risk dominance

Suppose \(\gamma>0\) and (-\gamma<x<0). The mixed threshold is
\[
p^*=\frac{F-\theta-s}{\gamma}=-\frac{x}{\gamma}.
\]
Against believed adoption probability (q), adoption is the unique best response for (q>p^*), nonadoption is the unique best response for (q<p^*), and both actions are best responses at (q=p^*). Under the usual symmetric best-response/tipping interpretation, initial beliefs above (p^*) lie in the basin of (B), those below it in the basin of (N), and the threshold itself is the unstable mixed equilibrium. For unrestricted asynchronous or heterogeneous adjustment, a dynamic protocol must be supplied before “basin” has a unique behavioral meaning.

The loss from unilaterally leaving (B) is (x+\gamma); the loss from unilaterally leaving (N) is (-x). Therefore
\[
B\text{ risk-dominates }N \iff x+\gamma>-x
\iff x>-\frac{\gamma}{2}
\iff p^*<\frac12.
\]
(N) risk-dominates when (x<-\gamma/2), and they tie at (x=-\gamma/2). With weak language, replace (>) by \(\ge\). Risk dominance is a refinement or selection **criterion** based on relative deviation losses/basin size; it is not an observed selection law and does not establish which equilibrium organizations will play.

## 3. Transfer-free social welfare

Treating the subsidy as a pure transfer, exclude (s) from the resource account. Total welfare with zero, one, or two adopters is
\[
W_0=0,\qquad W_1=b,\qquad W_2=2(b+\gamma).
\]
The complete welfare-maximizing correspondence is
\[
\mathcal A^W=
\begin{cases}
\{0\},&b+\gamma<0,\\
\{0,2\},&b+\gamma=0,\ \gamma>0,\\
\{0,1,2\},&b=\gamma=0,\\
\{2\},&b+\gamma>0.
\end{cases}
\]
Here “1” means either symmetric one-adopter allocation. One adopter is never uniquely optimal: to beat zero requires (b\ge0), while to beat two requires (b+2\gamma\le0); together these imply (b=\gamma=0), where all adoption counts tie.

This welfare ranking does not select among Nash equilibria. For example, at (b=x=-1/4, \gamma=1, s=0), both (N) and (B) are equilibria and (B) uniquely maximizes welfare; (N) remains an equilibrium.

### Inefficiency regions

* **Coordination failure is possible** when (b+\gamma>0) but (x\le0): (B) is socially unique, yet (N) is also a Nash equilibrium (weakly at (x=0)).
* **Strict excess adoption is possible** when (b+\gamma<0) but (x+\gamma\ge0): (N) is socially unique, yet (B) is a Nash equilibrium. This can only be created or sustained by the subsidy wedge, because at (s=0), (x=b).
* At (b+\gamma=0), (N) and (B) are welfare-tied, so neither is strictly excessive or deficient under this welfare criterion.

## 4. What subsidy changes equilibrium status?

Because (x=b+s):

* (B) is a Nash equilibrium iff (s\ge-b-\gamma) (also respecting (s\ge0)).
* (B) is the **unique** equilibrium iff (b+s>0).
* In strict coordination, (B) is strictly risk-dominant but not unique iff
  \[
  -\frac{\gamma}{2}<b+s<0.
  \]
  Equality on the left is the risk-dominance tie; equality on the right still leaves the weak equilibrium (N).

If (b>0), (s=0) already makes (B) unique. If (b\le0), the set of unique-(B) subsidies is (s>-b). Its infimum is (-b), but the infimum is not attained: at (s=-b), (x=0) and (N) remains a weak equilibrium. Thus a “minimum subsidy guaranteeing strict uniqueness” need not exist.

None of these statements supplies an equilibrium selection mechanism. A subsidy that merely changes the equilibrium correspondence cannot be assigned a realized allocation without an additional selection device or dynamic.

## 5. Real financing cost

Now suppose financing a subsidy entails a real resource cost \(\lambda s\) per actual adopter, with \(\lambda>0\). Organizational payoffs and hence the Nash correspondence above are unchanged, but policy welfare becomes
\[
W_0^\lambda(s)=0,\qquad
W_1^\lambda(s)=b-\lambda s,\qquad
W_2^\lambda(s)=2(b+\gamma-\lambda s).
\]
For a fixed (s), replace (b) by (c=b-\lambda s) in the welfare correspondence:
\[
\arg\max_n W_n^\lambda(s)=
\begin{cases}
\{0\},&c+\gamma<0,\\
\{0,2\},&c+\gamma=0,\ \gamma>0,\\
\{0,1,2\},&c=\gamma=0,\\
\{2\},&c+\gamma>0.
\end{cases}
\]
Thus inducing both adoption passes the comparison with no adoption iff
\[
b+\gamma-\lambda s>0
\]
(ties at equality). The payment (s) itself is a transfer, but \(\lambda s\) is a resource loss and cannot be canceled from the social account.

Policy evaluation must be set-valued absent selection. At subsidy (s), report
\[
\mathcal W^{NE}(s)=\{W^\lambda(a;s):a\in NE(s)\},
\]
not a single predicted welfare number. For independent mixed probabilities ((p_1,p_2)), the expected value entering this set is
\[
\mathbb E W^\lambda=(b-\lambda s)(p_1+p_2)+2\gamma p_1p_2;
\]
in the strict symmetric mixed equilibrium, set (p_1=p_2=p^*). A sufficient robust comparison between two policies would require every equilibrium welfare under the proposed policy to exceed every equilibrium welfare under the baseline; other comparisons require an explicit selection rule or criterion.

For (b\le0), a welfare-positive subsidy making (B) unique exists iff there is an (s) satisfying
\[
-b<s<\frac{b+\gamma}{\lambda},
\]
equivalently (b+\gamma>\lambda(-b)), or \(\gamma>(1+\lambda)(-b)\). This is an existence result; the strict lower bound again means the infimum uniqueness subsidy is not attained. At the infimum, limiting both-adoption welfare is (2[b+\gamma+\lambda b]), but actual uniqueness still requires a slightly larger subsidy.

## 6. Numeric examples

Take (F=2) throughout.

| Case | \((\theta,s,\gamma)\) | Result |
|---|---:|---|
| Unique none | \((0,0,1)\) | (b=x=-2<-1): only (N) |
| Unique both | \((3,0,1)\) | (b=x=1>0): only (B) |
| Strict multiplicity, (B) risk-dominant | \((7/4,0,1)\) | (x=-1/4, p^*=1/4) |
| Strict multiplicity, (N) risk-dominant | \((5/4,0,1)\) | (x=-3/4, p^*=3/4) |
| Risk tie | \((3/2,0,1)\) | (x=-1/2, p^*=1/2) |
| Lower equality | \((1,0,1)\) | (x=-\gamma): exactly (N,B); also (W_0=W_2=0) |
| Upper equality | \((2,0,1)\) | (x=0): exactly (N,B); (N) weak |
| Full degeneracy | \((2,0,0)\) | every mixed-strategy pair is an equilibrium; all adoption counts welfare-tie |

For a fiscal counterexample, let (F=2, \theta=1.4), so (b=-0.6), with \(\gamma=1\) and \(\lambda=1\). At (s=0), (x=-0.6) and the equilibrium set is \(\{N,B,p^*=0.6\}\). Raising the subsidy to (s=0.7) makes (x=0.1), so (B) becomes unique, but
\[
W_2^\lambda(0.7)=2(-0.6+1-0.7)=-0.6<0=W_0.
\]
The subsidy changes—and even uniquely resolves—the equilibrium set while failing the fiscal welfare test. This also shows why “any equilibrium-changing subsidy improves welfare” is false.

**Derivation status:** verified piecewise over the stated domain. The accompanying deterministic rational-grid script independently enumerates pure best responses and checks thresholds, boundaries, welfare correspondences, fiscal classifications, and the two preserved counterexamples.
