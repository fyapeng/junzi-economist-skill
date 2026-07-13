import json
from pathlib import Path

import numpy as np

OUT = Path(__file__).resolve().parent
SEED = 561337
rng = np.random.default_rng(SEED)

# Intended population: independent eligible households at six observed subsidy indices.
x_levels = np.array([-1.4, -0.8, -0.2, 0.4, 1.0, 1.6])
n_per_level = 320
truth = {"alpha": -0.35, "beta": 1.05, "delta": 1.15, "pi_high": 0.38}
x = np.repeat(x_levels, n_per_level)
latent_high = rng.random(x.size) < truth["pi_high"]
index = truth["alpha"] + truth["beta"] * x + np.where(latent_high, truth["delta"], -truth["delta"])
p = 1.0 / (1.0 + np.exp(-index))
choice_uniform = rng.random(x.size)
y = (choice_uniform < p).astype(int)

raw = {
    "design": {
        "seed": SEED,
        "intended_population": "independent eligible households at six subsidy-index regimes",
        "expected_n": int(x.size),
        "realized_n": int(x.size),
        "x_levels": x_levels.tolist(),
        "n_per_level": n_per_level,
        "policy_x": 2.10,
        "true_parameters": truth,
        "normalization": "delta >= 0 labels the high-intercept type; logistic shocks use the standard zero-location normalization",
    },
    "observations": [
        {"id": int(i), "x": float(x[i]), "latent_high_draw": bool(latent_high[i]),
         "choice_uniform": float(choice_uniform[i]), "y": int(y[i])}
        for i in range(x.size)
    ],
}
(OUT / "raw_primitives.json").write_text(json.dumps(raw, indent=2), encoding="utf-8")
print(json.dumps({"seed": SEED, "n": int(x.size), "mean_y": float(y.mean())}))
