{
  "branch_decision": {
    "decision": "retain_both_coordinate_branches_interpret_ranked_supports_only",
    "evidence": "The two selected profile components are label-switched likelihood branches, while ranked supports and the policy mixture are invariant up to numerical error.",
    "scope": "No coordinate-label identification or continuous-set claim is made; grid-edge inclusion is reported as censoring."
  },
  "claim_status": "provisional_structural_grid_evidence",
  "economic_object": "Latent heterogeneity in repeated binary success and the model-implied response to a common log-odds policy shift.",
  "evaluated_grid_set": {
    "accepted_count": 15,
    "cutoff": 3.841458820694124,
    "evaluated_count": 15,
    "excluded_holes_inside_selected_span": [
      0.3,
      0.35,
      0.4,
      0.45,
      0.5,
      0.55,
      0.6,
      0.65,
      0.7
    ],
    "label": "evaluated-grid LR set; not a continuous confidence set",
    "lower_grid_censored": true,
    "lr_reference": "accepted unrestricted optimum of the same binomial-mixture likelihood",
    "selected_count": 6,
    "selected_pi": [
      0.15,
      0.2,
      0.25,
      0.75,
      0.8,
      0.85
    ],
    "upper_grid_censored": true
  },
  "sample_count_check": {
    "exact_match": true,
    "intended": 160,
    "realized": 160
  },
  "selected_only_policy_mapping": {
    "log_odds_shift": 0.4,
    "mapped_count": 6,
    "maximum_probability": 0.7301073575086675,
    "minimum_probability": 0.6663629798510762,
    "unselected_mapped_count": 0
  },
  "start_count_check": {
    "exact_match": true,
    "intended": 81,
    "realized": 81
  },
  "support_interpretation": "Coordinate A/B labels switch across observationally equivalent branches; economic labels are the ranked low and high success-probability supports.",
  "unrestricted": {
    "accepted": true,
    "kkt_inf": 2.0927612354171288e-07,
    "nll": 280.07068327545164,
    "p_a": 0.08491699960711376,
    "p_b": 0.781847212125916,
    "pi_coordinate_a": 0.2026346534670877,
    "support_labels": {
      "high": 0.781847212125916,
      "low": 0.08491699960711376
    }
  }
}
