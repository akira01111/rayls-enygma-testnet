# Change Report — Module 01: No-Overwrite Fix (v1.0.0 → v2.0.0)

Date: 21 Nov 2026 ~12:55 WIB
Status: fix complete, not committed/pushed, awaiting Anara's second review.
Module 02 not started.

## Issues found (Anara's review, 21 Nov 2026)

Script v1.0.0 used fixed file names and write mode (`"w"`), so running
it again would overwrite the raw JSON, CSV, metadata, checksums,
and report from the previous run. There was no run identity, and the
checksum manifest did not cover the script or the verification report.

## What changed — per request item

### 1. Unique run ID based on UTC timestamp
- Each execution creates a `run_id` from the start time in UTC,
  format `YYYYMMDDTHHMMSSZ` (example: `20261121T054711Z`).
- Function `new_run_id()`; the run ID is recorded in the raw JSON, metadata, and report.

### 2. Each run stores its output in a different location
- All output now lives in `runs/<run_id>/` with the same layout
  as before inside that run directory:
  `raw-data/rpc-responses/`, `datasets/`, `findings/verified-facts/`,
  plus `scripts/` for the script copy.
- No more writing to the canonical `raw-data/`, `datasets/`,
  `findings/` locations at the repo root.

### 3. Script refuses to overwrite if evidence files already exist
- The run directory is created with `exist_ok=False`; an existing
  directory is never reused.
- If `runs/<run_id>` already exists, the run ID gets a `-2`, `-3`,
  etc. suffix so a new run never touches an old run.
- All files are written in exclusive mode (`"x"`, via
  `write_text_exclusive` / `write_bytes_exclusive` /
  `write_json_exclusive`). If a file already exists, the script stops
  with exit code 2 and writes no other file.
- Proven with an isolated test (without running the script): a second
  write to the same file is rejected and the file's contents do not change.

### 4. Raw JSON must not be modified after capture completes
- Raw JSON is written once (mode `"x"`) immediately after the 4 RPC calls
  complete, then immediately `chmod 0o444` (read-only).
- The script never opens raw JSON for writing again.
- The script copy inside the run dir is also `chmod 0o444`.
- Any later change is still detected via the SHA256 manifest.

### 5. SHA256 of the Python script and verification report go into the manifest
- `datasets/01_network_identity_checksums.sha256` now contains 5 entries:
  raw JSON, metadata, CSV, the script copy, and the verification report.
- The manifest is written LAST (after the report is finished) so the
  report's hash can be recorded too. The report itself lists the raw,
  metadata, CSV, and script hashes, plus a note that the manifest covers
  the report itself.
- The script also stores a byte-identical copy of itself in
  `runs/<run_id>/scripts/01_network_identity.py`, so every run
  is self-contained: the code that produced it is stored with it.

### 6. Metadata records the run ID and script version
- `datasets/01_network_identity_metadata.json` now contains `run_id`,
  `run_dir`, `script_version` (v2.0.0), `script`, `script_copy`, and
  `script_sha256`.
- The report also shows the Run ID, Run directory, and script version.

### 7. Evidence from previous runs is not deleted or replaced
- Evidence from the PASS run of 21 Nov 05:47:11 UTC was moved byte-identically
  from the canonical location to `runs/20261121T054711Z/` (moved, not copied
  and then emptied — `mv`, same bytes).
- SHA256 verified identical before and after the move:
  - script v1.0.0: `39caa42b31b928b814c3317ded316fbade8db498bcf7031619d272702a05be4b`
  - raw JSON: `2131d69031ca3b8e085004a807e8ebd169780c12c25b68afd1c0f3e8124fb85c`
  - CSV: `156c0b719499d212f3ba096c38b188c669463f6fd0069cf42b34aaadc4db9282`
  - metadata: `8d4e60119fce820f605007684ac834c3f50e1e1523d8a470a43405578620208f`
  - checksums: `7b730708c59c7f848fad8d2a5d5e3c7304287d081db050cb82b2f000ef5c84b6`
  - verification report: `aa544d470d734c90b154e099d50bff23bbf6cc590ca6eced83dbadc898a74eb8`
