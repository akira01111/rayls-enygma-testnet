> **Translator's note (public version):** This document is a faithful English translation of the frozen Indonesian source (SHA-256 `b8e64ffff4c5a028ffc036994b8ff66e9ba6eed7a8ee36fa1b6ca476fd1c347a`), prepared for the public repository. It is a translation only — not a revision, update, or new version. All findings, numbers, hashes, addresses, URLs, tables, evidence classifications, limitations, and conclusions are unchanged from the frozen source. The Indonesian source is retained privately in the project archive and is not included in this repository.

# Addendum — Correction of §6 F17 + Pre-commit Check (22 Nov 2026)

**Addendum for:** `ARTICLE-AUDIT-2026-11-22-r3.md`
(59,742 bytes, SHA-256 `6a1be437ce51227286f23861615781c01d8e394c5a3b07ea34262ba785c6638f` —
the r3 file is NOT changed; this addendum corrects it by reference.)
**Date:** 22 Nov 2026, ~14:20 WIB.
**Scope:** (A) correction of the §6 F17 classification; (B) sweep for
similar classifications; (C) content and publication-suitability check
for the 80-file candidate commit list (r3 §8.6). No audit repeated, no
change to raw evidence, VO, or the certified comparator. The original
video files (final 720p/1080p) and original chk-21/22 are unchanged —
the public versions (`…-public.mp4`, `chk-21/22-public.jpg`) are
derivatives made in the sanitization round (see C.6).
No staging, commit, push, or ticket submission.
**Status:** Anara's review completed 22 Nov 2026 — the audit substance
and all decisions approved. Commit authorization and push authorization
(two separate approvals) still pending.

## A. Correction of §6 F17 — Classification Split

**F17 in r3 (line 486) — WRONG (merged):**

| # | Finding | Label | Source + reason |
|---|---|---|---|
| F17 | Statement[3–8] = nullifier, 3 commitments, vault address, fee | Verified fact | fresh value matching (§2.2) |

The problem: this line merges statement[3–8] under a single
"Verified fact" label, so the meaning of "fee" on statement[8] is also
read as a verified fact. That is not correct.

**The correct F17 (replacing the line above):**

| # | Finding | Label | Source + reason |
|---|---|---|---|
| F17a | Statement[3–7]: nullifier, three commitments, and vault address | Verified fact | fresh value matching (§2.2): statement[3] = nullifier (same as topic[3] of log[0]); statement[4–6] = 3 commitments (same as topic[2] of log[1–3]); statement[7] = vault address `0x9c5ad5e5…` |
| F17b | Statement[8]: integer 4.416 × 10¹⁸ | Verified fact (the integer); RLS unit = interpretation; meaning "total fee" = inference | integer read fresh from calldata (§2.2); RLS unit comes from the app display (see §3.2); meaning "total fee" established via app display + arithmetic, not a verified on-chain schema (§3.2) |

**Consequence for the article claims:** claim §7.5 number 3 in r3 is
already correct ("the integer 4.416 × 10¹⁸ appears in the transaction's
statement. The app presents that integer as 4.416 RLS and as the
total fee" — verified fact for the integer; inference for the RLS label
and total fee meaning) and does not need to change. Only the F17
classification in §6 changes.

## B. Sweep for Similar Classifications — F17 Is the Only One Remaining

All mentions of "total fee" and 4.416 in r3 were checked (grep,
22 Nov 2026). Result: **F17 is the only classification that still
calls 4.416 a verified total fee.** All others are already correct:

| Location in r3 | Content | Verdict |
|---|---|---|
| §2.2, line 149 (statement[8]) | integer + "RLS unit and 'total fee' meaning are interpretation" | correct |
| §3.1, lines 240–241 | integer = verified fact; RLS unit = interpretation; "total fee" = inference | correct |
| §3.2, lines 249–288 | three layers separated; "total fee" = inference | correct |
| §4.1, line 339 | integer = verified fact; unit + meaning = inference, "NOT an on-chain fact" | correct |
| §6 F6a/F6b, lines 474–475 | F6a integer = verified fact; F6b "total fee" = inference | correct |
| §6 F8, line 477 | 3.84 = 4.416 − 0.576 = reconstruction; unit of each term from different sources | correct |
| §6 F16, line 485 | mapping of 3 notes = reconstruction; unit + "fee" meaning = interpretation | correct |
| §7.1, lines 511–512 | integer = verified fact; RLS label + "total fee" meaning = inference | correct |
| §7.3, line 587 | semantic meaning of "total fee" — integer verified, interpretation inference | correct |
| §7.5 claim 3, lines 631–635 | integer = verified fact; RLS label + "total fee" = inference | correct |
| §6 F17, line 486 | statement[3–8] merged as verified fact, including "fee" | **WRONG — corrected in §A above** |

