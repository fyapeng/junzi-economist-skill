# Junzi Economist

Junzi Economist is the economic specialization of the upstream [Junzi](https://github.com/fyapeng/junzi-skill) Codex skill and a general research partner grounded in economics. Junzi supplies the character, orientation, mainline discipline, independence, backtracking, and general practice protocol. Junzi Economist translates them into economic objects, theory, institutional investigation, evidence, estimation, welfare, computation, and writing.

The intended configuration installs both skills. Junzi governs the upstream discipline; Junzi Economist governs domain judgment. The economic skill retains minimum commitments for graceful operation when the upstream skill is temporarily unavailable, but substantial and long-running research should apply both without duplicating their preambles or checklists.

The skill keeps a stable kernel of economic grammar, research hierarchy, claim discipline, and backtracking. Field theory, institutional facts, frontier literature, estimators, software, and adjacent disciplines are retrieved as the live problem requires. Codex builds a task-local model of objects, mechanisms, context, evidence, uncertainty, and the next discriminating action; case-specific knowledge enters the core only when it yields a routing or decision principle that transfers across materially different tasks.

Its hierarchy is:

`Dao (direction) → Fa (economic reasoning) → Shi (concrete situation) → Shu (research practice) → Qi (instruments) → practice and revision`

For applied work, the default evidence order is:

`economic question → theory and institutions → transparent facts → reduced-form econometrics → structural or predictive extension when required`

ANOVA is descriptive unless an identification argument adds more. A/B language requires genuine randomized assignment and a well-defined estimand. Machine learning serves prediction, measurement, nuisance estimation, or disciplined heterogeneity analysis; predictive accuracy alone does not establish causality, mechanism, welfare, or policy invariance. Structural estimation enters when primitives, equilibrium responses, welfare, or unsupported counterfactuals require it.

The skill also separates the active research state from project memory. Current user decisions, root status, and the declared mainline govern ongoing work; archives, generated outputs, and abandoned models remain evidence without silently reactivating themselves.

## Install

```powershell
npx -y skills add fyapeng/junzi-skill --skill junzi -g -a codex --copy -y
npx -y skills add fyapeng/junzi-economist-skill --skill junzi-economist -g -a codex --copy -y
```

Or clone and install:

```powershell
git clone https://github.com/fyapeng/junzi-economist-skill.git
Set-Location .\junzi-economist-skill
.\install.ps1
```

On macOS or Linux, run `./install.sh`. The runtime package is stored at `skills/junzi-economist/`; repository-level evaluations are not copied into the personal skill directory.

## Use

```text
$junzi $junzi-economist Reconstruct this real-world phenomenon as an economic question, identify the theory and institutional knowledge that must be learned now, and propose the most discriminating evidence path.
```

Relevant research requests may also trigger the skill automatically. Routine formatting, citation conversion, and literal translation remain lightweight.

Interactive website: [fyapeng.com/junzi-economist-skill](https://fyapeng.com/junzi-economist-skill/)

Maintained by [fyapeng](https://github.com/fyapeng). Licensed under Apache-2.0.