- The raw JSON and the v1.0.0 script copy in the run dir are read-only
  (`-r--r--r--`).
- The combined file (complete report) was regenerated into the run dir with
  the same observations; only path references and one move/version note changed.
  The old combined file in
  `findings/verified-facts/` was deleted because it had been replaced by the
  run-dir version.
- One deliberate exception: the old run's metadata was NOT given
  `run_id`/`script_version` fields, because changing it would change
  the hash and damage the evidence. The old run's run ID and script version are recorded in
  `runs/README.md` and in the combined file.

## What was NOT done
- Script v2.0.0 was NOT re-run (no new run). What was
  checked: `python3 -m py_compile` (passed) and an isolated logic test
  for run ID, directory collision, and overwrite rejection (passed,
  without network and without touching evidence).
- Previous observations were NOT changed (chain ID, block, hashes,
  timestamps, and PASS status remain the same).
- NO commit or push.
- Module 02 was NOT started.

## Verification performed
1. `python3 -m py_compile scripts/01_network_identity.py` — OK.
2. Isolated test (import the module, no network):
   - run ID format `YYYYMMDDTHHMMSSZ` — OK;
   - existing run directory → `-2` suffix — OK;
   - run ID usable as-is — OK;
   - second text write to the same file rejected, contents unchanged — OK;
   - second bytes write rejected — OK.
3. SHA256 of all six evidence files identical before and after the move
   (list above).
4. `git status`: only new untracked files (`runs/`,
   `scripts/01_network_identity.py`); no commit/push.

## Files changed / added
- Changed: `scripts/01_network_identity.py` (v1.0.0 → v2.0.0, 23,497 bytes).
- Moved (byte-identical): 6 evidence files of run 20261121T054711Z to
  `runs/20261121T054711Z/` + v1.0.0 script copy to
  `runs/20261121T054711Z/scripts/`.
- Regenerated: `runs/20261121T054711Z/findings/verified-facts/01_network_identity_complete_report.md`
  (33,445 bytes; paths updated + move note).
- Added: `runs/README.md` (run layout + run table).
- Deleted: `findings/verified-facts/01_network_identity_complete_report.md`
  (old version, replaced by the run-dir version).
- Added: this report file, `01-no-overwrite-fix-report.md`.

## Notes
- The combined file for review is currently in Markdown (.md) format. If
  Anara wants a real PDF export of that combined file,
  just ask — not made yet.
- Next run behavior: `python3 scripts/01_network_identity.py`
  will create a new `runs/<current-UTC-timestamp>/` and will not
  touch `runs/20261121T054711Z/` at all.

## Update — 21 Nov 2026 (Anara's second review)

Anara's second review (21 Nov 2026 ~13:18 WIB): overall results good, first run
data PASS 9/9 and the no-overwrite fix done. Before
commit/push, tasks A–D below were requested. No commit/push yet.
Module 02 not started.

### A. Source checksum verification (task A)

- The requested command was run from the repo root: the manifest printed,
  but `sha256sum -c datasets/01_network_identity_checksums.sha256`
  from inside `runs/20261121T054711Z/` FAILED with "No such file or
  directory" for all three files. Cause: the v1.0.0 manifest uses bare
  file names (no path), while the files live in
  `raw-data/rpc-responses/` and `datasets/`. The v1.0.0 manifest cannot
  be verified directly with `sha256sum -c` from any
  directory — this is a v1.0.0 manifest format defect, not evidence damage.
- Replacement verification (without changing any file): the SHA256 of all six old files was computed
  and matched against the hash list in this report (§7) —
  all six OK (script v1.0.0, raw JSON, CSV, metadata, checksums,
  verification report). The three manifest entries were also matched one by
  one against the actual files — all three OK.
