# Index - Rayls Enygma Public Testnet research archive

This index maps the research packages and records their provenance and status. It distinguishes source evidence, derived outputs, and sanitized public copies. Some original video and screenshot files are local-only; their provenance is recorded in the journey manifest and the exclusions in section 5.

Repository: `rayls-enygma-public-testnet-research` (public). The current public `main` branch points to `3424be4` ("Merge docs/public-documentation-review into main", 22 Nov 2026), which merges the documentation branch `3c442be` on top of the Phase 1 restructure `deb3d09` ("Restructure repo presentation (Phase 1)", 22 Nov 2026). This index records that restructure and the repository state described by the cited evidence; its historic working-tree snapshots are not statements about the current checkout.

Start with [README.md](README.md) for the findings and repository map. Use [REPRODUCE.md](REPRODUCE.md) to verify saved evidence or repeat checks, and [RESEARCH-TRAIL.md](RESEARCH-TRAIL.md) for the chronological record.

## 1. Entry points

| Path | Purpose and status |
|---|---|
| [README.md](README.md) | Research summary, evidence limits, and navigation. |
| [INDEX.md](INDEX.md) | This archive index, including provenance and path history. |
| [RESEARCH-TRAIL.md](RESEARCH-TRAIL.md) | Chronological research record and unresolved questions. |
| [REPRODUCE.md](REPRODUCE.md) | Commands, expected checks, and limits of reproduction. |
| [audit-reports/](audit-reports/) | Initial audit report, retained verbatim, and its provenance note. |
| [audit_report.json](audit_report.json) | Generated machine-readable summary; integrity status and finding classifications are separate. |
| [datasets/](datasets/) | Derived CSVs, build and verification scripts, and checksums. |
| [experiments/transactions/tx-09edab2b/README.md](experiments/transactions/tx-09edab2b/README.md) | Guide to the raw transaction evidence, decoded records, derived datasets, scripts, manifest, and reports. |
| [experiments/testnet-journeys/week2-private-payment/](experiments/testnet-journeys/week2-private-payment/) | Week 2 public video journey and governing article audit (r3 + F17 addendum). |
| [runs/](runs/) | Network Identity Audit runs and their evidence. |
| [scripts/](scripts/) | Audit and verification scripts. |

## Package organization

The repository is organized by research package, with shared collections for reusable scripts and datasets. For new, self-contained work, use a package README as the entry point and keep its inputs, processed outputs, run metadata, reports, exact script copy, and checksum record together. Shared derived datasets can remain in `datasets/` when they combine evidence from multiple packages.

Existing packages already follow parts of this model: each Network Identity run in `runs/<run_id>/` contains its raw response, processed CSV, metadata, verification report, script copy, and checksums; the Week 2 journey keeps its media, build inputs, and manifest together; and the transaction package keeps raw RPC/Explorer responses, decoded records, manifest, and audit notes together. The dataset builder and verifier are shared under `datasets/`; the transaction fetch, decode, and verify scripts are shared under `scripts/` and linked from the transaction package guide.

### Layout for new research packages

For a new, self-contained experiment, group the files by experiment rather than by extension:

```text
experiments/<family>/<experiment-id>/
  README.md                 # question, scope, navigation, reproduce steps
  raw/                      # captured source responses; immutable
  processed/                # decoded or normalized records
  derived/                  # outputs used only by this experiment
  scripts/                  # fetch, decode, build, and verify code
  reports/                  # audit and QA reports
  findings/                 # claims, interpretations, unknowns, and gaps
  metadata.json             # retrieval context and tool versions
  manifest.json             # source/output inventory with SHA-256
```

A run that produces repeated snapshots can put a `runs/<run-id>/` directory beneath that package, with its own raw data, processed outputs, metadata, exact script copy, report, and checksums. Keep cross-package CSVs and shared builders/verifiers in `datasets/` and `scripts/`, and link them from the package README. For media journeys, keep source inputs and sanitized public outputs clearly distinguished and record both in provenance metadata when the source is local-only.
No evidence files are moved in this review. The current script paths, run-relative checksums, TX and journey manifests, generated CSV paths, raw-response provenance records, and historical audit references depend on the existing layout. Keep this layout for those frozen packages; apply the package pattern to new work or prepare a separately tested migration before relocating any legacy files.

