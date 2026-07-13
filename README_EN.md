# Junzi Economist

Junzi Economist is a Codex skill for economic research. It starts from real economic problems and human consequences, uses microeconomic and macroeconomic theory to define the object, investigates institutions and data generation, and then chooses evidence and methods.

Its hierarchy is:

`Dao (direction) → Fa (economic reasoning) → Shi (concrete situation) → Shu (research practice) → Qi (instruments) → practice and revision`

For applied work, the default evidence order is:

`economic question → theory and institutions → transparent facts → reduced-form econometrics → structural or predictive extension when required`

ANOVA is descriptive unless an identification argument adds more. A/B language requires genuine randomized assignment and a well-defined estimand. Machine learning serves prediction, measurement, nuisance estimation, or disciplined heterogeneity analysis; predictive accuracy alone does not establish causality, mechanism, welfare, or policy invariance. Structural estimation enters when primitives, equilibrium responses, welfare, or unsupported counterfactuals require it.

The skill also separates the active research state from project memory. Current user decisions, root status, and the declared mainline govern ongoing work; archives, generated outputs, and abandoned models remain evidence without silently reactivating themselves.

## Install

```powershell
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
$junzi-economist Build a reduced-form evidence mainline for this hospital-performance question from economic theory, institutions, and credible variation.
```

Relevant research requests may also trigger the skill automatically. Routine formatting, citation conversion, and literal translation remain lightweight.

Interactive website: [fyapeng.com/junzi-economist-skill](https://fyapeng.com/junzi-economist-skill/)

Maintained by [fyapeng](https://github.com/fyapeng). Licensed under Apache-2.0.