- Manifest v2.0.0 and later uses paths relative to the run dir
  (5 entries) and can be verified directly with `sha256sum -c` from
  inside the run dir (see `runs/README.md`).

### B. Script v2.0.1 (task B)

- New version: `2.0.1` (patch on 2.0.0). v1.0.0 run data NOT changed.
- JSON-RPC response validation (new): every response is checked — the
  `jsonrpc` version must be `"2.0"`, the response `id` must equal the
  request `id`, no `error` object, the `result` field must exist, and
  the result must be shaped per the method (hex string for
  eth_chainId/eth_blockNumber; a block object with number/hash/timestamp
  for eth_getBlockByNumber). Validation results are recorded per call in the raw
  JSON (`validation: {ok, problems}`) and as 4 new
  `response_valid_*` checks. Total checks now 13 (previously 9).
- Full hash validation (new): a hash must be `0x` + exactly 64 hex digits
  (`is_full_hash`); a short or non-hex hash makes the check FAIL
  with a detail naming its value.
- Drift check name clarified (changed): `block_number_matches_latest_block`
  → `block_number_within_drift_of_latest_block`. The old name suggested
  the two numbers must be exactly equal; in fact the check allows the latest block
  0–10 blocks ahead, never behind. The check detail states
  the bound explicitly.
- Malformed response / invalid value handling (new): all parsing
  goes through safe helpers (`parse_hex_int`, `is_full_hash`,
  `block_timestamp_iso`) that return None instead of raising.
  Check evaluation moved into an `evaluate()` function that never raises
  on malformed data: an invalid value becomes FAIL with a clear detail
  (e.g. "hash is not a full 64-hex hash", "cannot compare"), and the run
  still writes all output with FAIL status (exit 1).
- Raw JSON clarification (new): the docstring + report explain that raw JSON
  is the captured-and-serialized response structure (the
  request object + already-parsed JSON response + transport metadata),
  NOT a byte-level HTTP capture (no raw HTTP bytes, headers,
  or TLS data).
- Archive root path (new): `find_repo_root()` walks up from the script
  file until it finds a directory containing both `scripts/` AND `runs/`.
  An archive copy run from `runs/<run_id>/scripts/` still
  finds the repo root and writes a new run in the repo's `runs/`, never
  inside the archive run. If not found, the script refuses to run
  (exit 2) with a clear message.
- Metadata now also records `checks_total` and `checks_passed`.
- Isolated test (no network, without touching evidence): 39/39 passed —
  response validation (good/wrong id/wrong version/error object/missing
  result/non-hex result/null block/non-dict block/short hash/
  transport failure/non-dict response/HTTP 500), safe parsing,
  `evaluate()` with good data (PASS 13/13), garbage data (FAIL without
  exception), all calls dead (FAIL, 0 passed), root path (live, archive,
  outside repo), run ID, directory collision, overwrite rejection.
  `python3 -m py_compile` passed. Script v2.0.1: 35,544 bytes.

### C. Documentation (task C)

- `runs/README.md`: distinguishes files created automatically by the script
  (6 files; 5 of them covered by the manifest) from the combined review
  report (made by a separate process, NOT by the script, NOT covered by
  the manifest, read-only copy). Added manifest verification instructions
  (`sha256sum -c` from inside the run dir) and an explanation that the manifest
  does not hash itself, plus a note on the v1.0.0 manifest format defect
  (bare file names).