Sweep of related phrases in r3: 0 occurrences of "transfer lanjutan",
"moved 0.576 RLS to", and "fee settlement" as statements of fact
(grep, 22 Nov 2026).

## C. Content and Publication-Suitability Check — 80-File Commit List

**Method.** File list from r3 §8.6.4 (71 untracked) + 9 tracked-modified
(§8.6.2) = 80 files, reconstructed from `git status` and verified by
count (80 lines). Checks: (1) secret-pattern sweep across all 80 files
(mnemonic, seed phrase, private key, api key, password, bearer token,
recovery phrase); (2) sweep for email and phone numbers; (3) search for
Anara's Binance wallet address (`0x3D9F…`); (4) direct reading of
3 screenshots, the ticket draft, and samples of raw RPC responses;
(5) check of `.gitignore`, total size, and PDF source. No file was
changed during this check.

### C.1 General Sweep Results (80 files)

| Check | Result |
|---|---|
| Secret-pattern matches | **10 pattern matches, not secret findings.** All of them meta statements: statements in script headers and run reports that the scripts need no credentials; one guideline sentence in `scripts/README.md`; a list of things that must not be included (`RESEARCH-TRAIL.md:405`); and the description of the sweep method in this document itself (section C above) which names the patterns searched for. **No real secrets.** |
| Email / phone numbers | **0 findings.** |
| Anara's Binance wallet address (`0x3D9F…`) | **0 findings** in the 80 files. |
| Total size of 80 files | **31,837,274 bytes (~30.4 MB)** — figure for the ORIGINAL list (before sanitization). Largest at the time: original 1080p video 20,622,942 B, original 720p video 8,523,526 B, PDF 904,036 B, `.src/index.html` 506,135 B. New list after sanitization: **32,977,402 bytes (~31.4 MB)** (see sanitization round note at the end of this document); largest now public 1080p video 20,153,708 B and public 720p video 10,041,261 B. |

**Deliberately public inside these files** (not findings):
username @anara / @kittynim, EVM addresses `0x0c5b…` / `0x680d…`
(from the public registry + video), relayer/vault/contract addresses
(public on-chain data), and the `0x71af…` address (on-chain transfer
argument). All of these are already public via the registry, the explorer,
and the experiment video.

### C.2 runs/ — 20 Files (3 Runs + README)

| Contents | Result |
|---|---|
| `runs/*/datasets/` (csv, sha256 checksums, json metadata) — 9 files | Small (285–801 B). Network identity data (chain id, genesis, RPC). Suitable for publication. |
| `runs/*/findings/verified-facts/` (verification + complete report) — 4 files | Module 01 reports (2,964–33,459 B). No personal data. Suitable for publication. |
| `runs/*/raw-data/rpc-responses/01_network_identity_raw.json` — 3 files (6,046 / 6,374 / 6,374 B; total 18,794 B) | **Read directly.** Public testnet JSON-RPC: `eth_chainId`, `eth_getBlockByNumber`, `eth_getCode`, etc., plus `rpc_endpoint`, `retrieved_at_utc`, `http_status`, `attempts`. Sensitive sweep on all three: **0 findings**. Suitable for publication. |
| `runs/*/scripts/01_network_identity.py` — 3 files | Stdlib, read-only; header states "No private key, no wallet, no API secret". Suitable for publication. |
| `runs/README.md` (7,705 B) | Run documentation. Suitable for publication. |

### C.3 Screenshots — 3 Files in the Batch (Viewed Directly)

| File | Contents | Verdict |
|---|---|---|
| `raw-data/screenshots/chk-21-public.jpg` (121,762 B) | @kittynim home wallet: balance, EVM `0x680D…0eFC`; key rows "Enygma Spend" and "Enygma View" obscured (blur) — their hex values are not stated in this addendum | Suitable for publication (sanitized version — see C.6) |
| `raw-data/screenshots/chk-22-public.jpg` (127,132 B) | @kittynim home wallet, slightly different scroll: balance + "NFTs: None yet"; the same Spend/View key rows obscured (blur) | Suitable for publication (sanitized version — see C.6) |
| `raw-data/screenshots/chk-23.jpg` (86,426 B) | @kittynim Receive page: QR + full EVM address `0x680D90983da58Bcb7d127e3421193274e84E0eFC` | Suitable for publication (address already in registry + video) |

Original files `chk-21.jpg` (86,116 B) and `chk-22.jpg` (92,135 B) are
**local-only**: unchanged, not sanitized, and excluded from the batch (see C.6).

### C.4 PDF Source — `.src/index.html` (506,135 B)

- PDF build source, 21 Nov (`01_tx_audit_complete_history.pdf`, 904,036 B).
  Mentions `09edab2b` 125×. The old text "(the check has not been run yet)"
  appears **exactly 1×** — already documented in the 22 Nov finalization
  as a historical artifact deliberately retained (editing it would make
  the source differ from the PDF already built).
