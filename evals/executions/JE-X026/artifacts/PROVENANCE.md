# JE-X026 Provenance

## Scope

- Evaluation endpoint: JE-X026
- Repository commit under evaluation: `b85466e`
- Retrieval cutoff: 2026-07-13
- Runtime timestamp used for final checks: 2026-07-13T11:34:12+08:00
- Workspace: `C:\Users\ENAN\AppData\Local\Temp\junzi-economist-frontier-x026`
- Repository files were not modified.
- Existing repository evaluation run records were not read.

## Skill material read

1. `skills/junzi-economist/SKILL.md`
2. `references/SITUATION_AND_FRONTIER.md`
3. `references/FRONTIER_SEARCH.md`
4. `references/SOURCE_PROTOCOL.md`
5. `references/BRANCH_AND_DECISION_PROTOCOL.md`

These references determined the separation of webpage/document dates, claim-level verification, data-generating-process audit, and the explicit pause/backtrack decision.

## Retrieved artifacts retained locally

- `w30380.pdf`: live NBER current-PDF URL, 3,523,032 bytes, SHA-256 `F1A5345821CDA6BF9DDC7D8B7E8D27341EB30F102D16B1DA00C34DCD667CCC85`.
- `nber-page.html`: live NBER landing page, SHA-256 `3D90C1580C10D1707765F84CAEF74974B55A2AA347E89EC9381E3EF1E2F8FC1E`.
- `nhs-diversion.html`: live NHS England page, SHA-256 `59A511495A3414D83CBCECC1C46B204EB47ECB4E02092D9973203F0F076974DC`.

The two HTML hashes identify response snapshots saved for this audit at `2026-07-13T11:34:12+08:00`. They were retrieved with an ordinary `GET` through Windows PowerShell `Invoke-WebRequest`; no authentication, cookies, conditional-request fields, cache-control directives, or other special request headers were supplied. Dynamic HTML may change because of templates, scripts, analytics markup, edge delivery, or server-generated content, so a later request is not expected to reproduce these files byte for byte. These hashes identify what was inspected in this run; the downloaded NBER PDF hash is the stable version anchor for the paper.

The NHC page rejected direct scripted download with HTTP 412. Its official text was inspected through the web retrieval surface; no locally reconstructed file is represented as original bytes.

## Version-conflict handling

Search/open caches returned an older NBER state in one surface (May 2024; 78-page parser result), while a fresh live download and live HTML both identified April 2026. The substantive record uses the artifact actually downloaded and hashed. The conflict is disclosed rather than silently reconciled.

## Integrity notes

- File hashes establish the exact bytes inspected, not the truth of the authors' claims.
- Dynamic-page hashes establish the saved response snapshot only; the NBER PDF hash anchors the manuscript version.
- HTTP `Last-Modified` establishes server-object metadata, not manuscript revision date.
- “Official-text-verified” establishes what the institution states, not implementation fidelity or causal identification.
- Unknown date fields remain unknown; retrieval dates and search-engine dates were not substituted.
