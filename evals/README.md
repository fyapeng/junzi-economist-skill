# Evaluation corpus

This directory preserves development evidence for Junzi Economist. It is part of the repository and is not copied into the installed skill.

## Structure

- `cases.yaml` and `triggers.yaml` define representative research and invocation tasks.
- `executions/` preserves responses, verdicts, failures, corrections, and selected computational artifacts.
- `runs/` records development rounds and the decisions they changed.
- `audits/` contains cross-execution reviews.
- `completion_audit.yaml` distinguishes proved, partial, missing, and contradicted requirements.

Historical artifacts remain frozen when possible. Machine-specific paths in provenance files describe the environment in which an execution occurred; they are not installation instructions and do not make an archived script portable. A passing record supports only the task and criterion it actually exercised. It does not prove universal behavior.

Validate record structure and declared artifact hashes from the repository root:

```text
python scripts/validate_eval_records.py
```

Use future substantive research tasks to extend behavioral evidence. Do not create repeated synthetic audits merely to increase execution counts or promote a capability label.

## Data boundary

Do not add confidential, restricted, identifiable, or licensed research data to this corpus. Keep real project data and credentials outside Git. Commit only purpose-built synthetic inputs, small disclosure-safe fixtures, code, and evidence required to understand a recorded result. Before publishing a new execution, inspect its provenance, paths, source permissions, and generated artifacts deliberately.