- Suitable for publication **with that note** (no change proposed in this round).

### C.5 Ticket Draft — `tickets/rayls-team-questions-draft-2026-11-22.md` (10,268 B, Read in Full)

This draft is **not yet sent** and marked DRAFT. Its contents were checked:
no personal data, secrets, or Anara's wallet address. However, this draft
contains **5 classifications that are now outdated against r3** and must be
updated before commit or before sending:

| Location in draft | Currently written | Should be (per r3 + this addendum) |
|---|---|---|
| Q5, Verified facts | "Calldata `statement[8]` = 4.416 RLS total fee (verified fact, on-chain)" | Integer 4.416 × 10¹⁸ = verified fact; RLS unit = interpretation; "total fee" = inference |
| Q5, Verified facts | "Chain gas for the tx = 0.063168048 RLS (verified fact, receipt)" | 0.063168048 native gas units (verified fact for the number); RLS unit not yet certain — app text conflicts (RLS vs USDr, r3 §3.3 / Q-B) |
| Q6, Verified facts | "statement[3]–statement[8] are verified by value matching (vault binding, fee total 4.416 RLS, etc.)" | statement[3–7] verified by value matching; statement[8] integer verified, "fee total" inference (F17 correction, §A) |
| Q7, Verified facts | "It received the 0.576 RLS settlement 4 blocks after the shielded transfer" | A separate transaction calls transfer() with arguments (`0x71af…`, 0.576 RLS); transfer purpose unknown — do not call it a "settlement" as fact (r3 correction 5) |
| Q10, Verified facts | "The 0.576 RLS settlement arrived as a separate ERC-20 transfer 4 blocks later." | Same as Q7: neutralize "settlement" to a transfer() call with its arguments |