## Repository state at restructure

The sections below document the repository contents and decisions recorded during the Phase 1 restructure on 22 Nov 2026. Counts, file sizes, and hashes are point-in-time provenance notes; they are not current checkout status. The Phase 1 restructure is published on `main` as commit `deb3d09`.

## 2. Module 01 — Network Identity Audit (21 Nov 2026)

Script: `scripts/01_network_identity.py` v2.0.1, 35,650 bytes,
SHA-256 `5ff78700346b2ebd0c1a1e14c2f615b3fd4d422bb7cbbec489b3d48743260ae0`.
Change report: `runs/01-no-overwrite-fix-report.md`, 15,432 bytes,
SHA-256 `2ccd1b66e4946e2f…` (English translation, 23 Nov 2026; Indonesian
source retained privately, SHA-256 `435c75d289b172a69…`). Runs guide: `runs/README.md`, 7,705 bytes,
SHA-256 `4e8fa10506a679d4a…`.

| run | script | result | evidence |
|---|---|---|---|
| `runs/20261121T054711Z/` | v1.0.0 | PASS 9/9 | raw `2131d690…`, CSV `156c0b71…`, metadata `8d4e6011…`, checksums file `7b730708…`, verification report `aa544d47…`, combined report `2cbdc977…` (English translation, 23 Nov 2026; Indonesian source SHA-256 `bc7692ef…` retained privately), script copy `39caa42b…` (v1 manifest uses bare filenames — verify individually, see `runs/README.md`) |
| `runs/20261121T063234Z/` | v2.0.1 (build `c09d88eb…`, short check names) | PASS 13/13 | manifest 5/5 OK via `sha256sum -c` from the run dir |
| `runs/20261121T063327Z/` | v2.0.1 (build `5ff78700…`, long check names) | PASS 13/13 | manifest 5/5 OK via `sha256sum -c` from the run dir; final run |

Each run dir holds: `runs/<run_id>/raw-data/rpc-responses/01_network_identity_raw.json`,
`runs/<run_id>/datasets/` (CSV + metadata + checksums manifest),
`runs/<run_id>/findings/verified-facts/`
(verification report; run 1 also has the combined reading-copy report),
`runs/<run_id>/scripts/01_network_identity.py` (byte copy of the script that ran).

## 3. Initial audit report (21 Nov 2026)

- `audit-reports/ENYGMA-TESTNET-AUDIT-REPORT.md` — 65,433 bytes, 617 lines,
  SHA-256 `13622c8faf80ab4c70077d8976b7d8893b34ebebe41f06f9174e3dd98ce76b10`.
  English version (translated from the Indonesian original on 22 Nov 2026,
  on Anara's instruction; promoted to the main version the same evening on
  her approval). The Indonesian original is kept in the local archive, not
  in this repository. Provenance in `audit-reports/README.md`.
- Coverage: contract map (§C), observable activity (§D), volume (§E),
  privacy limits (§F), experiment plan G.1–G.6 (§G), repo structure (§H),
  source/address/hash register (§I). Its conclusion (selective auditing not
  independently verifiable) STANDS unless new evidence appears.

## 4. Week 2 TX audit package (21–22 Nov 2026)

`experiments/transactions/tx-09edab2b/` — TX
`0x09edab2bb8914aea3c905608ea9fcd09c056a470a5e150df03e0b324eff525bb`,
block 24825928. 20 manifest files + combined review PDF + `.src/` build
artifacts. Manifest: `manifest.json`, 9,351 bytes,
SHA-256 `58e68862de4c6825…` (covers all 20 files; the manifest itself and
the PDF are not listed in it). Updated 22 Nov 2026 for the stage-1
close-out (TODO.md entry only); all other entries unchanged and
re-verified against disk; verifier 23/23 PASS.

