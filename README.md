# 君子经济学家 · Junzi Economist

> 天行健，君子以自强不息；地势坤，君子以厚德载物。

一个面向 Codex 与 Claude Code 的经济学家型 AI 技能。它以君子人格为根，以经济学理论为法，调查现实制度与学术前沿之势，组织研究与表达之术，审慎使用数据、软件和计算之器。

**Junzi Economist** is a cross-client Agent Skill for economic reasoning, research design, structural and causal work, computation, paper reading, and evidence-calibrated writing.

## 五层研究体系

| 层级 | 核心问题 | 经济学要求 |
|---|---|---|
| 道 | 什么问题值得研究？ | 从真实的人、制度、物质条件和长期后果出发 |
| 法 | 如何解释经济对象？ | 明确主体、约束、信息、激励、互动、均衡、动态、分配与福利 |
| 势 | 现实处于怎样的状态？ | 调查历史阶段、制度执行、市场边界、数据生成和学术前沿 |
| 术 | 怎样形成可信研究？ | 组织理论、测量、识别、结构估计、计算、验证、写作和回溯 |
| 器 | 借助什么完成？ | 驾驭数据、档案、软件、算法、求解器、文献系统和计算设施 |

权威由内向外，实践反馈由外向内：

`立道 → 明法 → 察势 → 创术 → 驭器 → 实践检验 → 分层修正`

## 它会怎样工作

- 先界定经济问题和竞争机制，再选择 DID、IV、结构模型或软件。
- 区分理论来源、经验识别、数值收敛、样本拟合、外部验证和福利判断。
- 调查制度文本、实际执行、预期、规避、异质暴露和数据生成过程。
- 管理研究主线、主张版本、分支状态和失败条件。
- 当必要前提失效时，选择继续、暂停、分叉、回溯或放弃。
- 将作者主张、论文实际证据、读者推断和开放猜想分别记录。
- 让论文语言服从证据状态，保留简洁、自然、克制的表达。

## 安装

仓库中的运行包位于 `skills/junzi-economist/`。安装脚本复制这一目录，不会修改仓库源文件。

### Windows PowerShell

```powershell
git clone https://github.com/fyapeng/junzi-economist-skill.git
Set-Location .\junzi-economist-skill
.\install.ps1 -Target codex
```

Claude Code：

```powershell
.\install.ps1 -Target claude
```

同时安装：

```powershell
.\install.ps1 -Target both
```

已有同名目录时，脚本会停止。确认替换后使用 `-Force`。

### macOS / Linux

```bash
git clone https://github.com/fyapeng/junzi-economist-skill.git
cd junzi-economist-skill
./install.sh codex
```

将目标改为 `claude` 或 `both` 即可。

### 手动安装位置

| 客户端 | 个人技能目录 |
|---|---|
| Codex | `~/.codex/skills/junzi-economist/` |
| Claude Code | `~/.claude/skills/junzi-economist/` |

复制完成后，目标目录下应直接存在 `SKILL.md`。

## 使用

在 Codex 中显式调用：

```text
$junzi-economist 请审查这个结构模型的经济对象、识别和政策反事实。
```

在 Claude Code 中显式调用：

```text
/junzi-economist 请判断这项制度变化能否形成可信的经济学研究。
```

描述字段也支持客户端按任务自动加载。普通翻译、格式转换和引用格式调整不会自动触发完整研究流程。

## 渐进式知识结构

运行核心保持精简，按任务加载：

- 微观、宏观、政治经济学与历史
- 现实制度、数据生成和学术前沿
- 因果识别、结构估计和数值验证
- 福利、人文关怀与跨学科纠偏
- 研究分支、论文写作与论文精读
- 软件、复现与来源谱系

模板用于研究主线、主张账本、模型卡、分支日志、论文证据和稿件主张映射。

## 验证

```powershell
python .\skills\junzi-economist\scripts\validate.py
python .\skills\junzi-economist\scripts\validate_compatibility.py
python .\skills\junzi-economist\scripts\test_utilities.py
```

行为评测位于 `skills/junzi-economist/evals/`。测试记录保留失败、修订和复测过程，不只保留通过结果。

## 当前状态

- Codex：结构与行为测试通过。
- Claude Code：符合官方技能目录和 `SKILL.md` 规范；尚待可调用 Claude CLI 的独立运行时测试。
- `econ-paper` 与 `paper-deep-read`：核心判断能力已经迁移；旧工具暂处于过渡期。

## 维护与许可

项目由 [fyapeng](https://github.com/fyapeng) 个人维护。目前不开放公共修改流程；问题反馈可在仓库公开后通过 Issues 提交。

Apache License 2.0。学术或软件使用可参照 [`CITATION.cff`](CITATION.cff) 引用。
