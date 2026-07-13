# Data and measurement — 从经济对象到分析数据

Use this module when research depends on defining, cleaning, linking, reshaping, or handing off data. Treat data construction as economic measurement: every row, variable, key, omission, and transformation should correspond to a stated object or reveal where that correspondence fails.

## Define the object before the table

State the target population, observational unit, decision or event, stock or flow, time basis, geography or market, price and quantity concepts, and intended claim. Distinguish people, episodes, transactions, facilities, firms, products, markets, and administrative records. Decide whether repeated rows represent repeated choices, duplicated records, overlapping spells, or valid multiple relationships.

For each core construct, record the economic concept, observed proxy, source fields, unit, denominator, timing, support, aggregation rule, and known gap. A variable name does not establish that utilization measures demand, expenditure measures welfare, destination measures referral, or listed price measures the paid price.

## Reconstruct the recording process

Identify who produced each source, for what operational purpose, under which rules, and with what incentives. Record coverage dates, version or extraction date, revisions, coding changes, eligibility, reporting thresholds, missing institutions or people, and policy-induced changes in measurement.

Treat identifiers and linkability as empirical objects. Establish whether an ID is stable across time, facilities, products, systems, and ownership changes. If person paths, referrals, firms, or markets cannot be linked, reduce the claim before inventing continuity from aggregates.

Use `assets/templates/DATA_CONSTRUCTION_MAP.yaml` for consequential multi-source work. Keep restricted paths, credentials, and row-level sensitive information in local project configuration, never in the public skill or Git history.

## Preserve source and transformation layers

Keep raw source bytes unchanged. Build staging and analysis data through scripts with explicit inputs and outputs. Record source provenance, versions, hashes when appropriate, licenses or access restrictions, code entry points, environments, and every manual judgment.

Maintain a variable dictionary that preserves labels, types, units, missing codes, categories, reference groups, transformations, and claim jobs. Store identifiers that can have leading zeros or exceed exact numeric precision as stable strings. Parse dates and encodings explicitly. Prefer formats that preserve types and labels; treat CSV as an encoding- and type-sensitive interchange format.

## Audit keys, links, and crosswalks

Before every join:

1. declare the expected cardinality—one-to-one, one-to-many, many-to-one, or a deliberate many-to-many relation;
2. test candidate-key uniqueness on each side;
3. explain duplicates using the economic unit and recording process;
4. record matched, left-only, right-only, and multiplied rows;
5. inspect unmatched and duplicate rates by economically meaningful groups;
6. decide whether nonmatches imply exclusion, missing information, timing mismatch, or a different population.

Version geographic, industry, product, provider, firm, and policy crosswalks. Record boundary changes, code reuse, mergers, splits, ownership changes, effective dates, and the rule used to map observations. Do not silently force changing classifications into a timeless key.

## Construct time and event structure

For panels and spells, define entry, exit, gaps, left and right censoring, repeated episodes, treatment timing, anticipation, and time-varying eligibility. Report whether balance is designed, selected, or accidental. Do not fill absent rows with zeros unless absence truly denotes a zero economic outcome.

For event studies, construct event time from the verified exposure event and retain calendar time. Resolve multiple events, reversals, partial implementation, and never-treated or not-yet-treated states explicitly. For stocks and flows, enforce the correct accumulation and accounting identities.

## Make transformations economically explicit

Record denominators, weights, deflators, exchange rates, seasonal adjustments, top or bottom coding, winsorization, logs, zero and negative handling, per-capita conversions, market aggregation, and sample restrictions. Preserve both source and transformed variables when feasible.

Use survey, probability, frequency, analytic, and population weights according to their actual design and estimand. Name the price index, base period, geography, and deflation order. Check whether monetary, quantity, and real-resource variables share a unit before combining them.

## Diagnose missingness and selection

Separate true absence, zero, inapplicability, nonresponse, suppression, linkage failure, coding error, and unavailable history. Retain source missing codes until their meanings are mapped. Report missingness and exclusions across time, treatment, outcome, institution, geography, and other mechanism-relevant groups.

Maintain a sample-flow account from source populations to every analysis sample. Each exclusion needs a rule, count, economic consequence, and claim impact. Attrition, market survival, solver success, or complete-case availability must not silently redefine the target population.

## Validate in proportion to the claim

During exploration, check schemas, key uniqueness, ranges, units, missingness, distributions, and decisive accounting identities. For research evidence, add source-to-analysis reconciliation, merge and sample-flow audits, institutional benchmarks, alternative defensible constructions, and sensitivity of the principal result. Public releases should include a data dictionary, executable construction entry point, source inventory, environment, and disclosure-safe provenance.

Use checks that can reveal a different economic object: impossible state transitions, negative quantities, duplicated exclusive events, balance identities, totals against official aggregates, stable pre-policy definitions, and discontinuities at coding changes. Passing a schema test does not validate the measurement bridge.

## Hand off to methods and backtrack when needed

Before estimation, state the final unit, population, treatment or policy mapping, outcome construction, support, sample flow, and remaining measurement error. Pass those objects into the estimand and claim ledger; do not let a downstream estimator silently redefine them.

Backtrack to **Shi** when recording rules, coverage, linkability, or institutions were misunderstood. Backtrack to **Fa** when the observed variable cannot represent the intended economic choice, constraint, price, technology, equilibrium, or welfare object. Repair **Shu** or **Qi** when the object is valid but the transformation, join, code, or format fails. Stop cleaning when the analysis dataset and material limitations are reproducible and further polish cannot change the estimand, claim status, or next research decision.