| group | files |
|---|---|
| raw (chmod 444) | `transaction.json`, `receipt.json`, `logs.json`, `block.json`, `contracts.json`, `explorer.json`, `explorer-relayer-txlist.json`, `registry-usernames.json`, `related-tx-0xacc7d175.json` (9 files: 5 script-generated + 4 manual — see REPRODUCE.md §2) |
| decoded | `decoded_events.json`, `audit_summary.json`, `bundle-abi-extract.json`, `lookups-4byte.json` |
| docs | `TX-AUDIT-REPORT.md` (16,604 B), `gaps.md` (5,004 B), `TODO.md` (3,765 B; re-fetch box checked at stage-1 close-out, 22 Nov 2026), `ADDENDUM-2026-11-22.md` (2,650 B; @kittynim owner-confirmed + integration note) |
| scripts | `scripts/tx_audit_09edab2b.py` v1.1.0, `scripts/decode_tx_09edab2b.py` v1.0.0, `scripts/verify_tx_audit_09edab2b.py` v1.0.1 |
| review copy | `01_tx_audit_complete_history.pdf`, 904,036 bytes, 155 pp, SHA-256 `b449fd80633393f9…` (derivative only, not in the manifest) |

Verification: independent verifier 23/23 PASS (re-run 22 Nov 2026,
exit 0). Key results: transferV2 proven, direct to SharedVaultProxy,
7 logs (1 Nullifier / 3 Commitment / 3 EncryptedNote), integer
4.416 × 10¹⁸ in calldata statement[8] (the RLS unit is an
interpretation from the app display and the "total fee" meaning is an
inference — see the article audit r3 §3.2), chain gas 0.063168048
native units (token identity disputed: RLS vs USDr — r3 §3.3), and a
separate ERC-20 transfer() call with arguments (`0x71af…`, 0.576 RLS)
4 blocks later (recipient identity and purpose unknown — r3 §7.5
claim 5). Receiver @kittynim → `0x680d90983da58bcb7d127e3421193274e84e0efc`
(on-chain verified + owner-confirmed 22 Nov 2026).

## 5. Week 2 video journey (21 Nov 2026)

`experiments/testnet-journeys/week2-private-payment/` — 9 files in the
manifest + README + manifest itself + article audit (r1/r2/r3/addendum).
Manifest `manifest.json`, 8,827 bytes, SHA-256 `0b4ba448d8517b2c…`, covers
16 files incl. inputs in `raw-data/`.

- Public finals (sanitized, 22 Nov 2026 — committed):
  `enygma-week2-private-payment-final-720p-public.mp4` (720p, 10,041,261 B,
  `b5c91ee1…`); `enygma-week2-private-payment-final-1080p-public.mp4`
  (upscale, 20,153,708 B, `e1e7a339…`). Truncated Enygma Spend/View key
  fragments are blurred at t 20–24, 82–88, 109–115, 138–144, 176–185.533 s;
  otherwise the same content as the originals (see the journey README and
  the article audit addendum §C.6).
- Original finals (`enygma-week2-private-payment-final.mp4`,
  `enygma-week2-private-payment-final-1080p.mp4`) are **LOCAL-ONLY,
  excluded from the public repository by `.gitignore`** (22 Nov 2026):
  they still show the key fragments. Hashes kept in the journey manifest
  for provenance.
- `subs.ass` (44 cues, `f9aa42fa…`), `build_subs.py`, `build_video_v2.py`,
  `EDIT-PLAN.md`, `QA-REPORT-V2.md`.
- Article audit (current): `ARTICLE-AUDIT-2026-11-22-r3.md` (61,062 B,
  `709565ac…`) + `ARTICLE-AUDIT-2026-11-22-addendum-f17.md` (18,593 B,
  `f3f16550…`) (F17 split F17a/F17b + pre-commit checks). Both are the
  English translations (23 Nov 2026) of the frozen Indonesian sources
  (r3 SHA-256 `6a1be437…`, F17 SHA-256 `b8e64fff…`, retained privately).
  Revisions r1/r2 are superseded, local record only, NOT committed.
- Inputs in `raw-data/videos/`: source footage (24,777,960 B,
  `610a5cd30d…` — filename is its content hash) + VO mp3 (2,953,936 B,
  `ebb2fdda…`). **Both are LOCAL-ONLY, excluded from the public
  repository by `.gitignore` (22 Nov 2026); hashes kept in the journey
  manifest for provenance.**
- Spelling-check frames in `raw-data/screenshots/`: `chk-21-public.jpg`,
  `chk-22-public.jpg` (public sanitized versions, key line blurred),
  `chk-23.jpg` (all read "Enygma"). Originals `chk-21.jpg`/`chk-22.jpg`
  are LOCAL-ONLY (see above).
