#!/usr/bin/env python3
"""Build the root-level datasets for rayls-enygma-public-testnet-research.

Reads 11 JSON source files from the Week 2 TX audit package
(experiments/transactions/tx-09edab2b/) and writes, in exclusive mode
(refuses to overwrite):

  datasets/tx_logs.csv                 (7 rows, one per TX log)
  datasets/registry_usernames.csv      (195 rows, one per UsernameSet log)
  datasets/statement.csv               (10 rows, one per statement word)
  datasets/relayer_txs.csv             (2 rows, deduplicated by tx hash)
  audit_report.json                    (root; integrity + findings)
  datasets/datasets_checksums.sha256   (SHA-256 of the 4 CSVs + audit_report.json)

Stdlib only. Paths are derived from __file__ (repo root = parent of
datasets/), so the script works from any working directory and in a fresh
clone.

Rules that bind this script (restructure plan v2, 22 Nov 2026):

- The statement array is RE-PARSED from the raw calldata
  (raw/transaction.json) with the same ABI word-splitting used by
  scripts/decode_tx_09edab2b.py v1.0.0 (word() / receipt-tuple walk,
  copied here with attribution). The re-parsed values must equal the
  values in decoded/decoded_events.json; a mismatch fails the build.
- Classification labels do NOT come from the old JSONs. In particular,
  decoded_events.json `calldata.statement_interpretation.statement_8`
  and audit_summary.json q8 call statement[8] "the TOTAL fee ... =
  4.416 RLS exactly" as a verified fact. That label is SUPERSEDED by
  r3 §4.1 + addendum F17 (F17b): the integer is a verified fact, the RLS
  unit is an interpretation, "total fee" is an inference. The labels in
  statement.csv and audit_report.json are hardcoded below, each with a
  comment citing r3 §4.1 / addendum F17 §A.
- Event names in tx_logs.csv come from the demo-bundle ABI
  (decoded/bundle-abi-extract.json) via topic0 keccak matching, as done
  by the decode script. The deployed SharedVault implementation
  (0xAd966704...) has NO verified source, so the names are signature
  matches only — not proof of internal contract logic. The CSV's
  evidence_label column says so on every row.
- audit_report.json is split into `integrity` (PASS = data integrity +
  internal consistency ONLY) and `findings` (each finding carries its
  own classification). See the `status_note` field.
- The verifier result (23/23 PASS) is a RECORDED value from the 22 Nov
  2026 run (see RESEARCH-TRAIL.md); this script does not run the TX
  verifier. The two manifests ARE checked from disk during the build:
  every present entry must match bytes + SHA-256, and every absent entry
  must be a local-only entry (expected absent). A mismatch fails the
  build, so no PASS report can be written over broken evidence.
- Output is LF only (csv lineterminator='\\n', json with '\\n'), and
  files are written in mode 'x' — never overwrite committed data.

Usage:
    python3 datasets/build_datasets.py
"""

import csv
import hashlib
import io
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PKG = REPO / "experiments" / "transactions" / "tx-09edab2b"
RAW = PKG / "raw"
DEC = PKG / "decoded"
JOURNEY = REPO / "experiments" / "testnet-journeys" / "week2-private-payment"
OUT = REPO / "datasets"

# --- recorded values (not recomputed by this script) -----------------------
# TX verifier outcome, run 22 Nov 2026, recorded in RESEARCH-TRAIL.md.
# The verifier itself is run as a separate test step (restructure plan §8.3).
VERIFIER_RECORDED = (
    "scripts/verify_tx_audit_09edab2b.py 23/23 PASS (run 22 Nov 2026)"
)

# --- classification labels (r3 §4.1 + addendum F17 §A; NOT from old JSONs) -
CLS_F17A = "verified-fact"
BASIS_F17A = "F17a (r3 §4.1): value matches log topic/data"
CLS_F17B = "verified-fact (integer); RLS unit = interpretation; 'total fee' = inference"
BASIS_F17B = "F17b (r3 §4.1 + addendum F17 §A)"
CLS_UNKNOWN = "unknown"
BASIS_UNKNOWN = "unidentified (r3 §4.1)"

EVENT_EVIDENCE_LABEL = (
    "verified-fact (signature match); implementation logic unproven"
)

