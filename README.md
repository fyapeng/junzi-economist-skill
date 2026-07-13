<div align="center">

<img src="assets/readme-hero.svg" width="100%" alt="君子经济学家：经济问题、理论制度、事实、简约式证据、必要的结构分析">

# 君子经济学家 · Junzi Economist

### 让经济学决定方法，让证据约束主张

[![Validate skill](https://github.com/fyapeng/junzi-economist-skill/actions/workflows/validate.yml/badge.svg)](https://github.com/fyapeng/junzi-economist-skill/actions/workflows/validate.yml)
[![Pages](https://github.com/fyapeng/junzi-economist-skill/actions/workflows/pages.yml/badge.svg)](https://fyapeng.com/junzi-economist-skill/)
[![License](https://img.shields.io/badge/license-Apache--2.0-8d2e27)](LICENSE)

**[交互网站](https://fyapeng.com/junzi-economist-skill/)** · **[技能核心](skills/junzi-economist/SKILL.md)** · **[英文概要](README_EN.md)**

</div>

> 天行健，君子以自强不息；地势坤，君子以厚德载物。

`junzi-economist` 是面向 Codex 的经济学研究技能。它把君子的道、法、势、术、器落实为一条研究纪律：从真实经济问题与人的处境出发，用微观和宏观理论组织对象，调查制度和数据生成过程，优先建立透明的描述事实与简约式计量证据，再为必要的参数、均衡、福利和反事实引入结构方法。

## 五层经济学体系

| 层级 | 研究问题 | 经济学要求 |
|:---:|---|---|
| **道** | 什么值得研究？ | 面向真实的人、制度、物质条件、分配后果与人的发展 |
| **法** | 经济对象怎样运行？ | 明确主体、目标、约束、信息、激励、互动、均衡、动态与福利 |
| **势** | 当前具体情势怎样？ | 调查历史阶段、制度执行、市场边界、权力关系、数据生成与学术前沿 |
| **术** | 怎样形成可信研究？ | 组织测量、简约式识别、理论模型、结构估计、计算、写作与回溯 |
| **器** | 借助什么完成？ | 驾驭数据、档案、文献、软件、算法、求解器和计算设施 |

<div align="center">

`立道 → 明法 → 察势 → 创术 → 驭器 → 实践检验 → 分层修正`

</div>

## 方法有次序

应用研究默认沿着下面的证据链推进：

```text
经济问题 → 理论机制与制度环境 → 透明事实 → 简约式计量证据 → 必要的结构或预测扩展
```

- **简约式证据是应用研究的中轴。** 当政策变化、制度差异或行为边际能够提供可信变异时，先明确 estimand、识别假设、支持范围和竞争解释。
- **结构模型回答额外问题。** 只有行为原语、均衡调整、福利或样本外政策反事实确有需要，且简约式证据无法独立回答时，才承担额外假设与验证负担。
- **方差分析属于描述。** 它可以定位差异来源，不能单独建立经济机制或因果解释。
- **A/B test 需要真实随机化。** 必须核对分配单位、干预暴露、依从、干扰、聚类和制度实施；两个观测组的比较不能仅靠改名成为实验。
- **机器学习承担明确角色。** 可用于预测、测量、辅助函数估计和诚实的异质性探索；预测精度不会自动升级为因果、机制、福利或政策不变性。

## 守住研究主线

进入已有项目时，技能先辨认当前状态。用户最近确认的目标、根目录状态和当前研究主线具有优先性；旧稿、归档、历史输出与废弃模型保存经验，但不会因文件更多、更新时间更晚或技术更复杂而重新成为默认路线。

当关键前提失效，技能会返回最近仍成立的判断节点，保留学到的事实和可复用成果，再选择继续、暂停、分叉或放弃。连续验证若不再改变主要主张、现实风险或下一项研究决定，就应停止局部优化，回到当前主要矛盾。

## 能力结构

运行核心按任务渐进加载：

| 理论与现实 | 证据与方法 | 成果与治理 |
|---|---|---|
| 微观、宏观、政治经济学与历史 | 数据测量、简约式识别、结构估计 | 研究主线、主张账本、分支决策 |
| 制度执行、市场边界与学术前沿 | 数值求解、模拟、复现与软件选择 | 论文阅读、经济写作、双语表达 |
| 人文关怀、福利、权力与跨学科纠偏 | 反事实、异质性与不确定性 | 失败记录、证据状态与诚实终点 |

## 安装

推荐从 GitHub 直接安装：

```powershell
npx -y skills add fyapeng/junzi-economist-skill --skill junzi-economist -g -a codex --copy -y
```

移除 `-g` 可安装到当前项目。查看仓库中可安装的技能：

```powershell
npx -y skills add fyapeng/junzi-economist-skill --list
```

也可以克隆后使用本项目的事务式安装脚本：

```powershell
git clone https://github.com/fyapeng/junzi-economist-skill.git
Set-Location .\junzi-economist-skill
.\install.ps1
```

macOS / Linux：

```bash
git clone https://github.com/fyapeng/junzi-economist-skill.git
cd junzi-economist-skill
./install.sh
```

已有同名技能时，脚本会先停止；确认替换后使用 PowerShell 的 `-Force` 或 shell 的 `--force`。运行包位于 `skills/junzi-economist/`，开发评测与历史记录不会复制到个人技能目录。

## 使用

```text
$junzi-economist 请从经济理论、制度背景和可识别变异出发，为医院管理绩效研究建立简约式证据主线。
```

符合描述的经济研究任务也可由 Codex 自动加载。普通格式转换、逐字翻译和简单引用调整保持轻量。

## 验证与边界

```powershell
python .\skills\junzi-economist\scripts\validate.py
python .\skills\junzi-economist\scripts\validate_compatibility.py
python .\scripts\test_utilities.py
python .\scripts\validate_eval_records.py
```

行为记录位于 [`evals/`](evals/README.md)，其中保留失败、修订与复测。测试支持的只是已覆盖任务，不证明任意模型、数据或研究环境中的稳定表现。当前项目收缩为 **Codex skill**；其他客户端适配暂不构成发布目标。

## 维护与许可

项目由 [fyapeng](https://github.com/fyapeng) 个人维护，采用 [Apache License 2.0](LICENSE)。学术或软件使用可参照 [`CITATION.cff`](CITATION.cff) 引用。
