# runs/ — Module 01 Network Identity Audit: run evidence

Every execution of `scripts/01_network_identity.py` (v2.0.0 and later;
current version 2.0.1) writes to its own run directory, named by the UTC
timestamp of the run start (`YYYYMMDDTHHMMSSZ`). A run directory is never
reused and no file inside it is ever overwritten:

- the run directory is created with `exist_ok=False`;
- every output file is created in exclusive mode (`"x"`);
- the raw JSON is set read-only (`chmod 0o444`) right after capture;
- the checksum manifest covers the five files the script produces
  besides the manifest itself, including the verification report.

## What the script writes vs what is added separately

Files written automatically by the script (6 files; 5 of them covered
by the checksum manifest, the manifest itself being the sixth):

- `raw-data/rpc-responses/01_network_identity_raw.json` — captured
  request/response structures (request object + parsed JSON response +
  transport metadata), read-only after capture. This is a
  captured-and-serialized response structure, not a byte-level HTTP
  capture: no raw HTTP bytes, headers, or TLS data are stored.
- `datasets/01_network_identity.csv` — one-row processed dataset.
- `datasets/01_network_identity_metadata.json` — run metadata (run ID,
  script version, observed values, check counts).
- `datasets/01_network_identity_checksums.sha256` — SHA256 manifest of
  the raw JSON, metadata, CSV, script copy, and verification report.
- `findings/verified-facts/01_network_identity_verification.md` —
  verification report with all checks and observed values.
- `scripts/01_network_identity.py` — byte copy of the script that ran,
  read-only after capture.

Combined review report (NOT written by the script):

- `findings/verified-facts/01_network_identity_complete_report.md` —
  a combined reading copy (summary + verification report + terminal
  output + metadata + checksums + dataset + raw JSON + full code)
  assembled by a separate process for review. It is NOT produced by
  the script, NOT covered by the checksum manifest, and never replaces
  the separate evidence files: a merged editable file cannot carry
  checksum integrity for its parts, and the script must stay a
  runnable `.py` file.

## Verifying a run

From inside the run directory (v2.0.0 and later; the manifest uses
paths relative to the run directory):

```
cd runs/<run_id>
sha256sum -c datasets/01_network_identity_checksums.sha256
```

All five entries must report OK. The manifest does not hash itself:
a file cannot contain its own SHA256, so the manifest's own integrity
is established by the fact that it is written last, in exclusive mode,
and by the verification report, which lists the same five hashes.

Note on the first run (20261121T054711Z, script v1.0.0): its manifest
lists bare filenames (`01_network_identity_raw.json`, ...) with no
directory paths, so `sha256sum -c` cannot verify it directly from any
directory — the files live in `raw-data/rpc-responses/` and `datasets/`.
Its three entries were verified individually on 21 Nov 2026 against the
actual files (all OK) and against the six-file hash list in
`runs/01-no-overwrite-fix-report.md` (all six OK). Manifests from v2.0.0
onward use run-dir-relative paths and are directly verifiable with the
command above.

Layout inside each run directory:

```
runs/<run_id>/
  raw-data/rpc-responses/01_network_identity_raw.json
  datasets/01_network_identity.csv
  datasets/01_network_identity_metadata.json
  datasets/01_network_identity_checksums.sha256
  findings/verified-facts/01_network_identity_verification.md
  findings/verified-facts/01_network_identity_complete_report.md  (combined review copy, separate process)
  scripts/01_network_identity.py  (byte copy of the script that ran)
```

## Runs

| Run ID | Retrieved (UTC) | Script | Status | Notes |
|---|---|---|---|---|
| 20261121T054711Z | 2026-11-21T05:47:11Z | 1.0.0 | PASS (9/9) | First run. Evidence was first written to the canonical paths (raw-data/, datasets/, findings/) by script v1.0.0, then moved byte-identically into this directory on 21 Nov 2026 ~12:55 WIB during the v2.0.0 no-overwrite fix. All SHA256 verified identical before and after the move. Its metadata predates the run_id/script_version fields, so run ID and script version for this run are recorded here and in the combined report. Raw JSON and script copy are read-only (chmod 444). |
| 20261121T063234Z | 2026-11-21T06:32:34Z | 2.0.1 | PASS (13/13) | First v2.0.1 validation run. Chain ID 7295799, latest block 24805207 (drift +5), genesis hash same as the first run. Response checks used short names (response_valid_latest / response_valid_genesis) while the docstring specified the full names; superseded by 20261121T063327Z after the label alignment. Manifest verified with sha256sum -c (5/5 OK). |
| 20261121T063327Z | 2026-11-21T06:33:27Z | 2.0.1 | PASS (13/13) | Final v2.0.1 validation run after aligning response check names to the docstring (response_valid_eth_getBlockByNumber_latest / _genesis; label-only change, no behaviour change). Chain ID 7295799, latest block 24805303 (drift +4), genesis hash same as the first run. Script hash equals script-copy hash (5ff78700…). Manifest verified with sha256sum -c (5/5 OK). No combined report for this run yet (separate process). |

## Two v2.0.1 script builds

Both v2.0.1 runs carry the same version number, but they ran different
script builds. The script copy inside each run directory is the build
that ran, and its SHA256 is recorded in that run's manifest:

| Run ID | Script SHA256 | Response check names |
|---|---|---|
| 20261121T063234Z | c09d88eb835ba69d9a6bf4ee8d976584a709b97d140fd379b39385f5050701e0 | short: `response_valid_latest`, `response_valid_genesis` |
| 20261121T063327Z | 5ff78700346b2ebd0c1a1e14c2f615b3fd4d422bb7cbbec489b3d48743260ae0 | long: `response_valid_eth_getBlockByNumber_latest`, `response_valid_eth_getBlockByNumber_genesis` |

The only difference between the two builds is the two response-check
labels. The labels were aligned to the names the v2.0.1 docstring
already specified; no validation logic, threshold, RPC call, or output
value changed. Both runs PASS 13/13 on the same chain observations
(chain ID 7295799, same genesis hash), so the label change cannot
explain any difference in results — there is none to explain. The live
script (`scripts/01_network_identity.py`) is byte-identical to the
063327Z build (SHA256 `5ff78700…`).

## Documentation erratum — v2.0.1 docstring (raw data wording)

Erratum recorded 21 Nov 2026 (review ketiga Anara). The last sentence
of the v2.0.1 docstring (line 93 in the live script and in both run
copies) reads:

> "Raw data is written exactly as received and is never modified afterwards."

That wording is imprecise. The raw JSON is NOT a byte-level HTTP
capture and its contents are not "exactly as received" from the wire:
for each call it stores the request object, the parsed JSON response,
and transport metadata (HTTP status, attempt count, any error, and the
validation verdict) — a captured-and-serialized response structure.
No raw HTTP bytes, headers, or TLS data are stored. The second half of
the sentence ("never modified afterwards") is correct: the file is
written once and set read-only after capture.

Recommended replacement sentence for the next script version:

> "Captured response data is serialized once and never modified after capture."

The script v2.0.1 and its historical copies are NOT changed to apply
this correction: the docstring text is part of the evidence (it is
covered by the run manifests), so the fix is recorded here as an
erratum for the next version only.
