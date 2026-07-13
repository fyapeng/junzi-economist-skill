# Binary-audit moral hazard with limited liability

## 1. Environment and notation

Let
\[
\Delta=p_1-p_0>0,\qquad a=\frac{k}{\Delta},\qquad
L=\frac{k p_0}{\Delta}=p_1a-k,
\]
where necessarily \(0\le p_0<p_1\le1\). Write the outcome-wage spread as \(d=t_1-t_0\). Expected wages are
\[
W_e=(1-p_e)t_0+p_et_1=t_0+p_ed.
\]
The unit's utility is \(W_e-ke\). High effort is weakly (strictly) implemented iff \(d\ge a\) (\(d>a\)); low effort is weakly (strictly) implemented iff \(d\le a\) (\(d<a\)). Limited liability is \(t_0,t_1\ge0\).

“Accept” below means an indifferent unit accepts, so participation is weak. “Reject” means an indifferent unit rejects, so participation is strict. Shutdown gives the principal zero and leaves the unit its outside utility \(U\).

## 2. Least-cost low-effort contracts

Under weak participation, the minimum expected wage is always \(C_0=U\), the rent is zero, and every minimizer can be written
\[
(t_0,t_1)=\bigl(U-p_0d,\ U+(1-p_0)d\bigr).
\]
For weak low-effort implementation, the complete spread correspondence is
\[
D_0^w=
\begin{cases}
[-U,\,a],&p_0=0,\\
[-U/(1-p_0),\,\min\{U/p_0,a\}],&0<p_0<p_1.
\end{cases}
\]
For strict low-effort implementation, replace the condition \(d\le a\) by \(d<a\):
\[
D_0^s=
\begin{cases}
[-U,\,a),&p_0=0,\\
[-U/(1-p_0),\,U/p_0]\cap(-\infty,a),&0<p_0<p_1.
\end{cases}
\]
These sets are nonempty even when \(U=0\): \(d=0<a\) works. Thus strict low-effort incentives do not destroy the minimum under weak participation.

Under strict participation, neither weak nor strict low-effort implementation has a least-cost contract. The cost infimum is \(U\), but it is unattained because every accepted contract must have \(W_0>U\). Contracts with \(d=0\) and \(t_0=t_1=U+\varepsilon\) approach it.

## 3. Least-cost high-effort contracts

Define
\[
A=U+k,\qquad H=\max\{A,p_1a\}=k+\max\{U,L\}.
\]
Here \(H\) is the high-effort cost infimum in all four convention combinations. Whenever a minimum cost \(C\) is attained, all its contracts are
\[
(t_0,t_1)=\bigl(C-p_1d,\ C+(1-p_1)d\bigr),
\]
with the spread restrictions in the following table.

| Effort implementation | Participation | Minimum? | Complete least-cost spread correspondence |
|---|---|---:|---|
| weak | accept | yes, always | \(d\in[a,H/p_1]\) |
| strict | accept | iff \(U>L\) | if it exists, \(C=A\) and \(d\in(a,A/p_1]\) |
| weak | reject | iff \(U<L\) | if it exists, \(C=p_1a\), \(d=a\), hence \((t_0,t_1)=(0,a)\) |
| strict | reject | never | empty; infimum \(H\) only |

The equality cases are substantive:

- If \(U=L\), then \(A=p_1a=H\). Weak effort with acceptance has the unique minimum \((0,a)\). Strict effort with acceptance has only an infimum. Weak effort with rejection also has only an infimum. Strict effort with rejection never has a minimum.
- If \(U<L\), weak/accept has the unique minimum \((0,a)\), with rent \(L-U>0\). Strict/accept has only an infimum because \(d>a\). Weak/reject attains \((0,a)\) because its limited-liability rent makes participation strict.
- If \(U>L\), weak/accept has the interval \(d\in[a,A/p_1]\); strict/accept deletes only its left endpoint and still attains cost \(A\). Under rejection, participation is open, so neither high-effort formulation attains its infimum.

For every attained high-effort minimum, rent is \(C-k-U\). Hence weak/accept rent is
\[
\rho_1=(L-U)_+.
\]
Strict/accept has zero rent whenever its minimum exists; weak/reject has rent \(L-U>0\) whenever its minimum exists. Where no minimum exists, it is more precise to report no least-cost rent. The limiting rent at the infimum is \((L-U)_+\), but strict participation means every accepted contract has strictly more rent than its relevant participation boundary.

The result includes \(p_0=0\): then \(L=0\). With \(U=0\), the weak/accept high contract is uniquely \((0,a)\), while strict effort or strict participation destroys attainment at that boundary. With \(U>0\), strict/accept has genuine minimizers \(d\in(a,(U+k)/p_1]\).

## 4. Principal's project-mode correspondence and nonexistence

Let the low- and high-mode **profit suprema** be
\[
P_0=p_0R-U,\qquad
P_1=p_1R-H=p_1R-k-\max\{U,L\}.
\]
Let \(I_0\) indicate whether the low-mode cost minimum exists and \(I_1\) whether the high-mode cost minimum exists:

| Convention | \(I_0\) | \(I_1\) |
|---|---:|---:|
| weak effort, accept | 1 | 1 |
| strict effort, accept | 1 | \(1\{U>L\}\) |
| weak effort, reject | 0 | \(1\{U<L\}\) |
| strict effort, reject | 0 | 0 |

