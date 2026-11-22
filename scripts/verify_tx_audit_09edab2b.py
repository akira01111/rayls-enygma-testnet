#!/usr/bin/env python3
"""Independent verification script for the Rayls Enygma Week 2 TX audit.

Version: 1.0.1 (2026-11-22: EXPECTED_FILES extended with
ADDENDUM-2026-11-22.md — Anara's @kittynim confirmation; no check logic
changed from 1.0.0.)
Target tx: 0x09edab2bb8914aea3c905608ea9fcd09c056a470a5e150df03e0b324eff525bb
Network: Rayls Public Testnet, chain ID 7295799. Block 24825928.

This script is INDEPENDENT of the fetch script (scripts/tx_audit_09edab2b.py)
and the decode script (scripts/decode_tx_09edab2b.py): it does not import
either of them. It re-reads the evidence files from disk, recomputes every
SHA-256, checks the manifest, and re-derives the basic cross-consistency
facts with its own minimal parsing (keccak is NOT needed here; the checks
below use direct value comparison against the raw files).

Checks:
  A. manifest.json is valid JSON and lists every expected package file.
  B. every listed file exists, has the listed byte size, and matches the
     listed SHA-256 (recomputed from disk).
  C. cross-consistency, re-derived from the raw files:
     - receipt blockNumber == block.json number == 24825928
     - tx hash in transaction.json == receipt transactionHash == target hash
     - receipt log count == logs.json receipt_logs_copy count ==
       decoded_events.json log count == 7
     - transaction to-address == SharedVaultProxy 0x9c5ad5e5...
     - chainId == 0x6f5337 (7295799)
     - vault EIP-1967 implementation slot == 0xad9667049f14d1757d147f652c41dc241c57091c
     - calldata statement[8] (re-parsed independently) == 4,416,000,000,000,000,000 wei
     - related-tx ERC20 transfer amount == 576,000,000,000,000,000 wei (0.576 RLS)
     - calldata ciphertexts SHA-256 == EncryptedNote log ciphertexts SHA-256
     - registry resolves @anara -> 0x0c5b369ad7d0c4e051a2887575f7fc85e0ccd0b5
       and @kittynim -> 0x680d90983da58bcb7d127e3421193274e84e0efc
     - gasUsed x effectiveGasPrice == 63,168,048,000,000,000 wei

Exit code: 0 only if every check passes, else 1.
Usage: python3 scripts/verify_tx_audit_09edab2b.py
"""
import hashlib
import json
import os
import sys

SCRIPT_NAME = "scripts/verify_tx_audit_09edab2b.py"
SCRIPT_VERSION = "1.0.1"
REPO = os.path.expanduser("~/workspace/rayls-enygma-public-testnet-research")
PKG = os.path.join(REPO, "experiments/transactions/tx-09edab2b")
TX_HASH = "0x09edab2bb8914aea3c905608ea9fcd09c056a470a5e150df03e0b324eff525bb"
VAULT = "0x9c5ad5e5ea5b5910e7fd1e1cc7b70ce0e4bf06c2"
VAULT_IMPL = "0xad9667049f14d1757d147f652c41dc241c57091c"
SENDER = "0x0c5b369ad7d0c4e051a2887575f7fc85e0ccd0b5"
RECEIVER = "0x680d90983da58bcb7d127e3421193274e84e0efc"

