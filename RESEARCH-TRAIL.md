# Research trail — Rayls Enygma Public Testnet (21–22 Nov 2026)

Chronological record of what was searched, checked, and found — and what was
NOT found. Synthesised only from the files in this repository and the
verbatim audit report in `audit-reports/`; no step is recorded here unless a
file documents it. Anything unclear is marked unknown, not filled in.

Labels (binding, same 6-label taxonomy as the initial audit):
**verified fact / official claim / direct observation / reconstruction /
inference / unknown.**

Times are WIB (UTC+7) unless marked UTC. The chain is Rayls Public Testnet,
chain ID 7295799 (`0x6f5337`), RPC `https://testnet-rpc.rayls.com`,
Explorer `https://testnet-explorer.rayls.com`,
demo `https://enygma-testnet.rayls.com/`.

## 21 Nov 2026 — initial audit (04:50–05:05 UTC / 11:50–12:05 WIB)

**What was searched/checked:** live chain identity (eth_chainId,
eth_blockNumber), vault + registry log growth vs the 15 Nov baseline,
EIP-1967 implementation slots for 3 proxies, the demo bundle (page + JS
hash), docs/blog wording (6 sources), GitHub repos (`raylsnetwork/Enygma`
family), auditor events, username registrations, unshielding payouts,
volume measurability.
**Method:** read-only curl (browser User-Agent) + Explorer API
`module=logs&action=getLogs`, paginated per 200,000 blocks (API cap 1,000
results/call); `eth_getCode`, `eth_getStorageAt`, `eth_getTransactionByHash`.
**Found:** chain ID 7295799 re-verified; block 24,793,989 (04:50:45 UTC);
vault yx 2,128 logs / 511 tx; registry yx 405 logs / 207 tx, 131 new
usernames; yx implementations match the bundle; unshielding fully public
(41 payouts, 0 mismatches); auditor key escrow IS implemented in
`enygma_retail_payments` (code context, not live proof); new DvP ciphertext
binding (commit 6a6a23b1…).
**NOT found / unresolved:** live bx proxy implementations are NOT in the
bundle (registry bx `0x66f87eaf…`, vault bx `0x8551f451…`); bx ownerCalls
upgrade never executed; auditor scope conflict unresolved (blog: scoped keys;
Private Network doc: network-wide; Public doc: per deployment); 0.0001 RLS
fee discrepancy unresolved; RLS token slot anomaly (slot holds its own
address); proof-time figures differ across sources (408 ms / ~2.2 s / ~3 s /
"under 4 s"); no on-chain event shows an auditor decrypting/auditing.
**Obstacles:** Explorer API 1,000-result cap → pagination per 200k blocks;
one HTTP 403 from urllib without a User-Agent → curl + browser UA; two exec
calls returned exit 1 with no data loss (recorded as a tooling limitation).
**Output:** `audit-reports/ENYGMA-TESTNET-AUDIT-REPORT.md` (verbatim copy;
original in `~/workspace/rayls-enygma-audit/`).

## 21 Nov 2026 — Module 01, Network Identity Audit (12:47–15:31 WIB)

**What was searched/checked:** chain identity via 4 RPC calls
(eth_chainId, eth_blockNumber, eth_getBlockByNumber latest + genesis).
**Method:** Python stdlib script (`scripts/01_network_identity.py`),
browser-like UA, up to 5 attempts per call, drift allowance 0..+10 blocks.
**Found:** chain ID 7295799; genesis block 0, hash
`0x33b818f13cab5c2e3e7bb589cbd0612e78e1139f3add29f0d5f0d6a03a5c9545`,
timestamp 2026-03-12T16:22:30Z (new data — the initial audit never recorded
the genesis hash). Run 1 (v1.0.0): PASS 9/9. Runs 2–3 (v2.0.1): PASS 13/13
each (13 checks: 9 identity checks + 4 response-validation checks).
**Obstacles:** v1.0.0 crashed on unhandled IncompleteRead; urllib
RemoteDisconnected vs the same endpoint via curl (proxy drops) → retry logic
+ curl transport in later scripts; block-number equality too strict for a
live chain → drift allowance; v1 manifest used bare filenames (not directly
verifiable with `sha256sum -c`) → v2 manifests use run-relative paths;
no-overwrite redesign (unique run IDs, exclusive writes, chmod 444, manifest
covers script + report) after Anara's review.
**Output:** `runs/20261121T054711Z/`, `runs/20261121T063234Z/`,
`runs/20261121T063327Z/`, `runs/README.md`,
`runs/01-no-overwrite-fix-report.md`. Review PDFs in `pdf/` are local-only.

## 21 Nov 2026 — repository created (12:13–12:20 WIB)