This table, together with the following rule, is the complete principal correspondence including every tie. Set
\[
M=\max\{0,P_0,P_1\}.
\]
The maximizer correspondence is
\[
\mathcal M_P=
\{D:0=M\}
\cup\{L:P_0=M,\ I_0=1\}
\cup\{H:P_1=M,\ I_1=1\},
\]
provided this set is nonempty; attach to each selected active mode its complete least-cost contract correspondence above. If the displayed set is empty, the principal's overall contracting problem has **no maximizer**. In particular, an active mode whose supremum ties \(M\) but is unattained is not in the correspondence.

Equivalently, nonexistence occurs exactly when
\[
M>0\quad\text{and every active mode attaining the numerical supremum }M
\text{ has }I_e=0.
\]
Expanded by convention:

- weak/accept: a maximizer always exists;
- strict/accept with \(U\le L\): no maximizer iff \(P_1>\max\{0,P_0\}\); otherwise an attainable shutdown or low mode realizes the maximum (when \(U>L\), a maximizer always exists);
- weak/reject with \(U<L\): no maximizer iff \(P_0>\max\{0,P_1\}\); with \(U\ge L\), no maximizer iff \(\max\{P_0,P_1\}>0\);
- strict/reject: no maximizer iff \(\max\{P_0,P_1\}>0\).

These strict inequalities correctly handle ties. For example, if an unattained high supremum ties an attained low maximum, low is a maximizer; nonattainment of the tied high mode does not destroy existence.

For interpreting the numerical supremum before the attainment filter: shutdown is a supremum winner iff \(P_0\le0\) and \(P_1\le0\); low is one iff \(P_0\ge0\) and \(P_0\ge P_1\); high is one iff \(P_1\ge0\) and \(P_1\ge P_0\). All weak equalities give set-valued ties.

## 5. Social project-mode correspondence and the exact wedge

Transfers cancel socially, while employing the unit sacrifices outside utility \(U\). Incremental social values relative to shutdown are
\[
S_0=p_0R-U,qquad S_1=p_1R-k-U,qquad S_D=0.
\]
Therefore the complete social correspondence is
\[
\mathcal M_S=\arg\max_{m\in\{D,L,H\}}\{0,S_0,S_1\}.
\]
Equivalently,
\[
\begin{aligned}
D\in\mathcal M_S&\iff p_0R\le U\ \text{and}\ p_1R\le U+k,\\
L\in\mathcal M_S&\iff p_0R\ge U\ \text{and}\ \Delta R\le k,\\
H\in\mathcal M_S&\iff p_1R\ge U+k\ \text{and}\ \Delta R\ge k.
\end{aligned}
\]
Because every inequality is weak, this includes all two-way and three-way ties.

The exact limited-liability implementation wedge is
\[
H-(U+k)=(L-U)_+.
\]
It is the forced high-effort rent under the weak/accept benchmark. Consequently, relative to low effort, society prefers high at \(\Delta R\ge k\), whereas the principal's supremum comparison prefers high at
\[
\Delta R\ge k+(L-U)_+.
\]
Limited liability therefore creates no value wedge when \(U\ge L\), and creates the exact incremental wedge \(L-U\) when \(U<L\). Strict incentive and acceptance conventions add a separate **topological nonattainment problem**; they do not change the infimum wedge.

## 6. Numerical boundary examples

1. **The \(p_0=0\), equality boundary.** Let \((p_0,p_1,k,U)=(0,0.5,1,0)\). Then \(a=2\), \(L=0=U\), and \(H=1\). Weak/accept high effort has the unique contract \((0,2)\). Strict/accept, weak/reject, and strict/reject high effort have infimum 1 but no minimum.

2. **Positive rent and inefficient effort choice.** Let \((p_0,p_1,k,U,R)=(0.2,0.6,1,0.1,3)\). Then \(a=2.5\), \(L=0.5\), and the wedge is \(0.4\). Social values are \((S_0,S_1)=(0.5,0.7)\), so high effort is uniquely social. Principal suprema are \((P_0,P_1)=(0.5,0.3)\), so under weak/accept the principal uniquely chooses low effort. Under weak/reject the low supremum is uniquely best but unattained, so the overall problem has no maximizer.

3. **Strict effort can retain a minimum.** Let \((p_0,p_1,k,U)=(0.2,0.6,1,0.8)\). Then \(L=0.5<U\), \(A=1.8\), and strict/accept high-effort minimizers have \(d\in(2.5,3]\), all with expected wage 1.8.

4. **A uniquely best unattained high mode.** Return to \((p_0,p_1,k,U)=(0.2,0.6,1,0.1)\) and set \(R=5\). Then \((P_0,P_1)=(0.9,1.5)\). Under strict effort with acceptance, high is uniquely best in supremum but has no least-cost contract, hence the principal has no maximizer—not a high-effort maximizer with payoff 1.5.

The derivation is `verified-piecewise`: the accompanying deterministic program checks feasibility and costs of the weak correspondences, all strict/open-boundary existence classifications, \(p_0=0\), equality cases, and the project-level nonexistence rule.
