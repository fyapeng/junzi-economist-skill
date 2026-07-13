# JE-X006 pre-protocol frontier audit

Status: reconstructed audit summary, not a strict raw execution record. The original answer produced a strong mechanism map but contained unsupported or incorrect version dates. It is preserved here to document the failure that motivated `FRONTIER_SEARCH.md`; it does not count toward strict execution coverage.

## 研究判断

这一前沿不能再被概括为“患者根据质量、距离和价格选择医院”。更准确的对象是一个受医生代理、组织网络和实时容量共同约束的配置过程：

\[
\text{患者需求}
\rightarrow
\text{医生筛选并提出转诊集合}
\rightarrow
\text{医院按容量和能力接收}
\rightarrow
\text{等待、治疗与结果}
\rightarrow
\text{后续转诊关系和能力调整}.
\]

因此，观察到的医院份额同时包含患者偏好、医生推荐、保险或组织激励、医院可接收性以及拥堵。把它们全部解释为患者效用，会错误估计质量偏好、替代关系和政策福利。

## 问题地图

| 研究层次 | 核心决策 | 当前前沿问题 |
|---|---|---|
| 患者选择 | 在实际获知或获准的医院中选择 | 患者是在完整市场中选择，还是只在医生提供的考虑集合中选择？ |
| 医生转诊 | 推荐哪些医院或专科医生 | 转诊反映临床质量、既有关系、支付激励、垂直整合、信息系统便利，还是规避等待？ |
| 医院接收 | 接收、排队、转出或拒绝哪些患者 | 容量是否改变患者的真实选择集，并导致按风险、支付或社会群体进行隐性配给？ |
| 动态学习 | 医生如何更新对医院质量的认识 | 医生是否从自己患者的结果中学习，还是依赖习惯和组织关系？ |
| 均衡反馈 | 转诊怎样改变容量、质量和进入 | 病例流动会不会强化中心医院拥堵、专业化、市场分割或能力积累差距？ |
| 福利 | 谁从重新配置中获益或受损 | 更低成本、更短等待、临床质量、出行、可及性和分配效应如何权衡？ |

## 基础研究