**What was done:** `gh repo create rayls-enygma-public-testnet-research`
(private, then changed to public per Anara's "jangan private"); structure
commits `28cce92` (stage 2: 13 folder READMEs) and `1676829` (stage 2b: 13
more subdirectories). HEAD is still `1676829`; everything since is
untracked in the working tree (no commit/push yet — Anara's rule). Note
(22 Nov 2026): that last clause describes the early state at creation —
at that point the working tree held only the structure READMEs and nothing
else had been added yet. The current status (8 tracked files modified, the
rest untracked new files, `pdf/` excluded) is in `INDEX.md` (Git status,
22 Nov 2026).

## 21 Nov 2026 — inventory review, 12:30 WIB (chat only — GAP)

An inventory of all existing Enygma audit material was delivered in chat
(format A–I + two file lists: publishable vs keep-private). **No file was
written for it.** This is recorded here as a gap: the inventory exists only
in the chat transcript, not in this repository. It is NOT reconstructed from
memory.

## 21 Nov 2026 — Week 2 TX audit, overnight (23:13–23:35 WIB)

**What was searched/checked:** one transaction,
`0x09edab2bb8914aea3c905608ea9fcd09c056a470a5e150df03e0b324eff525bb`
(block 24825928): tx data, calldata, receipt, all event logs, block,
destination contract + implementation slot, relayer role, commitment /
encrypted-note observability, fee vs wallet display, hidden-vs-visible
identifiers; plus one related fee-settlement tx and the registry
(195 usernames).
**Method:** read-only RPC via curl (18/18 calls), Explorer API
(gettxinfo, gettxreceiptstatus, relayer txlist, registry getLogs);
selector/topic resolution via 4byte.directory (all count 0) then local
pure-Python keccak256 against the demo-bundle IEnygmaDvp ABI; structural
ABI-word parsing; case-insensitive hex search; fee from receipt values.
**Found:** transferV2 proven (selector `0xaacd552c`), direct to
SharedVaultProxy (not via Multicall3); 7 logs (1 Nullifier, 3 Commitment,
3 EncryptedNote); fee total 4.416 RLS public in calldata statement[8];
chain gas 0.063168048 RLS (≠ wallet "3.84 gas" — that is the relayer service
fee); 0.576 RLS to `0x71af…` 4 blocks later; 4.416 = 3.84 + 0.576 and
3.84 × 15% = 0.576 exactly; sender/receiver/token/6 RLS NOT in the tx data
(proven by hex search of raw input/logs, not from the Explorer display);
no on-chain link from the tx to @anara (reconstruction only).
**NOT found / unresolved:** statement positions 0, 1, 2, 9 unidentified;
whether `0x71af…` is the Foundation fee address; exact nature of the 3.84
relayer fee; 3-note value mapping (reconstruction only); no verified
contract source for the vault implementation.
**Obstacles:** fetch v1.0.0 (urllib) failed on transport for 3 calls →
v1.1.0 switched to curl (18/18 pass); RPC `eth_getLogs` rejects ranges
>100,000 blocks → Explorer API pagination; two decode-script bugs (ABI
offsets from the wrong base; `bytes[]` offsets treated as lengths) → fixed,
outputs deleted and regenerated from scratch; raw files never touched.
**Output:** `experiments/transactions/tx-09edab2b/` (raw + decoded JSON,
manifest, report, gaps, TODO, addendum) + independent verifier 23/23 PASS
+ 155-page combined review PDF.

## 21 Nov 2026 — Week 2 video edit + QA (21:05–22:36 WIB)

**What was done:** Anara's activity recording + ElevenLabs (Zara) VO edited
into a documentary-style experiment video (720p, then 1080p upscale).
**Method:** faster-whisper word timestamps → subtitle timing; ffmpeg segment
edits + still-frame freezes + concat demuxer; VO as-is (adelay 800 ms,
volume ×2.0, alimiter 0.89); subtitles burned in (ASS, $RLS display rule).
**Found/fixed:** v1 tpad freezes rendered black → per-segment stills;
$USDr detour cut; 2.9 s unexplained black removed; subtitle/data collisions
fixed by top-aligning 2 cues; "Enigma" → "Enygma" in 2 subtitle cues
(verified at seconds 21/22/23); same-filename confusion on re-send → v2
renamed file (byte-identical). Receiver spelling @kittynim verified on
screen in 3 places.
**Output:** `experiments/testnet-journeys/week2-private-payment/` (finals,
subs, build scripts, edit plan, QA report, manifest) +
`raw-data/videos/` (source footage + VO) +
`raw-data/screenshots/chk-21.jpg`, `raw-data/screenshots/chk-22.jpg`,
`raw-data/screenshots/chk-23.jpg`.

## 22 Nov 2026 — @kittynim confirmation + this integration (~02:00 UTC)

- Anara confirmed the receiver username is **@kittynim** (not @kittymin),
  22 Nov 08:55 WIB. Recorded in the TX package addendum
  (`ADDENDUM-2026-11-22.md`). Note on the spelling check: the string
  "@kittymin" DOES appear in the repo, but only in explicit "not @kittymin"
  explanations documenting the brief/VO-transcript error — in
  `experiments/testnet-journeys/week2-private-payment/EDIT-PLAN.md`,
  `QA-REPORT-V2.md`, `build_subs.py` (a diagnostic counter), and the TX
  addendum. It never appears as the receiver's username in any finding,
  subtitle, address mapping, or manifest. Every evidence reference uses
  @kittynim.
- This integration (audit report copy, video journey, contract map, index,
  trail, reproduce guide) assembled the 21 Nov work into one archive without
  touching raw evidence or the old research repo.

## 22 Nov 2026 — REPRODUCE revision (path audit + corrections)

**What was checked:** the input/output path implementation of
`scripts/decode_tx_09edab2b.py`, `scripts/tx_audit_09edab2b.py`,
`scripts/verify_tx_audit_09edab2b.py`, and the video build scripts,
against the procedures in `REPRODUCE.md`.
**Found:** the decode script hard-codes `PKG` to the original repo (line
35) — the old "run it in a scratch copy" instruction was unsafe: an
unedited scratch copy tried to write to the ORIGINAL `decoded/` and failed
only because exclusive mode `x` refused (`FileExistsError`, tested 22 Nov
2026). The fetch script resolves paths from `__file__` and refuses before
any RPC call (exit 2, network-free, tested) — but a full-repo scratch copy
already contains `raw/`, so the re-fetch procedure must delete `raw/` in
the copy first. `cp -r` into an existing `/tmp/rayls-repro` creates a
nested copy — the procedure now starts with `rm -rf`. The video build
scripts hard-code the old workdir and need intermediates not in the repo
(`segments_v2/`, `zoom_long.mp4`, `video_only_v2.mp4`), so a full video
rebuild from the repo alone is not currently possible.
**Fixed in REPRODUCE.md:** read-only scope clarified (blockchain read-only,
local artifacts still written); reproducibility split into 4 levels
(local-only / needs RPC-Explorer / external snapshot / not reproducible);
decode/fetch/video procedures corrected and tested; verifier PASS explicitly
NOT equated with repeating the discovery process. `INDEX.md` git-status
section corrected: 8 tracked files modified, the rest untracked new files,
`pdf/` + validate PNGs excluded — the old line "everything below is
untracked" was too general.
**Not changed:** re-fetch stays TODO (not run); all audit notes kept
(fetch failure, decode bugs, bare-filename manifest, unresolved findings,
@kittynim correction). No script was edited — only the instructions.
**Test evidence:** corrected decode procedure reproduced byte-identical
decoded outputs in the scratch copy (`diff` empty); original decoded
SHA-256 unchanged afterwards (`5a8ad453…`, `19c3a36e…`); scratch copies
removed after testing.

## 22 Nov 2026 — final review round (9th file + normalizer + subtitle)

**9th raw file traced:** `raw/related-tx-0xacc7d175.json` (6,456 B) was the
unaccounted file — REPRODUCE §2 had explained 5 script + 3 manual files.
It is a manual curl step: 3 RPC calls (`eth_getTransactionByHash`,
`eth_getTransactionReceipt`, `eth_getBlockByNumber`) for the related tx
`0xacc7d175e08b72766796807b34141185e461fcec0d72df6ccb8dc621406509b2` (block
24825932), retrieved 2026-11-21T16:25:18Z, found by listing the relayer's
txs in blocks 24825800–24826200. Its call records store only `method` +
`endpoint` (no request params); re-fetch parameters are reconstructed from
the file's top-level `tx_hash` + `expected_block`. `checks[]` is empty —
no checks were recorded for it. NOT outside re-fetch scope; documented in
REPRODUCE §2B with the exact parameters.
**Normalizer:** the `sed` normalizer was replaced by a JSON/Python
comparator (parses the JSON; normalizes ONLY top-level `retrieved_at_utc`
and `calls[].attempts`). Tested 22 Nov 2026 in /tmp on copies of the 5
script files: (A) positive — metadata-only changes in all 5 files → 5/5
PASS, exit 0; (B) negative — one hex digit changed in `receipt.json`
(`blockNumber` `0x17ad049` vs `0x17ad048` — the last digit, `8` → `9`) → FAIL with the exact path
`$.calls[0].response.result.blockNumber`, the other 4 files PASS, overall
exit 1 (the failure in the 2nd file was not masked by the 3 later passes);
(C) decoy — `validation.attempts = 999` and `request.retrieved_at_utc`
injected in the wrong place → FAIL `transaction.json`, exit 1. The decoy
test caught a label bug in the first comparator version ("only in saved" /
"only in re-fetch" inverted); labels fixed, scenarios A and C re-run
(scenario B's value-diff path was unaffected by the label bug).
**Subtitle:** regeneration tested 22 Nov 2026 in a scratch copy (exact
commands in REPRODUCE §4): 44 cues, 0 bare RLS, 16 $RLS, @kittynim 3,
@kittymin 0, NBSP False; regenerated file byte-identical to the saved
`subs.ass` (SHA-256
`f9aa42faac8cbc83fab8a9f7d143b33fe599f631287b88e312094ecc07952e32`);
originals unchanged (repo + old workdir hashes equal before and after).
**Parameters completed:** REPRODUCE §2 now lists the full tx hash, every
RPC/Explorer parameter, the RPC getLogs range (single block 24825928, 3
addresses), the contract calls, the txlist ranges, and all 9 registry
getLogs chunks (195 logs). Process substitution removed from the guide
(§2C now uses the Python comparator); prerequisites note the shell snippets
are POSIX-only.

## 22 Nov 2026 — review round 4 (GPT review, terminology + Explorer params)

**Terminology:** "byte-identical" for the TX re-fetch replaced with
"parsed JSON values match" (REPRODUCE §2C, §5, §6 level 2) — the comparator
parses JSON and compares values, not raw bytes; whitespace and object key
order are not compared; types and values must match; key presence must
match; array order is compared. The 7 remaining "byte-identical" claims
are all genuine `diff` / `cmp` / SHA-256 checks (decode outputs, `subs.ass`,
audit-report copy, renamed video file) and were kept. The duplicated
byte-level-identity explanation in REPRODUCE §5 was merged into a single
bullet (same list, same distinction: re-fetch uses parsed-value comparison,
not byte comparison).
**Negative test corrected:** scenario B changed one hex digit (`8` → `9`
in `0x17ad049` vs `0x17ad048`), not one whole byte — corrected in REPRODUCE
and RESEARCH-TRAIL; FAIL + exit 1 unchanged.
**Explorer parameters:** completed from the stored evidence
(`calls[].endpoint` in `explorer.json` and
`explorer-relayer-txlist.json`, confirmed by TX-AUDIT-REPORT.md §1): full
txlist URLs including `address=0xa5f0…ac8`, and the full `gettxinfo` /
`gettxreceiptstatus` URLs with `txhash`. No parameter names invented.
**GNU sed:** added to the prerequisites — the `sed -i` edits in §3 and §4
need GNU sed (BSD/macOS `sed` requires a backup-suffix argument).
**INDEX updated:** sizes + SHA-256 of REPRODUCE and RESEARCH-TRAIL
refreshed in the §1 table.
Re-fetch status unchanged: still TODO, not run.

## 22 Nov 2026 — re-fetch executed + comparator v2 (stage 1 close-out)

**Re-fetch RUN 22 Nov 11:02 WIB** (REPRODUCE §2A+§2B, verbatim): fetch
script exit 0, 18/18 checks PASS, 28 requests, all attempts 1. Comparator
v1 exit 1 (4/5 PASS) — the single FAIL was the live `eth_blockNumber`
read. Manual re-fetch: gettxreceiptstatus + related tx 3/3 MATCH;
gettxinfo + txlist differ ONLY in `confirmations` (live field); registry
chunks 0–7 MATCH, chunk 8 has 4 new logs above the snapshot tip
(24,869,295); fresh[:195] == saved 195. Full report:
`~/workspace/rayls-refetch-2026-11-22/REFETCH-REPORT-2026-11-22.md`.
**Correction:** the initial report misgrouped three block numbers
(24.895.548 / 24.902.058 / 24.918.873); correct values are 24.889.548 /
24.890.258 / 24.891.873 (hex `0x17bc8cc` / `0x17bcb92` / `0x17bd1e1`).
Transcription error in the report, not a data error — verified against
raw evidence in
`~/workspace/rayls-refetch-check-2026-11-22/CHECK-REPORT-2026-11-22.md`
(chunk-8 URL re-run identical; all 9 chunk ranges validated; identity
comparison of the 195 logs: 195 identical, 0 changed, 0 missing, 4 new;
order-insensitive result the same). The initial report keeps a correction
note; the error is not erased.
**Comparator v2.0.0:** separates stable historical payload (must match),
dynamic fields (`eth_blockNumber` by method, Explorer `confirmations` by
field path — recorded and shown, never failing), and post-snapshot
registry events (above tip 24,869,295 — counted and listed separately).
No general tolerance, no wildcard. Tested 22 Nov: real run stable 9/9
PASS, 6 dynamics, 4 post-snapshot events, exit 0; negative (one hex
digit) FAIL exit 1; decoy FAIL exit 1; dynamic-only change still PASS
exit 0; manual mismatches (txlist `gasUsed`, registry log `data`) FAIL
exit 1. REPRODUCE §2B/§2C/§5/§6 updated; v1's exit 1 is preserved as a
fact, not rewritten as a PASS.
Re-fetch TODO checkbox in the TX package: left unchecked pending Anara's
review of this round — the run itself is done and verified; ticket +
experiments G.1–G.6 still pending decisions.

## 22 Nov 2026 — comparator v2.1.0 (review round 7, stage 1 still open)

Review round 7 found three logic gaps in comparator v2.0.0 (its test
results are unchanged; its exit 1 on the real run is preserved as a fact):
**P0** registry comparison was one-way only (saved → fresh) and silently
dropped duplicate log identities; **P1** the `confirmations` rule applied
wherever the key appeared and asymmetric presence was silently skipped
through `zip`; **P2** txlist envelopes were not checked at all.
**Comparator v2.1.0** fixes all three: registry comparison is two-way
(every saved log at/below tip must be in fresh AND every fresh log
at/below tip must be in saved) with duplicate-identity FAIL in either
dataset; `confirmations` applies only at two determined locations
(gettxinfo result, txlist tx objects, identified by the saved call's
`method` string) and asymmetric presence is reported explicitly as
`[ASYMMETRIC]` AND fails the run; Explorer `status`/`message` are
compared for explorer.json and both txlist responses; related-tx
`jsonrpc` is compared while `id` is not (request echo — re-fetch used
1,2,3, saved run used 1,1,1). No general tolerance, no wildcard.
REPRODUCE §2B/§2C/§5/§6 updated; v2.1.0 code embedded verbatim in §2C
(byte-identical to the tested file).
Tested 22 Nov (same saved vs fresh pair, /tmp copies): real run stable
**9/9 PASS, exit 0** (6 dynamics, 4 post-snapshot events; registry now
"195 stable logs identical two-way"). New negatives, all FAIL exit 1:
fresh registry log injected at block 23,212,110 (below tip); exact
duplicate chunk-0 log; `confirmations` deleted from fresh gettxinfo
only; explorer message "OK"→"NOTOK" + txlist status "1"→"0". Retained
tests all behave: receipt hex-digit FAIL, decoy FAIL, dynamic-only 9/9
PASS exit 0, txlist `gasUsed` FAIL, registry log `data` change FAIL.
The doc-extracted v2.1.0 also runs exit 0. Verifier 23/23 PASS; raw
9/9 SHA unchanged. Stage 1 close-out still awaits Anara's review of
this round.

## 22 Nov 2026 — comparator v2.1.1 (review round 8, patch from ChatGPT)

Patch files delivered by Anara as uploads, SHA-256 verified before use:
comparator `bfef1f66…`, regression test `d2e96c7f…`, addendum
`fd0b04c4…` — all three matched. Canonical copies in
`~/workspace/rayls-refetch-2026-11-22/` (`compare_raw_v2_1_1.py`,
`test_registry_chunk_validation_v2_1_1.py`,
`REPRODUCE_revision8_addendum.md`); v1 and v2.1.0 files/results
untouched.
**Change:** every registry chunk envelope and result shape is validated
before aggregation — only (`1`/`OK`/list) and (`0`/`No logs found`/`[]`)
are accepted; missing/non-list results, API errors, unknown envelopes,
malformed logs, missing required fields, and invalid hex block numbers
fail the run. Two-way matching, duplicate detection, confirmations, and
envelope rules unchanged. REPRODUCE §2B/§2C/§5/§6 updated per the
addendum; v2.1.1 embedded verbatim in §2C (byte-identical to the
standalone file; doc-extracted copy runs exit 0).
**DEFECT in the delivered patch (reported as-is):** the supplied
regression test imports `compare_raw_v2_1.py` (v2.1.0) instead of
`compare_raw_v2_1_1.py`, so it crashes with
`AttributeError: module 'comparator' has no attribute
'validate_registry_chunk'` (exit 1) and does NOT test v2.1.1 as
delivered. The same 8 focused cases run against the actual v2.1.1
module pass 8/8. The test file was left byte-identical (hash preserved).
v2.1.1 is NOT marked certified on the strength of the delivered test
file alone; certification awaits Anara's decision on the filename
reference. Minor: the v2.1.1 docstring Usage line still says
`compare_raw_v2_1.py` (stale from v2.1.0).
**Integrated tests (22 Nov, same saved vs fresh pair):** real run stable
9/9 PASS exit 0 (6 dynamics, 4 post-snapshot events); missing `result`
FAIL; API-error empty chunk FAIL; unknown envelope FAIL; non-list
result FAIL; malformed log FAIL; invalid hex `blockNumber` FAIL; failed
chunk 8 FAIL (even though chunk 8 is expected to hold the 4
post-snapshot events); fresh historical log below tip FAIL; duplicate
identity FAIL; asymmetric `confirmations` FAIL; Explorer message/status
FAIL; receipt hex-digit FAIL; decoy FAIL; txlist `gasUsed` FAIL;
registry log `data` FAIL; dynamic-only 9/9 PASS exit 0. All test logs
in `~/workspace/rayls-refetch-2026-11-22/v211-*.log`.
**Environment note:** /tmp scratch (`/tmp/rayls-repro`,
`/tmp/refetch-manual`) was gone at the start of this round (VM
replacement) — the integrated tests ran from the durable mirrors in
`~/workspace/rayls-refetch-2026-11-22/fresh-raw/` + `fresh-manual/`,
whose hashes match the 11:02 run exactly. Raw originals 9/9 SHA
unchanged before/after. Verifier 23/23 PASS.
**RESOLVED 22 Nov 12:27 WIB:** the regression-test defect is fixed —
ChatGPT supplied `test_registry_chunk_validation_v2_1_1_fixed.py`
(one line: import now points to `compare_raw_v2_1_1.py`;
SHA-256 `e159a96f…` verified). The fixed file replaced
`test_registry_chunk_validation_v2_1_1.py`; the original defective file
is preserved as
`test_registry_chunk_validation_v2_1_1_original_defective.py`
(`d2e96c7f…`). Run from the comparator directory: **8/8 focused cases
PASS, exit 0**. Comparator v2.1.1 hash unchanged (`bfef1f66…`); raw
9/9 SHA unchanged before/after; v1/v2.1.0 untouched; verifier 23/23
PASS. Certification decision is Anara's.
**CERTIFIED 22 Nov 12:33 WIB (Anara's decision):** comparator v2.1.1
**PASSES CERTIFICATION** for the re-fetch validation scope tested:
regression test 8/8 PASS, real run 9/9 PASS, 15 integrated negative
tests rejected as expected, dynamic-only PASS, TX verifier 23/23
PASS. Comparator and raw-evidence hashes intact. Scope: certification
applies ONLY to comparator v2.1.1 and the recorded test scope — NOT
to the whole repo and NOT to all Rayls audit claims. The comparator
must not be changed again without a new review round. The TX-package
TODO re-fetch checkbox stays UNCHECKED; stage 1 close-out is a
separate decision by Anara. No staging, commit, or push approved;
final repo + privacy review follows before any approval is requested.
**Final repo + privacy review (22 Nov 12:33 WIB, after certification):**
git 8 modified + 70 untracked = 78 files, 0 staged; untracked
59,475,194 B (~56.7 MB; +37,347 B vs 10:34 = REPRODUCE + TRAIL
growth only). INDEX verified: all embedded hashes OK except one
typo — `decode_tx_09edab2b.py` listed with 17 hex chars (extra
trailing `e`); file itself intact (full SHA
`e1dca19041676bede7aa…`), INDEX corrected to the 16-char prefix.
REPRODUCE's v2.1.0/v2.0.0 mentions are historical only. TODO.md
re-fetch checkbox still UNCHECKED (correct); its parenthetical
"(the check has not been run yet)" is now stale — wording fix
deferred to the stage-1 close decision. Standalone comparator .py
files live outside the repo (`~/workspace/rayls-refetch-2026-11-22/`);
the repo holds only the embedded copy in REPRODUCE.md — the procedure
is still reproducible from the repo alone. Privacy: no secrets
(private keys, API keys, passwords, mnemonics, Bearer/session
tokens), no emails, no phone numbers (the `08…` matches were false
positives inside hex blobs), no Siak/Riau/Pekanbaru, no XE/Hanura
references. "anara" appears in 19 files — intentional public
attribution (TX reconstruction + owner-confirmed @kittynim), repo is
public by design. **Main open item before commit:** raw footage
(24.8 MB) + VO mp3 (3.0 MB) are untracked and NOT gitignored — a
blanket `git add -A` would commit them, against the 9/10 evaluation's
recommendation, and the journey manifest/README still do not mark
them local-only. File-list cleanup is still undone. Verifier 23/23
PASS. Full findings in
`~/workspace/rayls-refetch-2026-11-22/final-review-2026-11-22.md`.
**STAGE 1 CLOSED 22 Nov ~12:40 WIB:** re-fetch evidence re-reviewed
(11:02 run, check report, v2.1.1 results, verifier) — all consistent:
v2.1.1 real run re-run 9/9 PASS exit 0 (6 dynamics, 4 post-snapshot
events), verifier 23/23 PASS, raw 9/9 SHA unchanged. TODO.md
re-fetch checkbox CHECKED; the stale "(the check has not been run
yet)" parenthetical replaced with the factual closed status. This
closes stage 1 (re-fetch verification) only — not the whole Rayls
audit, not the ticket, not G.1–G.6, not the commit.
**Integrated finalisation round (22 Nov ~12:40 WIB, this round):**
(1) Stage-1 evidence re-reviewed and closed (above). (2) File-list
cleanup: raw footage (24,777,960 B) + VO mp3 (2,953,936 B) excluded
from the commit by exact-path `.gitignore` rules (lines 10–11);
originals untouched (hashes 610a5cd3… / ebb2fdda… unchanged); marked
local-only in the journey manifest (new `local_only` flags + note;
manifest 12/12 entries still validate; manifest hash now
870cab90fdf0ddcc, 5,072 B), the journey README, `raw-data/videos/
README.md`, and INDEX §5. No other empty/temp/cache/log/build
artifacts found; largest commit candidates are the two finals (20.6 +
8.5 MB, intended). (3) TX manifest updated for the TODO.md change
only (3,344 → 3,765 B, b537fbaa…; all other 19 entries re-verified
against disk; manifest 9,351 B / 58e68862…; verifier 23/23 PASS).
(4) INDEX corrections: decode-hash typo fixed (17 → 16 chars);
run-1 "report" hash misattribution fixed — `aa544d47…` is the
verification report, the combined report is `bc7692ef…` (file itself
untouched, mtime 21 Nov 12:56); TRAIL "Standing unknowns" re-fetch
line corrected to DONE; README duplicate "## Status" heading fixed +
certification line added with scope; REPRODUCE §2C Usage-filename
note added OUTSIDE the embedded code block (embedded v2.1.1 still
byte-identical to the tested file). (5) Repo audit: 0 broken md links;
runs 2/3 manifests 5/5 OK; v1 run 6/6 files verified individually
(v1 manifest uses bare filenames — known limitation); only duplicate
groups are the intentional run script copies + the two identical
render-report pass files (build records, kept). Privacy re-check:
clean (only policy wording matches). @anara attribution still
correctly labelled "reconstruction, not an on-chain fact". (6) Ticket
draft written (`tickets/rayls-team-questions-draft-2026-11-22.md`,
10 questions, taxonomy-labelled, NOT SENT). (7) G.1–G.6 decision table
written (`experiments/g1-g6-decision-table.md`; read-only: G.2/G.4/
G.6; tx: G.1/G.3/G.5; nothing run). Full findings in
`~/workspace/rayls-refetch-2026-11-22/finalisation-report-2026-11-22.md`.

## 22 Nov 2026 — article audit r3 + addendum F17 + sanitization (public batch)

(1) Article audit r3 delivered (59,742 B, SHA `6a1be437…`): §4.1 + all
4,416 mentions split into integer / unit / "total fee" layers; §7.5
claim 4 uses "user-level sender/receiver"; r2 size/SHA discrepancy
explained (47,530 B measured before §8.4 was restored; +567 B =
48,097 B). (2) Anara's r3 review: one correction, §6 F17 — split into
F17a (statement[3–7] = verified fact) and F17b (statement[8] integer
4.416 × 10¹⁸ = verified fact; RLS unit = interpretation; "total fee" =
inference). Recorded in the addendum
(`ARTICLE-AUDIT-2026-11-22-addendum-f17.md`, 17,777 B, SHA `b8e64fff…`);
r3 itself frozen, not edited. Sweep: F17 was the only remaining
classification calling 4,416 a verified total fee. (3) Pre-commit
checks on the 80-file list (31,837,274 B): secret sweep clean (7
meta-statements only), email/phone 0, Binance wallet `0x3D9F…` 0;
runs/ 20 files + raw RPC (18,794 B, clean); `.src/index.html` stale
text ×1 (deliberate). Two findings needing decisions: (a) chk-21/22
show truncated Enygma Spend/View key fragments — same fragments also
in the final videos; (b) ticket draft carries 5 outdated
classifications (Q5 ×2, Q6, Q7, Q10). (4) Anara's decisions: F17
approved; sanitize before publication; ticket draft excluded from the
current batch (local draft, separate revision). (5) Sanitization done:
public `chk-21-public.jpg` / `chk-22-public.jpg` (PIL GaussianBlur
r=25 on the key line, verified by viewing); public 720p
(`b5c91ee1…`, 10,041,261 B) and 1080p (`e1e7a339…`, 20,153,708 B)
videos (ffmpeg full-width boxblur of the header band at t 20–24,
82–88, 109–115, 138–144, 176–185.533 s; verified one frame per range +
control at t=60 s). Originals untouched (hashes kept in the journey
manifest) and excluded via `.gitignore` exact-path rules. Addendum
sanitized: key fragments removed (0 remaining in any proposed text
file). (6) INDEX / RESEARCH-TRAIL / REPRODUCE updated to reference r3
+ addendum and the public versions; journey manifest 16/16 verified;
root README `tickets/` line corrected (draft, not sent). No staging,
commit, push, or ticket send.

## 22 Nov 2026 — repo restructure Phase 1 (presentation)

Reason: the GitHub homepage read as an archive of nested Markdown folders
(6 files + 10 folders at root; 13 folders holding only one README each),
while the scripts, JSON evidence, and CSVs were buried 2–4 levels deep.
Anara asked for the research surface to be visible from the root, using
`rayls-mainnet-block-research` as a display reference only (not its
content or methodology). Approved in principle 22 Nov 2026 with 9
corrections (v2 plan); execution approved the same evening. Phase 2
(path-robustness for the TX scripts) deferred to separate work — TX
scripts, manifests, and verifier untouched.

Changes (one commit, not pushed):
- Moved: `01-no-overwrite-fix-report.md` (root) → `runs/01-no-overwrite-fix-report.md` (byte-identical).
- Created: `audit_report.json` (root, generated — integrity PASS vs findings classifications kept separate) + `datasets/` content: `tx_logs.csv` (7 rows), `registry_usernames.csv` (195 rows), `statement.csv` (10 rows, r3/F17 labels), `relayer_txs.csv` (2 rows, dedup), `build_datasets.py`, `verify_datasets.py`, `datasets_checksums.sha256`. All derived by script from 11 TX-package JSONs; `verify_datasets.py` 9/9 PASS.
- Deleted: 12 empty-folder READMEs — `docs-review/`, `findings/` ×5, `raw-data/` ×4, `contracts/interactions/`, `contracts/token-flows/`. Their rules were transplanted verbatim first: token-flows (four-separation) + interactions → `contracts/README.md`; docs-review → INDEX.md §10; findings entry rules → `findings/README.md`; raw-data storage rules → `raw-data/README.md`.
- Edited (living docs only): `README.md` (rewritten in the reference shape), `INDEX.md` (§10 Docs review + §11 path history + datasets rows), `REPRODUCE.md` (§8 datasets), `contracts/README.md`, `findings/README.md`, `raw-data/README.md`, `datasets/README.md`, `runs/README.md`, and this file (this entry).
- Kept: `tickets/README.md` + `tickets/` (Anara's decision — rules for recording Rayls team Q&A). Kept untouched: all raw evidence, the TX package, the journey, runs data, scripts, and all frozen docs (r1/r2/r3, addendum F17, TX ADDENDUM, initial audit report). No ticket sent. No push — push only after Anara's separate approval.
- Governing interpretation unchanged: r3 + addendum F17 remain the latest authority; old labels in `audit_summary.json` q8 / TX report Q8 / `fee.comparison` are superseded (see INDEX.md §11).
- Note (execution): the `docs-review/` deletion removed the folder, but its rules live on in INDEX.md §10; the `findings/` and `raw-data/` subfolder READMEs held more than one-line rules, so their entry/storage rules were transplanted in full rather than dropped.

## Standing unknowns (consolidated, 22 Nov 2026)

- Selective auditing: not independently verified on this deployment; scope
  conflict unresolved (scoped vs network-wide vs per-deployment).
- bx proxy-vs-bundle mismatch; RLS token slot anomaly; 0.0001 RLS demo fee
  discrepancy; proof-time figures; statement positions 0/1/2/9; identity of
  `0x71af…`; exact nature of the 3.84 relayer fee; verified vault source.
- Experiments G.1–G.6: not run (need Anara's approval). Ticket to the Rayls
  team: draft written 22 Nov 2026 (10 questions), NOT SENT, excluded from
  the current public batch — local draft for separate revision.
- Re-fetch verification of the TX audit: DONE 22 Nov 2026 — comparator
  v2.1.1 CERTIFIED 12:33 WIB; stage 1 closed 22 Nov 2026 (see the
  stage-1 entry above). No longer an open unknown.
- The 12:30 WIB inventory report exists only in chat (see above).

## 23 Nov 2026 — English translation of the 8 Indonesian documents (public repos)

Anara's decision: no Indonesian-language document in either public
repository. All 8 remaining Indonesian documents were translated to
faithful English (23 Nov 2026, ~00:41–00:48 WIB); nothing else changed.
Indonesian sources are retained privately in
`~/workspace/backups/rayls-id-sources-20261123-0041/` (with
`SOURCES-HASHES.txt`) and are NOT in either repository.

- `ARTICLE-AUDIT-2026-11-22-r3.md` (frozen): 59,742 B / `6a1be437…` →
  61,062 B / `709565ac…`. Translator's note prepended; findings, numbers,
  hashes, tables, evidence labels, limitations, and conclusions unchanged.
  §8.5 still describes the frozen Indonesian source, as written.
- `ARTICLE-AUDIT-2026-11-22-addendum-f17.md` (frozen): 17,777 B /
  `b8e64fff…` → 18,593 B / `f3f16550…`. Translator's note prepended;
  F17a/F17b split and all classifications unchanged.
- `runs/01-no-overwrite-fix-report.md`: 15,329 B / `435c75d2…` → 15,432 B /
  `2ccd1b66…` (288 lines unchanged).
- `experiments/g1-g6-decision-table.md`: 6,251 B / `77b23d20…` → 6,287 B /
  `71a2fd25…` (43 lines unchanged).
- `runs/20261121T054711Z/findings/verified-facts/01_network_identity_complete_report.md`:
  33,459 B / `bc7692ef…` → 33,611 B / `2cbdc977…` (756 lines unchanged;
  only 25 lines carried Indonesian prose).
- `EDIT-PLAN.md`: 4,909 B / `cc0b8603…` → 4,885 B / `dd4c18fd…`.
- `experiments/transactions/tx-09edab2b/.src/build_tx_pdf.py`: comments
  were already English; the 10 Indonesian display strings were translated
  (14,097 B / `96e0296e…` → 14,151 B / `1c526e5f…`). Code behavior unchanged
  (AST identical except string constants); the generator now emits the same
  English labels as the translated `.src/index.html`.
- `experiments/transactions/tx-09edab2b/.src/index.html`: 506,135 B /
  `69f218a8…` → 506,189 B / `bcd9ee5b…` (6,234 lines; exactly 25 lines
  changed, visible text only — no tag, attribute, script, URL, number,
  hash, or path touched). The tracked PDF built from it is unchanged.

Verification (23 Nov 2026, re-run after translation): Indonesian-word
sweep of the full proposed trees — 0 files with ≥3 hits; 0x-hex and URL
sets identical per file vs the Indonesian sources; digit multisets
identical except the translator's-note SHAs in r3/F17, one added
"Module 01" clarifier in the no-overwrite report, and digit→word
rendering of "3 seconds" in two r3 prose bullets (value unchanged).
Journey manifest updated for the new EDIT-PLAN.md hash/size (16/16);
INDEX.md and REPRODUCE.md updated to the new r3/F17/report hashes.
TX verifier 23/23, datasets verifier 9/9, datasets checksums 5/5, runs
checksums 5/5 ×2 (+ 3/3 for the older v1 run), links 49/49, both public
videos match the manifest. Commit + push of branches
`docs/fix-doc-consistency` (old repo) and `fix/crlf-normalization`
(new repo) approved by Anara 23 Nov 2026 ~00:42 WIB; merge to `main`
NOT approved.