EXPECTED_FILES = [
    "experiments/transactions/tx-09edab2b/raw/transaction.json",
    "experiments/transactions/tx-09edab2b/raw/receipt.json",
    "experiments/transactions/tx-09edab2b/raw/logs.json",
    "experiments/transactions/tx-09edab2b/raw/block.json",
    "experiments/transactions/tx-09edab2b/raw/contracts.json",
    "experiments/transactions/tx-09edab2b/raw/explorer.json",
    "experiments/transactions/tx-09edab2b/raw/explorer-relayer-txlist.json",
    "experiments/transactions/tx-09edab2b/raw/registry-usernames.json",
    "experiments/transactions/tx-09edab2b/raw/related-tx-0xacc7d175.json",
    "experiments/transactions/tx-09edab2b/decoded/decoded_events.json",
    "experiments/transactions/tx-09edab2b/decoded/audit_summary.json",
    "experiments/transactions/tx-09edab2b/decoded/bundle-abi-extract.json",
    "experiments/transactions/tx-09edab2b/decoded/lookups-4byte.json",
    "experiments/transactions/tx-09edab2b/TX-AUDIT-REPORT.md",
    "experiments/transactions/tx-09edab2b/gaps.md",
    "experiments/transactions/tx-09edab2b/TODO.md",
    "experiments/transactions/tx-09edab2b/ADDENDUM-2026-11-22.md",
    "scripts/tx_audit_09edab2b.py",
    "scripts/decode_tx_09edab2b.py",
    "scripts/verify_tx_audit_09edab2b.py",
]

results = []


def check(name, ok, detail=""):
    results.append((name, bool(ok), detail))
    print(("PASS " if ok else "FAIL ") + name + ((" — " + str(detail)) if detail else ""))


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load(rel):
    with open(os.path.join(REPO, rel), encoding="utf-8") as fh:
        return json.load(fh)


def word(b, i):
    return int.from_bytes(b[i * 32:(i + 1) * 32], "big")