- Full file list with hashes: the journey `manifest.json`.

## 6. Contracts

- `contracts/addresses/addresses.json` — 9,202 bytes,
  SHA-256 `f78f012886035836…`. Machine-readable contract map extracted
  verbatim from the initial audit (§C.2/C.3): yx + bx deployments, EIP-1967
  implementation slots, auditor/relayer/Multicall3/forwarder/EnygmaDvp,
  unknown-provenance `0xd908…`. All 35 addresses verified present in the
  audit report. The bx mismatch is recorded in the file's notes.
- `contracts/abis/README.md` — points to the TX package's
  `experiments/transactions/tx-09edab2b/decoded/bundle-abi-extract.json` (canonical home; not duplicated).
- `contracts/verified-source/README.md` — states plainly: **no verified
  contract source exists** for the deployed vault/registry implementations.

## 7. Scripts (no on-chain writes or signing; some scripts write local artifacts)

| script | version | bytes | SHA-256 (first 16) | role |
|---|---|---|---|---|
| `scripts/01_network_identity.py` | v2.0.1 | 35,650 | `5ff78700346b2ebd` | Module 01 fetch + checks |
| `scripts/tx_audit_09edab2b.py` | v1.1.0 | 17,448 | `6bee0b827faa24c0` | TX audit raw fetch (curl) |
| `scripts/decode_tx_09edab2b.py` | v1.0.0 | 37,807 | `e1dca19041676bed` | TX audit decode + summary |
| `scripts/verify_tx_audit_09edab2b.py` | v1.0.1 | 10,734 | `e081c3c22cbcceaa` | TX audit independent verifier |

## 8. Gaps and TODO (open)

- TX package: `experiments/transactions/tx-09edab2b/gaps.md` (7 gap groups)
  and `TODO.md` (ticket, experiments G.1–G.6, fee-settlement pattern
  check, Module 02 blocked, commit/push). The re-fetch check is CLOSED
  (stage 1, 22 Nov 2026; comparator v2.1.1 CERTIFIED).
- Consolidated standing unknowns: `RESEARCH-TRAIL.md` (last section).
- Ticket to the Rayls team: draft written 22 Nov 2026
  (`tickets/rayls-team-questions-draft-2026-11-22.md`, 10 questions,
  taxonomy-labelled), NOT SENT, and **excluded from the current public
  batch** (22 Nov 2026 decision — its classifications predate r3; local
  draft for separate revision).

## 9. Explicit exclusions (not in this repo, by decision)

- **Old research repo** `~/workspace/rayls-enygma-research/` (19 files,
  13–15 Nov + inventory review): referenced, never copied, never mixed in.
  Its `technical-evidence.md` and the baseline PDF
  (`~/workspace/your_files/rayls-enygma-technical-evidence/rayls-enygma-technical-evidence.pdf`,
  23 pp, 494,423 B, SHA-256 `2193d48b61715809b4a045eccf13663675d032cd92b24ce5bcc2ad4b4ce3d3ee`,
  created 15 Nov 2026) stay outside this repo.
- **`pdf/`** (10 review PDFs + 138 validation PNGs + 19 build-source files
  = 167 files, counted 22 Nov 2026): local-only review archive, never to be
  committed.
- **Superseded video versions** (`*-v720-backup.mp4`, `subs-v2-backup.ass`,
  `...-1080p-v2.mp4` byte-duplicate) and video working intermediates
  (`video_only*.mp4`, `segments_v2/`, `frames/`, `qa/`, `transcript/`, …):
  retained in `~/workspace/enygma-week2-video/`, not copied here.
- **Other 21 Nov workstreams** (Groq connector, PocketPal, video-generation
  audit, Raka animation, Marivale game): different projects, not Rayls
  research — not in this repo.
- **The 12:30 WIB inventory review (21 Nov):** delivered in chat only; no
  file exists. Recorded as a gap in `RESEARCH-TRAIL.md`, not reconstructed.

## 10. Docs review

Notes on official Rayls documentation, blog posts, and public reference
implementations relevant to Enygma. (Moved here verbatim from the former
`docs-review/README.md` during the Phase 1 restructure, 22 Nov 2026; the
folder was removed after the move.)

Rules:

