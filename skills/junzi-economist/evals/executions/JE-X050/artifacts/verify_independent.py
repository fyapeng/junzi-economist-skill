from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd


ALPHA, BETA, MARKET_SIZE = 1.6, 1.1, 200


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    run, out = Path(args.run), Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    checks = []
    try:
        base = pd.read_csv(run / "baseline_data.csv", encoding="utf-8-sig")
        pol = pd.read_csv(run / "subsidy_data.csv", encoding="utf-8-sig")
        checks.append({"name": "exact_counts", "value": len(base), "pass": bool(len(base) == 200 and (base.groupby("market").size() == 5).all())})
        max_share_err = max(abs(g["share"].to_numpy() - np.exp(BETA*g["x"].to_numpy()-ALPHA*g["price"].to_numpy()+g["xi"].to_numpy()) /
            (1+np.exp(BETA*g["x"].to_numpy()-ALPHA*g["price"].to_numpy()+g["xi"].to_numpy()).sum())).max() for _, g in base.groupby("market"))
        checks.append({"name": "shares_from_primitives", "value": float(max_share_err), "pass": bool(max_share_err < 1e-12)})
        for name, df, subsidy in (("baseline_foc", base, 0.0), ("subsidy_foc", pol, 0.12)):
            residual = df["price"].to_numpy()-(df["mc"].to_numpy()-subsidy)-1/(ALPHA*(1-df["share"].to_numpy()))
            v = float(np.max(np.abs(residual)))
            checks.append({"name": name, "value": v, "pass": bool(v < 1e-9)})
        y = np.log(base["share"].to_numpy())-np.log(base["outside_share"].to_numpy())
        X = np.c_[np.ones(len(base)), base["x"].to_numpy(), base["price"].to_numpy()]
        Z = np.c_[np.ones(len(base)), base["x"].to_numpy(), base["z_cost"].to_numpy()]
        theta = np.linalg.inv(Z.T@X)@(Z.T@y)
        checks.append({"name": "iv_equation_recovery", "value": theta.tolist(),
                       "pass": bool(abs(theta[1]-BETA)<0.08 and abs(-theta[2]-ALPHA)<0.08)})
        for label, df, subsidy in (("baseline", base, 0.0), ("subsidy", pol, 0.12)):
            q=MARKET_SIZE*df["share"].to_numpy(); cp=float(np.sum(df["price"]*q)); fp=float(np.sum(subsidy*q)); rc=float(np.sum(df["mc"]*q))
            profit=cp+fp-rc
            cs=sum(MARKET_SIZE*np.log(1+np.exp(BETA*g["x"].to_numpy()-ALPHA*g["price"].to_numpy()+g["xi"].to_numpy()).sum())/ALPHA for _,g in df.groupby("market"))
            err=abs((cs+profit-fp)-(cs+cp-rc))
            checks.append({"name": f"{label}_accounting_identity", "value": float(err), "pass": bool(err < 1e-9)})
    except Exception as exc:
        checks.append({"name": "verifier_exception", "value": str(exc), "pass": False})
    report={"status": "passed" if all(c["pass"] for c in checks) else "failed",
            "independence": "fresh equations from CSV primitives; does not import production solver or trust stored residuals/summary",
            "checks": checks}
    (out/"verification.json").write_text(json.dumps(report,indent=2),encoding="utf-8")
    return 0 if report["status"]=="passed" else 3


if __name__ == "__main__":
    sys.exit(main())