**Recommendation:** update the draft first (needs Anara's approval to
edit — not done in this round), OR remove the draft from this commit
batch and commit after it is updated. Do not commit the draft as-is,
because its classifications conflict with r3.
**Resolution (22 Nov 2026, Anara's decision): removed from this commit
batch.** The draft is kept as a local draft for a separate revision; not
updated or sent at this stage.

### C.6 Sanitization Findings and Resolution

- chk-21 and chk-22 show fragments of @kittynim's **Enygma Spend**
  and **Enygma View** keys — only the first 10 characters + last 8
  characters of each key are visible, so the full keys **cannot be
  recovered** from those images. Their hex values are not stated in
  this addendum. The original files are **not sanitized** (not changed
  at all); only the public versions were obscured (see resolution
  below). The account is a public testnet account with no real value.
- **The same is also in the video:** frame of raw footage `raw_003.jpg`
  (the same @kittynim home screen, which went into the final video)
  shows the same key fragments. So removing the two screenshots alone
  does **not** remove those fragments from the repo — the **original**
  final videos (720p + 1080p, before sanitization) also contain them.
  The **public** sanitized videos no longer show those fragments (the
  key rows are blurred over their appearance ranges).
- This is not a leak of complete keys, but key-related material.
  **Resolution (22 Nov 2026, Anara's decision): sanitize before
  publication.** Public copies `chk-21-public.jpg` and
  `chk-22-public.jpg` were made with the key rows obscured (blur);
  public versions of the 720p and 1080p videos were made with the same
  fragments obscured over their appearance ranges. The original files
  (chk-21, chk-22, both final videos) were **not** overwritten or
  deleted — their original hashes are retained — but were **removed from
  the public batch** and excluded via `.gitignore` (exact-path).

### C.7 Verdict Summary per Group (80 Files)

| Group | Count | Verdict |
|---|---|---|
| 9 tracked-modified (README) | 9 | Suitable for publication |
| `.gitignore`, INDEX, REPRODUCE, RESEARCH-TRAIL, 01-no-overwrite-fix-report | 5 | Suitable for publication (INDEX/TRAIL/REPRODUCE already updated to reference r3 + this addendum — see sanitization round note) |
| `audit-reports/` (initial report + README) | 2 | Suitable for publication |
| `contracts/addresses/addresses.json` | 1 | Suitable for publication (public addresses) |
| `experiments/g1-g6-decision-table.md` | 1 | Suitable for publication |
| Journey (r3 + addendum + EDIT-PLAN + QA + README + 2 build scripts + 2 public videos + manifest + subs) | 11 | Suitable for publication (r3 = report in force; addendum = F17 correction; public videos already sanitized — see C.6; original videos removed from batch) |
| TX package (`.src/` + PDF + report + decoded + manifest + raw) | 24 | Suitable for publication (`.src/index.html` with the old-text ×1 note — see C.4) |
| `raw-data/screenshots/` | 3 | chk-23 suitable; original chk-21/22 removed, replaced by sanitized public versions (see C.6) |
| `runs/` | 20 | Suitable for publication |
| `scripts/` (4 scripts) | 4 | Suitable for publication |
| `tickets/` draft | 0 | **Removed from this commit batch** (local draft, separate revision — see C.5) |
| **Total proposed** | **80** | — |

## D. Anara's Decision Status

1. F17 correction in §A — **APPROVED** (22 Nov 2026). Use the F17a/F17b
   split; §7.5 claim 3 stays.
2. chk-21/chk-22 — **DECIDED: sanitize before publication** (see C.6).
   Public versions made; original files removed from batch.
3. Ticket draft — **DECIDED: removed from this commit batch.**
   Kept as a local draft for a separate revision; not updated or sent
   at this stage.
4. Update of INDEX/TRAIL/REPRODUCE to reference r3 (+ this addendum) —
   **DONE** (22 Nov 2026). INDEX, RESEARCH-TRAIL, and REPRODUCE already
   updated; journey README also updated.
5. Commit approval — **not yet given**.
6. Push approval — **not yet given** (separate approval from commit; push
   only after commit is approved and made).

**Count note (updated in the sanitization round, 22 Nov 2026):** the
80-file list in r3 §8.6 is the reviewed baseline. After the sanitization
decision, the candidate commit list became **80 new files** (same count,
changed composition): ticket draft out (−1), 4 original files out (−4:
2 final videos + chk-21/22), 4 public versions in (+4: 2 public videos
+ chk-21/22-public), and this addendum in (+1). So 80 − 1 − 4 + 4 + 1 =
80 files (9 tracked + 71 untracked). Table C.7 above already reflects
this new composition. r3 §8.6 was not changed in this round.

## Appendix — Verification in This Round

- r3 unchanged: SHA-256 `6a1be437ce51227286f23861615781c01d8e394c5a3b07ea34262ba785c6638f`
  (re-checked this round). r2: 48,097 bytes / `00e464f2…` (unchanged).
  r1: 35,269 bytes / `bd54c362…` (unchanged).
- Comparator v2.1.1 untouched: `bfef1f667408b227cac5b33e27c9352b5ad721ca0b78ed91899d8befdcac08a3`.
- Footage `610a5cd3…` + VO `ebb2fdda…` unchanged (re-checked this round).
- Journey manifest 12/12 is the result of this round's pre-commit check,
  before sanitization (12 entries). After sanitization, the manifest was
  updated to 16 entries (12 old entries + 4 new public versions; 4 original
  files marked local-only) and verified 16/16 — see sanitization round
  note. TX 20/20, verifier 23/23 PASS (re-run).
- Git: 28 status lines, 0 staged, no commit/push.

## Sanitization Round Note (22 Nov 2026, ~14:30 WIB)

Anara's decision (review of the r3 addendum) was carried out in full in this round:

1. F17 approved — F17a/F17b split per §A; §7.5 claim 3 stays.
2. Sanitization: public versions `chk-21-public.jpg` (121,762 B,
   `f62fd012…`) and `chk-22-public.jpg` (127,132 B, `9158ffa9…`) made
   (PIL GaussianBlur r=25 on the key rows; verified by direct viewing —
   key rows unreadable, balance and other UI intact); public 720p video
   (10,041,261 B, `b5c91ee1…`) and 1080p video (20,153,708 B,
   `e1e7a339…`) made (ffmpeg boxblur on the header band at t 20–24,
   82–88, 109–115, 138–144, 176–185.533 s; verified one frame per range
   + control at t=60 s without blur). Original files not
   overwritten/deleted (hashes retained in the journey manifest) and
   removed from the batch via `.gitignore` exact-path.
3. Ticket draft removed from the current commit batch; kept as a local
   draft for a separate revision; not updated or sent.
4. INDEX, RESEARCH-TRAIL, REPRODUCE updated to reference r3 + this
   addendum and the public versions; journey README updated; journey
   manifest 16/16 verified.
5. New candidate commit list: **80 files, 32,977,402 bytes (~31.4 MB)**
   (9 tracked + 71 untracked). Removed: ticket draft (outdated
   classifications), 2 original final videos + original chk-21/22 (key
   fragments), r1/r2 (superseded). Final verification this round:
   journey manifest 16/16, TX 20/20, verifier 23/23 PASS; r3
   `6a1be437…`, comparator `bfef1f66…`, footage `610a5cd3…`, VO
   `ebb2fdda…` unchanged; key-fragment sweep on the new list: 0; secret
   sweep: meta statements only; email/phone: 0; Binance wallet
   `0x3D9F…`: 0. Git: 28 status lines, 0 staged. No staging, commit,
   push, or ticket submission. Commit authorization and push
   authorization (two separate approvals) still pending.