- Every note records the source URL and the date it was accessed.
- A documented claim is recorded as a claim, not as a verified fact.
- Where docs and code disagree, or where two official sources disagree,
  both wordings are kept and the conflict is marked unresolved until the
  team gives context (see `tickets/`).

## 11. Path history — restructure Phase 1 (22 Nov 2026)

The Phase 1 restructure was published on `main` as commit `deb3d09`. This table records what moved, what was deleted, and where the content went. Frozen documents (r1/r2/r3, addendum F17, TX ADDENDUM, initial audit report) may still cite the old paths as historical records; use this table to resolve them.

| Change | Old path | New path / disposition |
|---|---|---|
| Moved | `01-no-overwrite-fix-report.md` (root) | `runs/01-no-overwrite-fix-report.md` (byte-identical) |
| Deleted (rules moved) | `contracts/token-flows/README.md` | Four-separation rule moved verbatim to `contracts/README.md` (§ "token-flows") |
| Deleted (rules moved) | `contracts/interactions/README.md` | Rule moved verbatim to `contracts/README.md` (§ "interactions") |
| Deleted (rules moved) | `docs-review/README.md` | Full text moved verbatim to INDEX.md §10 above; folder removed |
| Deleted (rules moved) | `findings/inferences/README.md` | Entry rules moved to `findings/README.md` |
| Deleted (rules moved) | `findings/official-claims/README.md` | Entry rules moved to `findings/README.md` |
| Deleted (rules moved) | `findings/reconstructions/README.md` | Entry rules moved to `findings/README.md` |
| Deleted (rules moved) | `findings/unknowns/README.md` | Entry rules moved to `findings/README.md` |
| Deleted (rules moved) | `findings/verified-facts/README.md` | Entry rules moved to `findings/README.md` |
| Deleted (rules moved) | `raw-data/explorer-exports/README.md` | Storage rule moved to `raw-data/README.md` |
| Deleted (rules moved) | `raw-data/original-documents/README.md` | Storage rule moved to `raw-data/README.md` |
| Deleted (rules moved) | `raw-data/rpc-responses/README.md` | Storage rule moved to `raw-data/README.md` |
| Deleted (rules moved) | `raw-data/transaction-receipts/README.md` | Storage rule moved to `raw-data/README.md` |
| Created | — | `audit_report.json` (root, generated) |
| Created | — | `datasets/tx_logs.csv`, `datasets/registry_usernames.csv`, `datasets/statement.csv`, `datasets/relayer_txs.csv` |
| Created | — | `datasets/build_datasets.py`, `datasets/verify_datasets.py`, `datasets/datasets_checksums.sha256` |
| Edited | `README.md`, `INDEX.md` (this file), `REPRODUCE.md`, `RESEARCH-TRAIL.md`, `contracts/README.md`, `findings/README.md`, `raw-data/README.md`, `datasets/README.md`, `runs/README.md` | Living docs only |
| Kept | `tickets/README.md` + `tickets/` | Kept by Anara's decision (rules for recording Rayls team Q&A) |

**Governing interpretation (unchanged by the restructure):** r3 +
addendum F17 are the latest interpretation authority. Labels in
`audit_summary.json` (notably q8) and the initial TX report that differ
from r3 are superseded:

| Topic | Old label (superseded) | Label that applies (r3 + F17) |
|---|---|---|
| statement[8] = 4.416×10¹⁸ wei | q8 / TX report Q8 / `fee.comparison`: "total fee IS public on-chain … = 4.416 RLS exactly" as verified-fact | F17b: integer = verified-fact; RLS unit = interpretation; "total fee" = inference |
| Chain gas 0.063168048 | q8 / TX report: "0.063168048 RLS" | Wei figure = verified-fact; token identity disputed (RLS vs USDr, r3 §3.3, Q-B open) |
| 0.576 RLS transfer | q8 (labelled verified-fact) frames it as the on-chain counterpart of the 0.58 fee; `related_tx.recipient_identity`: "recorded … as the Auditor EOA" | Transfer itself = verified-fact; role as foundation fee = reconstruction; recipient 0x71af… identity = unknown |

The old files themselves were NOT edited (frozen); the correction lives
in the new files (`audit_report.json`, the CSVs, `datasets/README.md`,
root README) and in this section.