def main():
    manifest_path = os.path.join(PKG, "manifest.json")
    try:
        manifest = json.load(open(manifest_path, encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        print("FAIL manifest.json unreadable: " + str(exc))
        return 1
    check("manifest.json is valid JSON", True)
    entries = {e["relative_path"]: e for e in manifest.get("files", [])}

    # A. coverage
    missing = [f for f in EXPECTED_FILES if f not in entries]
    extra = [f for f in entries if f not in EXPECTED_FILES]
    check("manifest lists every expected file", not missing, "missing: " + str(missing))
    check("manifest has no unexpected entries", not extra, "extra: " + str(extra))

    # B. hashes + sizes
    bad = []
    for rel, ent in sorted(entries.items()):
        p = os.path.join(REPO, rel)
        if not os.path.exists(p):
            bad.append(rel + " (missing file)")
            continue
        size = os.path.getsize(p)
        h = sha256_file(p)
        if size != ent.get("bytes") or h != ent.get("sha256"):
            bad.append(rel + f" (size {size} vs {ent.get('bytes')}, sha {h[:12]} vs {str(ent.get('sha256'))[:12]})")
    check("all manifest entries match disk (bytes + SHA-256)", not bad, "; ".join(bad) if bad else f"{len(entries)} files verified")

    # C. cross-consistency, re-derived from raw files
    txf = load("experiments/transactions/tx-09edab2b/raw/transaction.json")
    rcf = load("experiments/transactions/tx-09edab2b/raw/receipt.json")
    lgf = load("experiments/transactions/tx-09edab2b/raw/logs.json")
    blf = load("experiments/transactions/tx-09edab2b/raw/block.json")
    cof = load("experiments/transactions/tx-09edab2b/raw/contracts.json")
    rgf = load("experiments/transactions/tx-09edab2b/raw/registry-usernames.json")
    rtx = load("experiments/transactions/tx-09edab2b/raw/related-tx-0xacc7d175.json")
    dec = load("experiments/transactions/tx-09edab2b/decoded/decoded_events.json")

    tx = txf["calls"][2]["response"]["result"]
    rc = rcf["calls"][0]["response"]["result"]
    block = blf["calls"][0]["response"]["result"]

    check("tx hash matches target (transaction.json)", tx["hash"].lower() == TX_HASH.lower())
    check("receipt tx hash matches transaction", rc["transactionHash"].lower() == TX_HASH.lower())
    check("receipt blockNumber == block.json number == 24825928",
          rc["blockNumber"] == block["number"] == "0x17ad048")
    check("receipt log count (7) == logs.json receipt copy == decoded log count",
          len(rc["logs"]) == len(lgf["receipt_logs_copy"]) == len(dec["logs"]) == 7)
    check("to-address is the SharedVaultProxy", tx["to"].lower() == VAULT.lower())
    check("chainId is 0x6f5337 (7295799)", tx["chainId"] == "0x6f5337")
    impl = (cof.get("implementation_from_slot") or "").lower()
    check("vault EIP-1967 implementation is 0xad966704...",
          impl == VAULT_IMPL.lower(), impl)
    check("receipt status is success (0x1)", rc["status"] == "0x1")
    check("block has exactly this 1 transaction",
          len(block["transactions"]) == 1 and block["transactions"][0].lower() == TX_HASH.lower())

    # independent minimal calldata re-parse: statement[8] == 4.416e18
    params = bytes.fromhex(tx["input"][2:])[4:]
    off_receipt = word(params, 0)
    r = params[off_receipt:]
    stmt_off = word(r, 8)
    stmt_len = word(r, stmt_off // 32)
    stmt = [word(r, stmt_off // 32 + 1 + i) for i in range(stmt_len)]
    check("statement has 10 values", stmt_len == 10, stmt_len)
    check("statement[8] == 4,416,000,000,000,000,000 wei (4.416 RLS)",
          stmt[8] == 4416000000000000000, stmt[8])
    check("numberOfInputs == 1 and numberOfOutputs == 3",
          word(r, 9) == 1 and word(r, 10) == 3)

    # fee
    gas_cost = int(rc["gasUsed"], 16) * int(rc["effectiveGasPrice"], 16)
    check("gasUsed x effectiveGasPrice == 63,168,048,000,000,000 wei",
          gas_cost == 63168048000000000, gas_cost)

    # ciphertexts: calldata arrays vs EncryptedNote log data (independent parse)
    def parse_bytes_array(off):
        ln = word(params, off // 32)
        data_start = off + 32
        offs = [word(params, off // 32 + 1 + i) for i in range(ln)]
        out = []
        for o in offs:
            elen = word(params, (data_start + o) // 32)
            out.append(params[data_start + o + 32:data_start + o + 32 + elen])
        return out
    c1 = parse_bytes_array(word(params, 1))
    c2 = parse_bytes_array(word(params, 2))
    notes = [e for e in dec["logs"] if e["event_name"] == "EncryptedNote"]
    ok_ct = (len(c1) == 3 and len(c2) == 3 and all(
        hashlib.sha256(c1[i]).hexdigest() == notes[i]["decoded_fields"]["ciphertextI_sha256"] and
        hashlib.sha256(c2[i]).hexdigest() == notes[i]["decoded_fields"]["ciphertextII_sha256"]
        for i in range(3)))
    check("calldata ciphertexts == EncryptedNote log ciphertexts (SHA-256)", ok_ct)

    # related tx
    rres = rtx["calls"][0]["response"]["result"]
    rrc = rtx["calls"][1]["response"]["result"]
    rin = rres["input"]
    r_amount = int(rin[74:138], 16)
    check("related tx transfers 576,000,000,000,000,000 wei (0.576 RLS)",
          r_amount == 576000000000000000, r_amount)
    check("related tx recipient is 0x71af09966cbed4434cca97c40fa38b8083548b95",
          ("0x" + rin[10 + 24:10 + 64]).lower() == "0x71af09966cbed4434cca97c40fa38b8083548b95")

    # registry
    found = {}
    for lg in rgf["logs"]:
        d = bytes.fromhex(lg["data"][2:])
        ln = int.from_bytes(d[32:64], "big")
        found[d[64:64 + ln].decode("utf-8", errors="replace")] = "0x" + lg["topics"][1][-40:]
    check("registry resolves @anara", found.get("anara", "").lower() == SENDER.lower(), found.get("anara"))
    check("registry resolves @kittynim", found.get("kittynim", "").lower() == RECEIVER.lower(), found.get("kittynim"))
    check("registry has 195 UsernameSet logs", len(rgf["logs"]) == 195, len(rgf["logs"]))

    failed = [n for n, ok, _ in results if not ok]
    print()
    print(f"verify: {len(results) - len(failed)}/{len(results)} checks passed")
    if failed:
        print("FAILED: " + "; ".join(failed))
        return 1
    print("verify: ALL CHECKS PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
