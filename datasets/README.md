# datasets

Tabular data derived by script from the Week 2 TX audit package
(`experiments/transactions/tx-09edab2b/`), built 22 Nov 2026 in the
Phase 1 restructure. Derived data never replaces raw evidence. If a
number is questioned, the check goes back to the TX package JSONs.

Rules (unchanged):

- Every dataset states which source files it came from, the method used,
  the date it was built, and a checksum.
- Derived data never replaces raw evidence. If a number is questioned, the
  check goes back to the source JSONs.
- Observed, reconstructed, and estimated values are kept separate and labelled
  as such.

## Datasets (built 22 Nov 2026 by `datasets/build_datasets.py`)

| File | Rows | Bytes | SHA-256 (first 16) | Source (11 JSONs) | Rule |
|---|---|---|---|---|---|
| `tx_logs.csv` | 7 | 2,382 | `7e709d4aa4eb3db0` | `raw/logs.json` + `decoded/decoded_events.json` | One row per log, ordered by logIndex |
| `registry_usernames.csv` | 195 | 27,655 | `6c3c3ed53f55f08a` | `raw/registry-usernames.json` | username = ABI-decode of `data`; address = topics[1] last 20 bytes |
| `statement.csv` | 10 | 1,817 | `29729d4750e3fab7` | `raw/transaction.json` (calldata, re-parsed) + `decoded_events.json` | One row per statement word; labels from r3 §4.1/F17 |
| `relayer_txs.csv` | 2 | 491 | `5004978006c15457` | `raw/explorer-relayer-txlist.json` | Deduplicated by tx hash (2 calls return the same 2 txs; only `confirmations` differs — call-time metadata, excluded) |

Also in this folder: `build_datasets.py` (20,842 B, `9f51cc5aebed8281`),
`verify_datasets.py` (16,821 B, `288f3c8d798866a2`), and
`datasets_checksums.sha256` (416 B, `6058c743eb8678d3` — SHA-256 of the
4 CSVs + `../audit_report.json`).

## How to rebuild and verify

```bash
python3 datasets/build_datasets.py    # refuses to overwrite (mode "x")
python3 datasets/verify_datasets.py   # expect: 9/9 checks PASS, exit 0
sha256sum -c datasets/datasets_checksums.sha256   # run from datasets/
```

`verify_datasets.py` re-derives every CSV independently (it does not
import the build script) and checks `audit_report.json` field by field,
both manifests from disk (TX 20/20, journey 16/16), and LF-only output.
It does NOT run the TX verifier — run
`python3 scripts/verify_tx_audit_09edab2b.py` separately (23/23 PASS).

## Governing interpretation (r3 + addendum F17)

The labels in these files follow r3 §4.1 / addendum F17 — NOT the old
JSON labels. The old labels are superseded and were deliberately NOT
copied:

- `audit_summary.json` q8 (labelled verified-fact) and
  `decoded_events.json` `fee.comparison` call statement[8] "the TOTAL fee
  … = 4.416 RLS exactly" as a verified fact. Per F17b the integer
  4,416,000,000,000,000,000 wei is a verified fact, the RLS unit is an
  interpretation, and "total fee" is an inference. `statement.csv`
  carries the F17b label; `audit_report.json` carries it in
  `statement_8_classification`.
- Chain gas 0.063168048 is a verified wei figure; the token identity is
  disputed (RLS vs USDr, r3 §3.3) — the old "0.063168048 RLS" label is
  not used.
- The 0.576 RLS transfer (block 24825932) is a verified fact; its role
  as the foundation fee is a reconstruction; the recipient `0x71af…`
  is unknown — not "the Auditor EOA (verified fact)".

## Provenance of event names (`tx_logs.csv`)

Event names (Nullifier/Commitment/EncryptedNote) are resolved by
keccak-matching topic0 against the demo-bundle ABI signatures
(`decoded/bundle-abi-extract.json`). The deployed SharedVault
implementation (`0xAd966704…`) has NO verified source, so the names are
signature matches only — not proof of internal contract logic. Every
row's `evidence_label` says so:
"verified-fact (signature match); implementation logic unproven".

## What PASS means (`audit_report.json`)

`audit_report.json` splits into `integrity` and `findings`. PASS in
`integrity` means data integrity + internal consistency only (CSVs match
their sources, manifests match disk, cross-checks hold). It does NOT
mean every interpretation is proven — each finding carries its own
classification; see the file's `status_note` and r3 §7 limitations.
