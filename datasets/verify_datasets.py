#!/usr/bin/env python3
"""Verify the root-level datasets for rayls-enygma-public-testnet-research.

Independently re-derives every dataset from the 11 JSON sources in the
Week 2 TX audit package (experiments/transactions/tx-09edab2b/) and checks
the committed files byte-for-byte. This script does NOT import
build_datasets.py: the parsing, decoding, and CSV-building logic is
re-implemented here on purpose, so a shared bug cannot pass both scripts.
Any drift between the two implementations fails loudly.

Checks (each printed PASS/FAIL; exit 0 only if all pass):

  1. tx_logs.csv — rebuilt from raw/logs.json + decoded/decoded_events.json
  2. registry_usernames.csv — rebuilt from raw/registry-usernames.json
     (ABI-decode of `data`; address from topics[1])
  3. statement.csv — rebuilt from a fresh parse of the raw calldata
     (raw/transaction.json) + r3 §4.1 / addendum F17 labels
  4. relayer_txs.csv — rebuilt from raw/explorer-relayer-txlist.json
     (deduplicated by tx hash)
  5. audit_report.json — every field re-derived from the sources;
     `integrity` vs `findings` split present; `status_note` present;
     classifications present on the sensitive findings
  6. datasets_checksums.sha256 — recomputed SHA-256 of each listed file
  7. TX manifest — all 20 entries present on disk, bytes + SHA-256 match
  8. Journey manifest — all 16 entries accounted for: present entries
     match bytes + SHA-256; absent entries must be local-only
     (expected absent)
  9. LF-only — no CR byte in any CSV or in audit_report.json

The TX verifier (scripts/verify_tx_audit_09edab2b.py, 23/23) is NOT run
by this script; it is a separate test step (restructure plan §8.3).

Usage:
    python3 datasets/verify_datasets.py
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

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, ok, detail))
    print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f" — {detail}" if detail else ""))


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def sha256_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def csv_text(rows, fieldnames):
    buf = io.StringIO(newline="")
    w = csv.DictWriter(buf, fieldnames=fieldnames, lineterminator="\n")
    w.writeheader()
    for row in rows:
        w.writerow(row)
    return buf.getvalue()


def _word(b, i):
    return int.from_bytes(b[i * 32:(i + 1) * 32], "big")


def _word_hex(b, i):
    return "0x" + b[i * 32:(i + 1) * 32].hex()


def parse_statement(tx_input_hex):
    """Fresh parse of the statement array from raw calldata (own code)."""
    inp = bytes.fromhex(tx_input_hex[2:])
    params = inp[4:]
    off_receipt = _word(params, 0)
    r = params[off_receipt:]
    stmt_off = _word(r, 8)
    stmt_len = _word(r, stmt_off // 32)
    statement = [_word_hex(r, stmt_off // 32 + 1 + i) for i in range(stmt_len)]
    return [int(v, 16) for v in statement], statement


def decode_username(data_hex):
    b = bytes.fromhex(data_hex[2:])
    if int.from_bytes(b[0:32], "big") != 32:
        raise ValueError("bad username string offset")
    n = int.from_bytes(b[32:64], "big")
    return b[64:64 + n].decode("ascii")


def check_manifest_file(manifest_path, label):
    manifest = load_json(manifest_path)
    matched = expected_absent = 0
    problems = []
    for entry in manifest["files"]:
        path = REPO / entry["relative_path"]
        if path.exists():
            if (path.stat().st_size != entry["bytes"]
                    or sha256_file(path) != entry["sha256"]):
                problems.append(entry["relative_path"])
            else:
                matched += 1
        elif entry.get("local_only"):
            expected_absent += 1
        else:
            problems.append(entry["relative_path"] + " (missing)")
    total = len(manifest["files"])
    ok = not problems and matched + expected_absent == total
    check(f"manifest {label}",
          ok,
          f"{matched}/{total} present+match, {expected_absent} local-only "
          f"expected absent" + (f"; problems: {problems}" if problems else ""))
    return ok


def main():
    txf = load_json(RAW / "transaction.json")
    rcf = load_json(RAW / "receipt.json")
    blf = load_json(RAW / "block.json")
    lgf = load_json(RAW / "logs.json")
    cof = load_json(RAW / "contracts.json")
    txlf = load_json(RAW / "explorer-relayer-txlist.json")
    rgf = load_json(RAW / "registry-usernames.json")
    de = load_json(DEC / "decoded_events.json")
    au = load_json(DEC / "audit_summary.json")

    tx = txf["calls"][2]["response"]["result"]
    rc = rcf["calls"][0]["response"]["result"]
    block = blf["calls"][0]["response"]["result"]

    label = "verified-fact (signature match); implementation logic unproven"

    # --- 1. tx_logs.csv ----------------------------------------------------
    raw_logs = sorted(lgf["receipt_logs_copy"], key=lambda e: int(e["logIndex"], 16))
    decoded_logs = {e["logIndex"]: e for e in de["logs"]}
    rows = []
    try:
        for raw in raw_logs:
            idx = int(raw["logIndex"], 16)
            dec = decoded_logs[idx]
            df = dec["decoded_fields"]
            if dec["event_name"] == "Nullifier":
                summary = (f"nullifier={df['nullifier']} "
                           f"vaultId={df['vaultId']} treeNumber={df['treeNumber']}")
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
                raise ValueError(dec["event_name"])
            rows.append({
                "log_index": idx, "event_name": dec["event_name"],
                "topic0": dec["topic0"], "address": dec["address"],
                "block_number": int(raw["blockNumber"], 16),
                "data_bytes": (len(raw["data"]) - 2) // 2,
                "decoded_summary": summary, "evidence_label": label,
            })
        rebuilt = csv_text(rows, ["log_index", "event_name", "topic0", "address",
                                  "block_number", "data_bytes", "decoded_summary",
                                  "evidence_label"])
        on_disk = (OUT / "tx_logs.csv").read_text(encoding="utf-8")
        check("tx_logs.csv (7 rows)", rebuilt == on_disk and len(rows) == 7)
    except Exception as e:
        check("tx_logs.csv (7 rows)", False, str(e))

    # --- 2. registry_usernames.csv -----------------------------------------
    try:
        rows = []
        for entry in rgf["logs"]:
            rows.append({
                "username": decode_username(entry["data"]),
                "address": "0x" + entry["topics"][1][-40:],
                "block_number": int(entry["blockNumber"], 16),
                "block_timestamp": int(entry["timeStamp"], 16),
                "transaction_hash": entry["transactionHash"],
                "log_index": int(entry["logIndex"], 16),
            })
        rebuilt = csv_text(rows, ["username", "address", "block_number",
                                  "block_timestamp", "transaction_hash",
                                  "log_index"])
        on_disk = (OUT / "registry_usernames.csv").read_text(encoding="utf-8")
        ok = rebuilt == on_disk and len(rows) == 195
        by_name = {r["username"]: r["address"] for r in rows}
        ok = ok and by_name["anara"].lower() == au["registry_resolutions"]["anara"]["address"].lower()
        ok = ok and by_name["kittynim"].lower() == au["registry_resolutions"]["kittynim"]["address"].lower()
        check("registry_usernames.csv (195 rows)", ok)
    except Exception as e:
        check("registry_usernames.csv (195 rows)", False, str(e))

    # --- 3. statement.csv ---------------------------------------------------
    try:
        stmt_ints, stmt_hex = parse_statement(tx["input"])
        decoded_stmt = de["calldata"]["receipt_tuple"]["statement"]
        ok = (stmt_ints == decoded_stmt["values_int"]
              and stmt_hex == decoded_stmt["values_hex"]
              and len(stmt_ints) == 10 and stmt_ints[8] == 4416000000000000000)
        rows = []
        for i, (vi, vh) in enumerate(zip(stmt_ints, stmt_hex)):
            if i in (3, 4, 5, 6, 7):
                cls = "verified-fact"
                basis = "F17a (r3 §4.1): value matches log topic/data"
            elif i == 8:
                cls = ("verified-fact (integer); RLS unit = interpretation; "
                       "'total fee' = inference")
                basis = "F17b (r3 §4.1 + addendum F17 §A)"
            else:
                cls = "unknown"
                basis = "unidentified (r3 §4.1)"
            rows.append({"index": i, "value_decimal": vi, "value_hex": vh,
                         "classification": cls, "basis": basis})
        rebuilt = csv_text(rows, ["index", "value_decimal", "value_hex",
                                  "classification", "basis"])
        on_disk = (OUT / "statement.csv").read_text(encoding="utf-8")
        check("statement.csv (10 rows)", ok and rebuilt == on_disk)
    except Exception as e:
        check("statement.csv (10 rows)", False, str(e))

    # --- 4. relayer_txs.csv --------------------------------------------------
    try:
        # Dedup by tx hash; `confirmations` is call-time metadata and
        # may differ between calls — core fields must be identical.
        seen = {}
        for call in txlf["calls"]:
            for row in call["response"]["result"]:
                h = row["hash"]
                if h in seen:
                    a, b = seen[h], row
                    core = [k for k in a if k != "confirmations"]
                    assert all(a[k] == b.get(k) for k in core), (
                        f"duplicate relayer tx differs in core fields: {h}")
                else:
                    seen[h] = row
        rows = []
        for row in sorted(seen.values(), key=lambda r: int(r["blockNumber"])):
            rows.append({
                "tx_hash": row["hash"], "block_number": int(row["blockNumber"]),
                "timestamp": int(row["timeStamp"]), "from": row["from"],
                "to": row["to"], "value_wei": int(row["value"]),
                "gas": int(row["gas"]), "gas_price_wei": int(row["gasPrice"]),
                "gas_used": int(row["gasUsed"]), "is_error": row["isError"],
            })
        rebuilt = csv_text(rows, ["tx_hash", "block_number", "timestamp", "from",
                                  "to", "value_wei", "gas", "gas_price_wei",
                                  "gas_used", "is_error"])
        on_disk = (OUT / "relayer_txs.csv").read_text(encoding="utf-8")
        check("relayer_txs.csv (2 rows)", rebuilt == on_disk and len(rows) == 2)
    except Exception as e:
        check("relayer_txs.csv (2 rows)", False, str(e))

    # --- 5. audit_report.json ------------------------------------------------
    try:
        report = load_json(REPO / "audit_report.json")
        gas_used = int(rc["gasUsed"], 16)
        gas_price = int(tx["gasPrice"], 16)
        chain_gas_wei = gas_used * gas_price
        block_ts = int(block["timestamp"], 16)
        block_iso = datetime.fromtimestamp(block_ts, tz=timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ")
        vault_impl = "0x" + cof["implementation_from_slot"][-40:]
        related = de["related_tx"]
        f = report["findings"]
        i = report["integrity"]
        checks = [
            ("integrity.status", i["status"] == "PASS"),
            ("integrity.csv_sha256", i["csv_sha256"] == {
                n: sha256_file(OUT / n) for n in
                ("tx_logs.csv", "registry_usernames.csv", "statement.csv",
                 "relayer_txs.csv")}),
            ("integrity.manifest_tx", i["manifest_tx"] == "20/20 OK"),
            ("integrity.manifest_journey", i["manifest_journey"] == "16/16 OK"),
            ("integrity.cross_checks", i["cross_checks"] == {
                "total": 13, "boolean_checks_pass": 12,
                "log_count_receipt": 7, "all_match": True}),
            ("findings.chain_id", f["chain_id"] == 7295799),
            ("findings.tx_hash", f["tx_hash"] == tx["hash"]),
            ("findings.block", f["block"] == 24825928),
            ("findings.block_timestamp_utc", f["block_timestamp_utc"] == block_iso == "2026-11-21T09:40:42Z"),
            ("findings.from/to", f["from"] == tx["from"] and f["to"] == tx["to"]),
            ("findings.vault_implementation", f["vault_implementation"] == vault_impl),
            ("findings.logs", f["logs_total"] == 7 and f["logs_by_event"] == {"Commitment": 3, "EncryptedNote": 3, "Nullifier": 1}),
            ("findings.statement_8", f["statement_8_integer_wei"] == 4416000000000000000),
            ("findings.statement_8_classification", "inference" in f["statement_8_classification"] and "interpretation" in f["statement_8_classification"]),
            ("findings.chain_gas_wei", f["chain_gas_wei"] == chain_gas_wei == 63168048000000000),
            ("findings.chain_gas_token", "disputed" in f["chain_gas_token"]),
            ("findings.gas", f["gas_used"] == 1316001 and f["gas_limit"] == 1630484 and f["gas_price_wei"] == 48000000000),
            ("findings.related_tx", f["related_tx_hash"] == related["tx_hash"] and f["related_tx_block"] == 24825932 and f["related_tx_amount_rls"] == "0.576"),
            ("findings.related_tx_role", "reconstruction" in f["related_tx_role"] and "unknown" in f["related_tx_role"]),
            ("findings.registry_logs", f["registry_logs"] == 195),
            ("findings.registry_resolutions", f["registry_resolutions"] == {
                "anara": au["registry_resolutions"]["anara"]["address"],
                "kittynim": au["registry_resolutions"]["kittynim"]["address"]}),
            ("status_note", "integrity and internal consistency" in report["status_note"]),
        ]
        bad = [name for name, ok in checks if not ok]
        check("audit_report.json (all fields)", not bad,
              f"{len(checks) - len(bad)}/{len(checks)} field checks pass"
              + (f"; failed: {bad}" if bad else ""))
    except Exception as e:
        check("audit_report.json (all fields)", False, str(e))

    # --- 6. datasets_checksums.sha256 ----------------------------------------
    try:
        lines = (OUT / "datasets_checksums.sha256").read_text(encoding="utf-8").splitlines()
        ok = len(lines) == 5
        for line in lines:
            h, _sep, name = line.partition("  ")
            target = (OUT / name).resolve()
            if not target.exists() or sha256_file(target) != h:
                ok = False
        check("datasets_checksums.sha256 (5 entries)", ok)
    except Exception as e:
        check("datasets_checksums.sha256 (5 entries)", False, str(e))

    # --- 7-8. manifests -------------------------------------------------------
    check_manifest_file(PKG / "manifest.json", "TX")
    check_manifest_file(JOURNEY / "manifest.json", "journey")

    # --- 9. LF-only ------------------------------------------------------------
    try:
        bad = []
        for name in ("tx_logs.csv", "registry_usernames.csv", "statement.csv",
                     "relayer_txs.csv"):
            if b"\r" in (OUT / name).read_bytes():
                bad.append(name)
        if b"\r" in (REPO / "audit_report.json").read_bytes():
            bad.append("audit_report.json")
        check("LF-only (CSVs + audit_report.json)", not bad,
              f"CR found in: {bad}" if bad else "")
    except Exception as e:
        check("LF-only (CSVs + audit_report.json)", False, str(e))

    failed = [name for name, ok, _ in RESULTS if not ok]
    print(f"verify_datasets: {len(RESULTS) - len(failed)}/{len(RESULTS)} checks PASS")
    if failed:
        print(f"verify_datasets: FAILED: {failed}", file=sys.stderr)
        return 1
    print("verify_datasets: ALL PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
