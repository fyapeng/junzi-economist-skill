# Provenance

- Task artifact: `junzi-economist-struct-x048`
- Skill source: committed objects only from Git commit `e25b4d0` in `C:\Users\ENAN\junzi-economist-skill`.
- Read scope: `skills/junzi-economist/SKILL.md`, `references/EMPIRICAL_AND_STRUCTURAL_METHODS.md`, `references/THEORY_MODELING.md`, and `references/SOFTWARE_AND_COMPUTATION.md`, all via `git show`.
- Explicitly not read: evals, x044-x046, working-tree variants, and other references.
- Runtime: dedicated Conda environment `codex`; precise versions are recorded by the run in `outputs/run_summary.json`.
- Generated data: synthetic bounded uniform draws; no external data; no redraw, clipping, market dropping, or conditioning on shocks, prices, shares, costs, or solver outcomes.
- Primary executable: `replication.py`.
- Independent executable: `independent_check.py`, which reimplements shares and FOCs, performs fresh solves, and checks profit derivatives by finite differences.
