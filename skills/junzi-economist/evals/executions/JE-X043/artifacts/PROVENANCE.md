# Provenance — JE-X043

- Source commit: `845a0ae` in `C:\Users\ENAN\junzi-economist-skill`.
- Instruction sources were read only with:
  - `git show 845a0ae:skills/junzi-economist/SKILL.md`
  - `git show 845a0ae:skills/junzi-economist/references/MACROECONOMIC_LAW.md`
  - `git show 845a0ae:skills/junzi-economist/references/THEORY_MODELING.md`
  - `git show 845a0ae:skills/junzi-economist/references/SOFTWARE_AND_COMPUTATION.md`
- No eval files, prior x039/x042 artifacts, or uncommitted worktree contents were read.
- Numerical program: `solve_and_verify.py` in this directory.
- Interpreter actually used: `C:\Users\ENAN\miniforge3\envs\codex\python.exe`.
- The final run was executed from this fresh output directory; stdout/stderr are in `run_output.txt`, and machine-readable results are in `results.json`.
- All primitives were entered directly from JE-X043. No stored residual, policy, distribution, root, or prior result was used as an input.
- A preliminary strict run with `a_max=50` rejected the root region under the already declared tail/truncation rules. The grid design was backtracked to common baseline `a_max=100`; thresholds were not relaxed. The final three configurations were recomputed from primitives.
- `results.json` records Python, NumPy, SciPy, and platform versions; the full price scan; every unique evaluation; the ordered scan/root/tangency evaluation trace; all reliability checks; brackets; roots; and one-dimension-at-a-time comparisons.
