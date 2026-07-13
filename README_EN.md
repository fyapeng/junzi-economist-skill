# Junzi Economist

Junzi Economist is an Agent Skill for Codex and Claude Code. It treats economic theory as the foundation for research judgment, investigates concrete institutions and evidence before selecting methods, and uses data, software, models, and writing as subordinate instruments.

Its hierarchy is:

`Dao (direction) → Fa (economic law) → Shi (concrete situation) → Shu (research practice) → Qi (instruments) → practice and revision`

The skill supports microeconomics, macroeconomics, political economy, causal inference, structural estimation, computation, welfare analysis, academic-paper reading, and evidence-calibrated writing. It records claim status, preserves competing explanations, and backtracks when a branch loses a required premise.

## Install

Windows PowerShell:

```powershell
git clone https://github.com/fyapeng/junzi-economist-skill.git
Set-Location .\junzi-economist-skill
.\install.ps1 -Target codex
```

Use `claude` or `both` as the target when needed.

macOS or Linux:

```bash
git clone https://github.com/fyapeng/junzi-economist-skill.git
cd junzi-economist-skill
./install.sh codex
```

The runtime package is stored at `skills/junzi-economist/`. Manual installation copies this directory to `~/.codex/skills/` or `~/.claude/skills/`.

## Validate

```text
python skills/junzi-economist/scripts/validate.py
python skills/junzi-economist/scripts/validate_compatibility.py
python skills/junzi-economist/scripts/test_utilities.py
```

Codex structure and behavioral tests currently pass. Claude Code static compatibility follows the official skill layout; an independent Claude runtime test remains pending.

Maintained by [fyapeng](https://github.com/fyapeng). Licensed under Apache-2.0.