1. Gaynor、Propper 和 Seiler 利用英国 NHS 放松医院选择限制的改革，估计改革前受约束的考虑集合；改革后患者对临床质量更敏感，论文估计死亡率小幅下降和患者福利提高。[AER 原文与复制材料](https://www.aeaweb.org/articles?id=10.1257/aer.20121532)
2. Ho 和 Pakes 估计加州商业保险分娩患者的医院转诊，发现采用更多按人头付费医生的保险计划更重视医院价格，会把患者送往更远但价格较低、质量相近的医院。[NBER 工作论文及 AER 发表信息](https://www.nber.org/papers/w19333)
3. Beckert、Christensen 和 Collyer 建立患者—全科医生两阶段医院选择模型，指出忽略医生对选择集的策略性预筛选会导致估计偏误。[Journal of Health Economics 原文](https://doi.org/10.1016/j.jhealeco.2018.06.003)
4. Propper、Croxson 和 Shearer 研究英国 GP fundholding，表明家庭医生的医院转诊会考虑等待时间。[PubMed 原始书目信息](https://pubmed.ncbi.nlm.nih.gov/11939240/)
5. Ho 的医院网络模型显示，限制医院选择会降低消费者从网络获得的效用，但这种损失可能被保险人与医院谈判所得的价格下降抵消。[NBER 工作论文](https://www.nber.org/papers/w11819)

## 截至 2026-07-13 的最新前沿

### 学习、关系和容量

McCarthy 和 Richards-Shubik 的回答称其为“2024 年工作论文”，并使用 Medicare 骨科转诊研究医生对专科医生质量的学习、习惯持续和容量约束。[作者工作论文页](https://www.ianmccarthyecon.com/research/working-papers/physician-learning/)

Xue 和 Meyerhoefer 的 2025 年 NBER 工作论文发现，PCP 更换 EHR 开发商后，向相同开发商专科医生的转诊增加 5.8%，向旧开发商医生的转诊减少 4.2%；最常用的既有专科医生关系没有显著变化。[NBER Working Paper 33861](https://www.nber.org/papers/w33861)

### 垂直整合

Whaley 和 Zhao 使用 Medicare 数据，发现医生—医院整合使患者更多转向价格较高的医院门诊设施；论文的全体 PCP 整合反事实预测 Medicare 支出增加约 3.15 亿美元。[Journal of Public Economics 原文](https://doi.org/10.1016/j.jpubeco.2024.105175)

### 容量、等待和配给

Godøy 等利用挪威骨科手术队列拥堵变化，发现更长等待未显著提高后续医疗利用，却造成持续劳动供给下降和伤残领取增加。[AEJ: Economic Policy 原文及复制材料](https://www.aeaweb.org/articles?id=10.1257/pol.20210399)

回答称 Singh 和 Venkataramani 的论文存在“2026 年 4 月修订版”，并报告医院接近容量上限时黑人患者院内死亡率上升、白人患者没有同样变化。[NBER Working Paper 30380](https://www.nber.org/papers/w30380)

### 新容量进入

Arnold、Richards 和 Whaley 的 2026 年 NBER 工作论文研究精神专科住院机构进入：一般医院精神科住院约减少 60%，向精神专科机构出院转移约增加 50%，但急诊总量、短期社区犯罪、药物过量死亡和自杀没有下降。[NBER Working Paper 34772](https://www.nber.org/papers/w34772)

### 病例构成

回答引用 2026 年的一篇理论论文，称在受管制价格、异质性、容量约束及拥堵成本存在时，即使医院没有主动筛选，患者选择也能产生病例构成分化。[Economics & Human Biology DOI](https://doi.org/10.1016/j.ehb.2026.101599)

## 官方制度来源

- 英国 NHS 的选择框架规定，患者在转诊节点享有医院选择权，但选择通过 GP 和 e-Referral Service 实现。[英国政府 NHS Choice Framework](https://www.gov.uk/government/publications/the-nhs-choice-framework/the-nhs-choice-framework-what-choices-are-available-to-me-in-the-nhs)
- NHS England 容量提示在电子转诊系统中把容量有限服务标红、容量较充足服务标绿；官方页面报告早期采用点的红色机构转诊最多下降 38%、绿色机构最多增加 14%，但不能直接视为因果估计。[NHS England](https://www.england.nhs.uk/elective-care/best-practice-solutions/diversion-of-referrals/)
- CMS 的 physician self-referral law 原则上禁止医生把 Medicare 患者转往与其存在特定财务关系的实体，同时设有例外。[CMS](https://www.cms.gov/medicare/regulations-guidance/physician-self-referral)
- 中国国家卫生健康委 2024 年通知要求到 2025 年底在紧密型医联体和地级市建立转诊制度，并要求上级医院为基层转诊预留一定比例的门诊号源和住院床位。[国家卫生健康委](https://www.nhc.gov.cn/yzygj/c100068/202411/d85d3ba36c43460fa67deb333f52203b.shtml)

## 竞争机制

| 机制 | 主要预测 | 有辨别力的证据 |
|---|---|---|
| 患者质量偏好 | 信息改善后转向质量较高医院 | 同一医生、同一可选集合内响应独立质量信息 |
| 医生临床代理 | 转诊匹配病情和医院专长 | 病情—能力匹配强于支付、所有权和便利效应 |
| 医生学习 | 自己患者的意外结果改变后续转诊 | 医生特有结果冲击 |
| 关系或习惯 | 历史合作持续预测转诊 | 新质量信息后旧关系仍有黏性 |
| 财务激励 | 支付或所有权差异改变流向 | 相同患者、质量和距离下激励变化引起转诊 |
| 信息系统便利 | 同一 EHR 内转诊增加 | 系统切换后网络变化而临床匹配未改善 |
| 容量规避 | 拥堵医院收到更少转诊 | 意外容量冲击改变推荐集合 |
| 医院筛选 | 高成本或低支付患者更易被拒收或转出 | 给定推荐后接收概率仍按盈利性变化 |
| 能力约束 | 超出临床能力患者向上转诊 | 能力扩张后相关转诊下降 |
| 战略风险转嫁 | 亏损患者转给上级机构 | 转诊响应支付亏损强于能力缺口 |

## 矛盾与负面证据

- NHS 选择改革显示患者对质量更敏感，但 GP 预筛选研究说明患者并非面对无约束集合。
- 医生可能学习，但关系和信息系统兼容性仍能主导转诊。
- 容量分流可以降低局部压力，精神专科容量进入却未在短期改善多个社区结果。
- 拥堵损害可能具有分配差异，平均等待或死亡率会漏掉隐性配给。
- 病例结构差异既可能来自主动筛选，也可能由患者异质性和拥堵均衡产生。

核心张力是：转诊究竟改善临床匹配，还是重新分配支付责任、拥堵和风险？

## 对新研究设计的含义

建议利用中国上级医院为基层转诊预留号源和床位的制度，建立“基层医生—患者—接收医院”三方数据，观察患者病情、医生提出的目标及备选医院、转诊时点容量、医院接收、等待、自行绕开推荐、治疗、费用和结果。

候选识别来自不同医联体预留床位制度分批上线、疾病目录边界，或其他病种急诊冲击造成的短期容量变化。分别估计容量对医生推荐集合、医院接收概率、患者最终选择和临床匹配的作用。结构模型应把容量设为状态变量，并使用未参与估计的拥堵冲击或制度上线验证。

会推翻“预留容量改善配置”的证据包括：内部转诊增加但病情—能力匹配未改善；等待转移到其他环节；接收医院仍筛选高成本患者；健康结果未改善且总资源成本上升。

## 检索查询

- `hospital choice physician referral capacity constraints economics paper patient hospital demand referral`
- `site:nber.org hospital choice physician referrals capacity hospital working paper`
- `site:aeaweb.org hospital choice physician financial incentives referrals hospital paper`
- `2024 2025 economics working paper hospital capacity constraints patient choice referrals`
- `site:nber.org/papers hospital capacity patient allocation physician referral 2024 2025`
- `site:england.nhs.uk patient choice referral hospital capacity e-referral official`
- `site:gov.uk NHS patient choice hospital referral waiting times official guidance`
- `site:cms.gov physician self referral law official hospital referrals`
- `site:gov.cn 分级诊疗 转诊 医疗机构 容量 官方 2024 2025`
- `hospital capacity constraints quality patient choice economics journal paper occupancy mortality`
- `physician referral networks hospital integration economics primary paper 2024`

## 停止理由

回答认为检索已达到机制饱和：基础患者选择、医生代理、考虑集合、等待和网络均有原始论文；2024—2026 年的学习、EHR、垂直整合、容量配给和专科进入有一手论文或工作论文；英、美、中制度有官方来源；同时获得反例和负面结果。新增结果开始重复质量、关系、支付、信息系统和容量机制，因此停止。

**TEST PROVENANCE**

- 固定提交：`a91825887dea069bba9d8dd609f327396752a555`
- 实际读取技能文件：`SKILL.md`、`references/MICROECONOMIC_LAW.md`、`references/SITUATION_AND_FRONTIER.md`、`references/EMPIRICAL_AND_STRUCTURAL_METHODS.md`、`references/SOURCE_PROTOCOL.md`
- 检索来源：AEA、NBER、Journal of Health Economics/ScienceDirect、Journal of Public Economics、AEJ: Economic Policy、作者工作论文页、CMS、NHS England、GOV.UK、中国国家卫生健康委员会
- 客户端名称与版本：Codex；版本不知道
- 精确模型版本：不知道
