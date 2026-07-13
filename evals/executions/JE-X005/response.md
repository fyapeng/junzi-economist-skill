下面给出一个单患者、单医生、线性按量支付的最小模型。核心结论是：支付总会提高医生选择的治疗强度，但利他的方向不确定；支付提高福利也只在治疗不足且财政成本较低时成立。

## 1. 主体、时序与约束

主体：

- 患者：从治疗强度 \(t\) 获得净健康收益；
- 医生：选择治疗强度，兼顾收入、努力成本与患者利益；
- 支付方：事先规定单位治疗支付 \(p\)。

时序：

1. 支付方设定 \(p\geq 0\)；
2. 医生观察支付、患者状态和自身利他程度；
3. 医生选择 \(t\in[0,\bar t]\)；
4. 健康收益、治疗成本和支付实现。

令患者净健康收益为

\[
B(t)=vt-\frac q2t^2,\qquad v>0,\ q>0.
\]

其中 \(v\) 表示患者初始治疗收益，\(q\) 捕捉边际收益递减及过度治疗伤害。医生的真实努力或资源成本为

\[
C(t)=\frac c2t^2,\qquad c>0.
\]

医生效用为

\[
U_D(t;p,\alpha)=pt+\alpha B(t)-C(t),
\]

其中 \(\alpha\geq0\) 是医生赋予患者净健康收益的权重。

## 2. 最优治疗

医生的一阶条件为

\[
p+\alpha(v-qt)-ct=0.
\]

由于

\[
\frac{\partial^2U_D}{\partial t^2}=-(c+\alpha q)<0,
\]

无约束最优解唯一：

\[
\tilde t(p,\alpha)=\frac{p+\alpha v}{c+\alpha q}.
\]

考虑可行边界后，

\[
t^*(p,\alpha)
=
\min\left\{
\bar t,\,
\max\left[0,\frac{p+\alpha v}{c+\alpha q}\right]
\right\}.
\]

在内点区域：

\[
\frac{\partial t^*}{\partial p}
=
\frac{1}{c+\alpha q}>0.
\]

因此，更高的按量支付必然提高治疗强度，但利他会削弱医生对支付的边际反应：

\[
\frac{\partial^2t^*}{\partial p\,\partial\alpha}
=
-\frac{q}{(c+\alpha q)^2}<0.
\]

利他的比较静态为

\[
\frac{\partial t^*}{\partial\alpha}
=
\frac{vc-qp}{(c+\alpha q)^2}.
\]

所以：

\[
\frac{\partial t^*}{\partial\alpha}
\begin{cases}
>0,& p<vc/q,\\
=0,& p=vc/q,\\
<0,& p>vc/q.
\end{cases}
\]

利他并不机械增加治疗。它使医生的选择向患者单独最偏好的治疗强度

\[
t_P=\frac vq
\]

靠近。当支付已经诱导医生治疗超过 \(t_P\) 时，更利他的医生反而减少治疗。

## 3. 社会福利边界

若支付只是患者、支付方与医生之间的无成本转移，社会福利为

\[
W_0(t)=B(t)-C(t)
=vt-\frac{q+c}{2}t^2.
\]

社会最优治疗强度是

\[
t^{FB}=\frac{v}{q+c}.
\]

沿医生最优反应，支付的福利效应为

\[
\frac{dW_0}{dp}
=
\left[v-(q+c)t^*\right]\frac{1}{c+\alpha q}.
\]

因此：

- 当 \(t^*<t^{FB}\) 时，提高支付增加福利；
- 当 \(t^*=t^{FB}\) 时，支付的边际福利效应为零；
- 当 \(t^*>t^{FB}\) 时，提高支付降低福利。

在允许正负支付且不存在筹资成本时，实现一阶最优的单位支付为

\[
p^{FB}
=
\frac{cv(1-\alpha)}{q+c}.
\]

这说明医生利他程度与最优支付是替代关系：

- \(\alpha<1\) 时，需要正支付弥补医生对患者收益权重不足；
- \(\alpha=1\) 时，\(p^{FB}=0\)；
- \(\alpha>1\) 时，模型要求负边际支付才能避免过度治疗；若制度限制 \(p\geq0\)，一阶最优可能无法实现。

若公共支付需要扭曲性筹资，令每单位支付的额外社会成本为 \(\lambda\geq0\)，则

\[
W(t,p)
=
B(t)-C(t)-\lambda pt.
\]

此时

\[
\frac{dW}{dp}
=
\frac{v-(q+c)t^*-\lambda p}{c+\alpha q}
-\lambda t^*.
\]

即使治疗仍低于无筹资成本的一阶最优，较高支付也可能因财政机会成本而降低福利。

这个福利结论有明确边界：模型没有包括患者异质性、诊断不确定性、保险保护、医生收入效用的非线性、医院容量、候诊拥挤、其他患者被挤出、治疗质量、动态健康收益或创新激励。加入这些对象后，福利标准和最优支付都可能改变。

## 4. 两个反直觉参数例子

取

\[
v=q=c=1,\qquad \bar t=3.
\]

### 例一：利他越高，治疗越少

令 \(p=2\)，则

\[
t^*(2,\alpha)=\frac{2+\alpha}{1+\alpha},
\]

且

\[
\frac{\partial t^*}{\partial\alpha}
=
-\frac{1}{(1+\alpha)^2}<0.
\]

当 \(\alpha=0\) 时，\(t^*=2\)；当 \(\alpha=1\) 时，\(t^*=1.5\)。原因是患者自身最偏好的强度为 \(t_P=1\)，支付已经诱发过度治疗，利他使医生减少而不是增加治疗。

### 例二：支付越高，福利越低

令 \(\alpha=1\)、\(\lambda=0\)。当 \(p=0\) 时，

\[
t^*=\frac12=t^{FB},
\qquad
W_0=\frac14.
\]

把支付提高到 \(p=1\) 后，

\[
t^*=1,
\qquad
W_0=1-1=0.
\]

支付增加了治疗，却把选择从社会最优推向过度治疗，因此福利下降。若 \(\lambda>0\)，福利损失还会更大。

模型最终产生两个可推翻的命题：支付对治疗强度的效应应随利他程度上升而减弱；利他对治疗的方向应取决于既有支付是否已把治疗推过患者收益最大点。若数据系统性违背这些交互预测，就需要放弃或扩展这一最小结构。

**TEST PROVENANCE**

- 固定提交：`a918258`
- 实际读取文件：
  - `skills/junzi-economist/SKILL.md`
  - `skills/junzi-economist/references/MICROECONOMIC_LAW.md`
  - `skills/junzi-economist/references/HUMAN_WELFARE_AND_INSTITUTIONS.md`
- 客户端：Codex Desktop
- 客户端版本：不知道
- 模型系列：GPT-5
- 精确模型版本／构建号：不知道