- This update note: the combined PDF HAS been exported on 21 November
  2026 — 9 PDFs in `pdf/` (combined file 16 pages, script v2.0.0
  11 pages, raw JSON 4 pages, change report 3 pages,
  verification report 2 pages, the rest 1 page each). All passed the
  render gate and had their content + page counts checked. The old note in § Notes ("PDF
  combined not yet made") is kept as history and is now
  no longer valid.
- All historical notes in this report are kept; this section
  only adds, it does not rewrite.

### D. v2.0.1 validation run (task D)

- Two read-only RPC runs (only eth_chainId, eth_blockNumber,
  eth_getBlockByNumber; no testnet transactions, no wallet):
  - Run 1 — `20261121T063234Z` (06:32:34 UTC): PASS 13/13. Chain ID
    7295799, latest block 24805207 (drift +5), genesis hash same as the
    old run. Manifest 5/5 OK (`sha256sum -c` from the run dir).
  - Run 2 (final) — `20261121T063327Z` (06:33:27 UTC): PASS 13/13.
    Chain ID 7295799, latest block 24805303 (drift +4), genesis hash
    same as the old run. Manifest 5/5 OK. The live script and the script
    copy in the run dir have the same hash
    (`5ff78700346b2ebd0c1a1e14c2f615b3fd4d422bb7cbbec489b3d48743260ae0`).
- Check name correction between the two runs (not a behavior change):
  run 1 used the short names `response_valid_latest` /
  `response_valid_genesis`, while the v2.0.1 docstring already wrote
  the long names. The code was aligned to the docstring (labels only) and
  validation was repeated as run 2. The isolated test was updated (40/40
  passed, including an assert on the exact check names).
- Old run evidence NOT touched: all six hashes of run 20261121T054711Z
  still match the §7 list; run 1's manifest is still 5/5 OK
  after run 2 was created.
- Retries recorded in the final run's raw JSON: eth_chainId 3 attempts,
  eth_getBlockByNumber latest 2 attempts, the rest 1 attempt
  (the proxy briefly dropped the connection; all succeeded).
- No combined report for the new runs (made by a separate process,
  if requested).
- No commit/push yet. Module 02 not started.

## Update — 21 Nov 2026 (Anara's third review)

Anara's third review (21 Nov 2026 ~14:17 WIB): the complete Module 01 history PDF package
and audit structure accepted. Before commit review, the
build size clarification below was requested. No commit/push yet. Module 02 not started.

### v2.0.1 build size clarification

- The figure "Script v2.0.1: 35,544 bytes" in §B above refers to the build
  used by the first v2.0.1 run, `20261121T063234Z`: the script copy
  `runs/20261121T063234Z/scripts/01_network_identity.py`, 35,544 bytes,
  SHA256
  `c09d88eb835ba69d9a6bf4ee8d976584a709b97d140fd379b39385f5050701e0`.
- The build used by the final v2.0.1 run, `20261121T063327Z`, is
  35,650 bytes: the script copy
  `runs/20261121T063327Z/scripts/01_network_identity.py`, SHA256
  `5ff78700346b2ebd0c1a1e14c2f615b3fd4d422bb7cbbec489b3d48743260ae0`.
  The live script (`scripts/01_network_identity.py`) is byte-identical to
  this build (35,650 bytes, same hash).
- The 106-byte difference is the label change of the two check names
  (`response_valid_latest` / `response_valid_genesis` →
  `response_valid_eth_getBlockByNumber_latest` /
  `response_valid_eth_getBlockByNumber_genesis`); not a validation
  behavior change. Both script hashes are still listed above and
  in `runs/README.md` (section "Two v2.0.1 script builds"), and both
  are covered by their respective run manifests (verified 5/5 OK).

### Raw JSON docstring erratum

- A documentation erratum for the last sentence of the v2.0.1 docstring
  ("Raw data is written exactly as received...") is recorded in
  `runs/README.md` (section "Documentation erratum — v2.0.1 docstring
  (raw data wording)"), together with the recommended replacement sentence
  for the next version. Script v2.0.1 and its historical copies are
  unchanged.
- The complete Module 01 history PDF was regenerated in this round with
  the latest `runs/README.md` (7,705 bytes) and this change report,
  including that erratum; evidence files were not changed.