STATUS_NOTE = (
    "PASS refers only to data integrity and internal consistency. "
    "It does not mean every interpretation is proven — see each "
    "finding's classification and r3 §7 limitations."
)


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_text_exclusive(path, text):
    """Write in mode 'x': refuse to overwrite an existing file."""
    with open(path, "x", encoding="utf-8", newline="") as f:
        f.write(text)


def csv_text(rows, fieldnames):
    buf = io.StringIO(newline="")
    w = csv.DictWriter(buf, fieldnames=fieldnames, lineterminator="\n")
    w.writeheader()
    for row in rows:
        w.writerow(row)
    return buf.getvalue()


# --- ABI word helpers (copied from scripts/decode_tx_09edab2b.py v1.0.0) ---
def word(b, i):
    return int.from_bytes(b[i * 32:(i + 1) * 32], "big")


def word_hex(b, i):
    return "0x" + b[i * 32:(i + 1) * 32].hex()


def parse_statement_from_calldata(tx_input_hex):
    """Re-parse the 10-word statement array from the raw calldata.

    Same walk as decode_tx_09edab2b.py: params start after the 4-byte
    selector; word 0-2 are the head offsets (receipt, ciphertextI,
    ciphertextII); the receipt tuple starts at params[off_receipt];
    inside the tuple, word 8 is the statement offset, words 9/10 are
    numberOfInputs/numberOfOutputs; the statement array is
    (length word, then length words) at that offset within the tuple.
    """
    inp = bytes.fromhex(tx_input_hex[2:])
    params = inp[4:]
    off_receipt = word(params, 0)
    r = params[off_receipt:]
    stmt_off = word(r, 8)
    stmt_base = stmt_off
    stmt_len = word(r, stmt_base // 32)
    statement = [word_hex(r, stmt_base // 32 + 1 + i) for i in range(stmt_len)]
    return [int(v, 16) for v in statement], statement


def decode_username(data_hex):
    """ABI-decode a UsernameSet log `data` field to its username string.

    Layout: word0 = offset 0x20, word1 = byte length N, then N ASCII
    bytes. Returns (username, length). Raises on a malformed layout.
    """
    b = bytes.fromhex(data_hex[2:])
    offset = int.from_bytes(b[0:32], "big")
    if offset != 32:
        raise ValueError(f"unexpected string offset {offset}, expected 32")
    n = int.from_bytes(b[32:64], "big")
    return b[64:64 + n].decode("ascii"), n


def check_manifest(manifest_path, repo_root):
    """Check a manifest's files[] entries against disk.

    Returns (checked, matched, expected_absent). A present file must
    match bytes + SHA-256. An absent file is OK only if the entry is
    marked local_only; otherwise it is a failure.
    """
    manifest = load_json(manifest_path)
    checked = matched = expected_absent = 0
    for entry in manifest["files"]:
        rel = entry["relative_path"]
        path = repo_root / rel
        checked += 1
        if path.exists():
            actual_bytes = path.stat().st_size
            actual_sha = sha256_file(path)
            if actual_bytes != entry["bytes"] or actual_sha != entry["sha256"]:
                raise ValueError(
                    f"manifest mismatch: {rel} "
                    f"(disk {actual_bytes} B / {actual_sha[:16]}…, "
                    f"manifest {entry['bytes']} B / {entry['sha256'][:16]}…)"
                )
            matched += 1
        elif entry.get("local_only"):
            expected_absent += 1
        else:
            raise ValueError(f"manifest file missing on disk: {rel}")
    return checked, matched, expected_absent


def main():
    # --- load the 11 JSON sources -----------------------------------------
    txf = load_json(RAW / "transaction.json")
    rcf = load_json(RAW / "receipt.json")
    blf = load_json(RAW / "block.json")
    lgf = load_json(RAW / "logs.json")
    cof = load_json(RAW / "contracts.json")
    exf = load_json(RAW / "explorer.json")
    txlf = load_json(RAW / "explorer-relayer-txlist.json")
    rgf = load_json(RAW / "registry-usernames.json")
    rtxf = load_json(RAW / "related-tx-0xacc7d175.json")
    de = load_json(DEC / "decoded_events.json")
    au = load_json(DEC / "audit_summary.json")

    tx = txf["calls"][2]["response"]["result"]
    rc = rcf["calls"][0]["response"]["result"]
    block = blf["calls"][0]["response"]["result"]
    chain_id = txf["chain_id_expected"]
    assert chain_id == 7295799, f"unexpected chain_id {chain_id}"

    # --- tx_logs.csv -------------------------------------------------------
    raw_logs = sorted(
        lgf["receipt_logs_copy"], key=lambda e: int(e["logIndex"], 16)
    )
    decoded_logs = {e["logIndex"]: e for e in de["logs"]}
    assert len(raw_logs) == 7 and len(decoded_logs) == 7
    tx_log_rows = []
    for raw in raw_logs:
        idx = int(raw["logIndex"], 16)
        dec = decoded_logs[idx]
        assert dec["address"].lower() == raw["address"].lower()
        assert dec["topic0"].lower() == raw["topics"][0].lower()
        df = dec["decoded_fields"]
        if dec["event_name"] == "Nullifier":
            summary = (
                f"nullifier={df['nullifier']} "
                f"vaultId={df['vaultId']} treeNumber={df['treeNumber']}"
            )
        elif dec["event_name"] == "Commitment":
            summary = f"commitment={df['commitment']} vaultId={df['vaultId']}"
        elif dec["event_name"] == "EncryptedNote":
            summary = (
                f"commitment={df['commitment']} vaultId={df['vaultId']} "
                f"ciphertextI={df['ciphertextI_byte_length']}B "
                f"sha256={df['ciphertextI_sha256'][:16]}… "
                f"ciphertextII={df['ciphertextII_byte_length']}B "
                f"sha256={df['ciphertextII_sha256'][:16]}…"
            )
        else:
            raise ValueError(f"unexpected event {dec['event_name']}")
        tx_log_rows.append({
            "log_index": idx,
            "event_name": dec["event_name"],
            "topic0": dec["topic0"],
            "address": dec["address"],
            "block_number": int(raw["blockNumber"], 16),
            "data_bytes": (len(raw["data"]) - 2) // 2,
            "decoded_summary": summary,
            "evidence_label": EVENT_EVIDENCE_LABEL,
        })

    # --- registry_usernames.csv -------------------------------------------
    reg_rows = []
    for entry in rgf["logs"]:
        username, _n = decode_username(entry["data"])
        address = "0x" + entry["topics"][1][-40:]
        reg_rows.append({
            "username": username,
            "address": address,
            "block_number": int(entry["blockNumber"], 16),
            "block_timestamp": int(entry["timeStamp"], 16),
            "transaction_hash": entry["transactionHash"],
            "log_index": int(entry["logIndex"], 16),
        })
    assert len(reg_rows) == 195, f"expected 195 registry logs, got {len(reg_rows)}"
    # Cross-check the two owner-confirmed resolutions against audit_summary.
    by_name = {r["username"]: r["address"] for r in reg_rows}
    for name in ("anara", "kittynim"):
        assert by_name[name].lower() == au["registry_resolutions"][name]["address"].lower(), (
            f"registry resolution mismatch for @{name}"
        )

    # --- statement.csv -----------------------------------------------------
    # Re-parse from raw calldata; must equal the decoded file's values.
    stmt_ints, stmt_hex = parse_statement_from_calldata(tx["input"])
    decoded_stmt = de["calldata"]["receipt_tuple"]["statement"]
    assert decoded_stmt["length"] == 10, "unexpected statement length"
    assert stmt_ints == decoded_stmt["values_int"], (
        "re-parsed statement differs from decoded_events.json"
    )
    assert stmt_hex == decoded_stmt["values_hex"], (
        "re-parsed statement hex differs from decoded_events.json"
    )
    stmt_rows = []
    for i, (value_int, value_hex) in enumerate(zip(stmt_ints, stmt_hex)):
        if i in (3, 4, 5, 6, 7):
            cls, basis = CLS_F17A, BASIS_F17A
        elif i == 8:
            cls, basis = CLS_F17B, BASIS_F17B
        else:
            cls, basis = CLS_UNKNOWN, BASIS_UNKNOWN
        stmt_rows.append({
            "index": i,
            "value_decimal": value_int,
            "value_hex": value_hex,
            "classification": cls,
            "basis": basis,
        })
    assert stmt_ints[8] == 4416000000000000000, "statement[8] mismatch"

    # --- relayer_txs.csv ----------------------------------------------------
    # Dedup by tx hash: the two calls return the same 2 transactions.
    # The only field that differs between calls is `confirmations`
    # (call-time metadata that grows as blocks arrive); all core fields
    # must be identical. First call's row is canonical.
    seen = {}
    for call in txlf["calls"]:
        for row in call["response"]["result"]:
            h = row["hash"]
            if h in seen:
                a, b = seen[h], row
                core = [k for k in a if k != "confirmations"]
                assert all(a[k] == b.get(k) for k in core), (
                    f"duplicate relayer tx differs in core fields: {h}"
                )
            else:
                seen[h] = row
    assert len(seen) == 2, f"expected 2 unique relayer txs, got {len(seen)}"
    relayer_rows = []
    for row in sorted(seen.values(), key=lambda r: int(r["blockNumber"])):
        relayer_rows.append({
            "tx_hash": row["hash"],
            "block_number": int(row["blockNumber"]),
            "timestamp": int(row["timeStamp"]),
            "from": row["from"],
            "to": row["to"],
            "value_wei": int(row["value"]),
            "gas": int(row["gas"]),
            "gas_price_wei": int(row["gasPrice"]),
            "gas_used": int(row["gasUsed"]),
            "is_error": row["isError"],
        })

    # --- chain gas (recomputed, not copied) --------------------------------
    gas_used = int(rc["gasUsed"], 16)
    gas_price = int(tx["gasPrice"], 16)
    gas_limit = int(tx["gas"], 16)
    chain_gas_wei = gas_used * gas_price
    assert gas_used == 1316001 and gas_price == 48000000000
    assert gas_limit == 1630484
    assert chain_gas_wei == de["fee"]["onchain_gas_cost_wei"] == 63168048000000000

    # --- manifests (checked from disk; a mismatch fails the build) ---------
    tx_checked, tx_matched, tx_absent = check_manifest(PKG / "manifest.json", REPO)
    jn_checked, jn_matched, jn_absent = check_manifest(
        JOURNEY / "manifest.json", REPO
    )
    assert (tx_checked, tx_absent) == (20, 0), "TX manifest must be 20/20 present"
    assert jn_checked == 16, f"journey manifest must have 16 entries, got {jn_checked}"
    assert jn_matched + jn_absent == 16

    # --- cross-checks (decoded file) ----------------------------------------
    cc = de["cross_checks"]
    bool_checks = {k: v for k, v in cc.items() if isinstance(v, bool)}
    assert len(cc) == 13 and len(bool_checks) == 12
    assert all(bool_checks.values()), "a decoded cross-check is False"
    assert cc["log_count_receipt"] == 7 == de["log_summary"]["total"]

    # --- write the 4 CSVs (exclusive mode, LF only) -------------------------
    tx_logs_text = csv_text(tx_log_rows, [
        "log_index", "event_name", "topic0", "address", "block_number",
        "data_bytes", "decoded_summary", "evidence_label",
    ])
    reg_text = csv_text(reg_rows, [
        "username", "address", "block_number", "block_timestamp",
        "transaction_hash", "log_index",
    ])
    stmt_text = csv_text(stmt_rows, [
        "index", "value_decimal", "value_hex", "classification", "basis",
    ])
    relayer_text = csv_text(relayer_rows, [
        "tx_hash", "block_number", "timestamp", "from", "to", "value_wei",
        "gas", "gas_price_wei", "gas_used", "is_error",
    ])
    write_text_exclusive(OUT / "tx_logs.csv", tx_logs_text)
    write_text_exclusive(OUT / "registry_usernames.csv", reg_text)
    write_text_exclusive(OUT / "statement.csv", stmt_text)
    write_text_exclusive(OUT / "relayer_txs.csv", relayer_text)

    csv_hashes = {
        name: hashlib.sha256(text.encode("utf-8")).hexdigest()
        for name, text in [
            ("tx_logs.csv", tx_logs_text),
            ("registry_usernames.csv", reg_text),
            ("statement.csv", stmt_text),
            ("relayer_txs.csv", relayer_text),
        ]
    }

    # --- audit_report.json --------------------------------------------------
    block_ts = int(block["timestamp"], 16)
    block_ts_iso = datetime.fromtimestamp(block_ts, tz=timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )
    assert block_ts_iso == "2026-11-21T09:40:42Z"
    assert int(block["number"], 16) == 24825928
    assert len(block["transactions"]) == 1
    related = de["related_tx"]
    assert int(related["amount_wei"]) == 576000000000000000
    assert related["block"] == 24825932
    vault_impl = cof.get("implementation_from_slot")
    assert vault_impl is not None
    vault_impl = "0x" + vault_impl[-40:]

    report = {
        "integrity": {
            "status": "PASS",
            "csv_sha256": csv_hashes,
            "manifest_tx": f"{tx_matched}/{tx_checked} OK",
            "manifest_journey": f"{jn_checked}/{jn_checked} OK",
            "verifier": VERIFIER_RECORDED,
            "cross_checks": {
                "total": 13,
                "boolean_checks_pass": 12,
                "log_count_receipt": 7,
                "all_match": True,
            },
        },
        "findings": {
            "network": "Rayls Enygma Public Testnet",
            "chain_id": chain_id,
            "tx_hash": tx["hash"],
            "block": int(block["number"], 16),
            "block_timestamp_utc": block_ts_iso,
            "from": tx["from"],
            "to": tx["to"],
            "vault_implementation": vault_impl,
            "vault_implementation_source": "unverified",
            "logs_total": de["log_summary"]["total"],
            "logs_by_event": de["log_summary"]["by_event"],
            "logs_event_names_note": (
                "Event names are signature matches against the demo-bundle "
                "ABI (topic0 keccak); the deployed vault implementation "
                "has no verified source."
            ),
            "statement_8_integer_wei": stmt_ints[8],
            "statement_8_classification": CLS_F17B,
            "chain_gas_wei": chain_gas_wei,
            "chain_gas_display": "0.063168048",
            "chain_gas_token": "disputed (RLS vs USDr, r3 §3.3)",
            "gas_used": gas_used,
            "gas_limit": gas_limit,
            "gas_price_wei": gas_price,
            "related_tx_hash": related["tx_hash"],
            "related_tx_block": related["block"],
            "related_tx_amount_rls": "0.576",
            "related_tx_role": (
                "reconstruction (foundation fee counterpart); "
                "recipient identity unknown"
            ),
            "registry_logs": len(reg_rows),
            "registry_resolutions": {
                "anara": au["registry_resolutions"]["anara"]["address"],
                "kittynim": au["registry_resolutions"]["kittynim"]["address"],
            },
            "audit_document": (
                "ARTICLE-AUDIT-2026-11-22-r3.md + addendum F17"
            ),
        },
        "status_note": STATUS_NOTE,
    }
    report_text = json.dumps(report, indent=2) + "\n"
    write_text_exclusive(REPO / "audit_report.json", report_text)

    # --- checksums file (sha256sum format) ----------------------------------
    lines = []
    for name in ("tx_logs.csv", "registry_usernames.csv", "statement.csv",
                 "relayer_txs.csv"):
        lines.append(f"{csv_hashes[name]}  {name}")
    report_sha = hashlib.sha256(report_text.encode("utf-8")).hexdigest()
    lines.append(f"{report_sha}  ../audit_report.json")
    write_text_exclusive(OUT / "datasets_checksums.sha256", "\n".join(lines) + "\n")

    print("build_datasets: OK")
    print(f"  tx_logs.csv: 7 rows")
    print(f"  registry_usernames.csv: 195 rows")
    print(f"  statement.csv: 10 rows")
    print(f"  relayer_txs.csv: 2 rows")
    print(f"  audit_report.json: integrity PASS, "
          f"manifests TX {tx_matched}/{tx_checked}, "
          f"journey {jn_checked}/{jn_checked} "
          f"({jn_matched} present+match, {jn_absent} local-only expected absent)")
    for name, h in csv_hashes.items():
        print(f"  {name}: {h[:16]}…")
    print(f"  audit_report.json: {report_sha[:16]}…")


if __name__ == "__main__":
    try:
        main()
    except (AssertionError, ValueError, FileExistsError) as e:
        print(f"build_datasets: FAILED: {e}", file=sys.stderr)
        sys.exit(1)
